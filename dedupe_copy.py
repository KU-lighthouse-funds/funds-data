"""Remove repeated sentences from Quick info and Criteria in v4."""
import csv
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent / "funds with KU support - v4.csv"
FIELDS = ("Quick info", "Criteria")


def norm(s: str) -> str:
    return re.sub(r"[^\w\s]", "", s.lower()).split()


def dedupe(text: str) -> str:
    if not text.strip():
        return text
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", text.strip()) if p.strip()]
    kept: list[str] = []
    norms: list[str] = []
    for part in parts:
        n = " ".join(norm(part))
        if not n:
            continue
        dup = False
        for prev in norms:
            if n == prev:
                dup = True
                break
            if len(n) >= 20 and (n in prev or prev in n):
                dup = True
                break
        if dup:
            continue
        kept.append(part)
        norms.append(n)
    return " ".join(kept)


def main() -> None:
    with SRC.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        headers = list(reader.fieldnames or [])
        rows = list(reader)

    changed = 0
    for row in rows:
        for field in FIELDS:
            before = row.get(field, "")
            after = dedupe(before)
            if before != after:
                print(f"{row['Name']} [{field}]")
                print(f"  was: {before[:100]}...")
                print(f"  now: {after[:100]}...")
                row[field] = after
                changed += 1

    with SRC.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nCleaned {changed} field(s) in {SRC.name}")


if __name__ == "__main__":
    main()
