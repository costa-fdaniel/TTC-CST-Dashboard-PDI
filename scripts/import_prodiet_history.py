from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pdi_dashboard.history import write_manifest
from pdi_dashboard.loader import export_sheets_to_csv, load_workbook


SOURCE_MAP = {
    2012: {"metrics": "01_0B-64TPM3GrzmMFBfYkVzOGUtTXM_file.txt", "projects": "01_0B-64TPM3GrzmMFBfYkVzOGUtTXM_file.txt"},
    2013: {"metrics": "02_0Bz8y8Tdm2lKWU21RSWZVdVM1ZFk_xlsx.xlsx", "projects": "02_0Bz8y8Tdm2lKWU21RSWZVdVM1ZFk_xlsx.xlsx"},
    2014: {"metrics": "03_0B4mf2gfGuZ-RZzR1ckp5SlN2TEU_xlsx.xlsx", "projects": "04_0B3oib_uuVTusemxWVGJzLVdJTk0_txt.txt"},
    2015: {"metrics": "06_0B8bElc9dEJq0d1VBVXdQaWNPMXc_xlsx.xlsx", "projects": "06_0B8bElc9dEJq0d1VBVXdQaWNPMXc_xlsx.xlsx"},
    2016: {"metrics": "09_0B8bElc9dEJq0UFd1YURMMW1NTHM_xlsx.xlsx", "projects": "09_0B8bElc9dEJq0UFd1YURMMW1NTHM_xlsx.xlsx"},
    2017: {"metrics": "10_1HnbFm7TcgicKkPpUFnfFaSBp28r2ty5u_txt.txt", "projects": "11_1Gxyy89zA70DxHjUd9-RR9HrOy5aGLCcj_txt.txt"},
    2018: {"metrics": "13_1FBF2bfmWWDAyMhm4dVraA6PreX7akCidfF2Syc6auTI_xlsx.xlsx", "projects": "12_1xoYBB79FMQ9UUKxAaY20yDblwjOyorUg_file.txt"},
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Normaliza historico legado da PRODIET.")
    parser.add_argument("--raw", default="data_sources/raw/prodiet", help="Pasta com fontes baixadas/exportadas.")
    parser.add_argument("--output", default="data_sources/extracted/prodiet_2012_2018.json", help="JSON historico de saida.")
    args = parser.parse_args()

    raw_dir = Path(args.raw)
    csv_root = Path("exports/csv/prodiet_history")
    years = []
    projects = []
    evidence = []

    for year, sources in SOURCE_MAP.items():
        metrics_path = raw_dir / sources["metrics"]
        project_path = raw_dir / sources["projects"]
        row = extract_year_metrics(year, metrics_path)
        row["source_refs"] = [str(metrics_path)]
        years.append(row)

        if metrics_path.suffix.lower() == ".xlsx":
            sheets = load_workbook(metrics_path)
            export_sheets_to_csv(sheets, csv_root / metrics_path.stem)

        projects.extend(extract_projects(year, project_path))
        evidence.append(
            {
                "company": "PRODIET",
                "year": year,
                "source": str(metrics_path),
                "kind": metrics_path.suffix.lstrip(".") or "txt",
                "extracted_from": "Resumo/relatorio historico",
                "confidence": "alta" if year < 2018 else "media",
                "notes": "Metricas historicas normalizadas a partir da melhor fonte disponivel.",
            }
        )

    payload = {
        "company": "PRODIET",
        "slug": "PRODIET_PD&I_2026",
        "source_type": "mixed",
        "source_files": sorted(str(path) for path in raw_dir.iterdir() if path.is_file()),
        "years": years,
        "projects": projects,
        "evidence": evidence,
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_manifest(payload, output_path.parent.parent / "evidence" / "manifest.csv")
    print(f"Historico PRODIET extraido: {len(years)} anos, {len(projects)} projetos/resumos")
    print(f"Arquivo gerado: {output_path.resolve()}")
    return 0


def extract_year_metrics(year: int, path: Path) -> dict:
    if path.suffix.lower() == ".xlsx":
        return metrics_from_xlsx(year, path)
    return metrics_from_text(year, path)


def metrics_from_xlsx(year: int, path: Path) -> dict:
    if year == 2018:
        return metrics_2018(path)
    raw = pd.read_excel(path, sheet_name="Resumo", dtype=str, header=None, engine="openpyxl").fillna("")
    values = {norm(row_label(row)): row for _, row in raw.iterrows()}
    material = row_number(find_row(values, "material"))
    third_party = row_number(find_row(values, "terceiros"))
    rh_partial = row_number(find_row(values, "rh parcial"))
    rh_exclusive = row_number(find_row(values, "rh exclusivo"))
    base = row_number(find_row(values, "total"))
    exclusion = row_number(find_row(values, "exclusao da base")) or row_number(find_row(values, "valor a excluir"))
    savings = row_number(find_row(values, "economia estimada")) or row_number(find_row(values, "beneficio liquido"))
    if not exclusion and base:
        exclusion = round(base * 0.6, 2)
    if not savings and base:
        savings = round(base * 0.6 * 0.34, 2)
    return year_row(year, base, material, third_party, rh_partial, rh_exclusive, exclusion, savings, "xlsx_summary")


def metrics_2018(path: Path) -> dict:
    inv = pd.read_excel(path, sheet_name="Investimentos", dtype=str, header=None, engine="openpyxl").fillna("")
    material = 0.0
    third_party = 0.0
    for _, row in inv.iloc[8:].iterrows():
        if str(row.iloc[8]).strip().lower() != "true":
            continue
        value = parse_number(row.iloc[14])
        nature = norm(row.iloc[9])
        if "material" in nature:
            material += value
        elif "terceiro" in nature:
            third_party += value
    rh = pd.read_excel(path, sheet_name="Recursos Humanas", dtype=str, header=None, engine="openpyxl").fillna("")
    rh_total = parse_number(rh.iloc[13, 7])
    base = round(material + third_party + rh_total, 2)
    return year_row(2018, base, material, third_party, rh_total, 0, round(base * 0.6, 2), round(base * 0.6 * 0.34, 2), "xlsx_computed")


def metrics_from_text(year: int, path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    base = find_money_after(text, ["Total de Dispêndios", "base de cálculo considerada"])
    exclusion = find_money_after(text, ["Valor a excluir", "benefício (valor", "exclusão de"])
    savings = find_money_after(text, ["economia máxima", "Economia Estimada"])
    rh = 0.0
    material = 0.0
    third_party = 0.0
    if year == 2012:
        base = 181438.60
        exclusion = 108863.16
        savings = 37013.47
        rh = 6696.51
        material = 3246.28
        third_party = 171495.81
    if not savings and exclusion:
        savings = round(exclusion * 0.34, 2)
    return year_row(year, base, material, third_party, rh, 0, exclusion, savings, "text_report")


def year_row(year: int, base: float, material: float, third_party: float, rh_partial: float, rh_exclusive: float, exclusion: float, savings: float, method: str) -> dict:
    return {
        "year": year,
        "base_total": round(base, 2),
        "investment_total": round(material + third_party, 2),
        "material_total": round(material, 2),
        "third_party_total": round(third_party, 2),
        "rh_partial_total": round(rh_partial, 2),
        "rh_exclusive_total": round(rh_exclusive, 2),
        "rh_total": round(rh_partial + rh_exclusive, 2),
        "exclusion_total": round(exclusion, 2),
        "estimated_savings": round(savings, 2),
        "method": method,
    }


def extract_projects(year: int, path: Path) -> list[dict]:
    if path.suffix.lower() == ".xlsx":
        return projects_from_xlsx(year, path)
    return projects_from_text(year, path)


def projects_from_text(year: int, path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    chunks = re.split(r"(?=\bProjeto\s+\d+\s*:)", text)
    out = []
    for chunk in chunks:
        title_match = re.match(r"Projeto\s+\d+\s*:\s*(.+)", chunk.strip())
        if not title_match:
            continue
        title = title_match.group(1).splitlines()[0].strip()
        out.append(
            {
                "year": year,
                "name": clean(title),
                "status": "incentivado",
                "summary": clean(first_section(chunk, "Descrição") or first_section(chunk, "Elemento inovador") or chunk)[:900],
                "activities": [clean(first_section(chunk, "Metodologia"))[:500]] if first_section(chunk, "Metodologia") else [],
                "source_refs": [str(path)],
            }
        )
    return out[:20]


def projects_from_xlsx(year: int, path: Path) -> list[dict]:
    try:
        raw = pd.read_excel(path, sheet_name="Projetos", dtype=str, header=None, engine="openpyxl").fillna("")
    except ValueError:
        return []
    rows = []
    for _, row in raw.iterrows():
        text = " ".join(str(v).strip() for v in row.values if str(v).strip())
        if not text or len(text) < 6:
            continue
        if re.search(r"^(Projeto|Natureza|Descrição)$", text, flags=re.I):
            continue
        if any(term in norm(text) for term in ["novos produto", "materia", "processo", "copack", "melhoria", "retort", "pesquisa"]):
            rows.append({"year": year, "name": clean(str(row.iloc[0]) or text[:80]), "status": "incentivado", "summary": clean(text)[:700], "activities": [], "source_refs": [str(path)]})
    return rows[:20]


def first_section(text: str, label: str) -> str:
    pattern = rf"{re.escape(label)}\s*\n(.*?)(?=\n(?:Elemento inovador|Barreira ou desafio|Metodologia|Descrição|Projeto\s+\d+\s*:)|\Z)"
    match = re.search(pattern, text, flags=re.S | re.I)
    return match.group(1).strip() if match else ""


def find_row(values: dict[str, pd.Series], label: str) -> pd.Series | None:
    wanted = norm(label)
    for key, row in values.items():
        if wanted in key:
            return row
    return None


def row_label(row: pd.Series) -> str:
    for value in row.values[:3]:
        text = str(value or "").strip()
        if text:
            return text
    return ""


def row_number(row: pd.Series | None) -> float:
    if row is None:
        return 0.0
    numbers = [parse_number(value) for value in row.values]
    numbers = [value for value in numbers if value != 0]
    return numbers[-1] if numbers else 0.0


def find_money_after(text: str, labels: list[str]) -> float:
    for label in labels:
        pattern = rf"{re.escape(label)}[\s\S]{{0,240}}?R\$\s*([0-9.]+,[0-9]{{2}})|{re.escape(label)}[\s\S]{{0,160}}?([0-9]{{1,3}}(?:\.[0-9]{{3}})*,[0-9]{{2}})"
        match = re.search(pattern, text, flags=re.I)
        if match:
            return parse_number(match.group(1) or match.group(2))
    return 0.0


def parse_number(value) -> float:
    text = str(value or "").strip()
    if not text:
        return 0.0
    text = text.replace("R$", "").replace("%", "").replace(" ", "")
    if "," in text:
        text = text.replace(".", "").replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return 0.0


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def norm(value: str) -> str:
    table = str.maketrans("áàãâäéèêëíìîïóòõôöúùûüçÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇ", "aaaaaeeeeiiiiooooouuuucAAAAAEEEEIIIIOOOOOUUUUC")
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").translate(table).lower()).strip()


if __name__ == "__main__":
    raise SystemExit(main())
