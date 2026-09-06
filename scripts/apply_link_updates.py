"""Apply user-approved link/name updates from link audit."""
from __future__ import annotations

import csv
from pathlib import Path

CSV_PATH = Path(r"c:\Users\Kaja\Documents\Funds\updated file without VC - cleaned.csv")

# name -> new link (and optional field overrides)
UPDATES: dict[str, dict] = {
    "Creative Business Cup": {"Link": "https://www.cbnet.com/creative-business-cup"},
    "Dineros Iværksetterlegat": {
        "Link": "https://dinero.dk/ivaerksaetterlegat/",
        "Funding Amount": "DKK 10K (5 grants/year)",
        "Quick info": (
            "Visma Dinero annual entrepreneur grant (Iværksætterlegat): 5 × DKK 10,000. "
            "Open to founders who started a business within the last 24 months; Dinero user not required. "
            "Deadline typically 1 October."
        ),
    },
    "Hub for Innovation in Tourism": {
        "Link": "https://innohub.dk/",
        "Quick info": (
            "National Hub for Innovation in Tourism (HIT) — partnership of Dansk Kyst- og Naturturisme, "
            "MeetDenmark and Dansk Storbyturisme. Startup accelerator, matchmaking and network for "
            "tourism-relevant founders; co-funded by ESF+ and Danmarks Erhvervsfremmebestyrelse."
        ),
    },
    "Cancute": {
        "Name": "Canute",
        "Link": "https://canute.io/",
        # keep existing industrial segment as-is unless clearly wrong; Canute is general scaling, not health-only
        "Industrial segment": "General, Tech",
    },
    "Green Leap Challenge": {
        "Link": "https://www.foodbiocluster.dk/",
        "Criteria": "DK-based early agrifood / bioresource ideas (pre-sales)",
        "Industrial segment": "Cleantech, Sustainability, Food, Biotech",
        "Deadline": "Annual (varies; typically spring/autumn call)",
        "Quick info": (
            "Food & Bio Cluster Denmark annual idea competition for green agrifood and bioresource concepts "
            "(often pre-sales). Typically 3× DKK 50K prizes plus exposure. No evergreen challenge URL found; "
            "watch Food & Bio Cluster news/events for the next call. Dec 2025 awards event is past."
        ),
    },
    "Nordic Women in Tech Awards": {"Link": "https://nordicwomenintechawards.com/"},
    "Odin Award": {"Link": "https://igniteodense.nu/investor-odin-award/"},
    "CPH Townhall": {
        "Link": "https://techstartup.dk/",
        "Quick info": (
            "Townhall-style Copenhagen startup community events run under Techstartup.dk "
            "(pitches, networking, ecosystem updates). Townhall is one of their recurring formats."
        ),
    },
    "Danish Entrepreneurship Festival": {"Link": "https://ffefonden.dk/festival/"},
    "Founder Festival": {"Link": "https://foundersfestival.dk/"},
    "Odense Investor Summit": {"Link": "https://investinodense.com/odense-investor-summit/"},
    "SMIL": {
        "Link": "https://www.startupaarhus.com/events/smil",
        "Criteria": "DK-based startups (Aarhus-hosted national festival)",
        "Industrial segment": "General",
        "Quick info": (
            "Annual Aarhus startup festival curated by Startup Aarhus (next edition marketed as SMIL’27). "
            "Curated sessions connecting founders, investors and operators — not a cash-prize competition."
        ),
    },
    # StortTech: leave unchanged pending delete decision
    "Diversity Commitment": {"Link": "https://diversity-commitment.com/"},
    "Nordic Women’s Health Hub": {"Link": "https://nordicwomenshealth.com/"},
    "Time to Raise": {"Link": "https://timetoraise.co"},
    "Care Tech Challenge": {"Link": "https://www.danish.care/aktiviteter/for-startups-caretech-challenge/"},
    "Ideas Lab": {
        "Link": "https://filmbyaarhus.dk/english/industry-development/start-up-office-and-community",
        "Criteria": "Promising startups/talent in games, film, XR, animation (Aarhus)",
        "Industrial segment": "Media, Entertainment, Games",
        "Stage": "Early venture",
        "Quick info": (
            "Filmby Aarhus incubator / startup office (Ideas Lab) for digital creative ventures in games, "
            "film, XR and animation. Offers office space, mentoring, legal/accountant access, workshops "
            "and masterclasses toward acceleration."
        ),
    },
    # The Circular Lab: NOT applying Spanish GoCircular URL — flagged for user
    "Mikrolegat": {"Link": "https://mikrolegat.ffefonden.dk/"},
    "Nordlys Vækstpulje": {
        "Name": "Norlys Vækstpulje",
        "Link": "https://norlys.dk/om-norlys/vaekstpulje/",
        "Criteria": "DK-based growth companies (Norlys growth pool)",
        "Geography": "DK",
        "Quick info": (
            "Norlys Vækstpulje supports Danish growth companies. Confirm current amount ranges and "
            "eligibility on Norlys’ vækstpulje page before applying."
        ),
    },
    "Otto Mønsteds Fond": {"Link": "https://omfonden.dk/"},
    "Copenhagen Health Innovators": {
        "Name": "Copenhagen Health Innovation (CHI)",
        "Link": "https://copenhagenhealthinnovation.dk/",
        "Criteria": "Students + educators matched with Region H clinics/cases",
        "Quick info": (
            "Partnership platform (since 2016) connecting students and educators from Copenhagen-area "
            "universities/UCCs with hospitals and care organisations on real health-innovation cases. "
            "Focus is education-driven health innovation and entrepreneurship skills — not a classic "
            "startup grant programme. ‘Health Innovators’ appears as a CHI community metric."
        ),
    },
    "Fonden for Entreprenørskab": {"Link": "https://ffefonden.dk/"},
    "NextGen Innovation and Startup Hub": {
        "Link": "https://www.odenserobotics.dk/da/projects/nextgen-innovation/",
        "Criteria": "Student/young founders in robotics & related tech (Odense)",
        "Industrial segment": "Tech, Robotics",
        "Quick info": (
            "NextGen Innovation project under Odense Robotics supporting young founders and student-driven "
            "innovation in the robotics ecosystem."
        ),
    },
    "Start Up Factory": {
        "Link": "https://ingenioer.au.dk/uddannelser/startup-factory-au-engineering/",
        "Criteria": "AU Engineering students; early-stage ventures",
        "Quick info": (
            "Aarhus University Engineering Startup Factory — student entrepreneurship programme helping "
            "engineering students launch early-stage ventures."
        ),
    },
}


def main() -> None:
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        fieldnames = reader.fieldnames
        rows = list(reader)

    changed = []
    for row in rows:
        name = row["Name"]
        if name not in UPDATES:
            continue
        patch = UPDATES[name]
        before = {k: row.get(k) for k in patch}
        for k, v in patch.items():
            row[k] = v
        changed.append((name, before, {k: row.get(k) for k in patch}))

    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated {len(changed)} rows")
    for name, before, after in changed:
        print(f"- {name}")
        for k in after:
            if before.get(k) != after.get(k):
                print(f"    {k}: {before.get(k)!r} -> {after.get(k)!r}")


if __name__ == "__main__":
    main()
