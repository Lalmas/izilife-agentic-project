#!/usr/bin/env python3
"""Complète les horaires manquants depuis Google Maps.

Le mode par défaut collecte et produit un rapport sans écrire. `--apply` écrit les
horaires et applique uniquement les fermetures explicitement affichées par Google.
Un dry-run effectue donc bien des navigations externes Google Maps.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import time
import unicodedata
from difflib import SequenceMatcher
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
import urllib3
from playwright.sync_api import sync_playwright

ENVS = {
    "local": {"base_url": "https://localhost:4443/izilife-admin", "verify": False},
    "staging": {"base_url": "https://www.staging.izilife.co/izilife-admin", "verify": True},
    "prod": {"base_url": "https://www.izilife.co/izilife-admin", "verify": True},
}
DAY_IDS = {"lundi": 1, "mardi": 2, "mercredi": 3, "jeudi": 4, "vendredi": 5, "samedi": 6, "dimanche": 7}
CLOSED_MARKERS = ("fermé", "closed")
PERMANENT_MARKERS = ("fermé définitivement", "permanently closed", "définitivement fermé")
TEMPORARY_MARKERS = ("fermé temporairement", "temporarily closed", "temporairement fermé")


class Api:
    def __init__(self, env: str, token: str, timeout: int):
        self.env, self.cfg, self.timeout = env, ENVS[env], timeout
        self.headers = {"X-Agent-Token": token, "Accept": "application/json"}
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def post(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(self.cfg["base_url"] + endpoint, json=payload, headers=self.headers,
                                 timeout=self.timeout, verify=self.cfg["verify"])
        try: body = response.json()
        except ValueError: body = {"success": False, "error": response.text[:500]}
        if response.status_code >= 400: body.setdefault("error", f"HTTP {response.status_code}")
        return body

    def form(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(self.cfg["base_url"] + endpoint,
                                 data={"payload": json.dumps(payload, ensure_ascii=False)},
                                 headers=self.headers, timeout=self.timeout, verify=self.cfg["verify"])
        try: body = response.json()
        except ValueError: body = {"success": False, "error": response.text[:500]}
        if response.status_code >= 400: body.setdefault("error", f"HTTP {response.status_code}")
        return body


def accept_consent(page) -> None:
    for selector in ('button:has-text("Tout refuser")', 'button:has-text("Reject all")',
                     'button:has-text("Tout accepter")', 'button:has-text("Accept all")'):
        try:
            button = page.locator(selector).first
            if button.is_visible(timeout=800): button.click(); page.wait_for_timeout(1200); return
        except Exception: pass


def normalize_time(value: str) -> str:
    value = value.strip().replace("h", ":").replace("H", ":").replace(".", ":")
    match = re.search(r"\b(\d{1,2})(?::(\d{2}))?\b", value)
    if not match: raise ValueError(f"Heure illisible: {value}")
    hour, minute = int(match.group(1)), int(match.group(2) or 0)
    if hour > 23 or minute > 59: raise ValueError(f"Heure invalide: {value}")
    return f"{hour:02d}:{minute:02d}"


def parse_day_line(line: str) -> dict[str, Any] | None:
    clean = re.sub(r"\s+", " ", line.replace("\u202f", " ").replace("\xa0", " ")).strip()
    clean = re.sub(r"(\d{1,2})\s*[hH]\s*(\d{2})", r"\1:\2", clean)
    lowered = clean.lower()
    day_id = next((value for label, value in DAY_IDS.items() if lowered.startswith(label)), None)
    if not day_id: return None
    if any(marker in lowered for marker in CLOSED_MARKERS):
        return {"day_id": day_id, "closing_day": 1}
    ranges = re.findall(r"(\d{1,2}(?:(?::|h|H|\.)\d{2})?)\s*[–—-]\s*(\d{1,2}(?:(?::|h|H|\.)\d{2})?)", clean)
    if not ranges: return None
    first_open, first_close = map(normalize_time, ranges[0])
    result = {"day_id": day_id, "closing_day": 0, "opening_hour": first_open,
              "closure_hour": first_close, "with_break": 0,
              "is_overnight": int(first_close <= first_open)}
    if len(ranges) > 1:
        result.update({"with_break": 1, "reopening_hour": normalize_time(ranges[1][0]),
                       "reclosure_hour": normalize_time(ranges[1][1])})
    return result


GENERIC_NAME_TOKENS = {
    "le", "la", "les", "de", "du", "des", "a", "au", "aux", "l", "et",
    "cafe", "bar", "restaurant", "shop", "place", "parc", "centre", "lille",
}


def normalize_identity(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode("ascii").lower()
    tokens = re.findall(r"[a-z0-9]+", value)
    # Google peut localiser le même établissement avec un libellé anglais.
    # Normaliser ces synonymes évite de refuser une identité pourtant exacte
    # (ex. « auberge de jeunesse » côté iziLife, « hostel » côté Google).
    normalized: list[str] = []
    index = 0
    while index < len(tokens):
        if tokens[index:index + 3] == ["auberge", "de", "jeunesse"]:
            normalized.append("hostel")
            index += 3
            continue
        normalized.append(tokens[index])
        index += 1
    return " ".join(normalized)


def validate_identity(page, item: dict[str, Any], body_text: str) -> str:
    title = ""
    for selector in ("h1.DUwDvf", "h1", '[role="main"] h1'):
        try:
            candidate = page.locator(selector).first.inner_text(timeout=1200).strip()
            if candidate:
                title = candidate
                break
        except Exception:
            pass
    if not title:
        raise RuntimeError("Identité Google illisible: titre absent")
    expected = normalize_identity(item.get("name", ""))
    actual = normalize_identity(title)
    expected_tokens = {x for x in expected.split() if x not in GENERIC_NAME_TOKENS}
    actual_tokens = {x for x in actual.split() if x not in GENERIC_NAME_TOKENS}
    distinctive_overlap = bool(expected_tokens & actual_tokens)
    distinctive_subset = bool(expected_tokens) and expected_tokens.issubset(actual_tokens)
    ratio = SequenceMatcher(None, expected, actual).ratio()
    contains = min(len(expected), len(actual)) >= 5 and (expected in actual or actual in expected)
    if not distinctive_overlap or (ratio < 0.68 and not contains and not distinctive_subset):
        raise RuntimeError(f"Identité Google refusée: iziLife={item.get('name')} / Google={title}")

    # Pour une recherche sans Place ID, l'adresse ou au minimum la ville doit
    # aussi être visible sur la fiche Google.
    if not item.get("google_place_id"):
        body = normalize_identity(body_text)
        address = normalize_identity(item.get("address", ""))
        city = normalize_identity(item.get("city_name", ""))
        street_number = next(iter(re.findall(r"\b\d{1,4}\b", address)), "")
        address_tokens = {x for x in address.split() if len(x) >= 4}
        address_ok = bool(address_tokens and len(address_tokens & set(body.split())) >= min(2, len(address_tokens)))
        if street_number and street_number not in body.split():
            address_ok = False
        if not address_ok and (not city or city not in body):
            raise RuntimeError(f"Adresse Google non confirmée pour {item.get('scope_ref')}")
    return title


def scrape(page, item: dict[str, Any]) -> dict[str, Any]:
    query = " ".join(filter(None, [item.get("name"), item.get("address"), item.get("zip_code"), item.get("city_name")]))
    url = "https://www.google.com/maps/search/?api=1&query=" + requests.utils.quote(query)
    if item.get("google_place_id"):
        url += "&query_place_id=" + requests.utils.quote(item["google_place_id"])
    page.goto(url, wait_until="domcontentloaded", timeout=45000); accept_consent(page); page.wait_for_timeout(2500)
    text = page.locator("body").inner_text(timeout=15000)
    google_title = validate_identity(page, item, text)
    lowered = text.lower()
    closed_state = "ferme-definitivement" if any(x in lowered for x in PERMANENT_MARKERS) else (
        "ferme-temporairement" if any(x in lowered for x in TEMPORARY_MARKERS) else None)
    for selector in (
        'button:has-text("Voir plus d\'horaires")',
        '[role="button"]:has-text("Voir plus d\'horaires")',
        'button:has-text("More hours")',
        '[role="button"]:has-text("More hours")',
        'div[role="button"][aria-expanded]:has([aria-label*="Horaires" i])',
        'div[role="button"][aria-expanded]:has([aria-label*="Hours" i])',
        '[data-item-id="oh"][role="button"]',
    ):
        try:
            target = page.locator(selector).first
            if target.is_visible(timeout=1200): target.click(); page.wait_for_timeout(900); break
        except Exception: pass
    candidates = []
    for selector in ('table tr', 'tr.y0skZc', '[role="row"]', '[role="dialog"] tr', '[aria-label*="lundi" i]', '[aria-label*="mardi" i]'):
        try: candidates.extend(page.locator(selector).all_inner_texts())
        except Exception: pass
    candidates.extend(page.locator("body").inner_text().splitlines())
    parsed = {}
    for line in candidates:
        day = parse_day_line(line)
        if day: parsed[day["day_id"]] = day
    if parsed and len(parsed) != 7: raise RuntimeError(f"Seulement {len(parsed)}/7 jours interprétés")
    return {"url": page.url, "google_title": google_title, "closed_state_ref": closed_state,
            "days": [parsed[i] for i in range(1, 8)] if len(parsed) == 7 else [],
            "evidence": text[:1200]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Horaires Google Maps pour les fiches iziLife sans horaires")
    parser.add_argument("--env", required=True, choices=ENVS)
    parser.add_argument("--apply", action="store_true", help="Écrit réellement dans iziLife")
    parser.add_argument("--apply-closures", action="store_true", help="Autorise aussi la désactivation explicite des lieux fermés")
    parser.add_argument("--confirm-production")
    parser.add_argument("--max", type=int, default=100)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--scope-type", choices=["PLACE", "SHOP"])
    parser.add_argument("--only-ref")
    parser.add_argument("--targets-file", type=Path,
                        help="JSON contenant intelligent_targets; limite strictement le lot aux scope_type/scope_ref listés.")
    parser.add_argument("--include-without-google", action="store_true")
    parser.add_argument("--output")
    parser.add_argument("--timeout", type=int, default=90)
    args = parser.parse_args()
    token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token: raise RuntimeError("IZILIFE_AGENT_TOKEN manquant.")
    if args.apply and args.env == "prod" and args.confirm_production != "I_CONFIRM_PRODUCTION_HOURS":
        raise RuntimeError("Production refusée sans --confirm-production I_CONFIRM_PRODUCTION_HOURS.")
    api = Api(args.env, token, args.timeout)
    inventory_limit = 10000 if args.targets_file else args.max
    inventory = api.post("/scraper/agentListLocationsWithoutHours", {
        "limit": inventory_limit, "offset": max(0, args.offset), "scope_type": args.scope_type,
        "include_without_google": args.include_without_google,
    })
    if not inventory.get("success"): raise RuntimeError(inventory.get("error") or "Inventaire impossible")
    requested_targets = set()
    if args.targets_file:
        target_payload = json.loads(args.targets_file.read_text(encoding="utf-8"))
        target_rows = target_payload.get("intelligent_targets", target_payload) if isinstance(target_payload, dict) else target_payload
        for target in target_rows or []:
            if isinstance(target, dict) and target.get("scope_ref"):
                requested_targets.add((str(target.get("scope_type") or "").upper(), str(target["scope_ref"])))
    if args.only_ref:
        requested_targets.add((str(args.scope_type or "").upper(), args.only_ref))
    if requested_targets:
        inventory["items"] = [
            item for item in inventory.get("items") or []
            if (str(item.get("scope_type") or "").upper(), str(item.get("scope_ref") or "")) in requested_targets
               or ("", str(item.get("scope_ref") or "")) in requested_targets
        ]
        if not inventory["items"] and args.only_ref:
            raise RuntimeError(f"scope_ref absent du lot demandé: {args.only_ref}")
    journal = {"format": "izilife-google-hours-v1", "env": args.env, "apply": args.apply,
               "created_at": datetime.now().isoformat(), "items": []}
    output = Path(args.output or f"google-hours-{args.env}-{datetime.now():%Y%m%d-%H%M%S}.json").resolve()
    output.write_text(json.dumps(journal, ensure_ascii=False, indent=2), encoding="utf-8")
    with sync_playwright() as pw:
        # Google Maps est volontairement piloté dans Chromium visible. Le mode
        # headless renvoie parfois un DOM différent et des horaires incomplets.
        browser = pw.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(locale="fr-FR", timezone_id="Europe/Paris")
        page = context.new_page()
        for item in inventory.get("items") or []:
            entry = {"scope_type": item["scope_type"], "scope_ref": item["scope_ref"], "name": item["name"]}
            try:
                collected = scrape(page, item); entry["collected"] = collected
                if args.apply and args.apply_closures and collected["closed_state_ref"]:
                    entry["result"] = api.form("/scraper/agentMaintainLocation", {
                        "scope_type": item["scope_type"], "scope_ref": item["scope_ref"],
                        "closed_state_ref": collected["closed_state_ref"],
                        "is_active": "0", "listable": "0",
                    })
                elif args.apply and collected["days"]:
                    entry["result"] = api.post("/scraper/agentApplyGoogleHours", {
                        "scope_type": item["scope_type"], "scope_ref": item["scope_ref"], "days": collected["days"]})
                else: entry["result"] = {
                    "dry_run": not args.apply,
                    "action": "REVIEW_CLOSURE" if collected["closed_state_ref"] else "ADD_HOURS" if collected["days"] else "REVIEW",
                }
            except Exception as exc: entry["error"] = str(exc)
            journal["items"].append(entry)
            output.write_text(json.dumps(journal, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[{len(journal['items'])}/{len(inventory.get('items') or [])}] {entry['scope_type']} {entry['scope_ref']}", flush=True)
            time.sleep(random.uniform(8.0, 15.0))
        browser.close()
    output.write_text(json.dumps(journal, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Rapport: {output}")
    return 2 if any("error" in x for x in journal["items"]) else 0


if __name__ == "__main__": raise SystemExit(main())
