from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

import requests


def main() -> int:
    parser = argparse.ArgumentParser(description="Baixa/exporta fontes publicas do Google Drive/Docs.")
    parser.add_argument("--links", required=True, help="JSON com a lista de links.")
    parser.add_argument("--out", required=True, help="Pasta de destino.")
    args = parser.parse_args()

    payload = json.loads(Path(args.links).read_text(encoding="utf-8"))
    output_dir = Path(args.out)
    output_dir.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    manifest = []

    for idx, url in enumerate(payload.get("links") or [], start=1):
        parsed = parse_google_url(url)
        if not parsed:
            manifest.append({"index": idx, "url": url, "status": "unsupported"})
            continue
        downloads = export_urls(parsed)
        for kind, download_url, extension in downloads:
            target = output_dir / f"{idx:02d}_{parsed['id']}_{kind}.{extension}"
            status = download(session, download_url, target)
            manifest.append(
                {
                    "index": idx,
                    "url": url,
                    "document_id": parsed["id"],
                    "type": parsed["type"],
                    "kind": kind,
                    "target": str(target),
                    "status": status,
                }
            )
            print(f"{idx:02d} {kind}: {status} -> {target}")

    (output_dir / "_download_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


def parse_google_url(url: str) -> dict[str, str] | None:
    parsed = urlparse(url)
    match = re.search(r"/(?:spreadsheets|document|file)/d/([^/]+)", parsed.path)
    if not match:
        return None
    if "/spreadsheets/" in parsed.path:
        doc_type = "spreadsheet"
    elif "/document/" in parsed.path:
        doc_type = "document"
    else:
        doc_type = "file"
    query = parse_qs(parsed.query)
    resource_key = (query.get("resourcekey") or [""])[0]
    return {"id": match.group(1), "type": doc_type, "resourcekey": resource_key}


def export_urls(item: dict[str, str]) -> list[tuple[str, str, str]]:
    doc_id = item["id"]
    resource_key = item.get("resourcekey")
    extra = {"resourcekey": resource_key} if resource_key else {}
    if item["type"] == "spreadsheet":
        return [("xlsx", google_url("https://docs.google.com/spreadsheets/d/{id}/export", doc_id, {"format": "xlsx", **extra}), "xlsx")]
    if item["type"] == "document":
        return [
            ("docx", google_url("https://docs.google.com/document/d/{id}/export", doc_id, {"format": "docx", **extra}), "docx"),
            ("txt", google_url("https://docs.google.com/document/d/{id}/export", doc_id, {"format": "txt", **extra}), "txt"),
        ]
    return [("file", google_url("https://drive.google.com/uc", doc_id, {"export": "download", "id": doc_id, **extra}), "bin")]


def google_url(template: str, doc_id: str, query: dict[str, str]) -> str:
    return template.format(id=doc_id) + "?" + urlencode(query)


def download(session: requests.Session, url: str, target: Path) -> str:
    try:
        response = session.get(url, stream=True, timeout=60)
        response.raise_for_status()
    except Exception as exc:
        return f"error: {exc}"

    content_type = response.headers.get("content-type", "")
    chunks = []
    total = 0
    for chunk in response.iter_content(chunk_size=1024 * 512):
        if chunk:
            chunks.append(chunk)
            total += len(chunk)
            if total > 250 * 1024 * 1024:
                return "error: arquivo maior que 250MB"
    data = b"".join(chunks)
    if b"Google Drive - Virus scan warning" in data or b"confirm=" in data[:200000]:
        confirm = find_confirm_token(data.decode("utf-8", errors="ignore"))
        if confirm:
            separator = "&" if "?" in url else "?"
            return download(session, f"{url}{separator}confirm={confirm}", target)
    target.write_bytes(data)
    if "text/html" in content_type and not data.lower().lstrip().startswith(b"<!doctype html") and not data.lower().lstrip().startswith(b"<html"):
        return "downloaded_html_like"
    return f"downloaded:{len(data)}"


def find_confirm_token(html: str) -> str:
    match = re.search(r"confirm=([0-9A-Za-z_]+)", html)
    return match.group(1) if match else ""


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        sys.exit(130)
