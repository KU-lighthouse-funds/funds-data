#!/usr/bin/env python3
"""Refresh stale 2026 deadline strings (as of 10 Sep 2026)."""
import csv
from pathlib import Path

CSV = Path(__file__).resolve().parents[1] / "funds with KU support - v4.csv"

# Deadline column only — keep Quick info for substance, trim past-only anchors where duplicated.
DEADLINE = {
    "BII Upscalator": "Periodic calls (Sep 2026 closed 1 Sep; watch bii.dk)",
    "Founder Festival": "Annual (varies)",
    "Eurostars": "2x/year (next cut-off ~March 2027)",
    "EIC Accelerator": "6 batches/year (next: November 2026)",
    "EIC Pathfinder": "2x/year (next: October 2026)",
    "Carlsbergfondet": "Annual autumn call (1 Sep; 2026 round closed)",
    "ERC Proof of Concept": "2 cut-offs/year (next: 17 Sep 2026)",
    "EIC Transition": "Annual (closes 16 Sep 2026)",
    "IFD Innobooster": "4 windows/year (next closes 15 Oct 2026)",
    "Mikrolegat": "4x/year (next: 15 Nov 2026; Momentum 30 Nov 2026)",
    "Otto Bruuns Fond – Industrielle projekter": "4 rounds/year (next: 1 Nov 2026)",
    "Otto Bruuns Fond – Almennyttige projekter": "4 rounds/year (next: 1 Nov 2026)",
    "Karl Pedersen og Hustrus Industrifond": "Annual window — closes 30 Sep 2026",
}

QUICK_PATCHES = {
    "IFD Grand Solutions": (
        "Separate Defence technology call is one-phase with deadline 1 September 2026.",
        "Defence technology call (1 Sep 2026) has closed; main themes use two-phase Mar/Sep process.",
    ),
    "BII Upscalator": (
        "Up to four decision cycles per year (next: 1 September 2026, 14:00 CEST)",
        "Sep 2026 call closed 1 September 2026; further calls announced on bii.dk.",
    ),
}


def main() -> None:
    with CSV.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        fields = reader.fieldnames
        rows = list(reader)

    n_dl = n_qi = 0
    for row in rows:
        name = row["Name"]
        if name in DEADLINE:
            row["Deadline"] = DEADLINE[name]
            n_dl += 1
        if name in QUICK_PATCHES:
            old, new = QUICK_PATCHES[name]
            qi = row.get("Quick info", "")
            if old in qi:
                row["Quick info"] = qi.replace(old, new)
                n_qi += 1

    with CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter=";", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    print(f"Updated {n_dl} deadlines, {n_qi} quick-info patches")


if __name__ == "__main__":
    main()
