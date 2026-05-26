from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pdi_dashboard.history import extract_ndb_html


def main() -> int:
    parser = argparse.ArgumentParser(description="Extrai historico anual da NDB a partir do HTML legado.")
    parser.add_argument("--input", required=True, help="Caminho do HTML legado da NDB.")
    parser.add_argument("--output", default="data_sources/extracted/ndb_2011_2025.json", help="JSON historico de saida.")
    args = parser.parse_args()

    payload = extract_ndb_html(Path(args.input), Path(args.output))
    print(f"Historico extraido: {len(payload.get('years', []))} anos")
    print(f"Arquivo gerado: {Path(args.output).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
