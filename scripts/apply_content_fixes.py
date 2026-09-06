"""Apply content fixes after link audit (user-approved)."""
from __future__ import annotations

import csv
from pathlib import Path

CSV_PATH = Path(r"c:\Users\Kaja\Documents\Funds\updated file without VC - cleaned.csv")

DELETE = {
    "Diversity Commitment",
    "Norlys Vækstpulje",
}

# Patches keyed by current Name (before rename)
PATCHES: dict[str, dict] = {
    "Dineros Iværksetterlegat": {
        "Name": "Dinero Iværksætterlegat",
        "Criteria": "DK company started within last 24 months; CVR required",
        "Funding Amount": "DKK 10K (5 grants/year)",
        "Deadline": "1 October (annual)",
        "Quick info": (
            "Visma Dinero Iværksætterlegat: 5 × DKK 10,000 once yearly. Applicants must have started a company "
            "within the last 24 months and provide CVR plus ownership documentation. Dinero user not required. "
            "Max one A4 application page."
        ),
        "CVR at application": "Yes",
        "CVR at programme start": "Yes",
    },
    "Care Tech Challenge": {
        "Criteria": "DK startups 0–3 years old (CVR); limited commercial revenue on the solution",
        "Industrial segment": "Health, Care tech, Welfare tech",
        "Funding Amount": "No cash grant (accelerator + exposure; Danish.Care membership fee)",
        "Deadline": "Rolling screening for 2026/2027 cohort",
        "Quick info": (
            "Danish.Care CareTech CHALLENGE accelerator for assistive/welfare-tech startups. Activities include "
            "pitches, Investor Day, Health & Rehab exhibition, workshops and industry matchmaking. Participation "
            "requires screening plus paid Danish.Care membership (Group 1). Company age 0–3 years based on CVR."
        ),
        "CVR at application": "Yes",
        "CVR at programme start": "Yes",
    },
    "Mikrolegat": {
        "Criteria": "Students in higher ed / recent graduates (3 months) or youth/vocational (Momentum)",
        "Funding Amount": "Up to DKK 60K (higher ed); up to DKK 35K (Momentum)",
        "Deadline": "4x/year (15 Mar/May/Sep/Nov; Momentum 30 Mar/May/Sep/Nov)",
        "Quick info": (
            "Fonden for Entreprenørskab micro-grants for student/pupil ideas. Higher-education Mikrolegat up to "
            "DKK 60K; Momentum Mikrolegat for youth/vocational students up to DKK 35K. 25% co-financing if CVR "
            "registered."
        ),
    },
    "Time to Raise": {
        "Opportunity": "Incubator/Accelerator",
        "Criteria": "Founder-led startups currently fundraising or fundraising within ~6 months",
        "Industrial segment": "General",
        "Geography": "Nordics, EU",
        "Funding Amount": "No direct grant (fundraising accelerator)",
        "Deadline": "Rolling / per cohort",
        "Quick info": (
            "Techarena fundraising accelerator for founder-led companies (not women-only). Focuses on investor "
            "readiness, warm intros and raising capital faster; alumni report capital raised via the programme."
        ),
    },
    "Otto Mønsteds Fond": {
        "Name": "Otto Mønsteds Fond – Den Lyse Ide",
        "Link": "https://omfonden.dk/den-lyse-ide/",
        "Criteria": "Students and educators at Danish higher-education institutions with an innovative idea",
        "Industrial segment": "General, Tech, Innovation",
        "Stage": "Exploratory innovation",
        "Funding Amount": "DKK 500K total across winners (typically 2 prizes + bronze sculptures)",
        "Deadline": "Annual (opens ~15 April)",
        "Quick info": (
            "Otto Mønsteds Fond prize Den Lyse Ide recognising innovative student/educator ideas that can "
            "contribute to Danish trade and industry. Annual call; prize package includes cash (DKK 500K shared "
            "among winners) and commissioned bronze sculptures. Broader foundation also funds other trade/industry "
            "projects via omfonden.dk."
        ),
        "CVR at application": "Any",
        "CVR at programme start": "Any",
    },
    "NextGen Innovation and Startup Hub": {
        "Name": "NextGen Innovation (Odense Robotics)",
        "Opportunity": "Soft Funding",
        "Criteria": "SMEs with robotics/drone projects in partnership with a knowledge institution",
        "Industrial segment": "Tech, Robotics, Drones",
        "Stage": "PoC",
        "Funding Amount": "Up to DKK 350K total (max DKK 200K company + DKK 150K knowledge partner)",
        "Deadline": "Per call (check Odense Robotics; Jun 2025 call closed)",
        "Quick info": (
            "Odense Robotics / Fyn erhvervsfyrtårn development pool for robot and drone innovation. Requires "
            "min. one SME + one knowledge institution. Support is 50% of SME labour costs (de minimis) and 100% "
            "for the knowledge partner. Focus areas: large-structure production, advanced drones, autonomous "
            "near-coast shipping. Confirm current call status before applying."
        ),
        "CVR at application": "Yes",
        "CVR at programme start": "Yes",
    },
    "Founder Festival": {
        "Criteria": "Self-employed / sole traders / aspiring founders (Odense focus)",
        "Stage": "All stages",
        "Funding Amount": "Event (no grant)",
        "Deadline": "3 September 2026",
        "Quick info": (
            "One-day Founders Festival in Odense (Thrige Firkanten), organised by Ejendomsselskabet Olav de Linde "
            "and Odense Kommune. Talks, workshops and 1:1 advisor sessions for new and established self-employed "
            "founders and people considering starting."
        ),
    },
    "Danish Entrepreneurship Festival": {
        "Name": "Danmarks Entreprenørskabsfestival",
        "Criteria": "Pupils, students and educators in entrepreneurship education (primary to higher ed)",
        "Industrial segment": "General, Education",
        "Funding Amount": "Event / prizes within education programmes (varies)",
        "Deadline": "Annual (Nov; multiple locations)",
        "Quick info": (
            "Fonden for Entreprenørskab’s national entrepreneurship-in-education festival across six locations "
            "(primary, youth and higher education). Includes INSPIRE teacher conference, pitching finales "
            "(e.g. Projekt Edison, Start Up Programme) and prizes — primarily an education ecosystem event, "
            "not a general startup conference."
        ),
    },
    "Copenhagen Health Innovation (CHI)": {
        "Funding Amount": "No direct funding",
        "Quick info": (
            "Partnership platform (since 2016) connecting students and educators from Copenhagen-area "
            "universities/UCCs with hospitals and care organisations on real health-innovation cases. "
            "Education-driven collaboration and entrepreneurship skills — not a startup grant programme."
        ),
    },
    "Ideas Lab": {
        "Funding Amount": "In-kind (office, mentoring, workshops)",
        "Quick info": (
            "Filmby Aarhus incubator / startup office (Ideas Lab) for digital creative ventures in games, "
            "film, XR and animation. Office space, mentoring, legal/accountant access, workshops and "
            "masterclasses toward acceleration — no standard cash grant."
        ),
    },
    "The Circular Lab": {
        "Funding Amount": "No direct grant (community, visibility, challenges)",
        "Opportunity": "Incubator/Accelerator",
        "Quick info": (
            "Ecoembes TheCircularLab GoCircular: European open-innovation community for circular-economy "
            "startups. Visibility via goCircular Radar, networking, challenges and GoCircularPass certification. "
            "Open to European startups (including Nordics); not a classic DK cash grant."
        ),
    },
    "SMIL": {
        "Funding Amount": "Event (ticketed; no grant)",
    },
    "CPH Townhall": {
        "Funding Amount": "Event (no grant)",
        "Deadline": "Recurring / per event",
    },
    "Odense Investor Summit": {
        "Funding Amount": "Event (no grant)",
    },
    "Green Leap Challenge": {
        "Quick info": (
            "Food & Bio Cluster Denmark annual idea competition for green agrifood and bioresource concepts "
            "(often pre-sales). Typically 3 × DKK 50K prizes plus exposure. Watch Food & Bio Cluster "
            "news/events for the next call."
        ),
    },
    "Creative Business Cup": {
        "Geography": "DK, International",
        "Funding Amount": "Prize-based (national/global packages vary yearly)",
        "Quick info": (
            "Creative Business Network global competition for creative-industry startups. National rounds "
            "(incl. Denmark) feed Global Finals. Prize and in-kind packages vary by year and national partner."
        ),
    },
    "Odin Award": {
        "Quick info": (
            "Odense/Fyn awards (Odin, Tech, Concept, Impact) organised with Ignite Odense / Coworking Plus. "
            "Main prize historically around DKK 40K; category amounts vary. Concept targets early pre-company "
            "ideas; other categories favour established startups."
        ),
    },
    "Hub for Innovation in Tourism": {
        "Funding Amount": "Programme support (accelerator; not a fixed cash grant)",
    },
    "Canute": {
        "Funding Amount": "Paid advisory / programmes (varies)",
    },
    "Start Up Factory": {
        "Funding Amount": "Programme support (varies; education programme)",
        "Industrial segment": "Tech, Engineering",
    },
    "Fonden for Entreprenørskab": {
        "Funding Amount": "Varies (programmes; Mikrolegat listed separately)",
    },
    "Nordic Women’s Health Hub": {
        "Link": "https://nordicwomenshealth.com/",
        "Quick info": (
            "Nordic Women’s Health community/hub supporting women’s health innovation and female founders "
            "with network, visibility and sector programmes across the Nordics."
        ),
    },
    "Nordic Women in Tech Awards": {
        "Funding Amount": "Recognition only (no cash prize)",
    },
}


def main() -> None:
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        fieldnames = reader.fieldnames
        rows = list(reader)

    out = []
    deleted = []
    changed = []
    for row in rows:
        name = row["Name"]
        if name in DELETE:
            deleted.append(name)
            continue
        if name in PATCHES:
            patch = PATCHES[name]
            for k, v in patch.items():
                row[k] = v
            changed.append(name)
        out.append(row)

    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(out)

    print(f"Deleted ({len(deleted)}): {deleted}")
    print(f"Patched ({len(changed)}): {changed}")
    print(f"Rows: {len(rows)} -> {len(out)}")


if __name__ == "__main__":
    main()
