#!/usr/bin/env python3
"""Replace combined BII row with Bio Studio, Venture Lab, and Quantum Lab."""
import csv
from pathlib import Path

CSV_PATH = Path(r"c:\Users\Kaja\Documents\Funds\updated file without VC - cleaned.csv")

BII_PROGRAMS = [
    {
        "Opportunity": "Incubator/Accelerator",
        "Name": "BII Bio Studio",
        "Link": "https://bii.dk/programs/bio-studio/",
        "Criteria": "Principal Investigator (prof/assoc prof, 3+ years as independent group leader); challenge-call scoped; pre-commercial project with no existing company or external investment",
        "Industrial segment": "Biotech, Health, Cleantech",
        "Stage": "Exploratory innovation",
        "Geography": "DK",
        "Funding Amount": "Up to DKK 5.35M/year for up to 3 years (in-kind; convertible loan in year 3)",
        "Deadline": "Challenge calls ~2x/year (typically May and December)",
        "Quick info": "Company-creation programme for academic researchers. Highly selective multi-step process (expression of interest, scientific pitch, diligence; ~6–7 months). BII encourages early dialogue on project fit before applying. Project team is hired at BII; Entrepreneur-in-Residence leads company formation (spin-out typically around year 2). Thematic calls in Human Health, Planetary Health, and related focus areas.",
        "CVR required at application": "No",
        "CVR required at programme start": "No",
    },
    {
        "Opportunity": "Incubator/Accelerator",
        "Name": "BII Venture Lab",
        "Link": "https://bii.dk/programs/venture-lab/",
        "Criteria": "Early-stage life science or deep tech startup; Danish CVR required for funding; prioritises Danish HQ, operations, and leadership",
        "Industrial segment": "Biotech, Health, Deep Tech, Cleantech",
        "Stage": "Early venture",
        "Geography": "DK",
        "Funding Amount": "DKK 4.2M founder-friendly convertible loan (12 months)",
        "Deadline": "Per open call (rolling between calls)",
        "Quick info": "12-month accelerator maturing science and business readiness. Open-call programme for incorporated startups in Human Health, Planetary Health, and Quantum. May apply before CVR exists if a clear plan to establish a Danish entity before programme start. Eligible Danish teams may later apply for Venture House follow-on (DKK 10.5M).",
        "CVR required at application": "Optional",
        "CVR required at programme start": "Yes",
    },
    {
        "Opportunity": "Incubator/Accelerator",
        "Name": "BII Quantum Lab",
        "Link": "https://bii.dk/programs/quantum-lab/",
        "Criteria": "Early-stage startup HQ in NATO country; dual-use quantum technology addressing NATO DIANA challenge areas",
        "Industrial segment": "Quantum Tech, Defense Tech, Deep Tech",
        "Stage": "Early venture",
        "Geography": "Nordics",
        "Funding Amount": "EUR 100K contractual funding (6 months)",
        "Deadline": "Per programme call",
        "Quick info": "6-month programme (formerly Deep Tech Lab – Quantum), run with NATO DIANA. Supports dual-use quantum technologies with both civilian and defence applications. Access to NATO-wide defence, security, and resilience networks.",
        "CVR required at application": "Yes",
        "CVR required at programme start": "Yes",
    },
]


def main():
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        fieldnames = reader.fieldnames
        rows = [
            r
            for r in reader
            if r["Name"] != "Bio Innovation Institute (BII)"
        ]

    # Insert BII programmes where the old row was (alphabetically by name after removal)
    rows.extend(BII_PROGRAMS)
    rows.sort(key=lambda r: r["Name"].lower())

    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Replaced BII with {len(BII_PROGRAMS)} programme rows")
    print(f"Total rows: {len(rows)}")


if __name__ == "__main__":
    main()
