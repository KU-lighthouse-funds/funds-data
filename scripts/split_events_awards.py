#!/usr/bin/env python3
"""Split Events/Awards into Events and Awards; refine award stages."""
import csv
from pathlib import Path

CSV_PATH = Path(r"c:\Users\Kaja\Documents\Funds\updated file without VC - cleaned.csv")

EVENTS = {
    "CPH Townhall",
    "Danish Entrepreneurship Festival",
    "Digital Tech Summit",
    "Founder Festival",
    "Ignite",
    "JoinUp North",
    "Nordic Fintech Week",
    "Nordic Innovation Fair",
    "Odense Investor Summit",
    "Startup Aarhus Townhall",
    "Startup Lab",
    "Startup Planet",
    "StortTech Festival",
    "TechBBQ",
    "SMIL",
    "Seedster",
}

AWARDS = {
    "Creative Business Cup",
    "EY Entrepreneur of the Year",
    "Global Startup Awards",
    "Green Leap Challenge",
    "Nordic Proptech Awards 2026",
    "Nordic Women in Tech Awards",
    "Odin Award",
}

# Stage and content fixes for awards
AWARD_UPDATES = {
    "EY Entrepreneur of the Year": {
        "Opportunity": "Awards",
        "Stage": "Growth/scale",
    },
    "Green Leap Challenge": {
        "Opportunity": "Awards",
        "Stage": "Early venture",
        "Quick info": "Annual cleantech/sustainability challenge with prize-based support for Danish green startups.",
    },
    "Nordic Proptech Awards 2026": {
        "Opportunity": "Awards",
        "Quick info": "Annual awards recognising leading Nordic proptech startups and innovations in real estate technology.",
    },
    "Global Startup Awards": {
        "Opportunity": "Awards",
    },
    "Nordic Women in Tech Awards": {
        "Opportunity": "Awards",
    },
    "Creative Business Cup": {
        "Opportunity": "Awards",
    },
    "Seedster": {
        "Opportunity": "Events",
    },
}


def main():
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        fieldnames = reader.fieldnames
        rows = list(reader)

    changed = 0
    for row in rows:
        if row["Opportunity"] not in ("Events/Awards", "Events", "Awards"):
            continue
        name = row["Name"]
        if name in EVENTS:
            row["Opportunity"] = "Events"
            changed += 1
        elif name in AWARDS:
            row["Opportunity"] = "Awards"
            changed += 1
        else:
            raise ValueError(f"Unclassified Events/Awards row: {name}")

        if name in AWARD_UPDATES:
            for k, v in AWARD_UPDATES[name].items():
                row[k] = v

    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    events = sum(1 for r in rows if r["Opportunity"] == "Events")
    awards = sum(1 for r in rows if r["Opportunity"] == "Awards")
    print(f"Split {changed} rows -> Events: {events}, Awards: {awards}")


if __name__ == "__main__":
    main()
