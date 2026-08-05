#!/usr/bin/env python3
"""Apply agreed stage tags to all programmes (local audit)."""
import csv
from collections import Counter
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent / "funds with KU support - v4.csv"

STAGE_BY_NAME = {
    # —— All stages (events, awards, networks, cross-cutting schemes) ——
    "Creative Business Cup": "All stages",
    "EY Entrepreneur of the Year": "All stages",
    "Global Startup Awards": "All stages",
    "Nordic Proptech Awards 2026": "All stages",
    "Nordic Women in Tech Awards": "All stages",
    "Odin Award": "All stages",
    "CPH Townhall": "All stages",
    "Danmarks Entreprenørskabsfestival": "All stages",
    "Digital Tech Summit": "All stages",
    "Founder Festival": "All stages",
    "Ignite": "All stages",
    "JoinUp North": "All stages",
    "Nordic Fintech Week": "All stages",
    "Nordic Innovation Fair": "All stages",
    "Odense Investor Summit": "All stages",
    "Startup Aarhus Townhall": "All stages",
    "Startup Planet": "All stages",
    "TechBBQ": "All stages",
    "Even Founders": "All stages",
    "Found Diverse": "All stages",
    "Intech Founders": "All stages",
    "Kvinde kompagniet": "All stages",
    "Ladies First": "All stages",
    "Next Women": "All stages",
    "Nordic Female Founders": "All stages",
    "Nordic Women\u2019s Health Hub": "All stages",
    "Women in Front": "All stages",
    "Women in Tech": "All stages",
    "Climate-KIC Urban Mobility Food": "All stages",
    "Food and Bio Cluster": "All stages",
    "Global Innovation Network Programme (GINP)": "All stages",
    "Horizon Europe": "All stages",
    "IFD Grand Solutions": "All stages",
    "Industriens Fond": "All stages",
    "Plantefonden (Fonden for Plantebaserede Fødevarer)": "All stages",
    "Reinholdt W. Jorck og Hustrus Fond": "All stages",
    "Open Entrepreneurship": "All stages",
    # —— Exploratory innovation ——
    "Green Leap Challenge": "Exploratory innovation",
    "Lighthouse Launch": "Exploratory innovation",
    "IBIS (Initiative for Biofertilizer Innovation and Science)": "Exploratory innovation",
    "Lundbeck Frontier": "Exploratory innovation",
    "NNF Pioneer Innovator Grant": "Exploratory innovation, Commercial validation",
    "Open Discovery Innovation Network (ODIN)": "Exploratory innovation",
    "Plant2Food (NNF Open Innovation)": "Exploratory innovation",
    "EIC Pathfinder": "Exploratory innovation",
    "Otto Mønsteds Fond – Den Lyse Ide": "Exploratory innovation",
    "Otto Mønsteds Fond – Studiemeriterende ophold": "All stages",
    "Otto Mønsteds Fond – Kongresdeltagelse": "All stages",
    "Otto Mønsteds Fond – Forskningsophold": "Exploratory innovation",
    "Otto Mønsteds Fond – Udenlandske gæsteprofessorater": "All stages",
    "Otto Mønsteds Fond – Særlige formål": "All stages",
    "Novo Nordisk Foundation Fellowship Program Biomedical Design": "Exploratory innovation",
    "Spin-outs Denmark": "Exploratory innovation, Commercial validation, Venture formation",
    "Villum Foundation and VELUX Group": "Exploratory innovation",
    "Novo Nordisk External Research and Open Innovation": "Exploratory innovation",
    "UCPH Proof of Concept Fund (POC-TO-GO)": "Exploratory innovation, Commercial validation",
    "HeyFunding Legatet": "Exploratory innovation",
    # —— Commercial validation (employee, pre-CVR maturation) ——
    "UCPH Proof of Concept Fund (POC MAX)": "Commercial validation, Venture formation",
    "IFD Innoexplorer": "Exploratory innovation, Commercial validation",
    "SPARK Denmark": "Exploratory innovation, Commercial validation",
    "NNF Distinguished Innovator Grant": "Commercial validation, Venture formation",
    "Beta Health": "Commercial validation",
    "PreFlight": "Commercial validation",
    "Otto Bruuns Fond – Industrielle projekter": "Commercial validation",
    "Otto Bruuns Fond – Almennyttige projekter": "All stages",
    "Carlsbergfondet": "Exploratory innovation",
    "Alexander Foss' Industrifond": "Commercial validation",
    "Velliv Foreningen": "Commercial validation",
    "Miljø- og Energi Fonden": "Commercial validation",
    "Mikrolegat": "Exploratory innovation",
    # —— Venture formation ——
    "BII Bio Studio": "Commercial validation, Venture formation",
    "BII Quantum Lab": "Venture formation",
    "BII Venture Lab": "Venture formation",
    "BII AI Lab": "Venture formation",
    "IFD Innofounder": "Exploratory innovation, Venture formation",
    "IFD Innobooster": "Venture formation",
    "EIC Transition": "Venture formation",
    "NextGen Innovation (Odense Robotics)": "Venture formation",
    "Eureka": "Venture formation",
    "Eurostars": "Venture formation",
    "IFD Industrial Researcher (Industrial PhD/Postdoc)": "Venture formation",
    "LEO Innovation Lab": "Venture formation",
    "Nordic Innovation": "Venture formation",
    "Patent og Varemærkestyrelsen": "Venture formation",
    "Vissing Fonden": "Venture formation",
    "Care Tech Challenge": "Venture formation",
    "Akademikernes Startup": "Venture formation",
    "SMIL": "Venture formation",
    "Seedster": "Venture formation",
    "Startup Lab": "Venture formation",
    "CBS CSE (Copenhagen School of Entrepreneurship)": "Venture formation",
    "DIF Innovation Lab": "Venture formation",
    "Defence Tech Denmark": "Venture formation",
    "EESA": "Venture formation",
    "Future Manufacturers": "Venture formation",
    "Game Hub": "Venture formation",
    "Hub for Innovation in Tourism": "Venture formation",
    "Ideas Lab": "Venture formation",
    "Incuba": "Venture formation",
    "Leap Forward": "Venture formation",
    "Maritime Stars": "Venture formation",
    "Neighborhood": "Venture formation",
    "Odense Robotics Startup Fund": "Venture formation",
    "STEAR": "Venture formation",
    "Soundtech": "Venture formation",
    "Tech Nordic": "Venture formation",
    "The Circular Lab": "Venture formation",
    "Time to Raise": "Venture formation",
    "We Build Denmark": "Venture formation",
    "Copenhagen Health Innovation (CHI)": "Venture formation",
    "Fonden for Entreprenørskab": "Venture formation",
    "ITU Business Development": "Venture formation",
    "NOVI Legatet": "Venture formation",
    "ORB": "Venture formation",
    "Start Up Factory": "Venture formation",
    "Startup Station": "Venture formation",
    "Station": "Venture formation",
    "Synapse": "Venture formation",
    "UCN Next Step": "Venture formation",
    "Dinero Iværksætterlegat": "Venture formation",
    # —— Growth / scale ——
    "BII Upscalator": "Growth/scale",
    "Beyond Beta": "Growth/scale",
    "Canute": "Growth/scale",
    "Founder to Leader": "Growth/scale",
    "DSV Group Innovation Partnerships": "Growth/scale",
    "EIC Accelerator": "Growth/scale",
    "EIFO Green Accelerator": "Growth/scale",
    "EUDP": "Growth/scale",
    "GUDP": "Growth/scale",
    "MUDP": "Growth/scale",
    "Scaleup Europe Fund": "Growth/scale",
    "Karl Pedersen og Hustrus Industrifond": "Growth/scale",
}


def cvr_apply(row) -> str:
    return (row.get("CVR at application") or "Any").strip()


def parse_stages(stage_str: str) -> list[str]:
    return [s.strip() for s in (stage_str or "").split(",") if s.strip()]


def main() -> None:
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter=";"))
        fieldnames = list(rows[0].keys()) if rows else []

    missing = []
    changes = []
    for row in rows:
        name = row["Name"]
        old = (row.get("Stage") or "").strip()
        if name not in STAGE_BY_NAME:
            missing.append(name)
            continue
        new = STAGE_BY_NAME[name]
        if old != new:
            changes.append((name, old, new))
        row["Stage"] = new

    if missing:
        raise SystemExit(f"Missing stage mapping for: {missing}")

    # Guardrail: commercial validation is for pre-CVR at application
    for row in rows:
        if "Commercial validation" in parse_stages(row["Stage"]) and cvr_apply(row) == "Yes":
            raise SystemExit(f"CVR Yes at application but Commercial validation: {row['Name']}")

    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    counts = Counter(r["Stage"] for r in rows)
    print(f"Applied stages to {len(rows)} programmes ({len(changes)} changed)\n")
    for stage, n in counts.most_common():
        print(f"  {n:3}  {stage}")

    if changes:
        print(f"\nChanges ({len(changes)}):")
        for name, old, new in changes:
            if old != new:
                print(f"  {old:22} -> {new:22}  | {name[:55]}")


if __name__ == "__main__":
    main()
