import csv
from collections import Counter, defaultdict
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "funds with KU support - v4.csv"

STAGE_OPTIONS = {
    "Exploratory innovation",
    "Commercial validation",
    "Venture formation",
    "Growth/scale",
}
SEGMENT_OPTIONS = {
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
}

with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f, delimiter=";"))

print("=== STAGE VALUES IN CSV vs FILTER DROPDOWN ===")
for stage, n in Counter(r["Stage"].strip() for r in rows).most_common():
    ok = stage in STAGE_OPTIONS or stage == "All stages"
    print(f"  {n:3}  {stage!r:30}  {'OK' if ok else 'MISSED BY FILTER'}")

print("\n=== NON-DROPDOWN STAGES (22+55 programmes hidden when any stage picked) ===")
for r in rows:
    s = r["Stage"].strip()
    if s not in STAGE_OPTIONS and s != "All stages":
        segs = [x.strip() for x in r["Industrial segment"].split(",")]
        general = any(x.lower() == "general" for x in segs)
        ku = r["KU support unit"] or "—"
        print(f"  {r['Name'][:58]:58} | {s!r:22} | General={str(general):5} | KU={ku}")

print("\n=== GENERAL PROGRAMMES WITH BAD STAGE (hidden despite General tag) ===")
for r in rows:
    segs = [x.strip() for x in r["Industrial segment"].split(",") if x.strip()]
    if not any(x.lower() == "general" for x in segs):
        continue
    s = r["Stage"].strip()
    if s not in STAGE_OPTIONS and s != "All stages":
        print(f"  - {r['Name']} ({s})")

print("\n=== SEGMENT TAGS NOT IN DROPDOWN ===")
for seg, names in sorted(
    ((seg, ns) for seg, ns in defaultdict(list).items()),
):
    pass
seg_issues = defaultdict(list)
for r in rows:
    for seg in [x.strip() for x in r["Industrial segment"].split(",") if x.strip()]:
        if seg not in SEGMENT_OPTIONS:
            seg_issues[seg].append(r["Name"])
for seg, names in sorted(seg_issues.items()):
    print(f"  {seg!r}: {len(names)}")

print("\n=== COUNTS ===")
print(f"  Total programmes: {len(rows)}")
print(f"  PoC stage: {sum(1 for r in rows if r['Stage'].strip()=='PoC')}")
print(f"  Early venture: {sum(1 for r in rows if r['Stage'].strip()=='Early venture')}")
print(f"  General-tagged: {sum(1 for r in rows if any(x.strip().lower()=='general' for x in r['Industrial segment'].split(',')))}")
