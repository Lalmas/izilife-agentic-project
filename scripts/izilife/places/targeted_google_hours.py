#!/usr/bin/env python3
"""Collecte ciblée Google Maps pour une liste explicite de fiches iziLife."""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright
import requests

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from google_hours_agent import scrape


def api_lookup(scope_ref: str) -> dict:
    token = (os.getenv("IZILIFE_AGENT_TOKEN") or os.getenv("AGENT_SECRET_TOKEN") or "").strip()
    response = requests.post(
        "https://www.izilife.co/izilife-admin/scraper/agentInternalDataV0Lookup",
        headers={"X-Agent-Token": token, "Accept": "application/json"},
        json={"items": [{"type": "SHOP", "string_id": scope_ref}], "view": "full", "media_page_size": 1},
        timeout=60,
    )
    body = response.json()
    if response.status_code >= 400 or body.get("success") is False:
        raise RuntimeError(body.get("error") or f"HTTP {response.status_code}")
    result = (body.get("items") or [None])[0]
    if not isinstance(result, dict) or result.get("status") != "found":
        raise RuntimeError(f"SHOP {scope_ref} absent de production")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref", action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    journal = {"generated_at": datetime.now().isoformat(), "items": []}
    with sync_playwright() as pw:
        # Google Maps ne doit pas être interrogé en headless : l'interface et
        # le panneau d'horaires diffèrent, ce qui a produit de faux 1/7.
        browser = pw.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(locale="fr-FR", timezone_id="Europe/Paris")
        page = context.new_page()
        for ref in args.ref:
            entry = {"scope_type": "SHOP", "scope_ref": ref}
            try:
                current = api_lookup(ref)
                data = current.get("data") or {}
                item = {
                    "scope_type": "SHOP",
                    "scope_ref": ref,
                    "name": data.get("name"),
                    "address": data.get("address"),
                    "zip_code": data.get("zip_code"),
                    "city_name": (data.get("city_ref") or "").replace("-", " "),
                    "google_place_id": data.get("google_place_id"),
                }
                entry["name"] = item["name"]
                entry["collected"] = scrape(page, item)
            except Exception as exc:
                entry["error"] = str(exc)
            journal["items"].append(entry)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(journal, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[{len(journal['items'])}/{len(args.ref)}] {ref}: {'ERROR' if 'error' in entry else 'OK'}", flush=True)
        browser.close()
    return 2 if any("error" in item for item in journal["items"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
