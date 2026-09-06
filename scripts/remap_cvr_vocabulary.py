#!/usr/bin/env python3
"""
Remap CVR columns to three-value vocabulary:

  Yes  — CVR required at this point
  No   — Pre-CVR required (project must be pre-company / no CVR)
  Any  — Either with or without CVR; note in Quick info when CVR is advantageous
"""
import csv
import re
from pathlib import Path

CSV_PATH = Path(r"c:\Users\Kaja\Documents\Funds\updated file without VC - cleaned.csv")

# (at application, at programme start)
CVR = {
  # Awards
  "Creative Business Cup": ("Any", "Any"),
  "EY Entrepreneur of the Year": ("Any", "Any"),
  "Global Startup Awards": ("Any", "Any"),
  "Green Leap Challenge": ("Any", "Any"),
  "Nordic Proptech Awards 2026": ("Any", "Any"),
  "Nordic Women in Tech Awards": ("Any", "Any"),
  "Odin Award": ("No", "Any"),
  # Events
  "CPH Townhall": ("Any", "Any"),
  "Danish Entrepreneurship Festival": ("Any", "Any"),
  "Danmarks Entreprenørskabsfestival": ("Any", "Any"),
  "Digital Tech Summit": ("Any", "Any"),
  "Founder Festival": ("Any", "Any"),
  "Ignite": ("Any", "Any"),
  "JoinUp North": ("Any", "Any"),
  "Nordic Fintech Week": ("Any", "Any"),
  "Nordic Innovation Fair": ("Any", "Any"),
  "Odense Investor Summit": ("Any", "Any"),
  "Seedster": ("Any", "Any"),
  "SMIL": ("Any", "Any"),
  "Startup Aarhus Townhall": ("Any", "Any"),
  "Startup Lab": ("Any", "Any"),
  "Startup Planet": ("Any", "Any"),
  "TechBBQ": ("Any", "Any"),
  # Female initiatives
  "Even Founders": ("Any", "Any"),
  "Found Diverse": ("Any", "Any"),
  "Intech Founders": ("Any", "Any"),
  "Kvinde kompagniet": ("Any", "Any"),
  "Ladies First": ("Any", "Any"),
  "Next Women": ("Any", "Any"),
  "Nordic Female Founders": ("Any", "Any"),
  "Nordic Women's Health Hub": ("Any", "Any"),
  "Nordic Women\u2019s Health Hub": ("Any", "Any"),
  "Women in Front": ("Any", "Any"),
  "Women in Tech": ("Any", "Any"),
  # Incubators
  "Akademikernes Startup": ("Any", "Any"),
  "Beta Health": ("Any", "Any"),
  "Beyond Beta": ("Yes", "Yes"),
  "BII Bio Studio": ("No", "No"),
  "BII Quantum Lab": ("Yes", "Yes"),
  "BII Venture Lab": ("Any", "Yes"),
  "Canute": ("Any", "Yes"),
  "Care Tech Challenge": ("Yes", "Yes"),
  "Time to Raise": ("Any", "Any"),
  "CBS CSE (Copenhagen School of Entrepreneurship)": ("Any", "Any"),
  "Climate-KIC Urban Mobility Food": ("Any", "Any"),
  "Defence Tech Denmark": ("Any", "Any"),
  "DIF Innovation Lab": ("Yes", "Yes"),
  "EESA": ("Any", "Any"),
  "Food and Bio Cluster": ("Any", "Any"),
  "Founder to Leader": ("Any", "Yes"),
  "Future Manufacturers": ("Any", "Any"),
  "Game Hub": ("Any", "Any"),
  "Hub for Innovation in Tourism": ("Any", "Any"),
  "Ideas Lab": ("Any", "Any"),
  "Incuba": ("Any", "Any"),
  "Leap Forward": ("Any", "Any"),
  "Lighthouse Launch": ("Any", "Any"),
  "Maritime Stars": ("Any", "Any"),
  "Neighborhood": ("Any", "Any"),
  "Odense Robotics Startup Fund": ("Any", "Any"),
  "Open Entrepreneurship": ("Any", "Any"),
  "PreFlight": ("Any", "Any"),
  "Soundtech": ("Any", "Any"),
  "SPARK Denmark": ("No", "No"),
  "STEAR": ("Any", "Any"),
  "Tech Nordic": ("Any", "Any"),
  "The Circular Lab": ("Any", "Any"),
  "We Build Denmark": ("Any", "Any"),
  # Research grants
  "Lundbeck Frontier": ("Any", "Any"),
  "NNF Distinguished Innovator Grant": ("Any", "Any"),
  "NNF Pioneer Innovator Grant": ("No", "No"),
  "Open Discovery Innovation Network (ODIN)": ("Any", "Any"),
  # Soft funding
  "Dinero Iværksætterlegat": ("Yes", "Yes"),
  "Dineros Iværksetterlegat": ("Yes", "Yes"),
  "DSV Group Innovation Partnerships": ("Yes", "Yes"),
  "EIC Accelerator": ("Yes", "Yes"),
  "EIC Pathfinder": ("Any", "Any"),
  "EIC Transition": ("Yes", "Yes"),
  "EUDP": ("Yes", "Yes"),
  "Eureka": ("Yes", "Yes"),
  "Eurostars": ("Yes", "Yes"),
  "GUDP": ("Yes", "Yes"),
  "HeyFunding Legatet": ("Any", "Yes"),
  "Horizon Europe": ("Any", "Any"),
  "IFD Grand Solutions": ("Yes", "Yes"),
  "IFD Industrial Researcher (Industrial PhD/Postdoc)": ("Yes", "Yes"),
  "IFD Innobooster": ("Yes", "Yes"),
  "IFD Innoexplorer": ("No", "No"),
  "IFD Innofounder": ("Any", "Yes"),
  "LEO Innovation Lab": ("Yes", "Yes"),
  "Mikrolegat": ("Any", "Any"),
  "Miljø- og Energi Fonden": ("Any", "Yes"),
  "MUDP": ("Yes", "Yes"),
  "Nordic Innovation": ("Yes", "Yes"),
  "Novo Nordisk External Research and Open Innovation": ("Any", "Yes"),
  "Otto Bruuns Fond": ("Any", "Any"),
  "Otto Mønsteds Fond": ("Any", "Any"),
  "Otto Mønsteds Fond – Den Lyse Ide": ("Any", "Any"),
  "NextGen Innovation (Odense Robotics)": ("Yes", "Yes"),
  "Patent og Varemærkestyrelsen": ("Yes", "Yes"),
  "Spin-outs Denmark": ("No", "No"),
  "UCPH Proof of Concept Fund (POC MAX)": ("No", "No"),
  "UCPH Proof of Concept Fund (POC-TO-GO)": ("No", "No"),
  "Velliv Foreningen": ("Any", "Any"),
  "Villum Foundation and VELUX Group": ("Yes", "Yes"),
  "Vissing Fonden": ("Yes", "Yes"),
  # Student entrepreneurship
  "Copenhagen Health Innovation (CHI)": ("Any", "Any"),
  "Fonden for Entreprenørskab": ("Any", "Any"),
  "ITU Business Development": ("Any", "Any"),
  "NextGen Innovation and Startup Hub": ("Yes", "Yes"),
  "NOVI Legatet": ("Any", "Any"),
  "Novo Nordisk Foundation Fellowship Program Biomedical Design": ("Any", "Any"),
  "ORB": ("Any", "Any"),
  "Start Up Factory": ("Any", "Any"),
  "Startup Station": ("Any", "Any"),
  "Station": ("Any", "Any"),
  "Synapse": ("Any", "Any"),
  "UCN Next Step": ("Any", "Any"),
}

# Append to Quick info when CVR is optional but valuable (only if not already mentioned)
CVR_QUICK_INFO_NOTES = {
  "BII Venture Lab": "May apply before CVR exists if there is a clear plan to establish a Danish entity before programme start.",
  "IFD Innofounder": "CVR required before project start; grant is personal income for tax purposes.",
  "Miljø- og Energi Fonden": "Company CVR typically required for project implementation.",
  "Novo Nordisk External Research and Open Innovation": "Partnership deals usually require an incorporated entity.",
  "HeyFunding Legatet": "Incorporated entity typically needed to receive and deploy grant funds.",
  "Founder to Leader": "Programme targets founders with an operating company.",
  "Canute": "Scaling programmes assume an incorporated Danish startup.",
  "Creative Business Cup": "Incorporated startups often preferred for competition rounds.",
  "Green Leap Challenge": "Winners typically incorporate or already have CVR to receive DKK 50K.",
  "Odin Award": "Concept category targets pre-CVR ideas; Odin/Tech/Impact categories are for established startups (CVR expected).",
  "UCPH Proof of Concept Fund (POC MAX)": "Grant to UCPH researchers; no company CVR required.",
  "UCPH Proof of Concept Fund (POC-TO-GO)": "Grant to UCPH researchers/PhD students; no company CVR required.",
  "SPARK Denmark": "Funds proof-of-concept work for researchers; not for established companies.",
  "Spin-outs Denmark": "Postdoc salary grant via university; applicants apply as researchers, not as a company.",
}

NEW_HEADERS = {
  "CVR required at application": "CVR at application",
  "CVR required at programme start": "CVR at programme start",
}


def append_note(quick: str, note: str) -> str:
  quick = (quick or "").strip()
  if not note or note.lower() in quick.lower():
    return quick
  return f"{quick} {note}".strip() if quick else note


def main():
  with CSV_PATH.open(encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f, delimiter=";")
    fieldnames = list(reader.fieldnames)
    rows = list(reader)

  for old, new in NEW_HEADERS.items():
    if old in fieldnames:
      fieldnames[fieldnames.index(old)] = new

  missing = []
  for row in rows:
    name = row["Name"]
    if name not in CVR:
      missing.append(name)
      continue
    app, start = CVR[name]
    row["CVR at application"] = app
    row["CVR at programme start"] = start
    row.pop("CVR required at application", None)
    row.pop("CVR required at programme start", None)

    if name in CVR_QUICK_INFO_NOTES:
      row["Quick info"] = append_note(row.get("Quick info", ""), CVR_QUICK_INFO_NOTES[name])

  if missing:
    raise SystemExit(f"Missing CVR mapping: {missing}")

  with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

  from collections import Counter
  print(f"Updated {len(rows)} rows")
  print("CVR vocabulary: Yes | No (pre-CVR required) | Any")
  for col in ("CVR at application", "CVR at programme start"):
    print(f"\n{col}:")
    for v, n in Counter(r[col] for r in rows).most_common():
      print(f"  {v}: {n}")


if __name__ == "__main__":
  main()
