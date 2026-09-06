# Link check incidents — funds table
Checked: `updated file without VC - cleaned.csv` (116 links)
Date: 2026-08-04

No CSV changes made. Suggested replacements below are for your decision only.

---

## A. Wrong destination (high priority)
These load a real page, but **not** the programme we list.

| Name | Current link | Problem | Candidate (if you want to update) |
|------|--------------|---------|-----------------------------------|
| Creative Business Cup | https://cbc.dk | B2B marketing agency CBC, not the award | https://creativebusinesscup.com/ or https://www.cbnet.com/creative-business-cup |
| Dineros Iværksetterlegat | https://dineros.dk | Wrong domain; lands on Dinero accounting product site | https://dinero.dk/ivaerksaetterlegat/ |
| Hub for Innovation in Tourism | https://visitdenmark.com | VisitDenmark tourism marketing site | https://innohub.dk/ |
| Cancute | https://canute.io/ | Link works for **Canute** scale/advisory; table name spells **Cancute** | Keep link if entry = Canute; rename to Canute. Or delete if wrong programme |

---

## B. Dead domains (DNS does not resolve)
These hostnames do not resolve today. Programme may still exist elsewhere, or entry may be outdated.

| Name | Current link | Notes / possible home |
|------|--------------|------------------------|
| Green Leap Challenge | https://greenleap.dk | Run by Food & Bio Cluster (news pages exist); no dedicated greenleap.dk |
| Nordic Women in Tech Awards | https://nordicwomenintech.com | |
| Odin Award | https://odin-award.dk | Active on LinkedIn / Ignite Odense; no working .dk found |
| CPH Townhall | https://cph-townhall.dk | |
| Danish Entrepreneurship Festival | https://entrepreneurshipfestival.dk | |
| Founder Festival | https://founderfestival.dk | |
| Odense Investor Summit | https://odenseinvestorsummit.dk | |
| SMIL | https://smil.dk | Likely https://www.startupaarhus.com/smil-aarhus |
| StortTech Festival | https://storttech.dk | |
| Diversity Commitment | https://diversitycommitment.dk | |
| Nordic Women’s Health Hub | https://nordicwomenshealthhub.com | |
| Time to Raise | https://timetoraise.dk | |
| Care Tech Challenge | https://caretechchallenge.dk | |
| Ideas Lab | https://ideaslab.dk | Filmby Aarhus page mentions Ideas Lab; no ideaslab.dk |
| The Circular Lab | https://thecircularlab.dk | |
| Mikrolegat | https://mikrolegat.dk | Likely https://mikrolegat.ffefonden.dk/ |
| Nordlys Vækstpulje | https://nordlysvaekst.dk | |
| Otto Mønsteds Fond | https://otto-moensteds-fond.dk | Likely https://omfonden.dk/ |
| Copenhagen Health Innovators | https://copenhagenhealthinnovators.dk | |
| Fonden for Entreprenørskab | https://fondenforentreprenorskab.dk | Likely https://ffefonden.dk/ |
| NextGen Innovation and Startup Hub | https://nextgeninnovation.dk | |
| Start Up Factory | https://startupfactory.dk | |

---

## C. Unreachable / broken (domain may exist, site fails)
| Name | Current link | Issue |
|------|--------------|-------|
| Ignite | https://ignite.dk | Connection timeout |
| Startup Aarhus Townhall | https://startupaarhus.dk | Connection refused (Startup Aarhus may be startupaarhus.com) |
| Startup Lab | https://startuplab.dk | Connection reset |
| Maritime Stars | https://maritimestars.dk | Timeout |
| Neighborhood | https://neighborhood.dk | HTTP 503 |
| Next Women | https://nextwomen.com | HTTP 403 (may be bot-block) |
| PreFlight | https://preflight.io | HTTP 403 (may be bot-block) |
| Horizon Europe | https://ec.europa.eu/info/funding-tenders | HTTP 403 (may be bot-block) |
| Intech Founders | https://intechfounders.com | SSL certificate hostname mismatch |
| Nordic Female Founders | https://nordicfemalefounders.com | SSL certificate hostname mismatch |
| Soundtech | https://soundtech.dk | SSL certificate hostname mismatch |
| Tech Nordic | https://technordic.com | SSL certificate hostname mismatch |
| Synapse | https://synapse.dk | SSL certificate hostname mismatch |

---

## D. Works, but too generic / indirect
Homepage only, or third-party page — not the specific programme landing page.

| Name | Current link | Better target if you want specificity |
|------|--------------|----------------------------------------|
| EY Entrepreneur of the Year | https://ey.com/dk | https://www.ey.com/da_dk/entrepreneur-of-the-year |
| Climate-KIC Urban Mobility Food | https://climate-kic.org | Need programme-specific page |
| DIF Innovation Lab | https://dif.dk | Need Innovation Lab subpage |
| Lundbeck Frontier | https://www.lundbeck.com/ | Need Frontier programme page |
| DSV Group Innovation Partnerships | https://dsv.com/ | Need partnerships page |
| EIC Transition | https://catalyze-group.com/fund/eic-transition/ | Prefer official EIC page |
| Novo Nordisk External Research and Open Innovation | https://www.novonordisk.com/ | Need open innovation page |
| Novo Nordisk Foundation Fellowship Program Biomedical Design | https://novonordiskfonden.dk | Need fellowship grant page |
| ITU Business Development | https://itu.dk | Need BD/entrepreneurship page |
| UCN Next Step | https://ucn.dk | Need Next Step page |
| Velliv Foreningen | https://velliv.dk | Confirm grants vs insurer brand |
| Patent og Varemærkestyrelsen | https://dkpto.dk | Agency home (related; optional deepen) |

---

## E. Looks fine (no action needed for this pass)
~63–80 links returned a live page whose title/content matched the programme well enough (BII, IFD programmes, spinouts.dk, TechBBQ, Beyond Beta, etc.).

---

## Suggested next step
Tell me which buckets to act on, e.g.:
1. Fix only **A** (wrong destination) with the candidates above  
2. Fix **A + clear B candidates** (Mikrolegat, Fonden, Otto Mønsted, SMIL, HIT, Dinero, CBC)  
3. **Delete** specific dead rows you no longer want  
4. Leave **C/D** for you to hunt manually first
