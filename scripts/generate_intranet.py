from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pdi_dashboard.analyzer import analyze_workbook
from pdi_dashboard.cli import safe_name
from pdi_dashboard.history import load_history_for_company
from pdi_dashboard.intranet import render_intranet_site
from pdi_dashboard.loader import export_sheets_to_csv, load_workbook


def analyze_with_history(sheets, *, company: str, year: int | None, source: str, history: dict) -> dict:
    try:
        return analyze_workbook(sheets, company=company, year=year, source=source, history_data=history)
    except TypeError:
        analysis = analyze_workbook(sheets, company=company, year=year, source=source)
        analysis["history"] = history
        return analysis


def main() -> int:
    parser = argparse.ArgumentParser(description="Gera o hotsite intranet de relatorios PD&I.")
    parser.add_argument("--config", default="empresas_pdi_2026.json")
    parser.add_argument("--output", default="dist/intranet_pdi.html")
    parser.add_argument("--csv-root", default=None)
    parser.add_argument("--title", default="TTC CST Intranet PD&I")
    parser.add_argument("--sheets-url", default="")
    args = parser.parse_args()

    config_path = Path(args.config)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    csv_root = Path(args.csv_root or config.get("csv_root") or "exports/csv")
    analyses: list[dict] = []

    for company in config.get("companies") or []:
        name = company["name"]
        input_path = Path(company["input"])
        year = company.get("year", config.get("year"))
        slug = company.get("slug") or safe_name(name)
        csv_dir = csv_root / safe_name(slug)

        source_path = input_path if input_path.exists() else csv_dir
        sheets = load_workbook(source_path)
        if input_path.exists():
            export_sheets_to_csv(sheets, csv_dir)
        history = load_history_for_company(company=name, slug=company.get("slug"))
        analysis = analyze_with_history(sheets, company=name, year=year, source=str(source_path), history=history)
        analysis["slug"] = slug
        analysis["csv_dir"] = str(csv_dir)
        analyses.append(analysis)
        print(f"{name}: {len(sheets)} abas lidas para intranet")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_intranet_site(
            analyses,
            title=args.title or config.get("intranet_title", "Intranet PD&I"),
            sheets_url=args.sheets_url or config.get("sheets_url", ""),
        ),
        encoding="utf-8",
    )
    print(f"HTML intranet gerado em: {output_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
