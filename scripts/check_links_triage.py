"""Second-pass link triage: classify dead vs wrong-destination vs generic."""
from __future__ import annotations

import json
import socket
import ssl
import subprocess
import time
from pathlib import Path
from urllib.parse import urlparse

IN = Path(r"c:\Users\Kaja\Documents\Funds\link_check_results.json")
OUT = Path(r"c:\Users\Kaja\Documents\Funds\link_check_triage.json")

KNOWN_WRONG = {
    "Creative Business Cup": "cbc.dk is a B2B marketing agency, not Creative Business Cup",
    "Dineros Iværksetterlegat": "dineros.dk resolves to Dinero accounting software (wrong programme)",
    "Hub for Innovation in Tourism": "visitdenmark.com is national tourism marketing, not the HIT programme page",
    "Cancute": "URL is canute.io (different spelling); page is Canute scale programme — confirm whether this is the intended entry",
}

GENERIC_BUT_RELATED = {
    "EY Entrepreneur of the Year": "ey.com/dk is EY Denmark homepage, not Entrepreneur of the Year page",
    "Climate-KIC Urban Mobility Food": "climate-kic.org is org homepage, not specific Urban Mobility/Food programme",
    "DIF Innovation Lab": "dif.dk is Danish Sports Confederation homepage, not Innovation Lab page",
    "ITU Business Development": "itu.dk is ITU homepage, not Business Development page",
    "Novo Nordisk Foundation Fellowship Program Biomedical Design": "novonordiskfonden.dk homepage, not fellowship programme page",
    "Novo Nordisk External Research and Open Innovation": "novonordisk.com homepage, not open innovation programme page",
    "Lundbeck Frontier": "lundbeck.com homepage, not Frontier programme page",
    "DSV Group Innovation Partnerships": "dsv.com homepage, not innovation partnerships page",
    "Horizon Europe": "generic EU funding portal (or blocked); not Horizon Europe programme landing",
    "Velliv Foreningen": "velliv.dk may be insurer brand site rather than association grants page",
    "Patent og Varemærkestyrelsen": "dkpto.dk is agency homepage (related but generic)",
    "UCN Next Step": "ucn.dk homepage, not Next Step page",
    "EIC Transition": "points to Catalyze Group intermediary page, not official EIC Transition page",
}


def dns_ok(host: str) -> bool:
    try:
        socket.getaddrinfo(host, 443)
        return True
    except Exception:
        return False


def curl_check(url: str) -> dict:
    try:
        proc = subprocess.run(
            [
                "curl",
                "-sS",
                "-L",
                "-o",
                "NUL",
                "-w",
                "%{http_code}|%{url_effective}|%{ssl_verify_result}",
                "--max-time",
                "25",
                "-A",
                "Mozilla/5.0",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=40,
        )
        out = (proc.stdout or "").strip()
        parts = out.split("|")
        code = parts[0] if parts else ""
        final = parts[1] if len(parts) > 1 else ""
        return {
            "curl_code": code,
            "curl_final": final,
            "curl_err": (proc.stderr or "").strip()[:300],
            "curl_ok": code.isdigit() and 200 <= int(code) < 400,
        }
    except Exception as e:
        return {"curl_code": None, "curl_final": "", "curl_err": str(e), "curl_ok": False}


def main() -> None:
    rows = json.loads(IN.read_text(encoding="utf-8"))
    triage = []
    for r in rows:
        name = r["name"]
        url = r["url"]
        host = urlparse(url).hostname or ""
        item = {
            "index": r["index"],
            "name": name,
            "url": url,
            "first_ok": r["ok"],
            "first_status": r["status"],
            "first_title": r.get("title") or "",
            "first_match": r.get("match"),
            "first_error": r.get("error"),
            "dns_ok": dns_ok(host) if host else False,
        }

        # Re-check anything that failed or looks wrong
        needs = (
            (not r["ok"])
            or r.get("match") in {"mismatch_or_unclear", "http_error", "unreachable", "weak_match"}
            or name in KNOWN_WRONG
            or name in GENERIC_BUT_RELATED
        )
        if needs:
            print(f"recheck {name}", flush=True)
            c = curl_check(url)
            item.update(c)
            time.sleep(0.15)
        else:
            item.update({"curl_code": None, "curl_final": "", "curl_err": "", "curl_ok": None})

        if name in KNOWN_WRONG:
            item["category"] = "WRONG_DESTINATION"
            item["note"] = KNOWN_WRONG[name]
        elif name in GENERIC_BUT_RELATED and (item.get("curl_ok") or r["ok"]):
            item["category"] = "GENERIC_OR_INDIRECT"
            item["note"] = GENERIC_BUT_RELATED[name]
        elif not item["dns_ok"]:
            item["category"] = "DEAD_DNS"
            item["note"] = "Domain does not resolve"
        elif item.get("curl_ok") is False and not r["ok"]:
            item["category"] = "UNREACHABLE"
            item["note"] = item.get("curl_err") or r.get("error") or "unreachable"
        elif r.get("match") == "mismatch_or_unclear":
            item["category"] = "POSSIBLE_MISMATCH"
            item["note"] = f"title={r.get('title')}"
        else:
            item["category"] = "OK" if (r["ok"] or item.get("curl_ok")) else "REVIEW"
            item["note"] = ""

        triage.append(item)

    OUT.write_text(json.dumps(triage, ensure_ascii=False, indent=2), encoding="utf-8")

    from collections import Counter
    print("categories", Counter(t["category"] for t in triage))
    print("\nINCIDENTS:")
    for cat in ["WRONG_DESTINATION", "DEAD_DNS", "UNREACHABLE", "GENERIC_OR_INDIRECT", "POSSIBLE_MISMATCH", "REVIEW"]:
        items = [t for t in triage if t["category"] == cat]
        if not items:
            continue
        print(f"\n## {cat} ({len(items)})")
        for t in items:
            print(f"- {t['name']} | {t['url']} | {t['note']}")


if __name__ == "__main__":
    main()
