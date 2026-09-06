#!/usr/bin/env python3
"""Build v3 from v2: refresh BII Upscalator, add AI Lab, Scaleup Europe Fund and
the three DI-administered foundations, and drop EUopSTART.

Sources verified 2026-08-04 against the programme pages themselves.
BII Venture House is deliberately not added (Venture Lab already covers it).
EUopSTART is removed because the 2026 UFSN call admits only companies and GTS
institutes, so it is not actionable for KU researchers.
"""
import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

BASE = Path(__file__).resolve().parent
SRC = BASE / "funds with KU support - v2.csv"
OUT_CSV = BASE / "funds with KU support - v3.csv"
OUT_XLSX = BASE / "funds with KU support - v3.xlsx"

# name -> field overrides
UPDATES: dict[str, dict[str, str]] = {
    "BII Upscalator": {
        "Link": "https://bii.dk/programs/upscalator/",
        "Criteria": (
            "Biosolutions company with validated technology and core R&D completed, where further "
            "progress depends on scaling; no commercial investment or for-profit financing; core IP "
            "owned by, exclusively licensed to, or clearly licensable to the company"
        ),
        "Funding Amount": "Convertible loan of DKK 3–5M per project (milestone-based tranches)",
        "Deadline": "Up to four decision cycles per year (next: 1 September 2026, 14:00 CEST)",
        "Quick info": (
            "BII programme helping biosolutions companies move validated concepts toward production "
            "at scale. Provides a dedicated BII anchor plus access to BII's community, network, "
            "fundraising platform and events. Requires a team with the technical, operational and "
            "commercial capability to execute the scale-up."
        ),
        "PPT notes": (
            "PPT: Lighthouse-managed BII family. Link replaced with the stable BII programme page "
            "and all details refreshed from it (verified 2026-08-04)."
        ),
    },
}

# The 2026 UFSN call restricts EUopSTART to companies and GTS institutes, so a KU
# researcher cannot act on it; keeping the row would only mislead.
DELETIONS = {"EUopSTART"}

NEW_ROWS: list[dict[str, str]] = [
    {
        "Opportunity": "Incubator/Accelerator",
        "Name": "BII AI Lab",
        "Link": "https://bii.dk/programs/ai-lab/",
        "Criteria": (
            "Early-stage AI startup with a clear product hypothesis, a relevant industry "
            "application, and potential to build a venture-scale company; technically strong "
            "founders with deep domain knowledge"
        ),
        "Industrial segment": "AI, Tech, Deep Tech",
        "Stage": "Early venture",
        "Geography": "DK",
        "Funding Amount": (
            "Programme benefits worth more than DKK 1M; may qualify for pre-seed investment via the "
            "AI Fund"
        ),
        "Deadline": "Rolling applications, assessed every 10 weeks",
        "Quick info": (
            "12-month venture-building programme across three tracks: AI/Industry, AI/Tech and "
            "AI/Deep Tech. Provides tailored venture building, technical infrastructure, industry "
            "partners for validating use cases, investor connections and an alumni network."
        ),
        "CVR at application": "Any",
        "CVR at programme start": "Yes",
        "KU support unit": "Lighthouse",
        "KU faculty focus": "SUND, SCIENCE",
        "KU contact hint": "KU Lighthouse",
        "PPT notes": (
            "Not in the KU LH PPT; added 2026-08-04 from the BII programme page. Lighthouse routing "
            "assumed by analogy with the rest of the BII portfolio — confirm with Lighthouse."
        ),
    },
    {
        "Opportunity": "Investment Fund",
        "Name": "Scaleup Europe Fund",
        "Link": "https://eic.ec.europa.eu/eic-fund/scaleup-europe-fund_en",
        "Criteria": (
            "Late-stage/growth companies located in (or relocating to) an EU Member State or a "
            "country associated with Horizon Europe Pillar III, developing strategic technologies "
            "and raising very large rounds. No open call — the fund manager sources deals"
        ),
        "Industrial segment": "Deep Tech, Tech, Biotech, Health, Cleantech, Quantum Tech, AI, Energy",
        "Stage": "Growth/scale",
        "Geography": "EU",
        "Funding Amount": "Equity in rounds of ~EUR 100M and above (fund targets ~EUR 5bn)",
        "Deadline": "No application route; first investments expected autumn 2026",
        "Quick info": (
            "EU late-stage growth equity fund under the EIC Fund umbrella, managed by EQT, with the "
            "European Commission, Novo Holdings, EIFO and others as founding investors. There is no "
            "application process — EQT sources deals directly. Far beyond researcher or early-founder "
            "stage; listed for ecosystem awareness. Watch scaleupeuropefund.eu for updates."
        ),
        "CVR at application": "Yes",
        "CVR at programme start": "Yes",
        "KU support unit": "—",
        "KU faculty focus": "",
        "KU contact hint": "",
        "PPT notes": (
            "Not in the KU LH PPT. Added 2026-08-04 on request. Equity/VC instrument with no open "
            "application — kept visible but flagged as out of reach for typical KU projects."
        ),
    },
    {
        "Opportunity": "Soft Funding",
        "Name": "Alexander Foss' Industrifond",
        "Link": "https://www.danskindustri.dk/om-di/hvad-er-di/di-fonde/alexander-foss/",
        "Criteria": (
            "Danish entrepreneurs in the earliest phase developing a technologically novel solution "
            "embodied in a physical product. Software-only solutions excluded, as are companies that "
            "have already raised more than DKK 500K (Innofounder-type soft funding does not count)"
        ),
        "Industrial segment": "General, Tech, Manufacturing, Engineering",
        "Stage": "PoC",
        "Geography": "DK",
        "Funding Amount": "Typically DKK 50K–100K per grant",
        "Deadline": "Annual — 1 September 2026",
        "Quick info": (
            "DI-administered foundation (founded 1919) granting stipends to entrepreneurs building "
            "technologically innovative physical products. Funds prototype development, tooling, "
            "testing and components. Does not fund software-only work, patent costs, the founders' "
            "own salary, travel or study stays, general operating costs, or expenses already "
            "incurred. An optional video pitch can be attached; five to seven grants per year in "
            "recent rounds."
        ),
        "CVR at application": "Any",
        "CVR at programme start": "Any",
        "KU support unit": "—",
        "KU faculty focus": "",
        "KU contact hint": "",
        "PPT notes": (
            "Not in the KU LH PPT. Added 2026-08-04 from DI's fund page — one of three "
            "DI-administered foundations, split out per fund as requested."
        ),
    },
    {
        "Opportunity": "Scholarship",
        "Name": "Reinholdt W. Jorck og Hustrus Fond",
        "Link": "https://www.danskindustri.dk/om-di/hvad-er-di/di-fonde/reinholdt/",
        "Criteria": (
            "Students, graduates and PhDs spending at least 3 months abroad studying or "
            "researching within technical, commercial, legal, social science or medical fields; "
            "grade average of at least 8 and a strong recommendation from a supervisor, professor "
            "or recognised expert"
        ),
        "Industrial segment": "General, Education, Research",
        "Stage": "All stages",
        "Geography": "DK, International",
        "Funding Amount": "Varies (study/research stay scholarship; amount not published)",
        "Deadline": "Annual — 1 August to 15 September; recipients notified mid-December",
        "Quick info": (
            "Study- and research-abroad scholarship, not innovation or venture funding. Covers a "
            "stay abroad of at least 3 months — part of an ongoing degree, a full degree, or a "
            "research stay. DI does not administer the fund itself; it prioritises and nominates "
            "applicants within the technical field. Applications go through the fund's own "
            "electronic form."
        ),
        "CVR at application": "No",
        "CVR at programme start": "No",
        "KU support unit": "—",
        "KU faculty focus": "",
        "KU contact hint": "",
        "PPT notes": (
            "Not in the KU LH PPT. Added 2026-08-04 on request as the third DI-administered fund. "
            "Mobility scholarship rather than innovation funding — labelled as Scholarship so it "
            "reads clearly in the table."
        ),
    },
    {
        "Opportunity": "Soft Funding",
        "Name": "Karl Pedersen og Hustrus Industrifond",
        "Link": "https://www.danskindustri.dk/om-di/hvad-er-di/di-fonde/karl-pedersen/",
        "Criteria": (
            "Projects strengthening Danish export capability, preferably partnerships that do not "
            "normally collaborate — for example companies together with universities, business "
            "academies or other knowledge organisations. Must be novel and tied to Denmark"
        ),
        "Industrial segment": "General, Tech, Manufacturing, Industry",
        "Stage": "All stages",
        "Geography": "DK",
        "Funding Amount": "Varies (project grants; budget template provided by the fund)",
        "Deadline": "Annual window — 15 August to 30 September 2026",
        "Quick info": (
            "DI-administered foundation funding projects that strengthen Danish exports, across "
            "three priority areas: new export tools for SMEs, production technology developed "
            "jointly by companies and knowledge institutions, and strengthening Danish students' "
            "innovation and export skills. Company–university partnerships are explicitly "
            "prioritised, which makes this the most KU-relevant of the DI funds. Does not fund "
            "single-company profit projects, travel or study stays, or costs already incurred."
        ),
        "CVR at application": "Any",
        "CVR at programme start": "Any",
        "KU support unit": "—",
        "KU faculty focus": "",
        "KU contact hint": "",
        "PPT notes": (
            "Not in the KU LH PPT. Added 2026-08-04 from DI's fund page. Board includes a DTU "
            "professor; university collaboration is an explicit selection parameter."
        ),
    },
]


def main() -> None:
    with SRC.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        headers = reader.fieldnames
        rows = list(reader)

    applied = []
    for row in rows:
        overrides = UPDATES.get(row["Name"])
        if overrides:
            row.update(overrides)
            applied.append(row["Name"])

    missing = set(UPDATES) - set(applied)
    if missing:
        raise SystemExit(f"Expected rows not found in v2: {sorted(missing)}")

    not_found = DELETIONS - {r["Name"] for r in rows}
    if not_found:
        raise SystemExit(f"Rows marked for deletion not found in v2: {sorted(not_found)}")
    rows = [r for r in rows if r["Name"] not in DELETIONS]

    existing = {r["Name"] for r in rows}
    for new in NEW_ROWS:
        if new["Name"] in existing:
            raise SystemExit(f"Row already exists, refusing to duplicate: {new['Name']}")
        rows.append({h: new.get(h, "") for h in headers})

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    export_xlsx(headers, rows)
    print(f"Updated: {', '.join(sorted(applied))}")
    print(f"Deleted: {', '.join(sorted(DELETIONS))}")
    print(f"Added:   {', '.join(r['Name'] for r in NEW_ROWS)}")
    print(f"Rows:    {len(rows)}  ->  {OUT_CSV.name} / {OUT_XLSX.name}")


def export_xlsx(headers: list[str], rows: list[dict[str, str]]) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Funds"
    header_fill = PatternFill("solid", fgColor="1F4E79")
    header_font = Font(bold=True, color="FFFFFF")

    for c, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(wrap_text=True, vertical="top")

    for r, row in enumerate(rows, 2):
        for c, h in enumerate(headers, 1):
            val = row.get(h, "")
            cell = ws.cell(row=r, column=c, value=val)
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            if h == "Link" and val.startswith("http"):
                cell.hyperlink = val
                cell.font = Font(color="0563C1", underline="single")

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{len(rows) + 1}"
    widths = [18, 28, 35, 40, 22, 18, 10, 18, 16, 55, 18, 22, 20, 20, 22, 40]
    for i, w in enumerate(widths[: len(headers)], 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    wb.save(OUT_XLSX)


if __name__ == "__main__":
    main()
