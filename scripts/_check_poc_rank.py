import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys_path = ROOT / "funds-overview-site" / "data" / "programmes.json"
rows = json.loads(sys_path.read_text(encoding="utf-8"))["programmes"]


def has_ku(row):
    u = (row.get("KU support unit") or "").strip()
    return bool(u) and u not in ("—", "–", "-", "?")


def parse_stages(row):
    return [s.strip() for s in (row.get("Stage") or "").split(",") if s.strip()]


def parse_segments(row):
    return [s.strip() for s in (row.get("Industrial segment") or "").split(",") if s.strip()]


def row_matches_stages(row, picked):
    rs = parse_stages(row)
    if "All stages" in rs:
        return True
    return any(s in rs for s in picked)


def filter_rows(rows, stages, segments):
    out = []
    for row in rows:
        if stages and not row_matches_stages(row, stages):
            continue
        segs = parse_segments(row)
        if segments:
            general = any(x.lower() == "general" for x in segs)
            if not general and not any(s in segs for s in segments):
                continue
        out.append(row)
    return out


def sort_key(row, picked_stages):
    ku = 0 if has_ku(row) else 1
    dated = 1 if not (row.get("Deadline") or "").strip() else 0
    stage = (
        0
        if picked_stages and any(s in picked_stages for s in parse_stages(row))
        else 1
    )
    return (ku, dated, row.get("Name", ""), stage)


picked = ["Commercial validation"]
segments = ["Chemistry"]
matched = filter_rows(rows, picked, segments)
matched.sort(key=lambda r: sort_key(r, picked))

for i, r in enumerate(matched[:45]):
    mark = " <<<" if "POC MAX" in r["Name"] else ""
    print(f"{i + 1:2}. KU={has_ku(r)} | {r['Name'][:52]}{mark}")

idx = next(i for i, r in enumerate(matched) if "POC MAX" in r["Name"])
print(f"\nPoC MAX position: {idx + 1} of {len(matched)} (pagination shows 25 first)")
