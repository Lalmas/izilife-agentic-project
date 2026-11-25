#!/usr/bin/env python3
"""Collecte territoriale déterministe puis analyse sémantique générique.

Le mode par défaut collecte, normalise, rapproche dans iziLife et produit un
rapport. L'option --send-new-to-scraper transmet le HTML complet des pages NEW
au pipeline Scraper existant : ses parseurs structurés restent prioritaires et
son LLM générique prend le relais lorsque la source n'a pas de parseur dédié.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import unicodedata
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

import requests
from openpyxl import Workbook

BASE_URLS = {
    "local": ("https://localhost:4443/izilife-admin", False),
    "staging": ("https://www.staging.izilife.co/izilife-admin", True),
    "prod": ("https://www.izilife.co/izilife-admin", True),
}
TRACKING_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid", "ref", "source"}


class BrowserFallback:
    def __init__(self) -> None:
        self.playwright = None
        self.browser = None
        self.page = None

    def get(self, url: str, actions: dict[str, Any] | None = None) -> str:
        if self.page is None:
            from playwright.sync_api import sync_playwright
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=True)
            context = self.browser.new_context(
                locale="fr-FR",
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/132 Safari/537.36",
            )
            self.page = context.new_page()
        self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
        self.page.wait_for_timeout(2500)
        actions = actions or {}
        load_more_texts = [str(value).strip() for value in actions.get("load_more_texts") or [] if str(value).strip()]
        max_rounds = max(0, min(int(actions.get("max_rounds") or 0), 50))
        wait_ms = max(100, min(int(actions.get("wait_ms") or 600), 5000))
        for _ in range(max_rounds):
            clicked = False
            for label in load_more_texts:
                control = self.page.locator("button, a").filter(
                    has_text=re.compile(re.escape(label), re.IGNORECASE)
                ).last
                try:
                    if control.count() and control.is_visible() and control.is_enabled():
                        control.scroll_into_view_if_needed()
                        control.click(timeout=5000)
                        self.page.wait_for_timeout(wait_ms)
                        clicked = True
                        break
                except Exception:
                    continue
            if not clicked:
                break
        return self.page.content()

    def close(self) -> None:
        if self.browser is not None:
            self.browser.close()
        if self.playwright is not None:
            self.playwright.stop()


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.jsonld: list[str] = []
        self._jsonld_depth = 0
        self._jsonld_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag.casefold() == "a" and values.get("href"):
            self.links.append(str(values["href"]))
        if tag.casefold() == "script" and str(values.get("type") or "").casefold() == "application/ld+json":
            self._jsonld_depth = 1
            self._jsonld_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() == "script" and self._jsonld_depth:
            self.jsonld.append("".join(self._jsonld_parts))
            self._jsonld_depth = 0
            self._jsonld_parts = []

    def handle_data(self, data: str) -> None:
        if self._jsonld_depth:
            self._jsonld_parts.append(data)


@dataclass
class Candidate:
    source: str
    source_url: str
    title: str
    start_date: str
    start_hour: str = ""
    end_date: str = ""
    end_hour: str = ""
    place_name: str = ""
    place_string_id: str = ""
    city: str = ""
    ticket_url: str = ""
    description: str = ""
    address: str = ""
    primary_image_url: str = ""
    fingerprint: str = ""
    detail_html: str = ""
    match_status: str = "DISCOVERED"
    match_reason: str = ""
    match_object_type: str = ""
    match_object_id: str = ""

    def matcher_payload(self) -> dict[str, str]:
        return {key: value for key, value in {
            "source_url": self.source_url,
            "ticket_url": self.ticket_url,
            "title": self.title,
            "start_date": self.start_date,
            "start_hour": self.start_hour,
            "place_name": self.place_name,
            "place_string_id": self.place_string_id,
            "city": self.city,
        }.items() if value}


def canonical_url(value: str) -> str:
    parsed = urlparse(str(value or "").strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ""
    query = [(k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=True)
             if k.lower() not in TRACKING_KEYS and not k.lower().startswith("utm_")]
    path = re.sub(r"/{2,}", "/", parsed.path or "/")
    if path != "/":
        path = path.rstrip("/")
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", urlencode(query), ""))


def normalized_text(value: str) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(ch for ch in text if not unicodedata.combining(ch)).casefold()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def iso_date(value: Any) -> str:
    raw = str(value or "").strip()
    match = re.match(r"^(\d{4}-\d{2}-\d{2})", raw)
    if match:
        return match.group(1)
    compact = re.match(r"^(\d{4})(\d{2})(\d{2})(?:T|$)", raw)
    return "-".join(compact.groups()) if compact else ""


def iso_hour(value: Any) -> str:
    raw = str(value or "").strip()
    match = re.search(r"(?:T|\s)(\d{2}:\d{2})", raw)
    if match:
        return match.group(1)
    compact = re.search(r"T(\d{2})(\d{2})(?:\d{2})?", raw)
    return ":".join(compact.groups()) if compact else ""


def fingerprint(candidate: Candidate) -> str:
    decisive = "|".join([
        normalized_text(candidate.title), candidate.start_date,
        candidate.start_hour, normalized_text(candidate.place_name),
        canonical_url(candidate.ticket_url),
    ])
    return hashlib.sha256(decisive.encode("utf-8")).hexdigest()


def walk_jsonld(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        if str(value.get("@type", "")).casefold() == "event":
            yield value
        for child in value.values():
            yield from walk_jsonld(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_jsonld(child)


def jsonld_city(location: Any) -> str:
    if isinstance(location, list):
        location = location[0] if location else {}
    if not isinstance(location, dict):
        return ""
    address = location.get("address") or {}
    if isinstance(address, list):
        address = address[0] if address else {}
    if isinstance(address, dict):
        locality = address.get("addressLocality") or ""
        if isinstance(locality, dict):
            locality = locality.get("name") or locality.get("nom") or locality.get("label") or ""
        return str(locality).strip()
    return ""


def jsonld_address(location: Any) -> str:
    if isinstance(location, list):
        location = location[0] if location else {}
    if not isinstance(location, dict):
        return ""
    address = location.get("address") or {}
    if isinstance(address, str):
        return address.strip()
    if isinstance(address, list):
        address = address[0] if address else {}
    if not isinstance(address, dict):
        return ""
    parts = [address.get("streetAddress"), address.get("postalCode"),
             address.get("addressLocality")]
    return ", ".join(str(value).strip() for value in parts
                     if isinstance(value, (str, int)) and str(value).strip())


def jsonld_image(value: Any) -> str:
    if isinstance(value, list):
        value = value[0] if value else ""
    if isinstance(value, dict):
        value = value.get("url") or value.get("contentUrl") or ""
    return canonical_url(str(value or ""))


def extract_jsonld_events(html: str, page_url: str, source: str,
                          default_city: str = "") -> list[Candidate]:
    parser = PageParser()
    parser.feed(html)
    found: list[Candidate] = []
    for raw_json in parser.jsonld:
        try:
            data = json.loads(raw_json.strip())
        except (TypeError, json.JSONDecodeError):
            continue
        for event in walk_jsonld(data):
            location = event.get("location") or {}
            offers = event.get("offers") or {}
            if isinstance(offers, list):
                offers = offers[0] if offers else {}
            start = event.get("startDate") or ""
            candidate = Candidate(
                source=source,
                source_url=canonical_url(event.get("url") or page_url),
                title=str(event.get("name") or "").strip(),
                start_date=iso_date(start),
                start_hour=iso_hour(start),
                end_date=iso_date(event.get("endDate")),
                end_hour=iso_hour(event.get("endDate")),
                place_name=str(location.get("name") or "").strip() if isinstance(location, dict) else "",
                city=jsonld_city(location) or default_city,
                ticket_url=canonical_url(offers.get("url") or "") if isinstance(offers, dict) else "",
                description=str(event.get("description") or "").strip(),
                address=jsonld_address(location),
                primary_image_url=jsonld_image(event.get("image")),
                detail_html=html,
            )
            if candidate.title and candidate.start_date and candidate.source_url:
                candidate.fingerprint = fingerprint(candidate)
                found.append(candidate)
    return found


def discover_links(html: str, base_url: str, patterns: list[str], limit: int,
                   detail_regex: str = "") -> list[str]:
    parser = PageParser()
    parser.feed(html)
    base_host = urlparse(base_url).netloc.lower()
    result: list[str] = []
    for href in parser.links:
        url = canonical_url(urljoin(base_url, href))
        if not url or urlparse(url).netloc.lower() != base_host:
            continue
        if patterns and not any(pattern.casefold() in url.casefold() for pattern in patterns):
            continue
        if url not in result:
            result.append(url)
    if detail_regex:
        matcher = re.compile(detail_regex, re.IGNORECASE)
        # Le tri reste stable : on privilégie les fiches détail sans casser
        # l'ordre éditorial/chronologique fourni par la page source.
        result.sort(key=lambda value: 0 if matcher.search(value) else 1)
    return result[:limit]


def city_allowed(candidate: Candidate, config: dict[str, Any]) -> bool:
    allowed = [normalized_text(value) for value in config.get("allowed_cities") or []]
    if not allowed:
        return True
    current = normalized_text(candidate.city)
    if not current:
        return not bool(config.get("require_city"))
    return any(current == value or value in current for value in allowed)


def get_html(session: requests.Session, url: str, fallback: BrowserFallback,
             timeout: int = 40, browser_actions: dict[str, Any] | None = None) -> str:
    response = session.get(url, timeout=timeout)
    if response.status_code in {403, 429}:
        return fallback.get(url, browser_actions)
    response.raise_for_status()
    if not response.encoding or response.encoding.casefold() in {"iso-8859-1", "ascii"}:
        response.encoding = response.apparent_encoding or "utf-8"
    return response.text


def collect_source(session: requests.Session, fallback: BrowserFallback,
                   config: dict[str, Any], city: str,
                   max_links: int) -> tuple[list[Candidate], list[str]]:
    errors: list[str] = []
    try:
        listing_actions = config.get("browser_actions") or {}
        if listing_actions:
            listing = fallback.get(config["url"], listing_actions)
        else:
            listing = get_html(session, config["url"], fallback)
    except Exception as exc:
        return [], [f"{config['name']}: listing: {exc}"]
    default_city = city if config.get("trust_default_city", True) else ""
    candidates = extract_jsonld_events(listing, config["url"], config["name"], default_city)
    if not candidates and config.get("browser_retry_empty"):
        listing = fallback.get(config["url"], config.get("browser_actions"))
        candidates = extract_jsonld_events(listing, config["url"], config["name"], default_city)
    urls = discover_links(
        listing, config["url"], config.get("link_patterns") or [], max_links,
        str(config.get("detail_regex") or ""),
    )
    seen = {item.source_url for item in candidates}
    for url in urls:
        try:
            detail = get_html(session, url, fallback)
            extracted = extract_jsonld_events(detail, url, config["name"], default_city)
            if not extracted and config.get("browser_retry_empty"):
                detail = fallback.get(url)
                extracted = extract_jsonld_events(detail, url, config["name"], default_city)
            # Une fiche découverte dans le JSON-LD de la liste doit quand même
            # être téléchargée : c'est sa page complète qui contient souvent
            # les autres séances. Remplace alors la version sommaire.
            if extracted:
                extracted_urls = {item.source_url for item in extracted}
                candidates = [item for item in candidates if item.source_url not in extracted_urls]
                candidates.extend(extracted)
            seen.update(item.source_url for item in extracted)
        except Exception as exc:
            errors.append(f"{config['name']}: {url}: {exc}")
    unique: dict[tuple[str, str], Candidate] = {}
    for item in candidates:
        if not city_allowed(item, config):
            continue
        unique[(item.source_url, item.fingerprint)] = item
    return list(unique.values()), errors


def state_db(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.execute("""CREATE TABLE IF NOT EXISTS candidate_state (
        source TEXT NOT NULL, source_url TEXT NOT NULL, fingerprint TEXT NOT NULL,
        status TEXT NOT NULL, last_seen TEXT NOT NULL,
        PRIMARY KEY(source, source_url, fingerprint)
    )""")
    return db


def previously_seen(db: sqlite3.Connection, candidate: Candidate) -> bool:
    return db.execute(
        "SELECT 1 FROM candidate_state WHERE source=? AND source_url=? AND fingerprint=?",
        (candidate.source, candidate.source_url, candidate.fingerprint),
    ).fetchone() is not None


def save_state(db: sqlite3.Connection, candidate: Candidate) -> None:
    db.execute("""INSERT INTO candidate_state(source,source_url,fingerprint,status,last_seen)
        VALUES(?,?,?,?,?) ON CONFLICT(source,source_url,fingerprint)
        DO UPDATE SET status=excluded.status,last_seen=excluded.last_seen""",
        (candidate.source, candidate.source_url, candidate.fingerprint,
         candidate.match_status, datetime.now().isoformat(timespec="seconds")))


def api_post(env: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
    token = (os.getenv("IZILIFE_AGENT_TOKEN") or os.getenv("AGENT_SECRET_TOKEN") or "").strip()
    if not token:
        raise RuntimeError("IZILIFE_AGENT_TOKEN ou AGENT_SECRET_TOKEN absent.")
    base_url, verify = BASE_URLS[env]
    response = requests.post(
        base_url + path, json=payload, headers={"X-Agent-Token": token},
        verify=verify, timeout=120,
    )
    response.raise_for_status()
    return response.json()


def match_candidates(items: list[Candidate], env: str) -> None:
    for offset in range(0, len(items), 100):
        batch = items[offset:offset + 100]
        response = api_post(env, "/scraper/agentMatchEventCandidates",
                            {"items": [item.matcher_payload() for item in batch]})
        results = response.get("items") or []
        for item, result in zip(batch, results):
            item.match_status = str(result.get("status") or "ERROR")
            item.match_reason = str(result.get("reason") or "")
            match = result.get("match") or {}
            item.match_object_type = str(match.get("object_type") or "")
            item.match_object_id = str(match.get("object_id") or "")


def resolve_city_id(env: str, city: str) -> int:
    token = (os.getenv("IZILIFE_AGENT_TOKEN") or os.getenv("AGENT_SECRET_TOKEN") or "").strip()
    base_url, verify = BASE_URLS[env]
    response = requests.get(base_url + f"/scraper/cityByStringId/{city}",
                            headers={"X-Agent-Token": token}, verify=verify, timeout=40)
    response.raise_for_status()
    return int(response.json()["city"]["id"])


def send_new(items: list[Candidate], env: str, city: str) -> int:
    token = (os.getenv("IZILIFE_AGENT_TOKEN") or os.getenv("AGENT_SECRET_TOKEN") or "").strip()
    base_url, verify = BASE_URLS[env]
    sent = 0
    city_ids: dict[str, int] = {}
    for item in items:
        if item.match_status != "NEW":
            continue
        item_city = item.city or city
        if item.detail_html:
            if item_city not in city_ids:
                city_ids[item_city] = resolve_city_id(env, item_city)
            filename = "territorial-" + hashlib.sha1(item.source_url.encode("utf-8")).hexdigest()[:16] + ".html"
            response = requests.post(
                base_url + f"/scraper/agentUploadEventSources/{city_ids[item_city]}",
                files={"sources[]": (filename, item.detail_html.encode("utf-8"), "text/html")},
                data={"source_urls[]": item.source_url},
                headers={"X-Agent-Token": token}, verify=verify, timeout=240,
            )
            response.raise_for_status()
            result = response.json()
            if not result.get("success", True):
                raise RuntimeError(result.get("error") or "Analyse Scraper refusée.")
            item.match_status = "SENT_TO_SCRAPER"
            item.match_reason = "Page complète transmise au parseur/LLM générique."
            sent += 1
            continue

        payload = {
            "type": "event",
            "source": f"territorial_{item.source}",
            "fields": {
                "title": item.title,
                "description": item.description or None,
                "location_text": item.address or item.place_name or None,
                "place": item.place_name or None,
                "place_string_id": item.place_string_id or None,
                "address": item.address or None,
                "start_date": item.start_date,
                "start_hour": item.start_hour or None,
                "end_date": item.end_date or None,
                "end_hour": item.end_hour or None,
                "access_link": item.ticket_url or None,
                "primary_image_url": item.primary_image_url or None,
                "source_url": item.source_url,
                # A territorial zone is a discovery scope, not necessarily the
                # municipality of every result (Roubaix/Tourcoing/etc. may be
                # discovered from a Lille-zone source).
                "city_string_id": item_city,
            },
        }
        response = requests.post(
            base_url + "/scraper/agentIngestJson", json=payload,
            headers={"X-Agent-Token": token},
            verify=verify, timeout=180,
        )
        response.raise_for_status()
        result = response.json()
        first = (result.get("results") or [{}])[0]
        if not result.get("success") or not first.get("success"):
            raise RuntimeError(first.get("error") or "Ingestion Scraper refusée.")
        if first.get("skipped"):
            item.match_status = "MATCHED_TMP"
            item.match_reason = str(first.get("reason") or "Doublon ignoré par le Scraper.")
            item.match_object_type = "EVENT_TMP"
            item.match_object_id = str(first.get("duplicate_id") or "")
            continue
        if not first.get("tmp_id"):
            raise RuntimeError("Le Scraper n'a retourné aucun tmp_id après ingestion.")
        item.match_status = "SENT_TO_SCRAPER"
        item.match_object_type = "EVENT_TMP"
        item.match_object_id = str(first["tmp_id"])
        sent += 1
    return sent


def write_report(items: list[Candidate], errors: list[str], output_dir: Path,
                 config: dict[str, Any]) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = output_dir / f"territorial_candidates_{stamp}.json"
    report_items: list[dict[str, Any]] = []
    for item in items:
        report_item = asdict(item)
        # Le HTML brut sert uniquement à l'envoi optionnel au Scraper. Le
        # rapport reste léger et ne duplique pas des pages tierces complètes.
        report_item.pop("detail_html", None)
        report_items.append(report_item)
    json_path.write_text(json.dumps({"generated_at": datetime.now().isoformat(),
                                     "zone": config.get("zone"),
                                     "items": report_items,
                                     "errors": errors}, ensure_ascii=False, indent=2), encoding="utf-8")
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Candidates"
    headers = ["source", "status", "title", "start_date", "start_hour", "place_name",
               "city", "source_url", "ticket_url", "reason", "match_type", "match_id", "fingerprint"]
    sheet.append(headers)
    for item in items:
        sheet.append([item.source, item.match_status, item.title, item.start_date, item.start_hour,
                      item.place_name, item.city, item.source_url, item.ticket_url,
                      item.match_reason, item.match_object_type, item.match_object_id, item.fingerprint])
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    for index, width in enumerate([20, 18, 45, 14, 12, 32, 18, 65, 65, 55, 18, 14, 66], 1):
        sheet.column_dimensions[chr(64 + index)].width = width
    error_sheet = workbook.create_sheet("Errors")
    error_sheet.append(["error"])
    for error in errors:
        error_sheet.append([error])
    xlsx_path = output_dir / f"territorial_candidates_{stamp}.xlsx"
    workbook.save(xlsx_path)
    return json_path, xlsx_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_config = Path(__file__).with_name("territorial_sources") / "lille-zone.json"
    parser.add_argument("--config", type=Path, default=default_config)
    parser.add_argument("--env", choices=BASE_URLS, default="local")
    parser.add_argument("--max-links", type=int, default=100)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--no-api-match", action="store_true")
    parser.add_argument("--send-new-to-scraper", action="store_true")
    parser.add_argument("--confirm-write", action="store_true")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    zone = str(config.get("zone") or "zone")
    city = str(config.get("city_string_id") or "").strip()
    output_dir = args.output_dir or Path(__file__).with_name("reports") / zone / args.env
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; iziLifeTerritorial/1.0)"})
    fallback = BrowserFallback()
    all_items: list[Candidate] = []
    errors: list[str] = []
    for source in config.get("sources") or []:
        if not source.get("enabled"):
            continue
        items, source_errors = collect_source(session, fallback, source, city, max(1, args.max_links))
        all_items.extend(items)
        errors.extend(source_errors)
    cutoff = date.today() + timedelta(days=int(config.get("window_days") or 120))
    all_items = [item for item in all_items
                 if item.start_date and date.fromisoformat(item.start_date) >= date.today()
                 and date.fromisoformat(item.start_date) <= cutoff]
    state = state_db(output_dir / "territorial_state.sqlite3")
    for item in all_items:
        if previously_seen(state, item):
            item.match_status = "KNOWN_SOURCE"
            item.match_reason = "URL et empreinte déjà traitées par ce collecteur."
    to_match = [item for item in all_items if item.match_status == "DISCOVERED"]
    if to_match and not args.no_api_match:
        match_candidates(to_match, args.env)
    if args.send_new_to_scraper:
        if not args.confirm_write:
            raise SystemExit("--send-new-to-scraper exige --confirm-write.")
        sent = send_new(all_items, args.env, city)
        print(f"Pages NEW envoyées au Scraper : {sent}")
    for item in all_items:
        save_state(state, item)
    state.commit()
    json_path, xlsx_path = write_report(all_items, errors, output_dir, config)
    counts: dict[str, int] = {}
    for item in all_items:
        counts[item.match_status] = counts.get(item.match_status, 0) + 1
    print(json.dumps({"zone": zone, "env": args.env, "counts": counts,
                      "errors": len(errors), "json": str(json_path),
                      "xlsx": str(xlsx_path)}, ensure_ascii=False, indent=2))
    fallback.close()
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
