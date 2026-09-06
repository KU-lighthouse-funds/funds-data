#!/usr/bin/env python3
"""Set accurate Funding Amount for Awards; reclassify mis-tagged entries."""
import csv
from pathlib import Path

CSV_PATH = Path(r"c:\Users\Kaja\Documents\Funds\updated file without VC - cleaned.csv")

# Reclassify: paid bootcamp / networking festival are Events, not Awards
RECLASSIFY_TO_EVENTS = {
    "Seedster": {
        "Opportunity": "Events",
        "Funding Amount": "Paid attendance (~€995+ excl. VAT)",
        "Quick info": (
            "Week-long entrepreneurship bootcamp in Marbella (not a pitch competition). "
            "Mentorship, workshops, and networking; fee covers programme, catering, and hotel."
        ),
    },
    "SMIL": {
        "Opportunity": "Events",
        "Funding Amount": "",
        "Quick info": (
            "Aarhus startup festival connecting founders, investors, and ecosystem actors. "
            "Focus on curated networking and honest conversations — not a cash-prize competition."
        ),
    },
}

# Funding Amount vocabulary:
# - Specific DKK/EUR when documented
# - "Recognition only" = prestige/visibility, no standard cash prize
# - "Varies (cash + in-kind)" = prize competition but amount changes yearly
AWARD_FUNDING = {
    "Creative Business Cup": "Varies (e.g. DKK 10K–25K cash + in-kind; sponsor packages vary yearly)",
    "EY Entrepreneur of the Year": "Recognition only (no cash prize)",
    "Global Startup Awards": "Recognition only (in-kind from sponsors)",
    "Green Leap Challenge": "DKK 50K per winner (3 prizes/year)",
    "Nordic Proptech Awards 2026": "Recognition only (in-kind: mentorship, membership)",
    "Nordic Women in Tech Awards": "Recognition only (no cash prize)",
    "Odin Award": "DKK 40K (main prize; category amounts vary)",
}


def main():
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        fieldnames = reader.fieldnames
        rows = list(reader)

    changed = 0
    for row in rows:
        name = row["Name"]
        if name in RECLASSIFY_TO_EVENTS:
            for k, v in RECLASSIFY_TO_EVENTS[name].items():
                row[k] = v
            changed += 1
        elif row["Opportunity"] == "Awards" and name in AWARD_FUNDING:
            if row.get("Funding Amount") != AWARD_FUNDING[name]:
                row["Funding Amount"] = AWARD_FUNDING[name]
                changed += 1

    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    events = sum(1 for r in rows if r["Opportunity"] == "Events")
    awards = sum(1 for r in rows if r["Opportunity"] == "Awards")
    print(f"Updated {changed} rows -> Events: {events}, Awards: {awards}")


if __name__ == "__main__":
    main()
