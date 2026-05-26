from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pdi_dashboard.analyzer import analyze_workbook
from pdi_dashboard.history import write_manifest
from pdi_dashboard.loader import export_sheets_to_csv, load_workbook


PRODIET_FILES = {
    2020: "02_1DjFpKAlzV5iE_fnqeUtW0mmrQdz_Sk5C_-aCpKsP-dc_xlsx.xlsx",
    2021: "03_1UQ9kgMSMfMe7eSzJ5xEb_gCdLqNBSOJIE0n1zIxUyQw_xlsx.xlsx",
    2023: "05_1ZvGnQ-g2Au2Q3y8Qq93x4y0z3rLQidzzfdNX6ypD_fQ_xlsx.xlsx",
    2024: "06_1AgMQv_FuFn6oJRpr_9mN9Lpi5mMzU3Kzkbkwa6EWXNQ_xlsx.xlsx",
    2025: "07_1WexcBwsjYvYbW9uz9D2MvgyVAqHpUCXSePu7SJFy0vA_xlsx.xlsx",
}

NEM_FILES = {
    2023: "01_1vmCroeJel-et_erRw0RevviFGKpUBN5SF4BWp7Zu2KE_xlsx.xlsx",
    2024: "02_1Ii-SbCWJO9K7bxXkmQ7TOfkPXf3kthJ4N26rafKpgzE_xlsx.xlsx",
    2025: "03_1KZbcFfptA_QFTg2VTzY8NtlgF2Du3nQRJVl1FmRvc4Y_xlsx.xlsx",
}

PRODIET_BLOCKED = {
    2022: "https://docs.google.com/spreadsheets/d/1V4Vb0mqRYB3VcAYk26NIq04arse2eO5rmIoZJYl2ux0/edit?usp=sharing"
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Normaliza planilhas modernas de historico.")
    parser.add_argument("--company", choices=["prodiet", "nem"], required=True)
    args = parser.parse_args()

    if args.company == "prodiet":
        payload = build_payload(
            company="PRODIET",
            slug="PRODIET_PD&I_2026",
            raw_dir=Path("data_sources/raw/prodiet"),
            file_map=PRODIET_FILES,
            output=Path("data_sources/extracted/prodiet_2019_2025.json"),
            csv_root=Path("exports/csv/prodiet_history_modern"),
            blocked=PRODIET_BLOCKED,
            extra_project_files={2019: "01_1lv_w4BqBWpf-3Y0vHm3v294Sih8dsCXX2ItrvgVn-mA_xlsx.xlsx"},
        )
    else:
        payload = build_payload(
            company="NETZSCH NEM",
            slug="NEM_PD&I_2026",
            raw_dir=Path("data_sources/raw/nem"),
            file_map=NEM_FILES,
            output=Path("data_sources/extracted/nem_2023_2025.json"),
            csv_root=Path("exports/csv/nem_history"),
            blocked={},
            extra_project_files={},
        )
    print(f"{payload['company']}: {len(payload['years'])} anos, {len(payload['projects'])} projetos/resumos")
    return 0


def build_payload(company: str, slug: str, raw_dir: Path, file_map: dict[int, str], output: Path, csv_root: Path, blocked: dict[int, str], extra_project_files: dict[int, str]) -> dict:
    years = []
    projects = []
    evidence = []
    source_files = []

    for year, filename in sorted(file_map.items()):
        path = raw_dir / filename
        source_files.append(str(path))
        sheets = load_workbook(path)
        export_sheets_to_csv(sheets, csv_root / path.stem)
        analysis = analyze_workbook(sheets, company=company, year=year, source=str(path))
        row = metrics_from_resumo(path, year)
        row["projects_total"] = analysis.get("metrics", {}).get("projects_total", 0)
        row["projects_incentivized"] = analysis.get("metrics", {}).get("projects_incentivized", 0)
        row["eligible_hours"] = analysis.get("metrics", {}).get("eligible_hours", 0)
        row["top_projects"] = analysis.get("metrics", {}).get("top_projects", [])
        row["source_refs"] = [str(path)]
        years.append(row)
        projects.extend(projects_from_analysis(year, analysis, str(path)))
        evidence.append(evidence_row(company, year, path, "alta", "RESUMO moderno lido diretamente por linha fiscal."))

    for year, filename in sorted(extra_project_files.items()):
        path = raw_dir / filename
        source_files.append(str(path))
        sheets = load_workbook(path)
        export_sheets_to_csv(sheets, csv_root / path.stem)
        analysis = analyze_workbook(sheets, company=company, year=year, source=str(path))
        projects.extend(projects_from_analysis(year, analysis, str(path)))
        evidence.append(
            {
                "company": company,
                "year": year,
                "source": str(path),
                "kind": "xlsx",
                "extracted_from": "abas de revisao de projetos",
                "confidence": "media",
                "notes": "Fonte textual/narrativa sem RESUMO financeiro identificado.",
            }
        )

    for year, url in blocked.items():
        evidence.append(
            {
                "company": company,
                "year": year,
                "source": url,
                "kind": "google_sheet",
                "extracted_from": "download",
                "confidence": "bloqueado",
                "notes": "Google retornou 401 Unauthorized na exportacao XLSX; ano ainda sem metricas normalizadas.",
            }
        )

    payload = {
        "company": company,
        "slug": slug,
        "source_type": "xlsx",
        "source_files": source_files,
        "years": years,
        "projects": projects,
        "evidence": evidence,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_manifest(payload, output.parent.parent / "evidence" / "manifest.csv")
    print(f"Arquivo gerado: {output.resolve()}")
    return payload


def metrics_from_resumo(path: Path, year: int) -> dict:
    df = pd.read_excel(path, sheet_name="RESUMO", dtype=str, header=None, engine="openpyxl").fillna("")
    rows = {norm(row_label(row)): row for _, row in df.iterrows() if row_label(row)}
    material = row_total(find_row(rows, "material"))
    third_party = row_total(find_row(rows, "terceiros"))
    rh_partial = row_total(find_row(rows, "rh parcial"))
    rh_exclusive = row_total(find_row(rows, "rh exclusivo"))
    base = row_total(find_row(rows, "total 1")) or row_total(find_row(rows, "total"))
    exclusion = row_total(find_row(rows, "total exclusao")) or row_total(find_row(rows, "exclusao da base"))
    savings = row_total(find_row(rows, "economia estimada"))
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
        "method": "xlsx_resumo_direct",
    }


def projects_from_analysis(year: int, analysis: dict, source: str) -> list[dict]:
    out = []
    for row in (analysis.get("tables", {}).get("projetos") or [])[:80]:
        title = first_value(row, ["Projeto", "Attach", "Nome"])
        if not title:
            continue
        desc = first_value(row, ["Descrição", "Elemento tecnologicamente novo ou inovador", "Elemento inovador"])
        out.append(
            {
                "year": year,
                "name": clean(title),
                "status": "incentivado" if truthy(first_value(row, ["Incentivado?", "Lei do Bem?", "Projeto incentivado?"])) else "nao informado",
                "summary": clean(desc)[:900],
                "activities": [],
                "source_refs": [source],
            }
        )
    return out


def evidence_row(company: str, year: int, path: Path, confidence: str, notes: str) -> dict:
    return {
        "company": company,
        "year": year,
        "source": str(path),
        "kind": "xlsx",
        "extracted_from": "RESUMO",
        "confidence": confidence,
        "notes": notes,
    }


def find_row(rows: dict[str, pd.Series], label: str) -> pd.Series | None:
    wanted = norm(label)
    for key, row in rows.items():
        if wanted in key:
            return row
    return None


def row_label(row: pd.Series) -> str:
    for value in row.values[:3]:
        text = str(value or "").strip()
        if text:
            return text
    return ""


def row_total(row: pd.Series | None) -> float:
    if row is None:
        return 0.0
    values = [parse_number(value) for value in row.values]
    values = [value for value in values if value != 0]
    return values[-1] if values else 0.0


def first_value(row: dict, candidates: list[str]) -> str:
    norm_map = {norm(key): value for key, value in row.items()}
    for candidate in candidates:
        value = norm_map.get(norm(candidate))
        if str(value or "").strip():
            return str(value)
    return ""


def truthy(value: str) -> bool:
    return norm(value) in {"true", "verdadeiro", "sim", "yes", "1"}


def parse_number(value) -> float:
    text = str(value or "").strip()
    if not text or text == "-":
        return 0.0
    text = text.replace("R$", "").replace("%", "").replace(" ", "")
    if "," in text:
        text = text.replace(".", "").replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return 0.0


def clean(value: str) -> str:
    return " ".join(str(value or "").split())


def norm(value: str) -> str:
    table = str.maketrans("áàãâäéèêëíìîïóòõôöúùûüçÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇ", "aaaaaeeeeiiiiooooouuuucAAAAAEEEEIIIIOOOOOUUUUC")
    return "".join(ch if ch.isalnum() else " " for ch in str(value or "").translate(table).lower()).strip()


if __name__ == "__main__":
    raise SystemExit(main())
