#!/usr/bin/env python3
"""Map legacy industrial segment tags to canonical categories; archive old tags for search."""
import csv
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent / "funds with KU support - v4.csv"

CANONICAL_ORDER = [
    "General",
    "Life Sciences",
    "Food & Agriculture",
    "Quantum",
    "Chemistry",
    "Physics & Materials",
    "Deep Tech",
    "Tech & AI",
    "Cleantech & Energy",
    "Manufacturing & Industry",
    "Social Impact",
    "Creative & Media",
    "Defense",
]

# Legacy tag -> canonical filter category. None = search metadata only.
TAG_MAP = {
    "General": "General",
    "Health": "Life Sciences",
    "Biotech": "Life Sciences",
    "Neuroscience": "Life Sciences",
    "Drug Discovery": "Life Sciences",
    "Cell Therapy": "Life Sciences",
    "Digital Therapeutics": "Life Sciences",
    "Care tech": "Life Sciences",
    "Welfare tech": "Life Sciences",
    "Food": "Food & Agriculture",
    "Agri": "Food & Agriculture",
    "Food/AgriTech": "Food & Agriculture",
    "Quantum Tech": "Quantum",
    "Chemistry": "Chemistry",
    "Physics": "Physics & Materials",
    "Materials Science": "Physics & Materials",
    "Deep Tech": "Deep Tech",
    "Tech": "Tech & AI",
    "AI": "Tech & AI",
    "Robotics": "Tech & AI",
    "Engineering": "Tech & AI",
    "Drones": "Tech & AI",
    "Maritime Tech": "Tech & AI",
    "Fintech": "Tech & AI",
    "PropTech": "Tech & AI",
    "Cleantech": "Cleantech & Energy",
    "Sustainability": "Cleantech & Energy",
    "Energy": "Cleantech & Energy",
    "Manufacturing": "Manufacturing & Industry",
    "Industry": "Manufacturing & Industry",
    "Social Impact": "Social Impact",
    "Education": "Social Impact",
    "Creative Industries": "Creative & Media",
    "Media": "Creative & Media",
    "Entertainment": "Creative & Media",
    "Gaming": "Creative & Media",
    "Games": "Creative & Media",
    "Design": "Creative & Media",
    "Sports": "Creative & Media",
    "Tourism": "Creative & Media",
    "Audio": "Creative & Media",
    "Defense Tech": "Defense",
    "Research": None,
    "Innovation": None,
}


def parse_tags(raw: str) -> list[str]:
    return [p.strip() for p in (raw or "").split(",") if p.strip()]


def canonical_segments(old_tags: list[str]) -> list[str]:
    mapped = {TAG_MAP[t] for t in old_tags if TAG_MAP.get(t)}
    if not mapped and old_tags:
        mapped.add("General")
    return [c for c in CANONICAL_ORDER if c in mapped]


def segment_tags(old_tags: list[str]) -> str:
    seen: set[str] = set()
    kept: list[str] = []
    for tag in old_tags:
        key = tag.casefold()
        if key in seen:
            continue
        seen.add(key)
        kept.append(tag)
    return ", ".join(kept)


def main() -> None:
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter=";"))
        fieldnames = list(rows[0].keys()) if rows else []

    if "Segment tags" not in fieldnames:
        idx = fieldnames.index("Industrial segment") + 1
        fieldnames.insert(idx, "Segment tags")

    for row in rows:
        old = parse_tags(row.get("Industrial segment", ""))
        unknown = [t for t in old if t not in TAG_MAP]
        if unknown:
            raise SystemExit(f"Unmapped tags for {row.get('Name')}: {unknown}")
        row["Segment tags"] = segment_tags(old)
        row["Industrial segment"] = ", ".join(canonical_segments(old))

    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated {len(rows)} rows in {CSV_PATH.name}")


if __name__ == "__main__":
    main()
