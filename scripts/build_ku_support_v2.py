"""
Build funds with KU support - v2:
- Keep v1 structure
- Add PPT-only programmes (with verified links where found)
- Apply TRL to Stage + Quick info for PPT-covered programmes
"""
from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

BASE = Path(r"c:\Users\Kaja\Documents\Funds")
SRC = BASE / "funds with KU support - v1.csv"
OUT_CSV = BASE / "funds with KU support - v2.csv"
OUT_XLSX = BASE / "funds with KU support - v2.xlsx"
NEEDS_LINKS = BASE / "funds with KU support - v2 needs links.txt"

HEADERS = [
    "Opportunity",
    "Name",
    "Link",
    "Criteria",
    "Industrial segment",
    "Stage",
    "Geography",
    "Funding Amount",
    "Deadline",
    "Quick info",
    "CVR at application",
    "CVR at programme start",
    "KU support unit",
    "KU faculty focus",
    "KU contact hint",
    "PPT notes",
]

# Existing-row TRL updates (from PPT detail / overview slides)
TRL_UPDATES: dict[str, dict] = {
    "IFD Innofounder": {
        "trl": "TRL 1–3",
        "stage": "PoC",
        "extra_qi": "Monthly founder stipend + DKK 100K development grant; 12 months full-time.",
    },
    "IFD Innobooster": {
        "trl": "TRL 4–7",
        "stage": "Early venture",
        "extra_qi": "Knowledge-based SME development; max 35% IFD co-financing; up to 24 months.",
    },
    "IFD Innoexplorer": {
        "trl": "TRL 3–5",
        "stage": "PoC",
        "extra_qi": "Pre-commercial research-based maturation toward spin-out/start-up; up to 12 months.",
    },
    "IFD Grand Solutions": {
        "trl": "TRL 3–8",
        "stage": "All stages",
        "extra_qi": "Large collaborative high-risk solutions; up to 5 years; universities typically 90% funding rate.",
    },
    "NNF Pioneer Innovator Grant": {
        "trl": "TRL 1–3",
        "stage": "PoC",
        "extra_qi": "Academic pre-CVR proof-of-concept; up to DKK 1.2M / 1 year.",
    },
    "NNF Distinguished Innovator Grant": {
        "trl": "TRL 3–5",
        "stage": "PoC",
        "extra_qi": "Mature academic commercialisation by experienced innovators; up to DKK 7.6M / 3 years; pre-CVR.",
    },
    "Open Discovery Innovation Network (ODIN)": {
        "trl": "TRL low–mid (early discovery)",
        "stage": "Exploratory innovation",
        "extra_qi": "Patent-free open discovery network (universities + industry).",
    },
    "EIC Pathfinder": {
        "trl": "TRL low (breakthrough research)",
        "stage": "Exploratory innovation",
        "extra_qi": "Visionary deep-tech research toward radically new technologies.",
    },
    "EIC Transition": {
        "trl": "TRL 3–6",
        "stage": "PoC",
        "extra_qi": "Must build on eligible prior project results; technology + business maturation.",
    },
    "EIC Accelerator": {
        "trl": "TRL 6–9",
        "stage": "Growth/scale",
        "extra_qi": "Scale high-risk innovations; grant and/or equity for market deployment.",
    },
    "UCPH Proof of Concept Fund (POC-TO-GO)": {
        "trl": "TRL 1–3",
        "stage": "Exploratory innovation",
        "extra_qi": "Up to DKK 150K / 6 months; commercial or non-commercial UCPH projects.",
    },
    "UCPH Proof of Concept Fund (POC MAX)": {
        "trl": "TRL 3–9",
        "stage": "PoC",
        "extra_qi": "Up to DKK 500K / 18 months; commercial projects from approved patentable inventions.",
    },
    "SPARK Denmark": {
        "trl": "TRL low (academic PoC)",
        "stage": "PoC",
        "extra_qi": "Life-science mentoring + up to DKK 700K PoC funding.",
    },
    "Spin-outs Denmark": {
        "trl": "TRL low–mid (pre-spin-out)",
        "stage": "PoC",
        "extra_qi": "Junior researcher / postdoc pathway to research-based company.",
    },
    "Open Entrepreneurship": {
        "trl": "TRL low–mid",
        "stage": "Exploratory innovation",
        "extra_qi": "Matchmaking researchers with external entrepreneurs/investors.",
    },
    "BII Bio Studio": {
        "trl": "TRL 2–4",
        "stage": "PoC",
        "extra_qi": "Company-creation for entrepreneurial academic PIs; multi-year funding.",
    },
    "BII Venture Lab": {
        "trl": "TRL 3–5",
        "stage": "Early venture",
        "extra_qi": "Early-stage life science & deep tech; founder-friendly convertible funding.",
    },
    "BII Quantum Lab": {
        "trl": "TRL early (quantum startups)",
        "stage": "Early venture",
        "extra_qi": "Early-stage quantum startups (BII / NATO DIANA collaboration context).",
    },
}

# New programmes to add (from PPT, not previously in table)
NEW_ROWS: list[dict] = [
    {
        "Opportunity": "Research Grants",
        "Name": "Plant2Food (NNF Open Innovation)",
        "Link": "https://projects.au.dk/plant2food",
        "Criteria": "Researchers at partner universities (AU, UCPH, DTU, WUR) + industry partners; patent-free open projects",
        "Industrial segment": "Food, Agri, Sustainability, Biotech",
        "Stage": "Exploratory innovation",
        "Geography": "DK, International",
        "Funding Amount": "Project grants within platform (Type budgets typically DKK ~1–4M; platform up to DKK 200M)",
        "Deadline": "Open calls / rounds (see Plant2Food site; 2026 call published)",
        "Quick info": (
            "NNF Open Innovation in Science platform accelerating plant-based foods via patent-free university–industry "
            "projects. Hosted at Aarhus University; UCPH is a partner. Results published openly. TRL: low (early-stage / "
            "pre-competitive research)."
        ),
        "CVR at application": "Any",
        "CVR at programme start": "Any",
        "KU support unit": "Preaward",
        "KU faculty focus": "SCIENCE, SUND",
        "KU contact hint": "Preaward RSO (primary). Plant2Food Secretariat, Aarhus University.",
        "PPT notes": "PPT contact: Preaward. Grant size in overview 3–10M DKK (see call). TRL low.",
    },
    {
        "Opportunity": "Research Grants",
        "Name": "IBIS (Initiative for Biofertilizer Innovation and Science)",
        "Link": "https://ibis.dtu.dk/",
        "Criteria": "Open Innovation in Science calls; universities/public research + collaborators (Global North & South)",
        "Industrial segment": "Agri, Biotech, Sustainability",
        "Stage": "Exploratory innovation",
        "Geography": "DK, International",
        "Funding Amount": "OIS project calls within DKK 215M platform (NNF + Gates Foundation)",
        "Deadline": "Calls announced via IBIS / NNF (check ibis.dtu.dk)",
        "Quick info": (
            "Global biofertiliser R&D initiative hosted at DTU Bioengineering; UCPH is a partner. Open, non-GMO, "
            "no patents on organisms/use. Builds discovery-to-field pipeline. TRL: low–mid (foundational research through "
            "field-testing)."
        ),
        "CVR at application": "Any",
        "CVR at programme start": "Any",
        "KU support unit": "Preaward",
        "KU faculty focus": "SCIENCE, SUND",
        "KU contact hint": "Preaward RSO (primary). IBIS Secretariat, DTU Bioengineering.",
        "PPT notes": "PPT: Preaward. Budget DKK 215M total (2025–2030).",
    },
    {
        "Opportunity": "Soft Funding",
        "Name": "Plantefonden (Fonden for Plantebaserede Fødevarer)",
        "Link": "https://plantefonden.dk/hvad-stoetter-vi/tilskud-fra-plantefonden",
        "Criteria": "Projects developing the Danish plant-based food sector (apply via Landbrugs- og Fiskeristyrelsen)",
        "Industrial segment": "Food, Agri, Sustainability",
        "Stage": "All stages",
        "Geography": "DK",
        "Funding Amount": "Varies per call",
        "Deadline": "Annual (next window expected ~Feb 2027 after 2026 closed)",
        "Quick info": (
            "Danish fund for plant-based food sector development. Application materials via LFST tilskudsguide. "
            "PPT lists under Preaward for SCIENCE/SUND. Confirm current call before applying."
        ),
        "CVR at application": "Any",
        "CVR at programme start": "Any",
        "KU support unit": "Preaward",
        "KU faculty focus": "SCIENCE, SUND",
        "KU contact hint": "Preaward RSO (Frederiksberg+ / relevant faculty)",
        "PPT notes": "Also see LFST guide: lfst.dk tilskudsguide Plantefonden.",
    },
    {
        "Opportunity": "Soft Funding",
        "Name": "EUopSTART",
        "Link": "https://ufsn.dk/tilskud-puljer-og-bevillinger/forsknings-og-innovationsomraadet/find-danske-tilskudsprogrammer/euopstart/",
        "Criteria": "Danish companies and GTS preparing Horizon Europe / EDF applications (check current call – universities historically involved via partners)",
        "Industrial segment": "General, Tech, Research",
        "Stage": "All stages",
        "Geography": "DK",
        "Funding Amount": "Up to DKK 75K or 150K (role/programme dependent); covers up to 50% of prep costs",
        "Deadline": "Aligned with HE/EDF calls (via e-grant when open)",
        "Quick info": (
            "Danish Agency scheme reimbursing costs of preparing Horizon Europe / EDF proposals. Current UFSN wording "
            "targets companies and GTS; still listed in KU Preaward PPT as a support route for EU applications. "
            "Verify eligibility for your organisation type on the live call text."
        ),
        "CVR at application": "Yes",
        "CVR at programme start": "Yes",
        "KU support unit": "Preaward",
        "KU faculty focus": "Alle",
        "KU contact hint": "Preaward RSO",
        "PPT notes": "PPT: Preaward-managed. Link verified to UFSN EUopSTART hub.",
    },
    {
        "Opportunity": "Soft Funding",
        "Name": "Global Innovation Network Programme (GINP)",
        "Link": "https://ufsn.dk/english/funding-calls-and-grants/research-and-innovation/global-innovation-network-programme/",
        "Criteria": "Danish–international research/innovation networking (historical programme)",
        "Industrial segment": "General, Research",
        "Stage": "Exploratory innovation",
        "Geography": "DK, International",
        "Funding Amount": "Varies (networking grants)",
        "Deadline": "Final GINP round was 2025; successor international programme via Innovation Fund Denmark (2026–2029 agreement)",
        "Quick info": (
            "UFSN programme for international research/innovation networking. 2025 was the fourth and final GINP round; "
            "a new IFD-implemented international collaboration programme is planned. Keep for reference / successor watch."
        ),
        "CVR at application": "Any",
        "CVR at programme start": "Any",
        "KU support unit": "Preaward",
        "KU faculty focus": "Alle",
        "KU contact hint": "Preaward RSO",
        "PPT notes": "PPT listed under Preaward. Programme ending/transitioning — flag for user.",
    },
    {
        "Opportunity": "Incubator/Accelerator",
        "Name": "BII Upscalator",
        "Link": "https://bii.dk/community/news/novo-nordisk-foundation-grants-25-million-euros-to-bii-to-power-the-next-generation-of-biosolutions-companies/",
        "Criteria": "Early-stage European biosolutions startups ready to scale fermentation/production (lab → industrial)",
        "Industrial segment": "Biotech, Cleantech, Sustainability, Food",
        "Stage": "Growth/scale",
        "Geography": "DK, EU",
        "Funding Amount": "Up to ~€3M/project / €1.8M/startup context in BII family; Upscalator is €25M NNF initiative (convertible loan calls for CDMO scale-up)",
        "Deadline": "Calls via BII (e.g. convertible-loan call deadline noted 1 Sep 2026)",
        "Quick info": (
            "BII initiative (NNF-funded) helping biosolutions startups scale from lab to industrial production: advisory, "
            "process design/lab, CDMO network, funding vehicle and community. TRL: mid–high scale-up (PPT ~TRL 5–7). "
            "Dedicated evergreen programme URL may change with each call — start at BII / news link."
        ),
        "CVR at application": "Yes",
        "CVR at programme start": "Yes",
        "KU support unit": "Lighthouse",
        "KU faculty focus": "SUND, SCIENCE",
        "KU contact hint": "KU Lighthouse",
        "PPT notes": "PPT: Lighthouse-managed BII family. Link is announcement page — improve if BII publishes stable /programs URL.",
    },
    {
        "Opportunity": "Soft Funding",
        "Name": "Industriens Fond",
        "Link": "https://www.industriensfond.dk/",
        "Criteria": "Projects creating positive change for Danish companies (open innovation / competitive calls vary)",
        "Industrial segment": "General, Tech, Industry",
        "Stage": "All stages",
        "Geography": "DK",
        "Funding Amount": "Varies by call",
        "Deadline": "Per call (see industriensfond.dk)",
        "Quick info": (
            "Private industrial foundation funding original ideas that create change and positive effects for Danish "
            "companies. PPT lists under Lighthouse-managed programmes with commercial focus."
        ),
        "CVR at application": "Any",
        "CVR at programme start": "Any",
        "KU support unit": "Lighthouse",
        "KU faculty focus": "Alle – kommercielt fokus",
        "KU contact hint": "KU Lighthouse",
        "PPT notes": "PPT Lighthouse list.",
    },
    {
        "Opportunity": "Soft Funding",
        "Name": "EIFO Green Accelerator",
        "Link": "https://eifo.dk/en/our-work/special-schemes/green-accelerator-grants-for-sustainable-export-projects",
        "Criteria": "Danish companies / export alliances with mature green technologies ready for export maturation",
        "Industrial segment": "Cleantech, Sustainability, Energy",
        "Stage": "Growth/scale",
        "Geography": "DK",
        "Funding Amount": "Up to ~EUR 300K / company (de minimis); high co-financing share of eligible costs",
        "Deadline": "Periodic rounds (check EIFO)",
        "Quick info": (
            "EIFO grant scheme to mature green export projects (consultancy, market studies, legal/ESG, travel, etc.). "
            "Targets proven/export-ready solutions (often described as TRL 9). Company size/export thresholds apply. "
            "TRL: 9 (market-ready export maturation)."
        ),
        "CVR at application": "Yes",
        "CVR at programme start": "Yes",
        "KU support unit": "Lighthouse",
        "KU faculty focus": "Alle – kommercielt fokus",
        "KU contact hint": "KU Lighthouse (for researcher–company cases); applicants are typically companies",
        "PPT notes": "PPT lists several EIFO instruments; Green Accelerator is the clearest grant-style entry for this table.",
    },
]

# Flagged for user help (weak / transitional links)
NEEDS_USER_HELP = [
    "BII Upscalator — using BII news URL; prefer stable programme page if you have one",
    "BII AI Lab — NOT added (no solid public programme URL found; only mentioned in PPT)",
    "BII Venture House — NOT added as separate row (follow-on to Venture Lab; confirm if you want it)",
    "Scaleup Europe Fund — NOT added (equity / EIC Fund investment vehicle; VC-adjacent)",
    "Dansk Industris Fonde og legater (Alexander Foss etc.) — NOT added as separate rows; Industriens Fond added instead",
    "Other EIFO loan/guarantee schemes (Ukraine/Africa etc.) — NOT added (not researcher journey)",
    "GINP — added but marked as ending 2025 / successor via IFD",
    "EUopSTART — added; confirm whether KU researchers/institutions are eligible under current UFSN wording",
]


def append_trl_qi(qi: str, trl: str, extra: str = "") -> str:
    qi = (qi or "").strip()
    # Avoid duplicate TRL lines
    if re.search(r"\bTRL\b", qi, re.I):
        base = qi
    else:
        base = f"{qi} {trl}." if qi else f"{trl}."
    if extra and extra not in base:
        base = f"{base} {extra}"
    return re.sub(r"\s+", " ", base).strip()


def load_rows() -> list[dict]:
    with SRC.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def apply_trl(rows: list[dict]) -> list[dict]:
    out = []
    for row in rows:
        name = row["Name"]
        if name in TRL_UPDATES:
            u = TRL_UPDATES[name]
            row = dict(row)
            row["Stage"] = u["stage"]
            row["Quick info"] = append_trl_qi(row.get("Quick info", ""), u["trl"], u.get("extra_qi", ""))
            notes = row.get("PPT notes", "")
            trl_note = f"Stage aligned to {u['trl']}."
            if trl_note not in notes:
                row["PPT notes"] = f"{notes} {trl_note}".strip()
        out.append(row)
    return out


def add_new(rows: list[dict]) -> list[dict]:
    existing = {r["Name"] for r in rows}
    added = []
    for nr in NEW_ROWS:
        if nr["Name"] in existing:
            continue
        added.append(nr)
    return rows + added, added


def write_csv(rows: list[dict]) -> None:
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS, delimiter=";", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({h: r.get(h, "") for h in HEADERS})


def write_xlsx(rows: list[dict]) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Funds"
    header_fill = PatternFill("solid", fgColor="1F4E79")
    ku_fill = PatternFill("solid", fgColor="2E7D32")
    header_font = Font(bold=True, color="FFFFFF")
    ku_cols = {"KU support unit", "KU faculty focus", "KU contact hint", "PPT notes"}

    for c, h in enumerate(HEADERS, 1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.fill = ku_fill if h in ku_cols else header_fill
        cell.font = header_font
        cell.alignment = Alignment(wrap_text=True, vertical="top")

    for r, row in enumerate(rows, 2):
        for c, h in enumerate(HEADERS, 1):
            val = row.get(h, "")
            cell = ws.cell(row=r, column=c, value=val)
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            if h == "Link" and isinstance(val, str) and val.startswith("http"):
                cell.hyperlink = val
                cell.font = Font(color="0563C1", underline="single")

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(HEADERS))}{len(rows)+1}"
    widths = {
        "Opportunity": 18, "Name": 34, "Link": 34, "Criteria": 36, "Industrial segment": 22,
        "Stage": 18, "Geography": 14, "Funding Amount": 30, "Deadline": 24, "Quick info": 50,
        "CVR at application": 14, "CVR at programme start": 16, "KU support unit": 14,
        "KU faculty focus": 22, "KU contact hint": 40, "PPT notes": 42,
    }
    for i, h in enumerate(HEADERS, 1):
        ws.column_dimensions[get_column_letter(i)].width = widths.get(h, 18)

    # Legend
    leg = wb.create_sheet("KU support legend")
    leg["A1"] = "v2 additions & TRL→Stage rules"
    leg["A1"].font = Font(bold=True, size=13)
    lines = [
        "",
        "Base: funds with KU support - v1 (original cleaned file still untouched)",
        "",
        "Stage vocabulary (unchanged): Exploratory innovation → PoC → Early venture → Growth/scale (+ All stages)",
        "TRL mapping used:",
        "  TRL ~1–3 academic/pre-competitive → Exploratory innovation or PoC (PoC if commercialisation-oriented)",
        "  TRL ~3–5 → PoC",
        "  TRL ~4–7 → Early venture",
        "  TRL ~6–9 / market-ready → Growth/scale",
        "  Wide spans (e.g. 3–8) → All stages",
        "",
        "Items needing your link/decision help:",
    ] + [f"  - {x}" for x in NEEDS_USER_HELP]
    for i, t in enumerate(lines, 1):
        leg.cell(row=i, column=1, value=t)
    leg.column_dimensions["A"].width = 110

    cov = wb.create_sheet("KU coverage summary")
    cov.append(["KU support unit", "Count"])
    for k, v in sorted(Counter(r["KU support unit"] for r in rows).items(), key=lambda x: (-x[1], x[0])):
        cov.append([k, v])
    cov.append([])
    cov.append(["Stage", "Count"])
    for k, v in sorted(Counter(r["Stage"] for r in rows).items(), key=lambda x: (-x[1], x[0])):
        cov.append([k, v])

    wb.save(OUT_XLSX)


def main() -> None:
    rows = load_rows()
    rows = apply_trl(rows)
    rows, added = add_new(rows)
    # sort lightly by Opportunity then Name for readability
    rows.sort(key=lambda r: (r.get("Opportunity", ""), r.get("Name", "")))
    write_csv(rows)
    write_xlsx(rows)
    NEEDS_LINKS.write_text("\n".join(NEEDS_USER_HELP), encoding="utf-8")
    print(f"Rows: {len(rows)} (added {len(added)})")
    for a in added:
        print(f"  + {a['Name']} | {a['Link']}")
    print(f"CSV:  {OUT_CSV}")
    print(f"XLSX: {OUT_XLSX}")
    print("Needs user help:")
    for x in NEEDS_USER_HELP:
        print(" -", x)


if __name__ == "__main__":
    main()
