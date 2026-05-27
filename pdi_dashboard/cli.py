from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analyzer import analyze_workbook
from .html import render_dashboard, render_portfolio
from .history import load_history_for_company # Importa load_history_for_company
from .loader import export_sheets_to_csv, load_workbook


def build(args: argparse.Namespace) -> int:
    input_path = Path(args.input)
    output_path = Path(args.output)

    sheets = load_workbook(input_path)
    if not args.skip_csv_export:
        csv_dir = Path(args.csv_dir) if args.csv_dir else Path("exports") / "csv" / safe_name(input_path.stem or input_path.name)
        export_sheets_to_csv(sheets, csv_dir)

    # Carrega dados históricos para a empresa
    history_data = load_history_for_company(company=args.company, slug=safe_name(args.company))

    analysis = analyze_workbook(
        sheets,
        company=args.company,
        year=args.year,
        source=str(input_path),
        history_data=history_data, # Passa history_data
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_dashboard(analysis), encoding="utf-8")

    print(f"HTML gerado em: {output_path.resolve()}")
    print(f"Abas lidas: {len(sheets)}")
    if not args.skip_csv_export:
        print(f"CSVs brutos exportados em: {csv_dir.resolve()}")
    return 0


def portfolio(args: argparse.Namespace) -> int:
    config_path = Path(args.config)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    output_path = Path(args.output or config.get("output") or "dist/portfolio_pdi.html")
    csv_root = Path(args.csv_root or config.get("csv_root") or "exports/csv")
    companies = config.get("companies") or []
    if not companies:
        raise ValueError("Config sem empresas em 'companies'.")

    analyses = []
    for company in companies:
        name = company["name"]
        input_path = Path(company["input"])
        year = company.get("year", config.get("year"))
        csv_dir = csv_root / safe_name(company.get("slug") or name)

        sheets = load_workbook(input_path)
        export_sheets_to_csv(sheets, csv_dir)
        history_data = load_history_for_company(company=name, slug=company.get("slug")) # Carrega histórico para cada empresa
        analysis = analyze_workbook(sheets, company=name, year=year, source=str(input_path), history_data=history_data) # Passa history_data
        analysis["slug"] = company.get("slug") or safe_name(name)
        analysis["csv_dir"] = str(csv_dir)
        analyses.append(analysis)
        print(f"{name}: {len(sheets)} abas lidas, CSVs em {csv_dir.resolve()}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_portfolio(analyses, title=config.get("title", "Painel Executivo PD&I")), encoding="utf-8")
    print(f"HTML portfolio gerado em: {output_path.resolve()}")
    return 0


def safe_name(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in value.strip())
    return cleaned.strip("._") or "base"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pdi_dashboard",
        description="Gera um dashboard HTML estatico a partir de XLSX/CSVs de PD&I.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    build_parser = sub.add_parser("build", help="Gerar dashboard HTML")
    build_parser.add_argument("--input", required=True, help="Arquivo .xlsx ou pasta com CSVs")
    build_parser.add_argument("--output", required=True, help="Arquivo HTML de saida")
    build_parser.add_argument("--company", default="Empresa", help="Nome da empresa")
    build_parser.add_argument("--year", type=int, default=None, help="Ano-base do dashboard")
    build_parser.add_argument("--csv-dir", default=None, help="Pasta para salvar um CSV bruto por aba")
    build_parser.add_argument("--skip-csv-export", action="store_true", help="Nao exportar CSVs brutos das abas")
    build_parser.set_defaults(func=build)

    portfolio_parser = sub.add_parser("portfolio", help="Gerar painel multiempresa")
    portfolio_parser.add_argument("--config", required=True, help="JSON com empresas e caminhos XLSX/CSV")
    portfolio_parser.add_argument("--output", default=None, help="Arquivo HTML de saida")
    portfolio_parser.add_argument("--csv-root", default=None, help="Pasta raiz para CSVs por empresa")
    portfolio_parser.set_defaults(func=portfolio)

    args = parser.parse_args(argv)
    return args.func(args)
