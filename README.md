# KU Lighthouse — Funding data & build

This folder holds the **source dataset** and scripts that feed the public site.

| What | Where | Git |
|------|--------|-----|
| Programme CSV (source of truth) | `funds with KU support - v4.csv` | **this repo** |
| Build / clean scripts | `build_funds_v4.py`, `dedupe_copy.py` | **this repo** |
| Public website | `funds-overview-site/` | [**funds-overview**](https://github.com/KU-lighthouse-funds/funds-overview) (separate repo) |

## Why two repos?

- **This repo** — change management for the spreadsheet data and how it is built. Who changed which programme, when, and why.
- **Site repo** — HTML/CSS/JS and the generated `programmes.json` that GitHub Pages serves.

Both should be committed when you publish an update.

## Day-to-day workflow

1. Edit **`funds with KU support - v4.csv`** (or run `build_funds_v4.py` if you are applying structured updates).
2. Optional: remove duplicate sentences — `python dedupe_copy.py`
3. Push data to the site:
   ```powershell
   cd funds-overview-site
   python sync_data.py
   ```
4. Commit **this repo** (CSV + scripts).
5. Commit **site repo** (`data/programmes.json` and any UI changes), then push — that updates the live site.

## Reference files (local, not in git)

- `KU LH preaward funding support-AZ-JSJ.pptx` — programme source deck
- `brand directions.pptx` — KU INNO design guide
- Older `v1`–`v3` CSV/XLSX — kept on disk only unless you choose to archive them
