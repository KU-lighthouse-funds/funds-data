#!/usr/bin/env python3
"""Consolidate Stage column and complete CVR governance pass."""
import csv
from pathlib import Path

CSV_PATH = Path(r"c:\Users\Kaja\Documents\Funds\updated file without VC - cleaned.csv")

# Controlled stage vocabulary (single Stage column)
STAGE = {
    "Akademikernes Startup": "Early venture",
    "Beta Health": "PoC",
    "Beyond Beta": "Growth/scale",
    "BII Bio Studio": "Exploratory innovation",
    "CBS CSE (Copenhagen School of Entrepreneurship)": "Early venture",
    "BII Quantum Lab": "Early venture",
    "BII Venture Lab": "Early venture",
    "Bio Innovation Institute (BII)": "PoC",  # legacy if rebuild from old source
    "Cancute": "Growth/scale",
    "Care Tech Challenge": "Early venture",
    "Climate-KIC Urban Mobility Food": "Early venture",
    "Copenhagen Health Innovators": "Early venture",
    "CPH Townhall": "All stages",
    "Creative Business Cup": "Early venture",
    "Danish Entrepreneurship Festival": "All stages",
    "Defence Tech Denmark": "Early venture",
    "DIF Innovation Lab": "Early venture",
    "Digital Tech Summit": "All stages",
    "Dineros Iværksetterlegat": "Early venture",
    "Diversity Commitment": "Early venture",
    "DSV Group Innovation Partnerships": "Growth/scale",
    "EESA": "Early venture",
    "EIC Accelerator": "Growth/scale",
    "EIC Pathfinder": "Exploratory innovation",
    "EIC Transition": "PoC",
    "EUDP": "Growth/scale",
    "Eureka": "PoC",
    "Eurostars": "Growth/scale",
    "Even Founders": "Early venture",
    "EY Entrepreneur of the Year": "Growth/scale",
    "Fonden for Entreprenørskab": "Early venture",
    "Food and Bio Cluster": "Early venture",
    "Found Diverse": "Early venture",
    "Founder Festival": "Early venture",
    "Founder to Leader": "Growth/scale",
    "Future Manufacturers": "Early venture",
    "Game Hub": "Early venture",
    "Global Startup Awards": "All stages",
    "Green Leap Challenge": "Early venture",
    "GUDP": "Growth/scale",
    "HeyFunding Legatet": "Early venture",
    "Horizon Europe": "Exploratory innovation",
    "Hub for Innovation in Tourism": "Early venture",
    "Ideas Lab": "PoC",
    "IFD Grand Solutions": "Growth/scale",
    "IFD Innobooster": "Growth/scale",
    "IFD Innoexplorer": "PoC",
    "IFD Industrial Researcher (Industrial PhD/Postdoc)": "PoC",
    "IFD Innofounder": "Early venture",
    "Ignite": "All stages",
    "Incuba": "Early venture",
    "Intech Founders": "Early venture",
    "ITU Business Development": "Early venture",
    "JoinUp North": "All stages",
    "Kvinde kompagniet": "Early venture",
    "Ladies First": "Early venture",
    "Leap Forward": "Early venture",
    "Lighthouse Launch": "Exploratory innovation",
    "LEO Innovation Lab": "PoC",
    "Lundbeck Frontier": "Exploratory innovation",
    "Maritime Stars": "Early venture",
    "Mikrolegat": "Early venture",
    "Miljø- og Energi Fonden": "PoC",
    "MUDP": "Growth/scale",
    "Neighborhood": "Early venture",
    "Next Women": "Early venture",
    "NextGen Innovation and Startup Hub": "Early venture",
    "NNF Distinguished Innovator Grant": "Exploratory innovation",
    "NNF Pioneer Innovator Grant": "Exploratory innovation",
    "Nordic Female Founders": "Early venture",
    "Nordic Fintech Week": "All stages",
    "Nordic Innovation": "PoC",
    "Nordic Innovation Fair": "All stages",
    "Nordic Proptech Awards 2026": "Early venture",
    "Nordic Women in Tech Awards": "All stages",
    "Nordic Women\u2019s Health Hub": "Early venture",
    "Nordlys Vækstpulje": "Growth/scale",
    "NOVI Legatet": "Early venture",
    "Novo Nordisk External Research and Open Innovation": "PoC",
    "Novo Nordisk Foundation Fellowship Program Biomedical Design": "Exploratory innovation",
    "Odense Investor Summit": "All stages",
    "Odense Robotics Startup Fund": "Early venture",
    "Odin Award": "All stages",
    "Open Discovery Innovation Network (ODIN)": "Exploratory innovation",
    "Open Entrepreneurship": "Exploratory innovation",
    "ORB": "Early venture",
    "Otto Bruuns Fond": "PoC",
    "Otto Mønsteds Fond": "Exploratory innovation",
    "Patent og Varemærkestyrelsen": "PoC",
    "PreFlight": "PoC",
    "Seedster": "Early venture",
    "SMIL": "Early venture",
    "Soundtech": "Early venture",
    "SPARK Denmark": "PoC",
    "Spin-outs Denmark": "PoC",
    "Start Up Factory": "Early venture",
    "Startup Aarhus Townhall": "All stages",
    "Startup Lab": "Early venture",
    "Startup Planet": "All stages",
    "Startup Station": "Early venture",
    "Station": "Early venture",
    "STEAR": "Early venture",
    "StortTech Festival": "All stages",
    "Synapse": "Early venture",
    "Tech Nordic": "Early venture",
    "TechBBQ": "All stages",
    "The Circular Lab": "Early venture",
    "Time to Raise": "Early venture",
    "UCN Next Step": "Early venture",
    "UCPH Proof of Concept Fund (POC MAX)": "PoC",
    "UCPH Proof of Concept Fund (POC-TO-GO)": "PoC",
    "Velliv Foreningen": "PoC",
    "Villum Foundation and VELUX Group": "Exploratory innovation",
    "Vissing Fonden": "PoC",
    "We Build Denmark": "Early venture",
    "Women in Front": "All stages",
    "Women in Tech": "Early venture",
}

# CVR governance: (at application, at programme start)
# Values: Yes | No | Any
#   Yes — CVR required at this point
#   No  — Pre-CVR required (project must be pre-company / no CVR)
#   Any — Either with or without CVR is acceptable
from remap_cvr_vocabulary import CVR  # noqa: E402


def normalize_name(name: str) -> str:
    return name.replace("\u2019", "'").strip()


def main():
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        fieldnames = [fn for fn in reader.fieldnames if fn != "Innovation stage"]
        rows = list(reader)

    missing_stage = []
    missing_cvr = []

    for row in rows:
        name = row["Name"]
        key = name
        if key not in STAGE:
            for k in STAGE:
                if normalize_name(k) == normalize_name(name):
                    key = k
                    break

        if key in STAGE:
            row["Stage"] = STAGE[key]
        else:
            missing_stage.append(name)

        if key in CVR:
            app, start = CVR[key]
            row["CVR at application"] = app
            row["CVR at programme start"] = start
        else:
            missing_cvr.append(name)

        row.pop("CVR required at application", None)
        row.pop("CVR required at programme start", None)
        row.pop("Innovation stage", None)

    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated {len(rows)} rows")
    print(f"Stage column: single controlled vocabulary")
    print(f"Removed: Innovation stage column")
    if missing_stage:
        print(f"Missing stage mapping: {missing_stage}")
    if missing_cvr:
        print(f"Missing CVR mapping: {missing_cvr}")

    from collections import Counter
    stages = Counter(r["Stage"] for r in rows)
    print("\nStage distribution:")
    for s, n in sorted(stages.items()):
        print(f"  {s}: {n}")

    cvr_app = Counter(r.get("CVR at application", "") for r in rows)
    print("\nCVR at application:")
    for s, n in sorted(cvr_app.items()):
        print(f"  {s}: {n}")


if __name__ == "__main__":
    main()
