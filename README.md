# KU Lighthouse — Funding data

Source dataset and helpers for the public funds overview site.

| What | Where | Git |
|------|--------|-----|
| Programme CSV (source of truth) | `funds with KU support - v4.csv` | **this repo** |
| Active helpers | `scripts/` | **this repo** |
| User inputs & older versions | `old data/` | archive locally; large/scratch files gitignored |
| Public website | `funds-overview-site/` | [**funds-overview**](https://github.com/KU-lighthouse-funds/funds-overview) (separate repo) |

## Layout

```
Funds/
  funds with KU support - v4.csv   ← edit this
  funds with KU support - v4.xlsx
  README.md
  FUTURES.md
  sync_and_publish.ps1
  scripts/                         ← build / audit / one-off tools
  old data/                        ← decks, PDFs, Word comments, v1–v3, extracts
  funds-overview-site/             ← separate git repo (site)
```

## Day-to-day workflow

1. Edit **`funds with KU support - v4.csv`**
2. Optional: `python scripts/dedupe_copy.py`
3. Sync the site JSON:
   ```powershell
   cd funds-overview-site
   python sync_data.py
   ```
   Or from repo root: `.\sync_and_publish.ps1`
4. Commit **this repo** (CSV).
5. Commit **site repo** (`data/programmes.json`), then push for live Pages.

## Futures / backlog

See **[FUTURES.md](FUTURES.md)** for deferred items.
