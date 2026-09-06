#!/usr/bin/env python3
"""Enrich sparse Quick info fields with 1–2 extra sentences of programme context."""
import csv
from pathlib import Path

CSV_PATH = Path(r"c:\Users\Kaja\Documents\Funds\updated file without VC - cleaned.csv")

QUICK_INFO = {
    # Empty
    "Care Tech Challenge": (
        "Annual Danish health-tech innovation challenge connecting startups with healthcare providers "
        "for pilot opportunities and visibility across the Danish hospital ecosystem."
    ),
    "Dineros Iværksetterlegat": (
        "Annual entrepreneur grant from Dineros for early-stage Danish founders with promising business ideas. "
        "Supports idea validation and early commercialisation steps."
    ),
    "JoinUp North": (
        "Annual Nordic startup gathering connecting founders, investors, and ecosystem players across the region. "
        "Cross-border networking and matchmaking — no funding attached."
    ),
    "Nordic Fintech Week": (
        "Annual fintech conference and networking week for Nordic fintech startups, investors, and financial institutions. "
        "Programme tracks, panels, and investor meetings across the Nordic ecosystem."
    ),
    "NOVI Legatet": (
        "Annual student innovation grant at NOVI science park (North Jutland) supporting entrepreneurship projects by students. "
        "Helps student teams test and develop early business ideas."
    ),
    "Odense Investor Summit": (
        "Annual investor–startup summit in Odense connecting Funen-region companies with angels, VCs, and corporates. "
        "Pitching and curated matchmaking for the local growth ecosystem."
    ),
    "Otto Bruuns Fond": (
        "Private foundation awarding annual grants for Danish research and innovation projects in technology and social impact. "
        "Supports development and early demonstration of new solutions."
    ),
    "Otto Mønsteds Fond": (
        "Private foundation awarding annual grants to Danish non-profits and research institutions in health, research, and culture. "
        "Typically funds exploratory or early-stage research and innovation activities."
    ),
    "StortTech Festival": (
        "Annual Danish deep-tech festival in Copenhagen celebrating science-based startups and research commercialisation. "
        "Showcases university spin-outs, deep-tech founders, and investor connections."
    ),
    "Velliv Foreningen": (
        "Annual grants from Velliv for Danish health, well-being, and social-impact projects. "
        "Supports piloting and early development of solutions that improve quality of life."
    ),
    # Too short — add programme substance (keep budget facts where useful)
    "MUDP": (
        "Ministry of Environment programme co-funding development, test, and demonstration of environmental technology "
        "(pre-projects, ETV, dev/demo, and flagship projects). Typical grants DKK 1–4M with ~50% co-financing. "
        "2025 allocation DKK 135M."
    ),
    "EUDP": (
        "Danish Energy Agency programme for industry-led consortia developing and demonstrating green energy technology "
        "(typically TRL 4–8). Co-financing ~40–60%; typical project size DKK 2–15M. 2025 funding DKK 543M."
    ),
    "EIC Pathfinder": (
        "EU programme for ambitious early-stage research consortia pursuing breakthrough science and technology (TRL 1–4). "
        "Pathfinder Open and Challenges calls; highly competitive. Total budget EUR 262M. Success rate ~2.1% (2025)."
    ),
    "EIC Accelerator": (
        "EU blended finance for single SMEs at TRL 6–8: grant up to €2.5M plus optional equity. "
        "Grant-only support available once per company under Horizon Europe."
    ),
    "LEO Innovation Lab": (
        "LEO Pharma's external innovation unit supporting digital health and dermatology startups with pilots, "
        "mentorship, and access to LEO Pharma labs and patient registries."
    ),
    "NNF Distinguished Innovator Grant": (
        "Novo Nordisk Foundation grant for senior Nordic researchers with proven track records to pursue "
        "high-impact innovation projects. Must act as innovation ambassador within academia. Duration 3 years."
    ),
    "UCPH Proof of Concept Fund (POC MAX)": (
        "UCPH proof-of-concept fund for researchers validating commercial potential of university discoveries. "
        "Duration 12–18 months; funds must be spent within the project period."
    ),
    "Villum Foundation and VELUX Group": (
        "Collaborative research funding for sustainable building technology, daylight, indoor climate, and biophilic design. "
        "VELUX contribution qualifies as co-financing for Innobooster or EUDP."
    ),
    "The Gate": (
        "UCPH/AU lighter-touch postdoc entrepreneur network offering sparring, community, and pathways toward spin-out. "
        "Complementary to Spin-outs Denmark for researchers exploring commercialisation."
    ),
    "Symbion / Copenhagen Science City": (
        "Copenhagen life-science incubator cluster in the Nørrebro/Frederiksberg innovation district. "
        "Symbion BioHub offers wet lab space at subsidised rates for biotech and health startups."
    ),
    "Novo Nordisk External Research and Open Innovation": (
        "Novo Nordisk's external innovation partnerships including option-to-licence deals on research collaborations. "
        "Deals may include upfront payments and milestones rather than traditional grant funding."
    ),
    "Accelerace": (
        "Denmark's leading equity-free accelerator: 6-month programme with mentoring, investor access, and DKK 100K stipend. "
        "Has supported 750+ startups since 2008."
    ),
}


def main():
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        fieldnames = reader.fieldnames
        rows = list(reader)

    changed = 0
    for row in rows:
        name = row["Name"]
        if name in QUICK_INFO:
            row["Quick info"] = QUICK_INFO[name]
            changed += 1

    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Enriched Quick info for {changed} rows")


if __name__ == "__main__":
    main()
