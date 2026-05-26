from __future__ import annotations

import ast
import csv
import json
import re
from pathlib import Path
from typing import Any


def load_history_for_company(company: str, slug: str | None = None, root: Path | str = "data_sources/extracted") -> dict[str, Any]:
    root_path = Path(root)
    if not root_path.exists():
        return {"years": [], "projects": [], "evidence": []}

    wanted = {safe_key(company), safe_key(slug or "")}
    years: list[dict[str, Any]] = []
    projects: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []

    for path in sorted(root_path.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload_company = safe_key(payload.get("company", ""))
        payload_slug = safe_key(payload.get("slug", ""))
        if wanted.isdisjoint({payload_company, payload_slug}):
            continue
        years.extend(payload.get("years") or [])
        projects.extend(payload.get("projects") or [])
        evidence.extend(payload.get("evidence") or [])

    years = sorted({int(row["year"]): row for row in years if row.get("year")}.values(), key=lambda row: row["year"])
    return {"years": years, "projects": projects, "evidence": evidence}


def extract_ndb_html(input_path: Path, output_path: Path) -> dict[str, Any]:
    text = input_path.read_text(encoding="utf-8", errors="ignore")
    raw_rows = parse_raw_data(text)
    hours = parse_year_object(text, "horasIncentivadas")
    collaborators = parse_year_object(text, "colaboradoresIncentivados")
    quarterly = parse_quarterly(text)

    years: list[dict[str, Any]] = []
    for row in raw_rows:
        year = int(row["year"])
        hour_row = hours.get(year, {})
        collaborator_row = collaborators.get(year, {})
        total = number(row.get("total"))
        benefit = row.get("beneficio")
        years.append(
            {
                "year": year,
                "base_total": total,
                "investment_total": round(number(row.get("material")) + number(row.get("terceiros")), 2),
                "material_total": number(row.get("material")),
                "third_party_total": number(row.get("terceiros")),
                "rh_partial_total": number(row.get("rhParcial")),
                "rh_exclusive_total": number(row.get("rhExclusivo")),
                "rh_total": round(number(row.get("rhParcial")) + number(row.get("rhExclusivo")), 2),
                "estimated_savings": None if benefit is None else number(benefit),
                "eligible_hours_partial": hour_row.get("parcial"),
                "eligible_hours_exclusive": hour_row.get("exclusiva"),
                "collaborators_partial": collaborator_row.get("parcial"),
                "collaborators_exclusive": collaborator_row.get("exclusiva"),
                "quarterly": quarterly.get(year, []),
                "source_refs": [input_path.name],
            }
        )

    payload = {
        "company": "NETZSCH NDB",
        "slug": "NDB_PD&I_2026",
        "source_type": "html",
        "source_files": [str(input_path)],
        "years": years,
        "projects": [],
        "evidence": [
            {
                "company": "NETZSCH NDB",
                "source": str(input_path),
                "kind": "html",
                "extracted_from": "JavaScript constants rawData, horasIncentivadas, colaboradoresIncentivados, quarterlyData",
                "confidence": "alta",
                "notes": "Historico anual ja estava estruturado no HTML enviado.",
            }
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_manifest(payload, output_path.parent.parent / "evidence" / "manifest.csv")
    return payload


def write_manifest(payload: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    if output_path.exists():
        with output_path.open("r", newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh, delimiter=";")
            rows = list(reader)

    new_rows = []
    replacement_keys = set()
    for evidence in payload.get("evidence", []):
        years = [{"year": evidence.get("year")}] if evidence.get("year") else (payload.get("years") or [{}])
        for row in years:
            new_row = {
                "company": payload.get("company", ""),
                "year": row.get("year", ""),
                "source": evidence.get("source", ""),
                "kind": evidence.get("kind", ""),
                "field": "historical_metrics",
                "confidence": evidence.get("confidence", ""),
                "notes": evidence.get("notes", ""),
            }
            replacement_keys.add((str(new_row["company"]), str(new_row["year"]), str(new_row["source"]), str(new_row["field"])))
            new_rows.append(new_row)

    kept_rows = [
        row
        for row in rows
        if (str(row.get("company", "")), str(row.get("year", "")), str(row.get("source", "")), str(row.get("field", ""))) not in replacement_keys
    ]
    with output_path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh, delimiter=";")
        columns = ["company", "year", "source", "kind", "field", "confidence", "notes"]
        writer.writerow(columns)
        for row in kept_rows + new_rows:
            writer.writerow([row.get(column, "") for column in columns])


def parse_raw_data(text: str) -> list[dict[str, Any]]:
    body = extract_js_block(text, "rawData", "[", "]")
    rows: list[dict[str, Any]] = []
    for item in re.finditer(r"\{(.*?)\}", body, flags=re.S):
        row: dict[str, Any] = {}
        for key, value in re.findall(r"(\w+)\s*:\s*([^,\n}]+)", item.group(1)):
            row[key] = eval_number(value)
        if row.get("year"):
            rows.append(row)
    return rows


def parse_year_object(text: str, variable: str) -> dict[int, dict[str, Any]]:
    body = extract_js_block(text, variable, "{", "}")
    out: dict[int, dict[str, Any]] = {}
    pattern = re.compile(r"(\d{4})\s*:\s*\{(.*?)\}", flags=re.S)
    for match in pattern.finditer(body):
        year = int(match.group(1))
        values: dict[str, Any] = {}
        for key, value in re.findall(r"(\w+)\s*:\s*(\"[^\"]*\"|'[^']*'|[^,\n}]+)", match.group(2)):
            values[key] = parse_literal(value)
        out[year] = values
    return out


def parse_quarterly(text: str) -> dict[int, list[dict[str, Any]]]:
    body = extract_js_block(text, "quarterlyData", "{", "}")
    out: dict[int, list[dict[str, Any]]] = {}
    for match in re.finditer(r"(\d{4})\s*:\s*\{(.*?)\n\s*\}", body, flags=re.S):
        year = int(match.group(1))
        total = parse_array(match.group(2), "total")
        benefit = parse_array(match.group(2), "benefit")
        labels = ["T1", "T2", "T3", "T4"]
        out[year] = [
            {"name": labels[idx], "base": total[idx] if idx < len(total) else 0, "savings": benefit[idx] if idx < len(benefit) else 0}
            for idx in range(max(len(total), len(benefit)))
        ]
    return out


def parse_array(text: str, key: str) -> list[float]:
    match = re.search(rf"{re.escape(key)}\s*:\s*\[(.*?)\]", text, flags=re.S)
    if not match:
        return []
    return [number(eval_number(part.strip())) for part in match.group(1).split(",") if part.strip()]


def extract_js_block(text: str, variable: str, opener: str, closer: str) -> str:
    match = re.search(rf"const\s+{re.escape(variable)}\s*=\s*{re.escape(opener)}", text)
    if not match:
        return ""
    start = match.end() - 1
    depth = 0
    for idx in range(start, len(text)):
        char = text[idx]
        if char == opener:
            depth += 1
        elif char == closer:
            depth -= 1
            if depth == 0:
                return text[start + 1 : idx]
    return ""


def eval_number(value: str) -> Any:
    value = value.strip().rstrip(",")
    if value == "null":
        return None
    if re.fullmatch(r"[0-9.\s+\-*/()]+", value):
        return safe_eval(value)
    return parse_literal(value)


def safe_eval(expression: str) -> float:
    node = ast.parse(expression, mode="eval")
    return float(eval_ast(node.body))


def eval_ast(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp):
        left = eval_ast(node.left)
        right = eval_ast(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -eval_ast(node.operand)
    raise ValueError(f"Expressao numerica nao suportada: {ast.dump(node)}")


def parse_literal(value: str) -> Any:
    value = value.strip().rstrip(",")
    if value in {"null", "undefined"}:
        return None
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return eval_number(value)


def number(value: Any) -> float:
    if value is None or value == "":
        return 0.0
    return round(float(value), 2)


def safe_key(value: str) -> str:
    text = str(value or "").lower()
    table = str.maketrans("áàãâäéèêëíìîïóòõôöúùûüç&", "aaaaaeeeeiiiiooooouuuuce")
    text = text.translate(table)
    return re.sub(r"[^a-z0-9]+", "_", text).strip("_")
