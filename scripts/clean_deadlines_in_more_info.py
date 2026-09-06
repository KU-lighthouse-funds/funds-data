#!/usr/bin/env python3
"""Remove deadline/timing duplication from Quick info (kept in Deadline column)."""
import csv
import re
from pathlib import Path

CSV_PATH = Path(r"c:\Users\Kaja\Documents\Funds\updated file without VC - cleaned.csv")

# Phrases/sentences to strip from Quick info (deadline belongs in Deadline column)
PATTERNS = [
    r"\s*Single deadline[^.]*\.\s*",
    r"\s*Two calls/year[^.]*\.\s*",
    r"\s*Two annual calls\.?\s*",
    r"\s*Four deadlines yearly[;,.]?\s*",
    r"\s*Theme-based calls:[^.]*\.\s*",
    r"2026:\s*Pathfinder Open[^.]*\.\s*",
    r"\(September,\s*Copenhagen\):\s*",
    r"~\d+[–-]\d+\s*months\)\.\s*",  # evaluation timeline fragment after diligence;
]

# Per-row manual fixes where regex is cleaner
MANUAL = {
    "EIC Pathfinder": "Total budget EUR 262M. Success rate ~2.1% (2025).",
    "EIC Transition": "Predecessor project must have been active for at least 18 months before cut-off.",
    "EUDP": "2025 funding DKK 543M.",
    "IFD Grand Solutions": (
        "Co-financing: SMEs 35–75%, large companies 25–65%, research institutions up to 90% + overhead. "
        "Must address significant societal challenges."
    ),
    "GUDP": (
        "Green Development and Demonstration Programme for food, agriculture, fisheries, and aquaculture. "
        "Supports development, demonstration, and network projects with typical grants DKK 250K–15M; ~50% co-financing."
    ),
    "Mikrolegat": (
        "Fonden for Entreprenørskab micro-grants for students/recent graduates: up to DKK 60K (higher ed) "
        "or DKK 35K (Momentum, vocational). 25% co-financing if CVR registered."
    ),
    "BII Bio Studio": (
        "Company-creation programme for academic researchers. Highly selective multi-step process "
        "(expression of interest, scientific pitch, diligence). BII encourages early dialogue on project fit "
        "before applying. Project team is hired at BII; Entrepreneur-in-Residence leads company formation "
        "(spin-out typically around year 2). Thematic calls in Human Health, Planetary Health, and related focus areas."
    ),
    "TechBBQ": (
        "Nordic's major tech conference in Copenhagen: investor meetings, side events, and startup showcase."
    ),
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower().strip())


def clean_more_info(more: str, deadline: str) -> str:
    if not more:
        return more

    result = more.strip()

    # Drop sentences that largely repeat the Deadline column
    if deadline.strip():
        dl_norm = normalize(deadline)
        sentences = re.split(r"(?<=[.!?])\s+", result)
        kept = []
        for sent in sentences:
            sn = normalize(sent)
            if not sn:
                continue
            # skip if sentence is mostly the deadline text
            if dl_norm in sn or sn in dl_norm:
                continue
            # skip frequency-only sentences
            if re.search(
                r"^(annual|rolling|biannual|per call|multiple cohorts|open call|challenge calls)",
                sn,
            ):
                continue
            kept.append(sent.strip())
        result = " ".join(kept).strip()

    for pat in PATTERNS:
        result = re.sub(pat, " ", result, flags=re.IGNORECASE)

    result = re.sub(r"\s+", " ", result).strip()
    result = re.sub(r"\s+([,.;:])", r"\1", result)
    return result


def main():
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        fieldnames = reader.fieldnames
        rows = list(reader)

    changed = 0
    for row in rows:
        name = row["Name"]
        if name in MANUAL:
            new = MANUAL[name]
        else:
            new = clean_more_info(row.get("Quick info", ""), row.get("Deadline", ""))
        if new != row.get("Quick info", ""):
            row["Quick info"] = new
            changed += 1

    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Cleaned {changed} rows")


if __name__ == "__main__":
    main()
