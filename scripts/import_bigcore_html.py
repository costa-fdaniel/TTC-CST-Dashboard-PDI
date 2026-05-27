from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pdi_dashboard.history import write_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Extrai dados do dashboard HTML da BIGCORE.")
    parser.add_argument("--input", required=True, help="HTML BIGCORE recebido.")
    parser.add_argument("--output", default="data_sources/extracted/bigcore_2024_2025.json")
    parser.add_argument("--csv-dir", default="data_sources/extracted/bigcore_csv")
    parser.add_argument("--raw-dir", default="data_sources/raw/bigcore")
    args = parser.parse_args()

    input_path = Path(args.input)
    text = input_path.read_text(encoding="utf-8", errors="ignore")
    payload, csv_tables = extract_bigcore(text, str(input_path))

    raw_dir = Path(args.raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_copy = raw_dir / "BIGCORE_2025.html"
    shutil.copyfile(input_path, raw_copy)
    payload["source_files"] = [str(raw_copy)]
    for evidence in payload["evidence"]:
        evidence["source"] = str(raw_copy)
    for year in payload["years"]:
        year["source_refs"] = [str(raw_copy)]
    for project in payload["projects"]:
        project["source_refs"] = [str(raw_copy)]

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_manifest(payload, output.parent.parent / "evidence" / "manifest.csv")

    csv_dir = Path(args.csv_dir)
    csv_dir.mkdir(parents=True, exist_ok=True)
    for name, rows in csv_tables.items():
        write_csv(csv_dir / f"{name}.csv", rows)

    print(f"BIGCORE: {len(payload['years'])} anos, {len(payload['projects'])} projetos/grupos")
    print(f"JSON gerado: {output.resolve()}")
    print(f"CSVs gerados: {csv_dir.resolve()}")
    return 0


def extract_bigcore(text: str, source: str) -> tuple[dict[str, Any], dict[str, list[list[Any]]]]:
    data_block = extract_assignment(text, "DATA", "{", "}")
    rules_block = extract_assignment(text, "THIRD_RULES", "{", "}")
    work_block = extract_assignment(text, "WORK_CATALOG_BASE", "[", "]")

    years: list[dict[str, Any]] = []
    investments_rows = [["Fornecedor", "Natureza", "Valor", "Ano", "Descrição"]]
    resumo_rows = [["Natureza", "1", "2", "3", "4", "TOTAL"]]
    project_rows = [["Projeto", "Código", "Descrição", "Incentivado?", "Ano"]]
    work_rows = [["Projeto", "Atividade realizada", "Código", "Ano", "Projeto incentivado?", "Atividade incentivada?"]]

    projects: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []

    for year in sorted(extract_year_keys(data_block)):
        year_block = extract_property_block(data_block, str(year), "{", "}")
        company = string_prop(year_block, "company") or "BIGCORE SOLUÇÕES EM TECNOLOGIA LTDA"
        code = string_prop(year_block, "code") or "2025-061"
        project = clean(string_prop(year_block, "project") or "E-Log - Plataforma Inteligente e Adaptativa para Gestão Logística e Integração de Sistemas")
        quarters = parse_quarters(extract_property_block(year_block, "quarters", "{", "}"))
        thirds = parse_thirds(extract_property_block(year_block, "thirds", "[", "]"))
        rules = parse_rules(extract_property_block(rules_block, str(year), "{", "}"))

        third_total = round(sum(q.get("third", 0) for q in quarters), 2)
        third_full_total = round(sum(item["value"] for item in thirds), 2)
        rh_partial = round(sum(q.get("rhp", 0) for q in quarters), 2)
        base_total = round(sum(q.get("total", 0) for q in quarters), 2)
        exclusion = round(sum(q.get("excl", 0) for q in quarters), 2)
        savings = round(sum(q.get("eco", 0) for q in quarters), 2)
        eligible_thirds = round(sum(item["value"] * rule_pct(rules, item["name"]) for item in thirds), 2)

        top_projects = [{"name": item["name"], "value": item["value"]} for item in sorted(thirds, key=lambda item: item["value"], reverse=True)]
        years.append(
            {
                "year": year,
                "base_total": base_total,
                "investment_total": third_total,
                "material_total": 0.0,
                "third_party_total": third_total,
                "rh_partial_total": rh_partial,
                "rh_exclusive_total": 0.0,
                "rh_total": rh_partial,
                "exclusion_total": exclusion,
                "estimated_savings": savings,
                "method": "bigcore_html_dashboard",
                "projects_total": 1,
                "projects_incentivized": 1 if eligible_thirds > 0 else 0,
                "eligible_hours": 0.0,
                "top_projects": top_projects[:20],
                "third_party_full_total": third_full_total,
                "source_refs": [source],
            }
        )
        projects.append(
            {
                "year": year,
                "name": project,
                "status": "incentivado",
                "summary": "Projeto E-Log: plataforma inteligente e adaptativa para gestão logística, integração de sistemas, torre de controle, jornada operacional, auditoria, automações, ETA e processamento orientado a eventos.",
                "activities": work_activities(work_block, year)[:80],
                "source_refs": [source],
            }
        )
        evidence.append(
            {
                "company": company,
                "year": year,
                "source": source,
                "kind": "html",
                "extracted_from": "const DATA, THIRD_RULES e WORK_CATALOG_BASE",
                "confidence": "alta",
                "notes": "HTML BIGCORE continha dados anuais, fornecedores, regras de incentivo e backlog técnico estruturados em JavaScript.",
            }
        )

        resumo_rows.append(["Terceiros", *quarter_values(quarters, "third"), third_total])
        resumo_rows.append(["RH Inovação parcial", *quarter_values(quarters, "rhp"), rh_partial])
        resumo_rows.append(["TOTAL", *quarter_values(quarters, "total"), base_total])
        resumo_rows.append(["Exclusão da base", *quarter_values(quarters, "excl"), exclusion])
        resumo_rows.append(["Economia estimada", *quarter_values(quarters, "eco"), savings])
        project_rows.append([project, code, projects[-1]["summary"], "Sim", year])
        for item in thirds:
            rule = rules.get(norm_vendor(item["name"]), {})
            desc = rule.get("note") or "Fornecedor/terceiro vinculado ao dashboard BIGCORE."
            investments_rows.append([item["name"], "Serviços/terceiros", item["value"], year, desc])

    for activity in parse_work_catalog(work_block)[:450]:
        work_rows.append(
            [
                "E-Log - Plataforma Inteligente e Adaptativa para Gestão Logística e Integração de Sistemas",
                f"{activity.get('group', '')} - {activity.get('summary', '')}".strip(" -"),
                activity.get("key", ""),
                "",
                "Sim",
                "Sim",
            ]
        )

    payload = {
        "company": "BIGCORE SOLUÇÕES EM TECNOLOGIA LTDA",
        "slug": "BIGCORE_PD&I_2026",
        "source_type": "html",
        "source_files": [source],
        "years": years,
        "projects": projects,
        "evidence": evidence,
    }
    csv_tables = {
        "RESUMO": resumo_rows,
        "Projetos": project_rows,
        "Investimentos": investments_rows,
        "Trabalho": work_rows,
    }
    return payload, csv_tables


def extract_assignment(text: str, variable: str, opener: str, closer: str) -> str:
    match = re.search(rf"const\s+{re.escape(variable)}\s*=\s*{re.escape(opener)}", text)
    if not match:
        return ""
    return extract_balanced(text, match.end() - 1, opener, closer)


def extract_property_block(text: str, key: str, opener: str, closer: str) -> str:
    match = re.search(rf"(?:^|[\s,]){re.escape(key)}\s*:\s*{re.escape(opener)}", text)
    if not match:
        return ""
    return extract_balanced(text, match.end() - 1, opener, closer)


def extract_balanced(text: str, start: int, opener: str, closer: str) -> str:
    depth = 0
    quote = ""
    escape = False
    for idx in range(start, len(text)):
        char = text[idx]
        if quote:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == quote:
                quote = ""
            continue
        if char in {"'", '"', "`"}:
            quote = char
            continue
        if char == opener:
            depth += 1
        elif char == closer:
            depth -= 1
            if depth == 0:
                return text[start + 1 : idx]
    return ""


def extract_year_keys(data_block: str) -> list[int]:
    return [int(match.group(1)) for match in re.finditer(r"(20\d{2})\s*:\s*\{", data_block)]


def parse_quarters(block: str) -> list[dict[str, float]]:
    out: list[dict[str, float]] = []
    for match in re.finditer(r"Q\d\s*:\s*\{(.*?)\}", block, flags=re.S):
        row = {}
        for key, value in re.findall(r"(\w+)\s*:\s*([0-9.]+)", match.group(1)):
            row[key] = float(value)
        out.append(row)
    return out


def parse_thirds(block: str) -> list[dict[str, Any]]:
    out = []
    for match in re.finditer(r"\{(.*?)\}", block, flags=re.S):
        body = match.group(1)
        out.append(
            {
                "name": string_inline(body, "name"),
                "size": string_inline(body, "size"),
                "cnpj": string_inline(body, "cnpj"),
                "value": number_inline(body, "value"),
            }
        )
    return [item for item in out if item["name"]]


def parse_rules(block: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for match in re.finditer(r'"([^"]+)"\s*:\s*\{(.*?)\}', block, flags=re.S):
        name = match.group(1)
        body = match.group(2)
        out[norm_vendor(name)] = {
            "cls": string_inline(body, "cls"),
            "pctNow": number_inline(body, "pctNow"),
            "pctMax": number_inline(body, "pctMax"),
            "note": string_inline(body, "note"),
        }
    return out


def parse_work_catalog(block: str) -> list[dict[str, str]]:
    out = []
    for match in re.finditer(r"\{(.*?)\}", block, flags=re.S):
        body = match.group(1)
        out.append({"group": string_inline(body, "group"), "key": string_inline(body, "key"), "summary": string_inline(body, "summary")})
    return [item for item in out if item["key"] or item["summary"]]


def work_activities(work_block: str, year: int) -> list[str]:
    items = parse_work_catalog(work_block)
    return [f"{item['group']}: {item['summary'] or item['key']}".strip(": ") for item in items[:120]]


def string_prop(block: str, key: str) -> str:
    return string_inline(block, key)


def string_inline(body: str, key: str) -> str:
    match = re.search(rf'"?{re.escape(key)}"?\s*:\s*"((?:\\.|[^\"])*)"', body, flags=re.S)
    return clean(match.group(1).replace('\\"', '"')) if match else ""


def number_inline(body: str, key: str) -> float:
    match = re.search(rf'"?{re.escape(key)}"?\s*:\s*([0-9.]+)', body)
    return float(match.group(1)) if match else 0.0


def quarter_values(quarters: list[dict[str, float]], key: str) -> list[float]:
    values = [round(row.get(key, 0.0), 2) for row in quarters]
    return values + [0.0] * max(0, 4 - len(values))


def rule_pct(rules: dict[str, dict[str, Any]], name: str) -> float:
    return float((rules.get(norm_vendor(name)) or {}).get("pctNow") or 0)


def write_csv(path: Path, rows: list[list[Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh, delimiter=";")
        writer.writerows(rows)


def clean(value: str) -> str:
    return " ".join(str(value or "").split())


def norm_vendor(value: str) -> str:
    table = str.maketrans("áàãâäéèêëíìîïóòõôöúùûüçÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇ", "aaaaaeeeeiiiiooooouuuucAAAAAEEEEIIIIOOOOOUUUUC")
    return re.sub(r"\s+", " ", str(value or "").translate(table).upper()).strip()


if __name__ == "__main__":
    raise SystemExit(main())
