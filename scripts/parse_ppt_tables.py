"""Parse KU LH PPT tables into clean programme/responsibility data."""
from __future__ import annotations

import html
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile

PPTX = Path(r"C:\Users\Kaja\Documents\Funds\KU LH preaward funding support-AZ-JSJ.pptx")
OUT = Path(r"C:\Users\Kaja\Documents\Funds\_ppt_clean.txt")
OUT_JSON = Path(r"C:\Users\Kaja\Documents\Funds\_ppt_programmes.json")

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def cell_text(tc) -> str:
    bits = []
    for t in tc.findall(".//a:t", NS):
        if t.text:
            bits.append(t.text)
    return html.unescape("".join(bits)).strip()


def slide_tables(root) -> list[list[list[str]]]:
    tables = []
    for tbl in root.findall(".//a:tbl", NS):
        rows = []
        for tr in tbl.findall("./a:tr", NS):
            row = [cell_text(tc) for tc in tr.findall("./a:tc", NS)]
            # drop fully empty trailing? keep all
            if any(c.strip() for c in row):
                rows.append(row)
        if rows:
            tables.append(rows)
    return tables


def slide_title_guess(root) -> str:
    # first non-empty paragraph-ish texts outside tables can be noisy; use shape texts in order
    texts = []
    for t in root.findall(".//p:sp//a:t", NS):
        if t.text and t.text.strip():
            texts.append(t.text.strip())
            if len(texts) >= 8:
                break
    return " | ".join(texts[:4])


def main() -> None:
    lines = []
    programmes = {}  # name -> dict

    with ZipFile(PPTX) as z:
        slides = sorted(
            [n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)],
            key=lambda s: int(re.search(r"(\d+)", s).group(1)),
        )
        for name in slides:
            sid = int(re.search(r"(\d+)", name).group(1))
            root = ET.fromstring(z.read(name))
            title = slide_title_guess(root)
            tables = slide_tables(root)
            lines.append(f"===== SLIDE {sid} =====")
            lines.append(f"TITLE_GUESS: {title}")
            for ti, table in enumerate(tables, 1):
                lines.append(f"-- table {ti} ({len(table)} rows x {max(len(r) for r in table)} cols) --")
                for row in table:
                    # collapse whitespace and skip pure XML leftovers
                    clean = []
                    for c in row:
                        c = re.sub(r"\s+", " ", c).strip()
                        if "<a:" in c or "</a:" in c:
                            c = re.sub(r"<[^>]+>", " ", c)
                            c = re.sub(r"\s+", " ", c).strip()
                        clean.append(c)
                    lines.append(" || ".join(clean))
            lines.append("")

            # Heuristic: capture "Who to contact" style 2-col tables on programme slides
            for table in tables:
                flat = " | ".join(" | ".join(r) for r in table)
                # programme detail slides often start with fund name in first cell spanning
                if not table:
                    continue
                header0 = table[0][0] if table[0] else ""
                # Collect key-value rows
                kv = {}
                for row in table:
                    if len(row) >= 2 and row[0] and row[1]:
                        key = row[0].strip()
                        val = " | ".join(x for x in row[1:] if x).strip()
                        if key and val and len(key) < 80:
                            kv[key] = val
                # Identify programme name
                pname = None
                for cand in [header0, title.split("|")[0].strip()]:
                    cand = cand.strip()
                    if cand and cand.lower() not in {"who to contact", "purpose", "amount"} and len(cand) < 80:
                        # skip generic
                        if not cand.lower().startswith("ifd:") and "Lighthouse" not in cand:
                            pass
                        pname = cand
                        break
                # Prefer first cell if looks like programme
                if header0 and len(header0) < 80 and "||" not in header0:
                    pname = header0
                if pname and ("Who to contact" in flat or "Amount" in flat or "Purpose" in flat or "Deadline" in flat or "Eligibility" in flat):
                    entry = programmes.setdefault(pname, {"slide": sid, "fields": {}})
                    entry["slide"] = sid
                    entry["fields"].update(kv)

            # Matrix slides: look for faculty columns SCIENCE/SUND etc.
            for table in tables:
                header = [c.upper() for c in table[0]] if table else []
                faculty_idx = [i for i, h in enumerate(header) if any(x in h for x in ["SCIENCE", "SUND", "HUM", "SAMF", "TEO", "JUR", "FRB", "LH", "LIGHT", "RSO", "FAC"])]
                if len(faculty_idx) >= 2 and len(table) > 2:
                    lines.append(f"[MATRIX DETECTED slide {sid}] header={table[0]}")

    OUT.write_text("\n".join(lines), encoding="utf-8")

    import json
    OUT_JSON.write_text(json.dumps(programmes, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    print(f"programmes captured: {len(programmes)}")
    for k in sorted(programmes)[:40]:
        print(" -", k)


if __name__ == "__main__":
    main()
