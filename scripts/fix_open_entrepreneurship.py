#!/usr/bin/env python3
"""Fix Open Entrepreneurship row (was wrongly linked to startupdenmark.info)."""
import csv
from pathlib import Path

CSV_PATH = Path(r"c:\Users\Kaja\Documents\Funds\updated file without VC - cleaned.csv")

OPEN_ENTREPRENEURSHIP = {
    "Opportunity": "Incubator/Accelerator",
    "Name": "Open Entrepreneurship",
    "Link": "https://open-entrepreneurship.com/",
    "Criteria": "Researchers at Danish universities with research-based commercialisation potential",
    "Industrial segment": "Tech, Health, Biotech, General",
    "Stage": "Exploratory innovation",
    "Geography": "DK",
    "Funding Amount": "No direct funding (network and programmes)",
    "Deadline": "Rolling",
    "Quick info": (
        "National collaboration across all 8 Danish universities (since 2017; now state-funded). "
        "Matches researchers with external entrepreneurs and investors via co-founder runs, investor match, "
        "and E-corps. Verticals: Deep Tech, Life Sciences, Digital, SHAPE. Gateway to Innoexplorer and spin-out pathways."
    ),
    "CVR required at application": "No",
    "CVR required at programme start": "No",
}

def main():
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        fieldnames = reader.fieldnames
        rows = list(reader)

    updated = False
    for row in rows:
        if "Open Entrepreneur" in row["Name"] or row["Name"] == "Open Entrepreneurship":
            row.update(OPEN_ENTREPRENEURSHIP)
            updated = True
        if row["Name"] == "Start-up Denmark":
            row["_remove"] = True
        if row["Name"] in ("UCPH Lighthouse", "Copenhagen School of Entrepreneurship (CSE)"):
            row["_remove"] = True
        if "cse.ku.dk" in row.get("Link", ""):
            row["_remove"] = True
        if row["Name"] in ("Accelerace", "Symbion / Copenhagen Science City", "The Gate"):
            row["_remove"] = True

    rows = [r for r in rows if not r.pop("_remove", False)]

    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Fixed Open Entrepreneurship row: {updated}")
    print(f"Total rows: {len(rows)}")


if __name__ == "__main__":
    main()
