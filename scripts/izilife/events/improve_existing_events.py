"""Améliore des événements existants depuis des sources fiables, sans doublon."""
from __future__ import annotations

import argparse
import html as html_lib
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import openpyxl
import requests
from openpyxl.styles import Font, PatternFill

from core.paths import IZILIFE_ENVS, event_improve_file, normalize_env, normalize_zone
from core.place_resolution import MapsNameResolver, normalize_url
from objects.object_agent_common import load_env

HEADERS = [
    "EVENT_REF", "SOURCE_URL", "TEXTE_MANUEL", "INFORMATIONS_JSON",
    "EVENT_CATEGORY_REF", "LOCATION_REF", "ORGANIZER_PAGE_REF", "UPDATE_MODE",
    "STATUS", "ERREUR", "COMPTE_RENDU", "PAYLOAD_JSON",
]


def _clean_text(value: Any) -> str:
    text = html_lib.unescape(str(value or "")).replace("\xa0", " ")
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)).strip()


def fetch_html(url: str) -> str:
    response = requests.get(url, timeout=35, headers={"User-Agent": "Mozilla/5.0 iziLife Event Improver/1.0"})
    response.raise_for_status()
    try: return response.content.decode("utf-8")
    except UnicodeDecodeError: return response.text


def extract_event(url: str, supplied_text: str = "") -> dict[str, Any]:
    source = fetch_html(url)
    blocks = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', source, re.I | re.S)
    candidates: list[dict[str, Any]] = []
    for block in blocks:
        try:
            value = json.loads(html_lib.unescape(block))
        except json.JSONDecodeError:
            continue
        values = value if isinstance(value, list) else value.get("@graph", [value]) if isinstance(value, dict) else []
        candidates.extend(item for item in values if isinstance(item, dict) and str(item.get("@type", "")).casefold().endswith("event"))
    if not candidates:
        raise ValueError("Aucun Event JSON-LD fiable trouvé dans la source.")
    event = candidates[0]
    start = datetime.fromisoformat(str(event.get("startDate", "")).replace("Z", "+00:00"))
    end_raw = str(event.get("endDate") or event.get("startDate") or "")
    end = datetime.fromisoformat(end_raw.replace("Z", "+00:00"))
    location = event.get("location") if isinstance(event.get("location"), dict) else {}
    address = location.get("address") if isinstance(location.get("address"), dict) else {}
    image = event.get("image")
    image_url = image.get("url", "") if isinstance(image, dict) else image[0] if isinstance(image, list) and image else str(image or "")
    description = _clean_text(event.get("description"))
    if supplied_text.strip(): description = _clean_text(description + " " + supplied_text)
    price_match = re.search(r"(?:tarif\s+(?:unique\s*)?:?\s*)(\d+(?:[,.]\d+)?)\s*€", description, re.I)
    free = bool(re.search(r"\bgratuit(?:e|ement)?\b", description, re.I)) and not price_match
    booking = ""
    for match in re.finditer(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', source, re.I | re.S):
        if re.search(r"réserv|billet|ticket", _clean_text(match.group(2)), re.I): booking = html_lib.unescape(match.group(1)); break
    return {
        "title": _clean_text(event.get("name")), "description": description,
        "start_date": start.date().isoformat(), "start_hour": start.strftime("%H:%M"),
        "end_date": end.date().isoformat(), "end_hour": end.strftime("%H:%M"),
        "location_name": _clean_text(location.get("name")),
        "address": _clean_text(address.get("streetAddress")), "city_ref": _clean_text(address.get("addressLocality")),
        "zip_code": _clean_text(address.get("postalCode")), "source_url": normalize_url(url),
        "image_url": normalize_url(image_url), "access_link": normalize_url(booking),
        "basic_price": float(price_match.group(1).replace(",", ".")) if price_match else None,
        "is_free_event": free,
        "access_type_ref": "libre-et-gratuit" if free else "acces-payant" if price_match else None,
        "keywords": _clean_text(event.get("keywords")),
    }


def infer_category(item: dict[str, Any]) -> str:
    value = (item.get("keywords", "") + " " + item.get("title", "")).casefold()
    if "danse" in value or "bal" in value: return "spectacle-de-danse"
    return ""


def api_post(path: str, data: dict[str, Any], env: str) -> dict[str, Any]:
    cfg = IZILIFE_ENVS[env]
    token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token: return {"success": False, "error": "IZILIFE_AGENT_TOKEN manquant"}
    try:
        response = requests.post(cfg["base_url"].rstrip("/") + path, data=data,
            headers={"X-Agent-Token": token}, verify=cfg.get("verify_ssl", True), timeout=180)
        return response.json()
    except (requests.RequestException, ValueError) as exc:
        return {"success": False, "error": str(exc)}


def api_json(path: str, payload: dict[str, Any], env: str) -> dict[str, Any]:
    cfg = IZILIFE_ENVS[env]; token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token: return {"success": False, "error": "IZILIFE_AGENT_TOKEN manquant"}
    try:
        response = requests.post(cfg["base_url"].rstrip("/") + path, json=payload,
            headers={"X-Agent-Token": token}, verify=cfg.get("verify_ssl", True), timeout=90)
        return response.json()
    except (requests.RequestException, ValueError) as exc: return {"success": False, "error": str(exc)}


def location_candidate(item: dict[str, Any], env: str, resolver: MapsNameResolver) -> str:
    name = item.get("location_name", "")
    if not name: return ""
    resolver.resolve(name, item.get("city_ref", ""), "Event improver")
    maps = resolver.last_result
    payload = {"name": maps.canonical_name or name, "address": maps.address or item.get("address", ""),
        "google_place_id": maps.google_place_id, "city": item.get("city_ref", ""),
        "latitude": maps.latitude, "longitude": maps.longitude}
    result = api_json("/scraper/agentLocationIdentityCandidates", payload, env)
    matches = [m for m in result.get("candidates", []) if m.get("type") in {"PLACE", "SHOP", "EQUIPMENT"} and float(m.get("score", 0)) >= .94]
    return f"{matches[0]['type']}:{matches[0]['string_id']}" if len(matches) == 1 and matches[0].get("string_id") else ""


def analyze_editorial(event_ref: str, source: dict[str, Any], env: str) -> dict[str, Any]:
    source_text = json.dumps(source, ensure_ascii=False, default=str)
    result = api_json("/scraper/agentAnalyzeEditorialObject", {
        "type": "EVENT", "ref": event_ref, "source_text": source_text,
    }, env)
    if not result.get("success"):
        raise RuntimeError(result.get("error", "Analyse éditoriale Event impossible."))
    return result.get("proposal") or {}


def build_package(event_ref: str, source: dict[str, Any], manual: dict[str, Any], category: str,
                  location_ref: str, organizer_ref: str, update_mode: str = "ENRICH") -> dict[str, Any]:
    editorial = manual.pop("_editorial_proposal", {}) if isinstance(manual.get("_editorial_proposal"), dict) else {}
    data = {key: value for key, value in source.items() if key not in {"image_url", "location_name", "keywords"} and value not in (None, "")}
    data.update({key: value for key, value in manual.items() if value not in (None, "")})
    for key in ("event_category_ref", "principal_activity_category_string_id", "sport_string_id",
                "dance_string_id", "music_style_string_id", "artisan_technique_string_id",
                "editorial_signals"):
        if editorial.get(key) not in (None, "", [], {}): data.setdefault(key, editorial[key])
    data["event_category_ref"] = category or data.get("event_category_ref") or infer_category(source)
    if not data["event_category_ref"]: raise ValueError("EVENT_CATEGORY_REF absent et impossible à déduire.")
    if location_ref: data["location_ref"] = location_ref
    if organizer_ref: data["organizer_page_ref"] = organizer_ref
    media = [{"image_url": source["image_url"], "title": source["title"], "is_principal": True}] if source.get("image_url") else []
    return {"schema_version":"izi.event.package.v1","package_kind":"EDITORIAL_AGENDA",
        "publication":{"activate":False},"events":[{"client_ref":"improve-1","existing_ref":event_ref,
        "relation":"STANDALONE","update_mode":update_mode if update_mode in {"ENRICH","OVERWRITE"} else "ENRICH","data":data,
        "sources":[{"url":source["source_url"]}],"media":media}]}


def init_file(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Ameliorations"; ws.append(HEADERS)
    ws.freeze_panes = "A2"; ws.auto_filter.ref = "A1:K500"
    for cell in ws[1]: cell.font = Font(bold=True, color="FFFFFF"); cell.fill = PatternFill("solid", fgColor="1F4E78")
    wb.save(path)


def run(path: Path, env: str, dry_run: bool, maximum: int, use_maps: bool, with_ai: bool = False) -> None:
    wb = openpyxl.load_workbook(path); ws = wb["Ameliorations"]; headers = {str(c.value or "").upper(): i for i,c in enumerate(ws[1])}
    with MapsNameResolver(enabled=use_maps) as resolver:
        processed = 0
        for row in ws.iter_rows(min_row=2):
            def get(name): return str(row[headers[name]].value or "").strip()
            def put(name, value): ws.cell(row[0].row, headers[name]+1, value)
            if not get("EVENT_REF") or get("STATUS").casefold() in {"done"} or processed >= maximum: continue
            processed += 1
            try:
                source = extract_event(get("SOURCE_URL"), get("TEXTE_MANUEL"))
                manual = json.loads(get("INFORMATIONS_JSON") or "{}")
                if with_ai:
                    manual["_editorial_proposal"] = analyze_editorial(get("EVENT_REF"), source, env)
                loc_ref = get("LOCATION_REF") or (location_candidate(source, env, resolver) if not dry_run else "")
                package = build_package(get("EVENT_REF"), source, manual, get("EVENT_CATEGORY_REF"), loc_ref, get("ORGANIZER_PAGE_REF"), get("UPDATE_MODE").upper() or "ENRICH")
                put("PAYLOAD_JSON", json.dumps(package, ensure_ascii=False))
                if dry_run:
                    put("STATUS", "dry_run"); put("COMPTE_RENDU", "Extraction validée; aucun appel d'écriture.")
                    print(json.dumps(package, ensure_ascii=False, indent=2))
                else:
                    result = api_post("/scraper/agentIngestEventPackage", {"payload":json.dumps(package,ensure_ascii=False),"dry_run":"0"}, env)
                    if not result.get("success"): raise RuntimeError(result.get("error", str(result)))
                    put("STATUS", "done"); put("COMPTE_RENDU", json.dumps(result, ensure_ascii=False)); put("ERREUR", "")
            except Exception as exc:
                put("STATUS", "error"); put("ERREUR", str(exc)); print(f"ERREUR ligne {row[0].row}: {exc}")
            wb.save(path)


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--zone",required=True); parser.add_argument("--env",default="local",choices=["local","staging","prod"])
    parser.add_argument("--file"); parser.add_argument("--init",action="store_true"); parser.add_argument("--dry-run",action="store_true"); parser.add_argument("--no-maps",action="store_true"); parser.add_argument("--with-ai",action="store_true"); parser.add_argument("--max",type=int,default=100)
    args=parser.parse_args(); load_env(); env=normalize_env(args.env); path=Path(args.file) if args.file else event_improve_file(normalize_zone(args.zone),env)
    if args.init: init_file(path)
    else: run(path,env,args.dry_run,args.max,not args.no_maps,args.with_ai)


if __name__ == "__main__": main()
