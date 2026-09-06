#!/usr/bin/env python3
"""Apply adjustments from UCPH_Spinout_Grants_Overview Word comments to cleaned CSV."""
import csv
from pathlib import Path

CSV_PATH = Path(r"c:\Users\Kaja\Documents\Funds\updated file without VC - cleaned.csv")

REMOVE = {
    "Accelerace",  # Now primarily VC; cohort programme → Lighthouse Launch
    "Symbion / Copenhagen Science City",
    "The Gate",
}

ADD = [
    {
        "Opportunity": "Incubator/Accelerator",
        "Name": "CBS CSE (Copenhagen School of Entrepreneurship)",
        "Link": "https://cse.cbs.dk/",
        "Criteria": "Students, recent graduates, or researchers at Danish higher-ed institutions; startup or committed idea stage",
        "Industrial segment": "General",
        "Stage": "Early venture",
        "Geography": "DK",
        "Funding Amount": "No direct funding (incubation/acceleration support)",
        "Deadline": "Rolling",
        "Quick info": (
            "CBS entrepreneurship centre (distinct from former UCPH CSE/Venture Cup). "
            "Incubator and accelerator for founders at idea through growth stage; EXPLORE pre-incubation, "
            "Deep Green Innovators, and OpenInnovation with DTU Skylab and KU Actory."
        ),
        "CVR required at application": "Optional",
        "CVR required at programme start": "Optional",
    },
    {
        "Opportunity": "Incubator/Accelerator",
        "Name": "Lighthouse Launch",
        "Link": "https://lighthouse.ku.dk/en/students/lighthouselaunch/",
        "Criteria": "UCPH students, researchers, and postdocs with a concrete idea; KU affiliation required",
        "Industrial segment": "General",
        "Stage": "Exploratory innovation",
        "Geography": "DK",
        "Funding Amount": "DKK 30K grant (cohort programme)",
        "Deadline": "Rolling (cohort-based)",
        "Quick info": (
            "KU Lighthouse 14-week pre-accelerator for evidence-based idea validation through structured "
            "experiments. Open to students, researchers, and postdocs; replaces the former KU–Accelerace "
            "cohort pathway. Mentoring and workshops; prepares teams for POC funding, accelerators, or investment."
        ),
        "CVR required at application": "No",
        "CVR required at programme start": "No",
    },
    {
        "Opportunity": "Soft Funding",
        "Name": "IFD Industrial Researcher (Industrial PhD/Postdoc)",
        "Link": "https://www.innovationsfonden.dk/en/p/industrial-researcher",
        "Criteria": "DK company with CVR employs candidate; university supervisor; company co-finances salary",
        "Industrial segment": "Tech, Health, Biotech, Cleantech, General",
        "Stage": "PoC",
        "Geography": "DK",
        "Funding Amount": "Salary subsidy (company + university components; project-specific)",
        "Deadline": "2x/year (spring, autumn)",
        "Quick info": (
            "IFD funds company–university research hires: Industrial PhD (3 years) or Industrial Postdoc "
            "(1–3 years). Company must apply and co-finance; candidate splits time between company and university. "
            "Common spin-out route to fund a research employee while retaining academic supervision."
        ),
        "CVR required at application": "Yes",
        "CVR required at programme start": "Yes",
    },
]

QUICK_INFO_UPDATES = {
    "IFD Innobooster": (
        "Extension of the Innofounder pathway for incorporated SMEs: co-financing for salaries, external "
        "knowledge, equipment, and materials (not rent, transport, or sales/marketing). "
        "Eligible costs: salaries, external knowledge providers, equipment, materials. "
        "Often used after Innofounder."
    ),
    "IFD Grand Solutions": (
        "Large consortia addressing major societal challenges. Co-financing: SMEs 35–75%, large companies "
        "25–65%, research institutions up to 90% + overhead. UCPH applicants typically supported via faculty "
        "research offices (FRB+ for SCIENCE, Nørre Alle Campus office for SUND)."
    ),
    "NNF Pioneer Innovator Grant": (
        "Primarily supports early-stage research at universities and research institutes (grant to institution, "
        "not individual). Themes: cardiometabolic/infectious diseases, agriculture, food, industrial/environmental "
        "biotech, carbon capture, quantum tech. Combined annual budget DKK 190M."
    ),
    "EIC Pathfinder": (
        "EU programme for ambitious early-stage research consortia pursuing breakthrough science and technology "
        "(TRL 1–4). Pathfinder Open and Challenges calls; highly competitive. Total budget EUR 262M. "
        "Open call success rate ~2.1% (2025); historically 7–8% (2021–23); Challenges strand typically higher (~10%)."
    ),
    "Villum Foundation and VELUX Group": (
        "Joint Villum Foundation–VELUX Group programme (separate from Villum's wider grant portfolio). "
        "Collaborative research funding for sustainable building technology, daylight, indoor climate, and "
        "biophilic design. VELUX contribution qualifies as co-financing for Innobooster or EUDP."
    ),
    "Vissing Fonden": (
        "Energy and climate startup grants (typically DKK 200K–300K). CVR and Danish bank account required. "
        "Energy applications are routed via partner universities — at UCPH via Lighthouse, which provides the "
        "required university endorsement before submission. Other pools (medical research, children/youth) are "
        "separate direct application tracks."
    ),
}


def main():
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        fieldnames = reader.fieldnames
        rows = [r for r in reader if r["Name"] not in REMOVE]

    names = {r["Name"] for r in rows}
    for row in ADD:
        if row["Name"] not in names:
            rows.append(row)

    for row in rows:
        if row["Name"] in QUICK_INFO_UPDATES:
            row["Quick info"] = QUICK_INFO_UPDATES[row["Name"]]

    rows.sort(key=lambda r: (r["Opportunity"], r["Name"].lower()))

    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Removed: {len(REMOVE)}")
    print(f"Added: {len([a for a in ADD if a['Name'] not in names])}")
    print(f"Updated Quick info: {len(QUICK_INFO_UPDATES)}")
    print(f"Total rows: {len(rows)}")


if __name__ == "__main__":
    main()
