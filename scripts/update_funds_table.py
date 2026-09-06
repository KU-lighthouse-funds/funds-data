#!/usr/bin/env python3
"""Update funds CSV: opportunity types, fill missing Quick info, dedupe."""
import csv
import re
from pathlib import Path

CSV_PATH = Path(r"c:\Users\Kaja\Documents\Funds\updated file without VC.csv")
OUTPUT_PATH = Path(r"c:\Users\Kaja\Documents\Funds\updated file without VC - cleaned.csv")

# Opportunity type corrections (name -> new type).
# We deliberately keep PoC-style instruments (POC MAX, POC-TO-GO, Spin-outs Denmark)
# under soft funding rather than research grants, so they stay on the PoC part of the journey.
OPPORTUNITY_TYPE_UPDATES = {
    "Nordic Women in Tech Awards": "Awards",
    "Even": "Female Initiatives",  # confirm: network/program, not award
}

# Name/link fixes where research shows clear errors
NAME_LINK_UPDATES = {
    "Even": {
        "Name": "Even Founders",
        "Link": "https://www.evenfounders.com/",
    },
    "Cancute": {
        "Link": "https://canute.io/",
        "Criteria": "DK-based startups scaling internationally",
    },
}

# Deadline corrections where Rolling is inaccurate
DEADLINE_UPDATES = {
    "Beyond Beta": "Annual batches (varies)",
    "Beta Health": "Per programme call",
    "GUDP": "2x/year",
    "Mikrolegat": "4x/year (Mar, May, Sep, Nov)",
    "MUDP": "Annual call",
    "Miljø- og Energi Fonden": "Rolling (continuous applications)",
}

# Quick info content for rows that were empty (keyed by Name)
MORE_INFO_FILLS = {
    "Akademikernes Startup": "Member benefit from Akademikernes A-kasse: 3-month Copenhagen incubator, online incubator, and on-demand courses with mentoring and networking. Open to members exploring entrepreneurship, including while on dagpenge.",
    "Beta Health": "National hospital innovation platform (Novo Nordisk Foundation). Clinicians/researchers at Danish public hospitals apply for BETA.05 (DKK 500K) or BETA.10 (DKK 1M) grants plus structured accelerator support.",
    "Beyond Beta": "EU-funded 12-month national accelerator run by Accelerace, industry clusters, and Danish Business Hubs. Tailored mentoring, workshops, and investor access. Free to join.",
    "Cancute": "Scaling advisory and accelerator (now Canute by Thursday). Helps Danish founders enter US, UK, and Germany with market-entry programmes, fundraising strategy, and public-funding support.",
    "Climate-KIC Urban Mobility Food": "EIT Climate-KIC programmes for EU startups in urban mobility and sustainable food systems. Access to innovation programmes, pilots, and European cleantech networks.",
    "Copenhagen Health Innovators": "Student health-tech entrepreneurship programme connecting Copenhagen students with hospitals, mentors, and innovation challenges in healthcare.",
    "Defence Tech Denmark": "Community and support network for Danish defence and dual-use security startups, linking founders with defence stakeholders, testing opportunities, and ecosystem partners.",
    "DIF Innovation Lab": "DIF (Danish sports federation) innovation lab bridging sportstech startups with federations, clubs, athletes, and universities for user testing and scaling. SportsTech Denmark membership and government-funded innovation packages available.",
    "Diversity Commitment": "Corporate diversity pledge and startup ecosystem initiative promoting inclusive hiring and founder support in Danish tech.",
    "EESA": "Energy and sustainability accelerator/community supporting Danish cleantech startups with mentoring, industry connections, and programme activities in the green transition.",
    "Eureka": "Pan-European network for cross-border R&D collaboration between SMEs. Danish partners can join international consortium projects with national funding through IFD/Eureka national bodies.",
    "Even": "Non-profit supporting Nordic women founders via Startup School (12-week programme), investor database, co-founder matchmaking, and ecosystem partnerships. Tuborgfondet-backed.",
    "Fonden for Entreprenørskab": "National foundation for entrepreneurship education in schools and higher education; runs programmes, teacher resources, and student entrepreneurship activities across Denmark.",
    "Food and Bio Cluster": "Danish cluster organisation for food, bio, and agri-tech companies offering networking, internationalisation support, innovation projects, and sector-specific programmes.",
    "Found Diverse": "Non-profit promoting diversity in Danish entrepreneurship through events, mentoring, and community programmes (founded from NWiTA alumni network).",
    "Founder to Leader": "Leadership development programme for Danish startup founders focusing on management skills, team building, and scaling as a CEO.",
    "Future Manufacturers": "Manufacturing and industry 4.0 startup programme supporting Danish production-tech founders with sector expertise and scaling support.",
    "Game Hub": "Danish games industry hub offering community, events, mentoring, and business development for gaming and interactive media startups.",
    "GUDP": "Green Development and Demonstration Programme for food, agriculture, fisheries, and aquaculture. Supports development, demonstration, and network projects with typical grants DKK 250K–15M; ~50% co-financing. Two annual calls.",
    "HeyFunding Legatet": "Grant from HeyFunding for early-stage Danish startups with social impact focus. Supports idea validation and early development.",
    "Horizon Europe": "EU flagship R&D programme with rolling topic-specific calls. Danish SMEs and research institutions join collaborative consortia; national contact points and EUopSTART can support proposal preparation.",
    "Hub for Innovation in Tourism": "VisitDenmark-linked tourism innovation hub helping Danish tourism-tech startups with industry partnerships, pilots, and market access in hospitality and travel.",
    "Ideas Lab": "Early-stage idea development programme for Danish founders to validate concepts before formal incorporation or accelerator application.",
    "Incuba": "Danish incubator supporting early-stage tech startups with workspace, mentoring, and business development in Aalborg/North Denmark region.",
    "Intech Founders": "Community and programme for female-led tech startups in Denmark with networking, mentoring, and founder support events.",
    "ITU Business Development": "IT University of Copenhagen startup programme: co-founder matching, 3-month idea pipeline, and 6-month incubation with mentorship for ITU students.",
    "Kvinde kompagniet": "Danish network for female entrepreneurs offering peer community, events, and business sparring.",
    "Ladies First": "Copenhagen-based community supporting female founders with networking events, workshops, and mentorship.",
    "Leap Forward": "Tech startup growth programme offering mentoring and scaling support for Danish early-stage companies.",
    "Maritime Stars": "Maritime tech startup programme in Denmark connecting founders with shipping, offshore, and port industry partners for pilots and commercialisation.",
    "Mikrolegat": "Fonden for Entreprenørskab micro-grants for students/recent graduates: up to DKK 60K (higher ed) or DKK 35K (Momentum, vocational). Four deadlines yearly; 25% co-financing if CVR registered.",
    "Miljø- og Energi Fonden": "Private foundation funding Danish environmental and energy innovation projects with grants typically DKK 100K–5M for development and demonstration.",
    "Neighborhood": "Community-driven startup hub in Copenhagen supporting local, impact-oriented founders with workspace, events, and peer network.",
    "Next Women": "Nordic network and platform for female-led startups with events, visibility, and investor connections across the region.",
    "NextGen Innovation and Startup Hub": "Student-led innovation hub supporting young founders with programmes, hackathons, and startup community activities in Denmark.",
    "Nordic Female Founders": "Nordic community connecting female founders with mentors, investors, and cross-border networking opportunities.",
    "Nordic Innovation": "Inter-Nordic organisation funding cross-border innovation projects between Nordic countries. Typical grants €100K–1M for collaborative SME/research partnerships.",
    "Nordic Women's Health Hub": "Nordic hub supporting female-led health startups with mentoring, network access, and sector-specific programmes in women's health.",
    "Nordic Women\u2019s Health Hub": "Nordic hub supporting female-led health startups with mentoring, network access, and sector-specific programmes in women's health.",
    "Nordlys Vækstpulje": "Growth fund for early-stage Nordic startups with grants in the DKK 500K–5M range for scaling and market development.",
    "Odense Robotics Startup Fund": "Odense Robotics cluster support for Danish robotics, automation, and drone startups including mentoring, investor access, and internationalisation via cluster programmes.",
    "ORB": "Student entrepreneurship organisation (Odense/Aarhus region) supporting young founders with events, mentoring, and innovation activities.",
    "Patent og Varemærkestyrelsen": "Danish Patent and Trademark Office subsidies reducing patent and trademark application costs for Danish applicants. Apply when filing IP protection.",
    "PreFlight": "Nordic pre-seed programme helping very early startups validate ideas, build MVPs, and prepare for first funding rounds.",
    "Soundtech": "Audio and music technology incubator/community in Denmark for startups developing sound, music, and media-tech products.",
    "Start Up Factory": "Student entrepreneurship programme supporting Danish university students in launching early-stage ventures.",
    "Startup Lab": "Copenhagen startup community and event series offering networking, pitch opportunities, and ecosystem connections for early-stage founders.",
    "Startup Station": "Student innovation hub providing workspace, workshops, and mentoring for tech-oriented student founders in Denmark.",
    "Station": "Copenhagen student innovation hub (tech/design) with co-working, programmes, and community for young founders.",
    "STEAR": "Danish tech startup support programme offering mentoring and ecosystem access for early-stage founders.",
    "Synapse": "Student health/biotech innovation community connecting Danish students with life science entrepreneurship programmes and mentors.",
    "Tech Nordic": "Nordic tech startup community and support network for early-stage companies seeking cross-border connections and growth resources.",
    "The Circular Lab": "Circular economy incubator supporting Danish startups developing waste reduction, reuse, and sustainable business model innovations.",
    "Time to Raise": "Programme preparing female-led Danish startups for fundraising with investor readiness training, pitch coaching, and network access.",
    "UCN Next Step": "University College Nordjylland entrepreneurship programme for students developing business ideas and early ventures.",
    "Women in Front": "Network for Danish female leaders and entrepreneurs with events, mentorship, and leadership development.",
    "Women in Tech": "Danish community promoting women in technology through events, mentoring, role models, and career support.",
    # Annual events/awards & other rows still missing descriptions
    "Care Tech Challenge": "Annual Danish health-tech innovation challenge connecting startups with healthcare providers for pilot opportunities and visibility.",
    "CPH Townhall": "Copenhagen startup townhall event series with pitches, networking, and ecosystem updates for local founders.",
    "Creative Business Cup": "National creative-industries startup competition with regional rounds and prize-based recognition for Danish creative entrepreneurs.",
    "Danish Entrepreneurship Festival": "National entrepreneurship festival with talks, workshops, and networking for founders at all stages across Denmark.",
    "Digital Tech Summit": "Major Danish tech conference connecting startups, corporates, and investors with programme tracks across digital technologies.",
    "Dineros Iværksetterlegat": "Annual entrepreneur grant (DKK 50K–200K) from Dineros for early-stage Danish founders with promising business ideas.",
    "EY Entrepreneur of the Year": "Prestigious annual award programme recognising outstanding Danish entrepreneurs across categories; visibility and national profile.",
    "Founder Festival": "Danish founder festival with talks, workshops, and community networking for early-stage entrepreneurs.",
    "Global Startup Awards": "International startup awards with Nordic regional rounds celebrating founders across categories and stages.",
    "Green Leap Challenge": "Annual cleantech/sustainability challenge with prize-based support for Danish green startups.",
    "Ignite": "Odense entrepreneurship festival (Ignite Odense) with talks, networking, and award ceremonies for Funen-region startups.",
    "JoinUp North": "Annual Nordic startup gathering connecting founders, investors, and ecosystem players across the region.",
    "Nordic Fintech Week": "Annual fintech conference and networking week for Nordic fintech startups, investors, and financial institutions.",
    "Nordic Innovation Fair": "Fall innovation fair showcasing Nordic startups, research, and cross-border collaboration opportunities.",
    "Nordic Proptech Awards 2026": "Annual awards recognising leading Nordic proptech startups and innovations in real estate technology.",
    "Nordic Women in Tech Awards": "Volunteer-run annual awards gala celebrating female role models in Nordic tech across 11 categories; conference and networking events.",
    "NOVI Legatet": "Annual student innovation grant at NOVI (North Jutland science park) supporting entrepreneurship projects by students.",
    "Novo Nordisk Foundation Fellowship Program Biomedical Design": "Fellowship for Danish PhD students in biomedical design; funding and structured training to translate research into health solutions.",
    "Odense Investor Summit": "Annual investor-startup summit in Odense connecting Funen-region companies with angels, VCs, and corporates.",
    "Odin Award": "Odense startup awards (4 categories: Odin, Tech, Concept, Impact) celebrating scaleups and startups; held during Ignite Odense.",
    "Otto Bruuns Fond": "Annual grants (DKK 50K–500K) for Danish research and innovation projects in technology and social impact.",
    "Otto Mønsteds Fond": "Annual grants (DKK 100K–1M) for Danish non-profits and research institutions in health, research, and culture.",
    "Seedster": "Annual early-stage startup event/competition in Denmark with pitching and ecosystem networking.",
    "SMIL": "Annual media and entertainment startup competition with prizes for Danish creative industry entrepreneurs.",
    "Startup Planet": "Danish startup community event series for networking, inspiration, and founder connections.",
    "Startup Aarhus Townhall": "Aarhus startup townhall events with local founder pitches, ecosystem news, and networking.",
    "StortTech Festival": "Annual Danish deep-tech festival in Copenhagen celebrating science-based startups and research commercialisation.",
    "TechBBQ": "Nordic's major tech conference (September, Copenhagen): investor meetings, side events, and startup showcase.",
    "Velliv Foreningen": "Annual grants (DKK 50K–500K) from Velliv for Danish health, well-being, and social-impact projects.",
    "We Build Denmark": "Construction and built-environment innovation cluster programme; annual activities for cleantech and construction startups.",
}

# Deduped Quick info for rows that already had content (replaces entire field)
MORE_INFO_DEDUPED = {
    "Accelerace": "6-month equity-free programme. Has supported 750+ startups since 2008.",
    "Bio Innovation Institute (BII)": "Programmes: Bio Studio (academic researchers), Venture Lab (incorporated start-ups), BII Quantum Lab. DKK 5.5B Novo Nordisk Foundation funding for 2026–2035.",
    "DSV Group Innovation Partnerships": "In-kind access to DSV's global logistics infrastructure for pilot and partnership projects.",
    "EIC Accelerator": "Grant-only support available once per company under Horizon Europe.",
    "EIC Pathfinder": "2026: Pathfinder Open (12 May), Pathfinder Challenges (28 Oct). Total budget EUR 262M. Success rate ~2.1% (2025).",
    "EIC Transition": "Predecessor project must have been active for at least 18 months before cut-off. Single deadline 16 Sept 2026.",
    "EUDP": (
        "Danish Energy Agency programme for industry-led consortia developing and demonstrating green energy technology "
        "(typically TRL 4–8). Co-financing ~40–60%; typical project size DKK 2–15M. 2025 funding DKK 543M."
    ),
    "Eurostars": "Success rate ~25–30%. IFD funds Danish participants up to EUR 500K if multiple Danish partners.",
    "Global Entrepreneurship Programme (GEP)": "4–6 week in-market immersion periods. Operated with EIFO and Trade Council of Denmark.",
    "IFD Grand Solutions": "Co-financing: SMEs 35–75%, large companies 25–65%, research institutions up to 90% + overhead. Must address significant societal challenges. Theme-based calls: March open call, June.",
    "IFD Innobooster": "Eligible costs: salaries, external knowledge providers, equipment, materials. Excluded: operational optimisation, rent, transport, sales/marketing. Often used after Innofounder.",
    "IFD Innoexplorer": "Assessment: novelty/commercial potential, qualifications, feasibility. UCPH runs internal EoI via Lighthouse panel before full application.",
    "IFD Innofounder": "Non-EU/EEA applicants need Start-up Denmark visa or 1+ year in Denmark. Grant is personal income for tax. CVR required before project start.",
    "LEO Innovation Lab": "Access to LEO Pharma labs and patient registries.",
    "Lundbeck Frontier": "Focus: psychiatry, neurodegeneration, CNS drug discovery. Preserves publication rights and university IP ownership.",
    "MUDP": (
        "Ministry of Environment programme co-funding development, test, and demonstration of environmental technology "
        "(pre-projects, ETV, dev/demo, and flagship projects). Typical grants DKK 1–4M with ~50% co-financing. "
        "2025 allocation DKK 135M."
    ),
    "NNF Distinguished Innovator Grant": "Must act as innovation ambassador within academia. Duration 3 years.",
    "NNF Pioneer Innovator Grant": "Themes: cardiometabolic/infectious diseases, agriculture, food, industrial/environmental biotech, carbon capture, quantum tech. Combined annual budget DKK 190M. Grant to institution, not individual.",
    "Novo Nordisk External Research and Open Innovation": "Option-to-licence deals may include upfront + milestone payments.",
    "Open Discovery Innovation Network (ODIN)": "Results openly shared, not patented. DKK 54.5M pilot + DKK 14M from Lundbeck Foundation.",
    "Open Entrepreneur (Åben Iværksætter)": "Allows up to 2 years leave with right to return. Combinable with Innofounder and Innobooster.",
    "SPARK Denmark": "2×12-month structured mentoring; funds proof-of-concept studies, consultants, and prototyping only.",
    "Spin-outs Denmark": "Applications require department endorsement, written application, and oral pitch. 82 grants awarded.",
    "Symbion / Copenhagen Science City": "Symbion BioHub offers wet lab space at subsidised rates.",
    "The Gate": "Lighter-touch postdoc entrepreneur network; complementary to Spin-outs Denmark.",
    "UCPH Proof of Concept Fund (POC MAX)": "Duration 12–18 months; funds must be spent within project period.",
    "UCPH Proof of Concept Fund (POC-TO-GO)": "Supported activities: prototype development, IP assessment, market validation, feasibility studies.",
    "Villum Foundation and VELUX Group": "VELUX contribution qualifies as co-financing for Innobooster or EUDP.",
}

# Criteria tweaks to remove redundancy with fixed More info (optional light touch)
CRITERIA_UPDATES = {
    "Odin Award": "DK-based startups and scaleups (Odense/Fyn ecosystem)",
    "Beta Health": "Hospital-employed clinicians/researchers; Danish public hospitals",
    "Beyond Beta": "DK-based startups; CVR max 7 years; MVP or customers",
}


def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\sæøåäöü€]", "", text)
    return text


def dedupe_more_info(row: dict) -> str:
    """Remove sentences from Quick info that repeat other columns."""
    more = row.get("Quick info", "").strip()
    if not more:
        return more

    other_parts = [
        row.get("Criteria", ""),
        row.get("Stage", ""),
        row.get("Geography", ""),
        row.get("Funding Amount", ""),
        row.get("Deadline", ""),
        row.get("Industrial segment", ""),
    ]
    other_norm = normalize(" ".join(other_parts))

    sentences = re.split(r"(?<=[.!?])\s+", more)
    kept = []
    for sent in sentences:
        s = sent.strip()
        if not s:
            continue
        sn = normalize(s)
        # drop if sentence is largely contained in other columns
        words = [w for w in sn.split() if len(w) > 3]
        if words:
            overlap = sum(1 for w in words if w in other_norm) / len(words)
            if overlap > 0.65 and len(sn) < len(other_norm) * 0.8:
                continue
        # drop if sentence starts with same phrase as criteria
        crit = normalize(row.get("Criteria", ""))
        if crit and len(crit) > 15 and sn.startswith(crit[: min(40, len(crit))]):
            continue
        kept.append(s)

    return " ".join(kept).strip()


def infer_innovation_stage(row: dict) -> str:
    """
    Map each fund to an innovation journey stage.

    Rough buckets:
    - Exploratory innovation (pre-proof-of-concept)
    - PoC (proof-of-concept / validation)
    - Early venture (company building, pre-seed/seed)
    - Growth/scale (post-seed, scale-up)
    - All stages / Other when it really spans everything
    """
    name = row.get("Name", "")
    stage_text = row.get("Stage", "") or ""
    crit = row.get("Criteria", "") or ""
    combined = " ".join([name, stage_text, crit]).lower()

    # Strong name-based signals first
    if any(k in combined for k in ["poc ", " proof of concept", "proof-of-concept", "innoexplorer"]):
        return "PoC"
    if "innobooster" in combined:
        return "Growth/scale"
    if any(k in combined for k in ["pre-cvr", "pioneer innovator", "distinguished innovator", "frontier", "pathfinder"]):
        return "Exploratory innovation"

    # Generic stage-based mapping
    st = stage_text.lower()
    if "pre-seed" in st:
        return "PoC"
    if "growth-stage" in st or "growth" in st:
        return "Growth/scale"
    if "early-stage" in st:
        return "Early venture"
    if "all" in st:
        return "All stages"

    return ""


def infer_cvr_flags(row: dict) -> tuple[str, str]:
    """
    Infer whether a CVR number is required at application / at programme start.

    Returns (at_application, at_start) with values: Yes, No, Any
    """
    name = row.get("Name", "")
    text = (row.get("Criteria", "") + " " + row.get("Quick info", "")).lower()

    # Explicit pre-CVR instruments
    if "pre-cvr" in text:
        return "No", "No"

    # Can apply without CVR, but must have before start (e.g. Innofounder)
    if "apply without a cvr" in text or "can apply without a cvr" in text:
        return "Any", "Yes"

    # CVR explicitly required
    if "cvr number required" in text or "must have cvr" in text or "skal have cvr" in text:
        return "Yes", "Yes"

    return "Any", "Any"


def main():
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    # Ensure new governance columns exist
    if "Innovation stage" not in fieldnames:
        fieldnames.append("Innovation stage")
    if "CVR at application" not in fieldnames:
        fieldnames.append("CVR at application")
    if "CVR at programme start" not in fieldnames:
        fieldnames.append("CVR at programme start")

    for row in rows:
        name = row["Name"]

        if name in OPPORTUNITY_TYPE_UPDATES:
            row[fieldnames[0]] = OPPORTUNITY_TYPE_UPDATES[name]

        if name in NAME_LINK_UPDATES:
            for k, v in NAME_LINK_UPDATES[name].items():
                row[k] = v

        if name in DEADLINE_UPDATES:
            row["Deadline"] = DEADLINE_UPDATES[name]

        if name in CRITERIA_UPDATES:
            row["Criteria"] = CRITERIA_UPDATES[name]

        more = row.get("Quick info", "").strip()

        if name in MORE_INFO_DEDUPED:
            row["Quick info"] = MORE_INFO_DEDUPED[name]
        elif not more:
            fill = MORE_INFO_FILLS.get(name)
            if not fill:
                # fallback for encoding mismatches on special characters
                for k, v in MORE_INFO_FILLS.items():
                    if normalize(k) == normalize(name):
                        fill = v
                        break
            if fill:
                row["Quick info"] = fill
        elif more:
            row["Quick info"] = dedupe_more_info(row)

        # Final pass: dedupe filled rows against criteria/other columns
        if row["Name"] not in MORE_INFO_DEDUPED and row.get("Quick info", "").strip():
            row["Quick info"] = dedupe_more_info(row)

        # Innovation journey stage
        row["Innovation stage"] = infer_innovation_stage(row)

        # CVR governance flags
        cvr_app, cvr_start = infer_cvr_flags(row)
        row["CVR at application"] = cvr_app
        row["CVR at programme start"] = cvr_start

    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    filled = sum(1 for r in rows if r["Name"] in MORE_INFO_FILLS)
    deduped = sum(1 for r in rows if r["Name"] in MORE_INFO_DEDUPED)
    type_changes = sum(1 for r in rows if r["Name"] in OPPORTUNITY_TYPE_UPDATES)
    still_empty = [r["Name"] for r in rows if not r.get("Quick info", "").strip()]
    print(f"Updated {len(rows)} rows")
    print(f"Filled Quick info: {filled}")
    print(f"Rewrote deduped Quick info: {deduped}")
    print(f"Opportunity type changes: {type_changes}")
    if still_empty:
        print(f"Still empty ({len(still_empty)}): {still_empty}")
    else:
        print("All rows now have Quick info")


if __name__ == "__main__":
    main()
