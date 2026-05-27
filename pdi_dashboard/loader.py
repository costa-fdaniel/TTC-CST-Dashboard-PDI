from __future__ import annotations

import csv
import re
from pathlib import Path

import pandas as pd


SheetMap = dict[str, pd.DataFrame]


def load_workbook(path: Path) -> SheetMap:
    if not path.exists():
        raise FileNotFoundError(f"Entrada nao encontrada: {path}")

    suffix = path.suffix.lower()
    if suffix == ".gsheet":
        raise ValueError(
            "Arquivos .gsheet sao atalhos do Google Drive. Exporte a planilha como .xlsx "
            "ou CSVs e rode o comando novamente."
        )

    if path.is_dir():
        return _load_csv_folder(path)

    if suffix in {".xlsx", ".xlsm", ".xls"}:
        return _load_excel(path)

    if suffix == ".csv":
        return {path.stem: _read_csv(path)}

    raise ValueError(f"Formato nao suportado: {path.suffix}")


def export_sheets_to_csv(sheets: SheetMap, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_rows = [["sheet_name", "csv_file", "rows", "columns"]]
    used_names: dict[str, int] = {}
    for sheet_name, df in sheets.items():
        filename = _unique_csv_name(sheet_name, used_names)
        target = output_dir / filename
        df.to_csv(target, index=False, header=False, encoding="utf-8-sig", sep=";")
        rows = int(df.shape[0])
        cols = int(df.shape[1]) if not df.empty else 0
        manifest_rows.append([sheet_name, filename, str(rows), str(cols)])

    with (output_dir / "_manifest.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh, delimiter=";")
        writer.writerows(manifest_rows)


def _load_excel(path: Path) -> SheetMap:
    raw = pd.read_excel(path, sheet_name=None, dtype=str, header=None, engine="openpyxl")
    return {name: _strip_empty(df) for name, df in raw.items()}


def _load_csv_folder(path: Path) -> SheetMap:
    sheets: SheetMap = {}
    for file in sorted(path.glob("*.csv")):
        sheets[file.stem] = _read_csv(file)
    if not sheets:
        raise ValueError(f"Nenhum CSV encontrado em: {path}")
    return sheets


def _read_csv(path: Path) -> pd.DataFrame:
    encoding_candidates = ["utf-8-sig", "utf-8", "cp1252", "latin1"]
    sample = path.read_bytes()[:8192]
    delimiter = _sniff_delimiter(sample) or ";"

    for encoding in encoding_candidates:
        try:
            return _strip_empty(pd.read_csv(path, dtype=str, header=None, sep=delimiter, encoding=encoding))
        except pd.errors.EmptyDataError:
            return pd.DataFrame()
        except UnicodeDecodeError:
            continue
    try:
        return _strip_empty(pd.read_csv(path, dtype=str, header=None, sep=delimiter, encoding="latin1"))
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def _sniff_delimiter(sample: bytes) -> str | None:
    text = sample.decode("utf-8", errors="ignore")
    try:
        return csv.Sniffer().sniff(text, delimiters=",;\t|").delimiter
    except csv.Error:
        return None


def _strip_empty(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.map(lambda v: "" if pd.isna(v) else str(v).strip())
    df = df.loc[~df.apply(lambda row: all(v == "" for v in row), axis=1)]
    if df.empty:
        return pd.DataFrame()
    df = df.loc[:, ~df.apply(lambda col: all(v == "" for v in col), axis=0)]
    df.columns = range(df.shape[1])
    return df.reset_index(drop=True)


def _safe_filename(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._ -]+", "_", value).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned[:120].strip(" ._") or "aba"


def _unique_csv_name(sheet_name: str, used: dict[str, int]) -> str:
    base = _safe_filename(sheet_name)
    count = used.get(base, 0)
    used[base] = count + 1
    suffix = "" if count == 0 else f"_{count + 1}"
    return f"{base}{suffix}.csv"


def canonical_sheet_name(name: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", " ", _ascii_fold(name).lower()).strip()
    aliases = {
        "resumo": "resumo",
        "projetos": "projetos",
        "trabalho": "trabalho",
        "pessoal": "pessoal",
        "pessoal 2": "pessoal",
        "investimentos": "investimentos",
        "dias uteis e feriados": "dias_uteis",
        "dias uteis feriados": "dias_uteis",
        "encargos folha": "encargos",
        "salarios": "salarios",
        "verificacao rh": "verificacao_rh",
        "riscos e oportunidades": "riscos_oportunidades", # Nova aba
    }
    aliases["riscos"] = "riscos"
    return aliases.get(cleaned, cleaned.replace(" ", "_"))


def _ascii_fold(value: str) -> str:
    table = str.maketrans("áàãâäéèêëíìîïóòõôöúùûüçÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇ", "aaaaaeeeeiiiiooooouuuucAAAAAEEEEIIIIOOOOOUUUUC")
    return value.translate(table)
