"""Check all programme links in the cleaned funds CSV."""
from __future__ import annotations

import csv
import json
import re
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path

CSV_PATH = Path(r"c:\Users\Kaja\Documents\Funds\updated file without VC - cleaned.csv")
OUT_PATH = Path(r"c:\Users\Kaja\Documents\Funds\link_check_results.json")

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

CTX = ssl.create_default_context()


def fetch(url: str, method: str = "GET", timeout: int = 20) -> dict:
    req = urllib.request.Request(
        url,
        method=method,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,da;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
            final = resp.geturl()
            status = resp.status
            raw = resp.read(120_000)
            ctype = resp.headers.get("Content-Type", "")
            text = ""
            if "html" in ctype.lower() or not ctype:
                try:
                    text = raw.decode("utf-8", errors="ignore")
                except Exception:
                    text = raw.decode("latin-1", errors="ignore")
            title = ""
            m = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
            if m:
                title = re.sub(r"\s+", " ", m.group(1)).strip()
            # crude body snippet without scripts/styles
            body = re.sub(r"<script[^>]*>.*?</script>", " ", text, flags=re.I | re.S)
            body = re.sub(r"<style[^>]*>.*?</style>", " ", body, flags=re.I | re.S)
            body = re.sub(r"<[^>]+>", " ", body)
            body = re.sub(r"\s+", " ", body).strip()[:800]
            return {
                "ok": True,
                "status": status,
                "final_url": final,
                "title": title,
                "snippet": body,
                "error": None,
            }
    except urllib.error.HTTPError as e:
        return {
            "ok": False,
            "status": e.code,
            "final_url": getattr(e, "url", url) or url,
            "title": "",
            "snippet": "",
            "error": f"HTTPError {e.code}: {e.reason}",
        }
    except Exception as e:
        return {
            "ok": False,
            "status": None,
            "final_url": url,
            "title": "",
            "snippet": "",
            "error": f"{type(e).__name__}: {e}",
        }


def name_tokens(name: str) -> list[str]:
    # Keep meaningful tokens for soft match against title/snippet
    stop = {
        "the", "and", "of", "for", "a", "an", "to", "in", "at", "on", "by",
        "fund", "foundation", "lab", "labs", "programme", "program", "grant",
        "grants", "award", "denmark", "danish", "ucph", "ifd", "nnf",
    }
    raw = re.findall(r"[A-Za-z0-9æøåÆØÅ&+-]+", name.lower())
    toks = [t for t in raw if len(t) > 2 and t not in stop]
    return toks


def soft_match(name: str, title: str, snippet: str, final_url: str) -> str:
    blob = f"{title} {snippet} {final_url}".lower()
    toks = name_tokens(name)
    if not toks:
        return "unknown"
    hits = sum(1 for t in toks if t in blob)
    ratio = hits / len(toks)
    if ratio >= 0.45:
        return "likely_match"
    if hits >= 1 and ratio >= 0.25:
        return "weak_match"
    return "mismatch_or_unclear"


def main() -> None:
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter=";"))

    results = []
    for i, row in enumerate(rows, 1):
        name = (row.get("Name") or "").strip()
        url = (row.get("Link") or "").strip()
        print(f"[{i}/{len(rows)}] {name} -> {url}", flush=True)
        if not url:
            results.append(
                {
                    "index": i,
                    "name": name,
                    "url": url,
                    "ok": False,
                    "status": None,
                    "final_url": "",
                    "title": "",
                    "snippet": "",
                    "error": "missing_url",
                    "match": "missing",
                }
            )
            continue

        info = fetch(url)
        # Some sites block GET with 403/405 on urllib; retry HEAD then GET once
        if not info["ok"] and info.get("status") in {403, 405, 429}:
            time.sleep(0.4)
            info = fetch(url)
        match = "unreachable"
        if info["ok"] or (info.get("status") and info["status"] < 500):
            # even 403 pages may still be the right host; mark carefully
            if info["ok"]:
                match = soft_match(name, info["title"], info["snippet"], info["final_url"])
            else:
                match = "http_error"
        results.append(
            {
                "index": i,
                "name": name,
                "url": url,
                "ok": info["ok"],
                "status": info["status"],
                "final_url": info["final_url"],
                "title": info["title"],
                "snippet": info["snippet"][:400],
                "error": info["error"],
                "match": match,
            }
        )
        time.sleep(0.25)

    OUT_PATH.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    bad = [r for r in results if (not r["ok"]) or r["match"] in {"mismatch_or_unclear", "http_error", "missing", "unreachable"}]
    print("\n=== SUMMARY ===")
    print(f"Total: {len(results)}")
    print(f"OK HTTP: {sum(1 for r in results if r['ok'])}")
    print(f"Needs review: {len(bad)}")
    print("\nNeeds review:")
    for r in bad:
        print(
            f"- {r['name']} | {r['url']} | status={r['status']} | match={r['match']} | err={r['error']} | title={r['title'][:80]}"
        )


if __name__ == "__main__":
    main()
