#!/usr/bin/env python3
"""Apply stage taxonomy rules locally (idempotent)."""
import csv
from collections import Counter
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent / "funds with KU support - v4.csv"

# Named corrections from Lighthouse / Preaward discussion.
OVERRIDES = {
    "EIC Transition": "Venture formation",
    "NextGen Innovation (Odense Robotics)": "Venture formation",
    "IFD Innofounder": "Venture formation",
    "NNF Pioneer Innovator Grant": "Exploratory innovation",
    "Karl Pedersen og Hustrus Industrifond": "Growth/scale",
    "BII Bio Studio": "Venture formation",
    "Eureka": "Venture formation",
    "IFD Industrial Researcher (Industrial PhD/Postdoc)": "Venture formation",
    "LEO Innovation Lab": "Venture formation",
    "Nordic Innovation": "Venture formation",
    "Patent og Varemærkestyrelsen": "Venture formation",
    "Vissing Fonden": "Venture formation",
}


def cvr_at_application(row: dict) -> str:
    return (row.get("CVR at application") or "Any").strip()


def apply_rules(row: dict) -> str:
    stage = (row.get("Stage") or "").strip()
    name = row.get("Name", "")

    if name in OVERRIDES:
        return OVERRIDES[name]

    # Commercial validation = pre-CVR university maturation; not CVR-required schemes.
    if stage == "Commercial validation" and cvr_at_application(row) == "Yes":
        return "Venture formation"

    return stage


def main() -> None:
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter=";"))
        fieldnames = list(rows[0].keys()) if rows else []

    for row in rows:
        row["Stage"] = apply_rules(row)

    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    counts = Counter(r["Stage"] for r in rows)
    print(f"Updated {len(rows)} rows in {CSV_PATH.name}")
    for stage, count in counts.most_common():
        print(f"  {count:3}  {stage}")

    print("\nCommercial validation remaining:")
    for r in rows:
        if r["Stage"] == "Commercial validation":
            print(f"  {r['Name'][:55]:55} apply={cvr_at_application(r)}")


if __name__ == "__main__":
    main()
