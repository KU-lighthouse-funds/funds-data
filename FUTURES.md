# Futures list — UCPH Lighthouse funding overview

Tracked ideas and follow-ups that are **not** in scope right now.  
Revisit when there is a clear user need or measured problem — not for speculative polish.

Last updated: 2026-09-06

---

## Site — performance (deferred on purpose)

These were considered during the Aug 2025 load work and **left undone** because the cost outweighed the gain after hero priority + asset shrinking (~190 KB → ~90 KB first load).

| Item | Why deferred | Revisit if… |
|------|----------------|-------------|
| **`<picture>` fallback for WebP logos** | Logos are ~4 KB total; failure mode on old browsers is graceful (alt text). Dual assets add maintenance for Safari ≤12 / legacy Edge. | Analytics show meaningful traffic on pre-WebP browsers. |
| **Split `programmes.json` into index + detail** | Gzipped JSON is ~22 KB; cached after first visit. Splitting adds a fetch on every row expand (main interaction). | Programme count grows substantially (e.g. 300+) or expand payload becomes heavy. |
| **Service worker / offline cache** | GitHub Pages static site; browser cache + `localStorage` already cover repeat visits. | Offline use becomes a requirement. |
| **Remove Open Sans preload** | Font is ~29 KB (trimmed axis); `font-display: swap` already avoids blocking text. | Repeat measurements show font still wins the network race on slow connections. |

**Rule of thumb:** if the site feels slow again, **measure first** (Network tab, resource priority). The Aug fix was fetch priority, not byte-shaving.

---

## Site — annual funding wheel (explored, not pursued)

A circular **annual planning wheel** (funds + events on concentric tracks / month wedges) was prototyped locally in HTML several times in Sep 2026 and **removed**. Not shipped to the live site.

| Outcome | Notes |
|---------|--------|
| **Deferred / unlikely to retry** | User preference: do not pursue this format. |
| **Why it failed** | Full catalogue density (especially Mar/Sep) does not fit readable in-box labels on a static circle without a sidebar, legend, or heavy merging. Multiple layout approaches were tried (per-programme tracks, month wedges, quarter arcs, ~8-box planning poster). |
| **If ever revisited** | Only with a **narrow scope** (headline windows only, not full CSV), or a **different medium** (designed slide/Illustrator asset), or explicit acceptance of a companion list — not another open-ended HTML wheel iteration. |

Local prototype file `annual-wheel.html` was deleted; nothing was committed to `funds-overview`.

---

## Data — content & filters

| Item | Notes |
|------|--------|
| **IFD Grand Solutions stage tag** | Tagged `All stages`, so it appears in early-stage searches even though it requires CVR. Consider retagging to `Venture formation` / `Growth/scale` if that better matches eligibility. |
| **Audit “All stages” programmes** | Same pattern may affect other rows — worth a pass if stage filter accuracy is reported as confusing. |
| **Link audit follow-ups** | See `link_check_incidents.md` for dead/wrong URLs not yet resolved in v4 CSV. |
| **Re-run `audit_stages.py` after CSV edits** | Then `python funds-overview-site/sync_data.py` and commit both repos. |

---

## Done recently (for context)

- Stale-while-revalidate programme cache (`shared.js`)
- Hero/logo/font payload reduction; data preloaded above decoration
- Logos → palette-reduced WebP; font weight axis trimmed to 400–700
- Multi-stage tags + default sort (UCPH-supported first)
- Mobile results card layout
