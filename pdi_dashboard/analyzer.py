from __future__ import annotations

import math
import re
from dataclasses import asdict, dataclass
from typing import Any

import pandas as pd

from .loader import canonical_sheet_name


@dataclass
class Analysis:
    company: str
    year: int | None
    source: str
    sheets: dict[str, Any]
    metrics: dict[str, Any]
    validations: list[dict[str, Any]]
    tables: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def analyze_workbook(
    raw_sheets: dict[str, pd.DataFrame],
    *,
    company: str,
    year: int | None,
    source: str,
) -> dict[str, Any]:
    sheets: dict[str, dict[str, Any]] = {}
    tables: dict[str, list[dict[str, Any]]] = {}
    used_keys: dict[str, int] = {}

    for original_name, raw in raw_sheets.items():
        key = unique_key(canonical_sheet_name(original_name), original_name, used_keys)
        table = promote_header(raw)
        tables[key] = frame_to_records(table)
        sheets[key] = {
            "original_name": original_name,
            "rows_raw": int(raw.shape[0]),
            "cols_raw": int(raw.shape[1]) if not raw.empty else 0,
            "rows_table": int(table.shape[0]),
            "cols_table": int(table.shape[1]) if not table.empty else 0,
            "columns": list(map(str, table.columns)) if not table.empty else [],
        }

    metrics = collect_metrics(tables)
    validations = collect_validations(metrics)
    return Analysis(company, year, source, sheets, metrics, validations, tables).to_dict()


def unique_key(key: str, original_name: str, used: dict[str, int]) -> str:
    base = key or re.sub(r"[^a-z0-9]+", "_", original_name.lower()).strip("_") or "aba"
    count = used.get(base, 0)
    used[base] = count + 1
    return base if count == 0 else f"{base}_{count + 1}"


def promote_header(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    header_idx = find_header_row(df)
    headers = [clean_header(v, i) for i, v in enumerate(df.iloc[header_idx].tolist())]
    out = df.iloc[header_idx + 1 :].copy()
    out.columns = dedupe(headers)
    out = out.loc[~out.apply(lambda row: all(str(v).strip() == "" for v in row), axis=1)]
    out = out.loc[:, [not str(c).startswith("vazio_") for c in out.columns]]
    return out.reset_index(drop=True)


def find_header_row(df: pd.DataFrame) -> int:
    known = {
        "projeto",
        "funcionario",
        "fornecedor",
        "cnpj",
        "data",
        "valor",
        "mes",
        "ano",
        "salario",
        "descricao",
        "atividade",
        "horas",
    }
    best_idx = 0
    best_score = -1
    max_rows = min(20, len(df))
    for idx in range(max_rows):
        values = [str(v).strip() for v in df.iloc[idx].tolist()]
        non_empty = [v for v in values if v]
        normalized = {_norm(v) for v in non_empty}
        score = len(normalized & known) * 5 + len(non_empty)
        if any(re.fullmatch(r"INOV\d{5,}", v, flags=re.I) for v in non_empty):
            score += 2
        if score > best_score:
            best_score = score
            best_idx = idx
    return best_idx


def clean_header(value: Any, index: int) -> str:
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return f"vazio_{index}"
    return re.sub(r"\s+", " ", text).strip()


def dedupe(headers: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    out: list[str] = []
    for header in headers:
        count = seen.get(header, 0)
        seen[header] = count + 1
        out.append(header if count == 0 else f"{header}_{count + 1}")
    return out


def frame_to_records(df: pd.DataFrame, limit: int = 5000) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for row in df.head(limit).to_dict(orient="records"):
        record = {str(k): normalize_cell(v) for k, v in row.items()}
        if record_has_content(record):
            records.append(record)
    return records


def normalize_cell(value: Any) -> Any:
    if value is None:
        return ""
    text = str(value).strip()
    return "" if text.lower() == "nan" else text


def record_has_content(record: dict[str, Any]) -> bool:
    """Discard spreadsheet residue rows with only formulas/default values."""
    trivial_values = {"", "-", "0", "0.0", "0,0", "0.00", "0,00", "false", "falso", "nan"}
    context_only_columns = {"mes", "mês", "ano"}
    for key, value in record.items():
        text = str(value).strip()
        if not text:
            continue
        if _norm(text) in trivial_values:
            continue
        if _norm(key) in context_only_columns and re.fullmatch(r"\d{1,4}", text):
            continue
        return True
    return False


def collect_metrics(tables: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    resumo = tables.get("resumo", [])
    projects = tables.get("projetos", [])
    work = tables.get("trabalho", [])
    people = tables.get("pessoal", [])
    investments = tables.get("investimentos", [])
    salaries = tables.get("salarios", [])
    resumo_metrics = parse_resumo_metrics(resumo)
    investment_metrics = analyze_investments(investments)

    metrics: dict[str, Any] = {
        "projects_total": len([r for r in projects if get_value(r, ["Projeto"])]),
        "projects_incentivized": count_true(projects, ["Incentivado?", "Incentivado"]),
        "work_rows": len(work),
        "eligible_hours": sum_if_hours(work, ["Horas decimais", "Horas"], require_true=["Projeto incentivado?", "Atividade incentivada?"]),
        "people_pdi_total": resumo_metrics.get("rh_total") or sum_numeric_col(people, ["Total PD&I", "Total PDI", "Total PD&I "]),
        "people_effective_hours": sum_numeric_col(people, ["Horas efetivas (PD&I)", "Horas efetivas PDI"]),
        "investment_total": sum_numeric_col(investments, ["Valor"]),
        "investment_incentivized": resumo_metrics.get("investment_total") or investment_metrics["eligible_total"],
        "salary_rows": len([r for r in salaries if get_value(r, ["Funcionário", "Funcionario"])]),
        "base_total": resumo_metrics.get("base_total") or 0,
        "exclusion_total": resumo_metrics.get("exclusion_total") or 0,
        "estimated_savings": resumo_metrics.get("estimated_savings") or 0,
        "commission": resumo_metrics.get("commission") or 0,
        "quarterly": resumo_metrics.get("quarterly") or [],
        "resumo_natures": resumo_metrics.get("natures", []),
        "investment_by_nature": resumo_metrics.get("investment_by_nature") or investment_metrics["by_nature"],
    }
    if not metrics["base_total"]:
        metrics["base_total"] = round(metrics["people_pdi_total"] + metrics["investment_incentivized"], 2)
    if not metrics["estimated_savings"]:
        metrics["estimated_savings"] = round(metrics["base_total"] * 0.6 * 0.34, 2)

    metrics["projects_by_status"] = {
        "incentivados": metrics["projects_incentivized"],
        "nao_incentivados": max(metrics["projects_total"] - metrics["projects_incentivized"], 0),
    }
    metrics["top_projects"] = top_projects(projects, investments, people, resumo)
    metrics["hours_by_activity"] = group_sum(work, ["Atividade realizada", "Atividade"], ["Horas decimais", "Horas"], eligible_only=True)
    metrics["rh_by_employee"] = group_sum(people, ["Funcionário", "Funcionario"], ["Total PD&I", "Total PDI"])
    metrics["investment_by_supplier"] = investment_metrics["by_supplier"]
    return metrics


def parse_resumo_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    metrics: dict[str, Any] = {
        "natures": [],
        "investment_by_nature": [],
        "investment_total": 0.0,
        "rh_total": 0.0,
        "base_total": 0.0,
        "exclusion_total": 0.0,
        "estimated_savings": 0.0,
        "commission": 0.0,
        "quarterly": [],
    }
    quarters: dict[str, dict[str, float | str]] = {
        str(idx): {
            "name": f"{idx}º tri",
            "investment": 0.0,
            "rh": 0.0,
            "base": 0.0,
            "exclusion": 0.0,
            "savings": 0.0,
            "commission": 0.0,
        }
        for idx in range(1, 5)
    }
    for row in rows:
        label = str(get_value(row, ["Natureza", "Projetos"])).strip()
        if not label:
            continue
        value = parse_number(get_value(row, ["TOTAL", "Total", "2"]))
        quarter_values = {str(idx): parse_number(get_value(row, [str(idx)])) for idx in range(1, 5)}
        norm_label = _norm(label)
        is_investment = norm_label in {"material", "materiais", "servicos", "servico", "terceiros"} or (
            value and "rh" not in norm_label and norm_label not in {"total", "percentual exclusao"}
            and not any(term in norm_label for term in ["exclusao", "economia", "comissao", "observacoes", "equipe", "quadro", "valores por projeto", "projetos"])
        )
        if is_investment:
            if not norm_label.startswith("inov") and not norm_label.startswith("nrd") and not norm_label.startswith("projeto "):
                metrics["natures"].append({"name": label, "value": round(value, 2)})
                metrics["investment_by_nature"].append({"name": label, "value": round(value, 2)})
                metrics["investment_total"] += value
                for quarter, quarter_value in quarter_values.items():
                    quarters[quarter]["investment"] = float(quarters[quarter]["investment"]) + quarter_value
        if "rh" in norm_label and "inovacao" in norm_label:
            metrics["rh_total"] += value
            for quarter, quarter_value in quarter_values.items():
                quarters[quarter]["rh"] = float(quarters[quarter]["rh"]) + quarter_value
        elif norm_label == "total":
            metrics["base_total"] = value
            for quarter, quarter_value in quarter_values.items():
                quarters[quarter]["base"] = quarter_value
        elif "exclusao da base" in norm_label:
            metrics["exclusion_total"] = value
            for quarter, quarter_value in quarter_values.items():
                quarters[quarter]["exclusion"] = quarter_value
        elif "economia estimada" in norm_label:
            metrics["estimated_savings"] = value
            for quarter, quarter_value in quarter_values.items():
                quarters[quarter]["savings"] = quarter_value
        elif "comissao" in norm_label:
            metrics["commission"] = value
            for quarter, quarter_value in quarter_values.items():
                quarters[quarter]["commission"] = quarter_value
    for key in ["investment_total", "rh_total", "base_total", "exclusion_total", "estimated_savings", "commission"]:
        metrics[key] = round(metrics[key], 2)
    metrics["quarterly"] = [
        {key: round(value, 2) if isinstance(value, float) else value for key, value in quarter.items()}
        for quarter in quarters.values()
        if any(float(quarter.get(field, 0) or 0) for field in ["investment", "rh", "base", "exclusion", "savings", "commission"])
    ]
    return metrics


def investment_is_eligible(row: dict[str, Any]) -> bool:
    explicit = get_value(row, ["Valor Incentivado"])
    if explicit not in (None, ""):
        return parse_number(explicit) > 0
    flags = [
        get_value(row, ["Inovação?", "Inovacao?"]),
        get_value(row, ["Proj Incentivado?", "Projeto incentivado?", "Incentivado?"]),
    ]
    present = [flag for flag in flags if str(flag).strip() != ""]
    return bool(present) and all(parse_bool(flag) for flag in present)


def investment_value(row: dict[str, Any]) -> float:
    explicit = parse_number(get_value(row, ["Valor Incentivado"]))
    if explicit:
        return explicit
    return parse_number(get_value(row, ["Valor"]))


def analyze_investments(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_supplier: dict[str, float] = {}
    by_nature: dict[str, float] = {}
    eligible_total = 0.0
    for row in rows:
        if not investment_is_eligible(row):
            continue
        value = investment_value(row)
        if not value:
            continue
        eligible_total += value
        supplier = str(get_value(row, ["Fornecedor"])).strip() or "Nao informado"
        nature = str(get_value(row, ["Natureza"])).strip() or "Nao informado"
        by_supplier[supplier] = by_supplier.get(supplier, 0.0) + value
        by_nature[nature] = by_nature.get(nature, 0.0) + value
    return {
        "eligible_total": round(eligible_total, 2),
        "by_supplier": [{"name": k, "value": round(v, 2)} for k, v in sorted(by_supplier.items(), key=lambda item: item[1], reverse=True)[:12]],
        "by_nature": [{"name": k, "value": round(v, 2)} for k, v in sorted(by_nature.items(), key=lambda item: item[1], reverse=True)[:12]],
    }


def collect_validations(metrics: dict[str, Any]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    rh_total = metrics.get("people_pdi_total", 0) or 0
    investment_total = metrics.get("investment_incentivized", 0) or 0
    eligible_hours = metrics.get("eligible_hours", 0) or 0

    validations.append(status_row("RH PD&I", rh_total > 0, f"Total de RH PD&I identificado: {format_brl(rh_total)}"))
    validations.append(status_row("Investimentos incentivados", investment_total > 0, f"Valor incentivado identificado: {format_brl(investment_total)}"))
    validations.append(status_row("Horas elegiveis", eligible_hours > 0, f"Horas elegiveis identificadas: {eligible_hours:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")))
    return validations


def status_row(name: str, ok: bool, detail: str) -> dict[str, Any]:
    return {"name": name, "status": "ok" if ok else "aviso", "detail": detail}


def get_value(row: dict[str, Any], candidates: list[str]) -> Any:
    norm_map = {_norm(k): v for k, v in row.items()}
    for candidate in candidates:
        value = norm_map.get(_norm(candidate))
        if value not in (None, ""):
            return value
    return ""


def count_true(rows: list[dict[str, Any]], candidates: list[str]) -> int:
    return sum(1 for row in rows if parse_bool(get_value(row, candidates)))


def sum_if_hours(rows: list[dict[str, Any]], candidates: list[str], require_true: list[str]) -> float:
    total = 0.0
    for row in rows:
        if all(parse_bool(get_value(row, [field])) for field in require_true):
            total += parse_hours_or_number(get_value(row, candidates))
    return round(total, 2)


def sum_numeric_col(rows: list[dict[str, Any]], candidates: list[str]) -> float:
    return round(sum(parse_number(get_value(row, candidates)) for row in rows), 2)


def group_sum(rows: list[dict[str, Any]], key_candidates: list[str], value_candidates: list[str], eligible_only: bool = False) -> list[dict[str, Any]]:
    grouped: dict[str, float] = {}
    for row in rows:
        if eligible_only and not (
            parse_bool(get_value(row, ["Projeto incentivado?"])) and parse_bool(get_value(row, ["Atividade incentivada?"]))
        ):
            continue
        key = str(get_value(row, key_candidates)).strip() or "Nao informado"
        value = parse_hours_or_number(get_value(row, value_candidates))
        if value:
            grouped[key] = grouped.get(key, 0.0) + value
    return [{"name": k, "value": round(v, 2)} for k, v in sorted(grouped.items(), key=lambda item: item[1], reverse=True)[:12]]


def top_projects(projects: list[dict[str, Any]], investments: list[dict[str, Any]], people: list[dict[str, Any]], resumo: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    resumo_totals = top_projects_from_resumo(resumo or [])
    if resumo_totals:
        return resumo_totals
    totals: dict[str, float] = {}
    for row in projects:
        project = str(get_value(row, ["Attach", "Projeto"])).strip() or str(get_value(row, ["Projeto"])).split(" ")[0]
        if project:
            totals[project] = (
                totals.get(project, 0)
                + parse_number(get_value(row, ["Total investido"]))
                + parse_number(get_value(row, ["Total Help Desk"]))
            )

    if not totals:
        for source_rows, columns in [(investments, ["Valor Incentivado", "Valor"]), (people, ["Total PD&I", "Total PDI"])]:
            for row in source_rows:
                project = str(get_value(row, ["Projeto", "Attach"])).strip()
                if project:
                    totals[project] = totals.get(project, 0) + parse_number(get_value(row, columns))
    return [{"name": k, "value": round(v, 2)} for k, v in sorted(totals.items(), key=lambda item: item[1], reverse=True)[:12]]


def top_projects_from_resumo(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found_header = False
    totals: dict[str, float] = {}
    for row in rows:
        label = str(get_value(row, ["Natureza", "Projetos"])).strip()
        norm_label = _norm(label)
        if "valores por projeto" in norm_label:
            found_header = True
            continue
        if not found_header or not label:
            continue
        if norm_label in {"projetos", "subtotais"}:
            continue
        value = parse_number(get_value(row, ["2", "TOTAL", "Total"]))
        if value:
            totals[label] = totals.get(label, 0.0) + value
    return [{"name": k, "value": round(v, 2)} for k, v in sorted(totals.items(), key=lambda item: item[1], reverse=True)[:12]]


def parse_bool(value: Any) -> bool:
    text = _norm(str(value))
    return text in {"true", "verdadeiro", "sim", "yes", "1"}


def parse_hours_or_number(value: Any) -> float:
    text = str(value).strip()
    if re.fullmatch(r"\d+:\d{2}(:\d{2})?", text):
        parts = [int(p) for p in text.split(":")]
        return parts[0] + parts[1] / 60 + (parts[2] / 3600 if len(parts) > 2 else 0)
    return parse_number(text)


def parse_number(value: Any) -> float:
    text = str(value).strip()
    if not text or text in {"-", "nan"}:
        return 0.0
    text = text.replace("R$", "").replace("%", "").replace(" ", "")
    if "," in text:
        text = text.replace(".", "").replace(",", ".")
    try:
        number = float(text)
    except ValueError:
        return 0.0
    return 0.0 if math.isnan(number) else number


def format_brl(value: float) -> str:
    text = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {text}"


def _norm(value: str) -> str:
    text = value.lower().strip()
    table = str.maketrans("áàãâäéèêëíìîïóòõôöúùûüç", "aaaaaeeeeiiiiooooouuuuc")
    text = text.translate(table)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()
