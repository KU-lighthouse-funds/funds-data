#!/usr/bin/env python3
"""List UCPH-supported rows with deadline text (for review)."""
import csv
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "funds with KU support - v4.csv"
with path.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f, delimiter=";"))

for r in rows:
    unit = (r.get("UCPH support unit") or "").strip()
    if unit in ("", "—", "-", "?"):
        continue
    name = r["Name"]
    dl = (r.get("Deadline") or "").strip()
    print(f"{name}\t{dl}")
