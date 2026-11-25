#!/usr/bin/env python3
"""Collecte localement les pages bloquées côté serveur et les remet au Hub."""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import subprocess
from contextlib import nullcontext
from pathlib import Path
from datetime import date, timedelta

import requests
import re
from openpyxl import load_workbook
from playwright.sync_api import sync_playwright


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def truthy(value) -> bool:
    return str(value or "").strip().lower() in {"1", "oui", "yes", "true", "x"}


def fetch_html(page, url: str, wait_ms: int, scrolls: int, node_config=None, prefer_http: bool = False) -> str:
    if prefer_http:
        response = requests.get(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131 Safari/537.36"}, timeout=60)
        if response.ok and len(response.text.strip()) >= 200:
            return response.text
    if node_config:
        node_bin, helper, module_path = node_config
        result = subprocess.run(
            [node_bin, str(helper), module_path, url, str(wait_ms), str(scrolls)],
            capture_output=True, text=True, encoding="utf-8", timeout=120,
        )
        html = result.stdout
        blocked = "403 Forbidden" in html or "Access Denied" in html
        if result.returncode == 0 and len(html.strip()) >= 200 and not blocked:
            return html
        # Certains WAF refusent Chrome headless mais servent le HTML complet à
        # la même IP en HTTP classique. Ce secours reste exécuté sur le poste.
        response = requests.get(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131 Safari/537.36"}, timeout=60)
        response.raise_for_status()
        if len(response.text.strip()) < 200:
            raise RuntimeError(f"HTML local vide après Playwright et HTTP ({len(response.text)} octets): {url}")
        return response.text
    page.goto(url, wait_until="domcontentloaded", timeout=90000)
    page.wait_for_timeout(max(0, wait_ms))
    for _ in range(max(0, scrolls)):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(800)
    html = page.content()
    if len(html.strip()) < 200:
        raise RuntimeError(f"HTML vide ou trop court ({len(html)} octets): {url}")
    return html


def post(api_url: str, token: str, verify_ssl: bool, payload: dict) -> dict:
    response = requests.post(
        api_url, json=payload,
        headers={"X-Agent-Token": token, "Accept": "application/json"},
        timeout=600, verify=verify_ssl,
    )
    try:
        data = response.json()
    except ValueError as exc:
        # Les versions serveur antérieures au correctif de buffering peuvent
        # préfixer le JSON par les lignes CLI du Hub. Extraire uniquement
        # l'objet final permet de terminer le lot sans le rejouer aveuglément.
        match = re.search(r'\{\s*"ok"\s*:', response.text)
        if not match:
            raise RuntimeError(f"Réponse serveur non JSON ({response.status_code}): {response.text[:300]}") from exc
        try:
            data = json.loads(response.text[match.start():])
        except ValueError:
            raise RuntimeError(f"Réponse serveur non JSON ({response.status_code}): {response.text[:300]}") from exc
    if response.status_code >= 400:
        raise RuntimeError(f"Serveur HTTP {response.status_code}: {data}")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Collecteur Playwright local pour les endpoints Hub izilife")
    parser.add_argument("--workbook", required=True, type=Path)
    parser.add_argument("--env", type=Path, default=Path.cwd() / ".env")
    parser.add_argument("--headed", action="store_true", help="Affiche Chromium pendant la collecte")
    parser.add_argument("--only-endpoint", type=int, default=0)
    parser.add_argument("--node-bin", default=os.getenv("PLAYWRIGHT_NODE_BIN", ""))
    parser.add_argument("--playwright-module", default=os.getenv("PLAYWRIGHT_NODE_MODULE", ""))
    parser.add_argument("--discover-only", action="store_true", help="Découvre les fiches sans les charger ni appeler le LLM")
    args = parser.parse_args()

    load_dotenv(args.env)
    token = (os.getenv("IZILIFE_AGENT_TOKEN") or os.getenv("AGENT_SECRET_TOKEN") or "").strip()
    if not token:
        raise RuntimeError("IZILIFE_AGENT_TOKEN ou AGENT_SECRET_TOKEN absent.")

    wb = load_workbook(args.workbook)
    ws = wb["Endpoints"]
    headers = {str(cell.value).strip(): cell.column for cell in ws[1] if cell.value}
    required = {"enabled", "hub_id", "endpoint_id", "label", "source_url", "server_base_url"}
    missing = required - set(headers)
    if missing:
        raise RuntimeError("Colonnes manquantes: " + ", ".join(sorted(missing)))

    def value(row: int, name: str, default=None):
        col = headers.get(name)
        current = ws.cell(row, col).value if col else None
        return default if current in (None, "") else current

    node_config = None
    if args.node_bin and args.playwright_module:
        node_config = (args.node_bin, Path(__file__).with_name("playwright_fetch_local.mjs"), args.playwright_module)

    with (nullcontext(None) if node_config else sync_playwright()) as pw:
        if node_config:
            browser = None
            context = None
            page = None
        else:
            browser = pw.chromium.launch(headless=not args.headed)
            context = browser.new_context(locale="fr-FR", user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131 Safari/537.36")
            page = context.new_page()
        for row in range(2, ws.max_row + 1):
            if not truthy(value(row, "enabled")):
                continue
            endpoint_id = int(value(row, "endpoint_id", 0))
            if args.only_endpoint and endpoint_id != args.only_endpoint:
                continue
            hub_id = int(value(row, "hub_id", 0))
            label = str(value(row, "label", endpoint_id))
            source_url = str(value(row, "source_url", "")).strip()
            base = str(value(row, "server_base_url", "")).rstrip("/")
            # La production expose les contrôleurs du BO sous /izilife-admin.
            # Accepter aussi l'URL publique racine évite une configuration Excel
            # fragile et reste compatible avec les bases locales déjà préfixées.
            if base in {"https://www.izilife.co", "https://izilife.co"}:
                base += "/izilife-admin"
            api_url = base + "/scraper/agentHubLocalCollect"
            wait_ms = int(value(row, "wait_ms", 2500))
            detail_delay_ms = int(value(row, "detail_delay_ms", 1200))
            scrolls = int(value(row, "scrolls", 2))
            max_details = int(value(row, "max_details", 120))
            verify_ssl = truthy(value(row, "verify_ssl", 1))
            pagination_mode = str(value(row, "pagination_mode", "")).strip().upper()
            pagination_template = str(value(row, "pagination_template", "")).strip()
            pagination_max_pages = int(value(row, "pagination_max_pages", 0))
            status_col = headers.get("status")
            error_col = headers.get("last_error")
            processed_col = headers.get("processed_at")
            try:
                list_urls = [source_url]
                if pagination_mode == "WEEKLY_DATE_PATH":
                    if not pagination_template or "{yyyy}" not in pagination_template:
                        raise RuntimeError("pagination_template WEEKLY_DATE_PATH invalide")
                    today = date.today()
                    monday = today - timedelta(days=today.weekday())
                    for week in range(1, max(0, pagination_max_pages) + 1):
                        current = monday + timedelta(days=7 * week)
                        list_urls.append(pagination_template.format(
                            yyyy=f"{current.year:04d}", mm=f"{current.month:02d}", dd=f"{current.day:02d}"
                        ))
                by_url = {}
                for page_number, list_url in enumerate(list_urls, 1):
                    print(f"[{label}] collecte liste {page_number}/{len(list_urls)} {list_url}", flush=True)
                    list_html = fetch_html(page, list_url, wait_ms, scrolls, node_config, prefer_http=True)
                    discovery = post(api_url, token, verify_ssl, {
                        "phase": "DISCOVER", "hub_id": hub_id, "endpoint_id": endpoint_id,
                        "url": list_url, "html": list_html,
                    })
                    for link in discovery.get("links") or []:
                        by_url[str(link.get("url") or "")] = link
                links = list(by_url.values())[:max_details]
                print(f"[{label}] {len(links)} fiche(s) admise(s) par le Hub", flush=True)
                if args.discover_only:
                    if status_col: ws.cell(row, status_col).value = "DISCOVERED"
                    if error_col: ws.cell(row, error_col).value = ""
                    continue
                pages = []
                totals = {"fetched": 0, "tmp_inserted": 0, "ignored": 0, "errors": 0}
                for index, link in enumerate(links, 1):
                    detail_url = str(link["url"])
                    html = fetch_html(page, detail_url, wait_ms, scrolls, node_config)
                    pages.append({"item_id": int(link["item_id"]), "url": detail_url, "html": html})
                    if len(pages) == 10 or index == len(links):
                        result = post(api_url, token, verify_ssl, {
                            "phase": "INGEST_DETAILS", "hub_id": hub_id,
                            "endpoint_id": endpoint_id, "pages": pages,
                        })
                        for key in totals:
                            totals[key] += int((result.get("stats") or {}).get(key, 0))
                        pages = []
                    time.sleep(max(0, detail_delay_ms) / 1000)
                if status_col: ws.cell(row, status_col).value = "DONE"
                if error_col: ws.cell(row, error_col).value = ""
                print(f"[{label}] terminé {json.dumps(totals, ensure_ascii=False)}", flush=True)
            except Exception as exc:
                if status_col: ws.cell(row, status_col).value = "FAILED"
                if error_col: ws.cell(row, error_col).value = str(exc)[:1000]
                print(f"[{label}] ERREUR: {exc}", file=sys.stderr, flush=True)
            finally:
                if processed_col: ws.cell(row, processed_col).value = time.strftime("%Y-%m-%d %H:%M:%S")
                wb.save(args.workbook)
        if browser: browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
