"""AI-assisted EventTmp validator.

The agent is deliberately stateless. It asks the BO for pending candidates,
enriches the evidence with a normal HTTP fetch and can, during local rodage
only, use Playwright as an explicit fallback for dynamic/blocked pages.

Modes:
  review   (default): report only, no database write
  apply:             enrich EventTmp, never publish
  validate:          enrich and publish only when the BO reports zero blockers
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timedelta
from html import unescape
from urllib.parse import urljoin
from pathlib import Path
from typing import Any

import requests
import urllib3

CORE_ROOT = Path(__file__).resolve().parents[2]
if str(CORE_ROOT) not in sys.path:
    sys.path.append(str(CORE_ROOT))
from core.paths import (  # noqa: E402
    IZILIFE_ENVS, drive_workspace_root, izilife_places_zone,
    local_agent_workspace_root, normalize_zone,
)
from core.place_resolution import PlaceIdentity, normalize_url  # noqa: E402
from local_event_ocr import estimated_end_hour  # noqa: E402

EVENT_DETAIL_HEADERS = [
    "event_tmp_id", "event_url", "reason", "venue_name", "city", "address",
    "latitude", "longitude", "source_url", "best_candidate", "best_score",
    "location_type", "location_string_id", "status", "notes", "processed_at", "result",
]
VENUE_HEADERS = [
    "venue_key", "event_count", "venue_name", "city", "address", "latitude", "longitude",
    "best_candidate", "best_score", "decision", "event_tmp_ids", "event_urls", "source_urls",
    "location_type", "location_string_id", "status", "notes", "processed_at", "result",
]
AI_SOLVABLE_BLOCKERS = {
    "titre", "description", "date_debut", "heure_debut", "date_fin", "heure_fin",
    "categorie", "type_acces_payant", "activite_principale",
    "categorie_generique_interdite",
}

# The backend deliberately caps one validator run at 2,000 candidates.  The
# agent runs after collectors and must drain the ordinary EventTmp backlog in
# one invocation; a small interactive default (formerly 10) silently left most
# of the queue untouched.
DEFAULT_CANDIDATE_LIMIT = 2000


def clean_html(value: str) -> str:
    value = re.sub(r"(?is)<(script|style|noscript).*?>.*?</\1>", " ", value)
    value = re.sub(r"(?s)<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()[:24000]


def fetch_source_text(url: str, verify_ssl: bool) -> str:
    url = normalize_url(url)
    if not url or not re.match(r"^https?://", url, re.I):
        return ""
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; iziLifeEventValidator/1.0)"},
            timeout=20,
            verify=verify_ssl,
        )
        response.encoding = "utf-8"
        if response.status_code >= 400:
            return ""
        return clean_html(response.text)
    except requests.RequestException:
        return ""


def _page_image_url(html: str, base_url: str) -> str:
    """Extract an event image without asking the LLM or taking a screenshot."""
    patterns = (
        r'<meta[^>]+(?:property|name)=["\']og:image["\'][^>]+content=["\']([^"\']+)',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\']og:image["\']',
        r'<meta[^>]+(?:property|name)=["\']twitter:image(?::src)?["\'][^>]+content=["\']([^"\']+)',
    )
    for pattern in patterns:
        match = re.search(pattern, html, re.I)
        if match:
            return urljoin(base_url, unescape(match.group(1)).strip())
    for block in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.I | re.S):
        try:
            payload = json.loads(unescape(block))
        except (ValueError, TypeError):
            continue
        queue = payload if isinstance(payload, list) else [payload]
        while queue:
            item = queue.pop(0)
            if not isinstance(item, dict):
                continue
            image = item.get("image")
            if isinstance(image, str) and image.strip():
                return urljoin(base_url, image.strip())
            if isinstance(image, list):
                queue.extend({"image": value} for value in image)
            if isinstance(image, dict):
                candidate = image.get("url") or image.get("contentUrl")
                if isinstance(candidate, str) and candidate.strip():
                    return urljoin(base_url, candidate.strip())
            graph = item.get("@graph")
            if isinstance(graph, list):
                queue.extend(graph)
    return ""


def fetch_source_image(url: str, verify_ssl: bool) -> str:
    url = normalize_url(url)
    if not url or not re.match(r"^https?://", url, re.I):
        return ""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20,
                                verify=verify_ssl)
        if response.status_code >= 400:
            return ""
        return _page_image_url(response.text, response.url)
    except requests.RequestException:
        return ""


def fetch_source_text_browser(url: str) -> str:
    """Local diagnostic fallback; never enabled implicitly or in production."""
    if not url or not re.match(r"^https?://", url, re.I):
        return ""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright absent: installez-le seulement dans l'environnement agent local.") from exc
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=45_000)
            page.wait_for_timeout(1_500)
            return clean_html(page.content())
        finally:
            browser.close()


def fetch_source_image_browser(url: str) -> str:
    """Playwright fallback used by the local agent; returns the resource URL."""
    if not url or not re.match(r"^https?://", url, re.I):
        return ""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright absent: installez-le seulement dans l'environnement agent local.") from exc
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=45_000)
            page.wait_for_timeout(1_500)
            return _page_image_url(page.content(), page.url)
        finally:
            browser.close()


def blocking_doubts(doubts: list[Any], blockers: list[str]) -> list[Any]:
    """Ignore doubts about fields that are explicitly non-blocking."""
    aliases = {
        "end_hour": "heure_fin",
        "start_hour": "heure_debut",
        "end_date": "date_fin",
        "start_date": "date_debut",
        "reservation": "reservation",
        "réservation": "reservation",
        "booking": "reservation",
        "organisateur": "organisateur",
        "organizer": "organisateur",
        "lieu": "lieu_resolu",
        "location": "lieu_resolu",
    }
    relevant: list[Any] = []
    for doubt in doubts:
        if isinstance(doubt, dict):
            field = str(doubt.get("field") or "").strip()
            if not field or field in blockers:
                relevant.append(doubt)
            continue
        text_value = str(doubt).lower()
        matched = [target for word, target in aliases.items() if word in text_value]
        if not matched or any(target in blockers for target in matched):
            relevant.append(doubt)
    return relevant


def apply_time_fallbacks(
    event: dict[str, Any], proposal: dict[str, Any], blockers: list[str]
) -> dict[str, Any]:
    """Complete genuinely unpublished hours after source/Playwright analysis.

    Explicit source values always win.  These operational defaults are the
    final validator fallback requested for the production backlog, so a dated
    event is not kept indefinitely in EventTmp only because the publisher did
    not expose an hour.
    """
    result = dict(proposal)
    evidence = dict(result.get("evidence") or {})
    fallback_fields: set[str] = set()
    start_date = str(result.get("start_date") or event.get("start_date") or "")[:10]
    end_date = str(result.get("end_date") or event.get("end_date") or start_date)[:10]
    category = str(
        result.get("event_category_ref")
        or event.get("event_category_string_id")
        or event.get("category_name")
        or ""
    ).lower()
    title = str(result.get("title") or event.get("title") or "").lower()
    haystack = f"{category} {title}"

    if "heure_debut" in blockers and not result.get("start_hour"):
        daytime = (
            start_date and end_date and start_date != end_date
        ) or any(word in haystack for word in (
            "salon", "congres", "congrès", "forum", "marche", "marché",
            "festival", "convention", "exposition", "expo", "tournoi",
        ))
        evening = any(word in haystack for word in (
            "concert", "spectacle", "theatre", "théâtre", "comedie",
            "comédie", "one-man", "one man", "danse", "bal", "soiree",
            "soirée", "dj", "stand-up", "stand up",
        ))
        result["start_hour"] = "10:00" if daytime else ("20:00" if evening else "19:00")
        evidence["start_hour"] = "Horaire opérationnel de dernier recours du validateur; aucune heure publiée."
        fallback_fields.add("start_hour")

    if "heure_fin" in blockers and not result.get("end_hour"):
        start_hour = str(result.get("start_hour") or event.get("start_hour") or "")
        result["end_hour"] = estimated_end_hour(start_hour, haystack)
        if result["end_hour"] and start_hour and result["end_hour"] < start_hour and start_date:
            result["end_date"] = (
                datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=1)
            ).strftime("%Y-%m-%d")
        evidence["end_hour"] = "Fin contextuelle estimée; aucune durée ni heure de fin publiée."
        fallback_fields.add("end_hour")

    if fallback_fields:
        result["evidence"] = evidence
        result["doubts"] = [
            doubt for doubt in (result.get("doubts") or [])
            if not (isinstance(doubt, dict) and str(doubt.get("field") or "") in fallback_fields)
        ]
        result["confidence"] = max(float(result.get("confidence") or 0), 0.95)
    return result


class EventValidatorClient:
    def __init__(self, base_url: str, token: str, verify_ssl: bool):
        self.base_url = base_url.rstrip("/")
        self.verify_ssl = verify_ssl
        self.headers = {"X-Agent-Token": token, "Content-Type": "application/json"}

    def post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(
            self.base_url + path,
            headers=self.headers,
            json=payload,
            verify=self.verify_ssl,
            timeout=180,
        )
        response.encoding = "utf-8"
        try:
            body = response.json()
        except ValueError as exc:
            raise RuntimeError(f"HTTP {response.status_code}: réponse non JSON") from exc
        if response.status_code >= 400 or not body.get("success"):
            raise RuntimeError(body.get("error") or f"HTTP {response.status_code}")
        return body

    def candidates(self, city_id: int | None, limit: int, tmp_id: int | None = None,
                   from_date: str | None = None,
                   include_representations: bool = False) -> list[dict[str, Any]]:
        payload: dict[str, Any] = {
            "limit": limit,
            "include_representations": include_representations,
        }
        if city_id:
            payload["city_id"] = city_id
        if tmp_id:
            payload["tmp_id"] = tmp_id
        if from_date:
            payload["from_date"] = from_date
        return self.post("/scraper/agentEventValidatorCandidates", payload)["events"]

    def analyze(self, event: dict[str, Any], source_text: str) -> dict[str, Any]:
        return self.post("/scraper/agentAnalyzeEventTmp", {
            "tmp_id": int(event["id"]), "source_text": source_text,
        })

    def apply(self, tmp_id: int, proposal: dict[str, Any], validate: bool) -> dict[str, Any]:
        return self.post("/scraper/agentApplyEventValidation", {
            "tmp_id": tmp_id, "proposal": proposal, "validate": validate,
        })

    def validate_representation(self, tmp_id: int) -> dict[str, Any]:
        try:
            return self.post("/scraper/agentValidateRepresentation", {"tmp_id": tmp_id})
        except RuntimeError as exc:
            if "HTTP 404" not in str(exc):
                raise
            return self.post(
                "/scraper/agentApplyEventValidation",
                {
                    "tmp_id": tmp_id,
                    "proposal": {},
                    "validate": False,
                    "validate_representation": True,
                },
            )

    def resolve_location(self, tmp_id: int, location_type: str = "",
                         location_string_id: str = "", dry_run: bool = False) -> dict[str, Any]:
        payload: dict[str, Any] = {"tmp_id": tmp_id, "dry_run": dry_run}
        if location_type and location_string_id:
            payload.update({"location_type": location_type,
                            "location_string_id": location_string_id})
        return self.post("/scraper/agentResolveEventLocation", payload)


def feedback_path(env_name: str, zone: str) -> Path:
    return (drive_workspace_root(env_name) / "izilife" / "events_validator" /
            normalize_zone(zone) / "evtn_liste.xlsx")


def _normalized_venue_part(value: Any) -> str:
    value = unescape(str(value or "")).lower().strip()
    value = re.sub(r"\b(avenue|av\.?)(?=\s)", "av", value)
    value = re.sub(r"\b(boulevard|bd\.?)(?=\s)", "bd", value)
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def venue_key(entry: dict[str, Any]) -> str:
    shared = PlaceIdentity.build(name=entry.get("venue_name", ""), address=entry.get("address", ""),
                                 city=entry.get("city", ""), latitude=entry.get("latitude"), longitude=entry.get("longitude"))
    identity = "|".join((shared.name, shared.address, shared.city, str(shared.latitude or ""), str(shared.longitude or "")))
    return hashlib.sha1(identity.encode("utf-8")).hexdigest()[:16]


def _sheet_rows(sheet: Any) -> list[dict[str, Any]]:
    headers = [str(cell.value or "").strip() for cell in sheet[1]]
    return [dict(zip(headers, values)) for values in sheet.iter_rows(min_row=2, values_only=True)
            if any(value is not None for value in values)]


def _reset_sheet(workbook: Any, name: str, headers: list[str], widths: list[int]) -> Any:
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    sheet = workbook[name] if name in workbook.sheetnames else workbook.create_sheet(name)
    if sheet.max_row:
        sheet.delete_rows(1, sheet.max_row)
    sheet.append(headers)
    for cell in sheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="24364B")
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = f"A1:{openpyxl.utils.get_column_letter(len(headers))}1"
    for index, width in enumerate(widths, 1):
        sheet.column_dimensions[openpyxl.utils.get_column_letter(index)].width = width
    return sheet


def write_feedback(path: Path, entries: list[dict[str, Any]]) -> None:
    """Liste unique des lieux, avec les événements sources conservés dans un second onglet."""
    import openpyxl
    from openpyxl.styles import Alignment
    path.parent.mkdir(parents=True, exist_ok=True)
    old_details: list[dict[str, Any]] = []
    old_venues: dict[str, dict[str, Any]] = {}
    if path.exists():
        workbook = openpyxl.load_workbook(path)
        if "Événements concernés" in workbook.sheetnames:
            old_details = _sheet_rows(workbook["Événements concernés"])
        if "Lieux à créer" in workbook.sheetnames:
            rows = _sheet_rows(workbook["Lieux à créer"])
            if rows and "venue_key" in rows[0]:
                old_venues = {str(row["venue_key"]): row for row in rows if row.get("venue_key")}
            else:
                old_details.extend(rows)  # ancien format: une ligne par événement
    else:
        workbook = openpyxl.Workbook()
        workbook.remove(workbook.active)

    details = {int(row["event_tmp_id"]): row for row in old_details if row.get("event_tmp_id")}
    for entry in entries:
        tmp_id, previous = int(entry["event_tmp_id"]), details.get(int(entry["event_tmp_id"]), {})
        protected = {key: previous.get(key) for key in
                     ("location_type", "location_string_id", "status", "notes", "processed_at", "result")
                     if previous.get(key) not in (None, "")}
        details[tmp_id] = {**entry, **protected}

    grouped: dict[str, list[dict[str, Any]]] = {}
    for detail in details.values():
        grouped.setdefault(venue_key(detail), []).append(detail)
    venues: list[dict[str, Any]] = []
    for key, group in sorted(grouped.items(), key=lambda item: (-len(item[1]), str(item[1][0].get("venue_name") or ""))):
        representative = max(group, key=lambda row: float(row.get("best_score") or 0))
        previous, score = old_venues.get(key, {}), float(representative.get("best_score") or 0)
        venues.append({
            "venue_key": key, "event_count": len(group),
            **{field: representative.get(field) for field in
               ("venue_name", "city", "address", "latitude", "longitude", "best_candidate", "best_score")},
            "decision": "Vérifier/rattacher le candidat iziLife" if score >= .78 else "Créer le lieu",
            "event_tmp_ids": ",".join(str(row["event_tmp_id"]) for row in group),
            "event_urls": "\n".join(sorted({str(row.get("event_url")) for row in group if row.get("event_url")})),
            "source_urls": "\n".join(sorted({str(row.get("source_url")) for row in group if row.get("source_url")})),
            **{field: previous.get(field) or "" for field in
               ("location_type", "location_string_id", "status", "notes", "processed_at", "result")},
        })

    venue_sheet = _reset_sheet(workbook, "Lieux à créer", VENUE_HEADERS,
                               [18, 12, 32, 20, 48, 14, 14, 42, 12, 34, 34, 58, 58, 16, 32, 16, 45, 24, 55])
    detail_sheet = _reset_sheet(workbook, "Événements concernés", EVENT_DETAIL_HEADERS,
                                [14, 55, 22, 30, 20, 48, 14, 14, 55, 35, 12, 16, 32, 16, 45, 24, 55])
    for row in venues:
        venue_sheet.append([row.get(key) for key in VENUE_HEADERS])
    for row in sorted(details.values(), key=lambda item: int(item["event_tmp_id"])):
        detail_sheet.append([row.get(key) for key in EVENT_DETAIL_HEADERS])
    for sheet, link_columns in ((venue_sheet, (12, 13)), (detail_sheet, (2, 9))):
        for row_number in range(2, sheet.max_row + 1):
            for column in link_columns:
                cell = sheet.cell(row_number, column)
                if cell.value and "\n" not in str(cell.value):
                    cell.hyperlink, cell.style = str(cell.value), "Hyperlink"
            for cell in sheet[row_number]:
                cell.alignment = Alignment(vertical="top", wrap_text=True)
    workbook.save(path)


def apply_feedback_resolutions(path: Path, client: EventValidatorClient) -> list[dict[str, Any]]:
    """Applique un rattachement unique à tous les EventTmp qui partagent ce lieu."""
    try:
        exists = path.exists()
    except PermissionError:
        # Le montage Drive peut être temporairement verrouillé par Google
        # Sheets. Il ne doit jamais empêcher la validation côté serveur.
        return []
    if not exists:
        return []
    import openpyxl
    try:
        workbook = openpyxl.load_workbook(path)
    except (EOFError, OSError, ValueError, openpyxl.utils.exceptions.InvalidFileException):
        # Le classeur Drive est une aide opérateur, jamais un prérequis à la
        # validation. Une synchronisation partielle ne doit pas bloquer toute
        # la file EventTmp.
        return []
    sheet = workbook["Lieux à créer"] if "Lieux à créer" in workbook.sheetnames else workbook.active
    headers = [str(cell.value or "").strip() for cell in sheet[1]]
    results: list[dict[str, Any]] = []
    for row_number in range(2, sheet.max_row + 1):
        row = {header: sheet.cell(row_number, index + 1).value for index, header in enumerate(headers)}
        previous_status = str(row.get("status") or "").lower()
        if str(row.get("status") or "").strip().lower() not in {"ready", "resolved", "à appliquer", "a appliquer"}:
            continue
        tmp_ids = [int(value) for value in re.findall(r"\d+", str(row.get("event_tmp_ids") or row.get("event_tmp_id") or ""))]
        failures: list[str] = []
        for tmp_id in tmp_ids:
            try:
                response = client.resolve_location(tmp_id, str(row["location_type"]), str(row["location_string_id"]))
                results.append({"event_tmp_id": tmp_id, "status": "applied", "resolution": response.get("resolution")})
            except Exception as exc:
                failures.append(f"{tmp_id}: {exc}")
                results.append({"event_tmp_id": tmp_id, "status": "error", "error": str(exc)})
        status = "applied" if not failures else ("partial_error" if len(failures) < len(tmp_ids) else "error")
        sheet.cell(row_number, headers.index("status") + 1).value = status
        sheet.cell(row_number, headers.index("result") + 1).value = "; ".join(failures) or f"Lieu rattaché à {len(tmp_ids)} événement(s)"
        sheet.cell(row_number, headers.index("processed_at") + 1).value = datetime.now().astimezone().isoformat()
    workbook.save(path)
    return results


def _slug(value: Any) -> str:
    value = unescape(str(value or "")).lower().strip()
    try:
        import unicodedata
        value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    except Exception:
        pass
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", value)).strip("-")


def _is_virtual_venue(value: Any) -> bool:
    """Évite de transformer un libellé de diffusion en faux lieu physique."""
    return _slug(value) in {
        "en-ligne", "online", "internet", "visio", "visioconference",
        "distanciel", "a-distance",
    }


def append_missing_places_to_curate(env_name: str, zone: str,
                                    missing: list[dict[str, Any]]) -> tuple[Path, int]:
    """Ajoute une seule ligne par lieu réellement absent au pilote curate_places."""
    import openpyxl
    from openpyxl.styles import Alignment

    path = izilife_places_zone(zone, env_name) / "curate_places.xlsm"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        workbook = openpyxl.load_workbook(path, keep_vba=True)
        sheet = workbook["Lieux"] if "Lieux" in workbook.sheetnames else workbook.active
    else:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Lieux"
        sheet.append(["NOM", "VILLE", "TYPE_IMPOSE", "CATEGORY_STRING_ID",
                      "IN_ON_PLACE_REF", "NOTES", "STATUT"])

    headers = [str(cell.value or "").strip().upper() for cell in sheet[1]]
    required = ["NOM", "VILLE", "TYPE_IMPOSE", "CATEGORY_STRING_ID",
                "IN_ON_PLACE_REF", "NOTES", "STATUT"]
    if "NOM" not in headers:
        raise RuntimeError(f"Classeur curate_places invalide (NOM absent) : {path}")
    for header in required:
        if header not in headers:
            sheet.cell(1, len(headers) + 1).value = header
            headers.append(header)

    existing = {
        (_normalized_venue_part(row.get("NOM")), _slug(row.get("VILLE")))
        for row in _sheet_rows(sheet)
        if row.get("NOM")
    }
    added = 0
    for item in missing:
        name = str(item.get("venue_name") or "").strip()
        city = _slug(item.get("city"))
        address = str(item.get("address") or "").strip()
        # Le pilote createur_lieux recherche d'abord par nom + ville. Une
        # adresse améliore la recherche mais son absence ne doit pas empêcher
        # un lieu textuel issu d'un EventTmp d'entrer dans la file partagée.
        if (_is_virtual_venue(name) or len(_normalized_venue_part(name)) < 3
                or not city):
            continue
        key = (_normalized_venue_part(name), city)
        if key in existing:
            continue
        notes = (
            "Ajout automatique par events_validator après absence confirmée dans iziLife. "
            f"Adresse: {address or 'non fournie'}. "
            f"Coordonnées: {item.get('latitude')}, {item.get('longitude')}. "
            f"EventTmp: {item.get('event_tmp_ids')}."
        )
        values = {
            "NOM": name, "VILLE": city, "TYPE_IMPOSE": "",
            "CATEGORY_STRING_ID": "", "IN_ON_PLACE_REF": "",
            "NOTES": notes, "STATUT": "pending",
        }
        sheet.append([values.get(header, "") for header in headers])
        for cell in sheet[sheet.max_row]:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
        existing.add(key)
        added += 1
    if added:
        workbook.save(path)
    return path, added


def reconcile_feedback_locations(path: Path, client: EventValidatorClient,
                                 env_name: str, zone: str) -> dict[str, Any]:
    """Rejoue les lieux uniques, rattache les certains et exporte les vrais absents."""
    if not path.exists():
        return {"checked": 0, "resolved": 0, "missing": 0, "exported": 0}
    import openpyxl

    try:
        workbook = openpyxl.load_workbook(path)
    except (EOFError, OSError, ValueError, openpyxl.utils.exceptions.InvalidFileException):
        return {"checked": 0, "resolved": 0, "missing": 0, "exported": 0,
                "skipped": "feedback_workbook_unreadable"}
    sheet = workbook["Lieux à créer"] if "Lieux à créer" in workbook.sheetnames else workbook.active
    headers = [str(cell.value or "").strip() for cell in sheet[1]]
    checked = resolved = 0
    missing: list[dict[str, Any]] = []
    total = max(0, sheet.max_row - 1)
    for row_number in range(2, sheet.max_row + 1):
        row = {header: sheet.cell(row_number, index + 1).value for index, header in enumerate(headers)}
        previous_status = str(row.get("status") or "").lower()
        # Une ligne exportée doit être réévaluée aux passages suivants : le lieu
        # peut avoir été créé entre-temps par curate_places. Seules les lignes
        # effectivement appliquées sont terminales.
        if str(row.get("status") or "").lower() == "applied":
            continue
        tmp_ids = [int(value) for value in re.findall(r"\d+", str(row.get("event_tmp_ids") or ""))]
        if not tmp_ids:
            continue
        checked += 1
        if _is_virtual_venue(row.get("venue_name")):
            sheet.cell(row_number, headers.index("status") + 1).value = "manual_review"
            sheet.cell(row_number, headers.index("result") + 1).value = (
                "Lieu virtuel : aucune création dans curate_places"
            )
            sheet.cell(row_number, headers.index("processed_at") + 1).value = datetime.now().astimezone().isoformat()
            continue
        try:
            first = client.resolve_location(tmp_ids[0])
            resolution = first.get("resolution") or {}
            candidate = resolution.get("candidate") or {}
            if resolution.get("resolved") and not candidate:
                resolved_event = first.get("event") or resolution.get("event") or {}
                string_id = str(resolved_event.get("place_string_id") or "").strip()
                if string_id and resolved_event.get("for_place_id"):
                    candidate = {"type": "PLACE", "string_id": string_id}
                elif string_id and resolved_event.get("for_shop_id"):
                    candidate = {"type": "SHOP", "string_id": string_id}
            if resolution.get("resolved") and candidate.get("type") and candidate.get("string_id"):
                failures: list[str] = []
                for tmp_id in tmp_ids[1:]:
                    try:
                        client.resolve_location(tmp_id, str(candidate["type"]), str(candidate["string_id"]))
                    except Exception as exc:
                        failures.append(f"{tmp_id}: {exc}")
                sheet.cell(row_number, headers.index("location_type") + 1).value = candidate["type"]
                sheet.cell(row_number, headers.index("location_string_id") + 1).value = candidate["string_id"]
                sheet.cell(row_number, headers.index("status") + 1).value = "applied" if not failures else "partial_error"
                sheet.cell(row_number, headers.index("result") + 1).value = (
                    f"Rattaché automatiquement à {candidate['type']}:{candidate['string_id']}"
                    if not failures else "; ".join(failures)
                )
                resolved += 1
            else:
                # La ligne doit rester réévaluable après le passage de
                # curate_places, mais ne doit jamais être réexportée une
                # seconde fois pendant que son premier traitement est tracé.
                if previous_status != "exported_to_curate_places":
                    missing.append(row)
                sheet.cell(row_number, headers.index("status") + 1).value = "exported_to_curate_places"
                sheet.cell(row_number, headers.index("result") + 1).value = "Lieu absent : envoyé une seule fois à curate_places"
        except Exception as exc:
            sheet.cell(row_number, headers.index("status") + 1).value = "error"
            sheet.cell(row_number, headers.index("result") + 1).value = str(exc)
        sheet.cell(row_number, headers.index("processed_at") + 1).value = datetime.now().astimezone().isoformat()
        if checked % 25 == 0:
            print(json.dumps({"location_reconciliation": f"{checked}/{total}", "resolved": resolved,
                              "missing": len(missing)}, ensure_ascii=False), flush=True)
            workbook.save(path)
    curate_path, exported = append_missing_places_to_curate(env_name, zone, missing)
    workbook.save(path)
    return {"checked": checked, "resolved": resolved, "missing": len(missing),
            "exported": exported, "curate_places": str(curate_path)}


def public_event_url(env_name: str, unique_id: str | None) -> str:
    if not unique_id:
        return ""
    roots = {
        "local": "https://localhost:4443/izilife",
        "staging": "https://www.staging.izilife.co",
        "prod": "https://www.izilife.co",
    }
    return f"{roots[env_name]}/event/page/{unique_id}"


def progress_checkpoint(report: dict[str, Any], output: Path, processed: int, total: int, complete: bool = False) -> None:
    """Affiche la progression et écrit un checkpoint atomique tous les 25 événements."""
    if not complete and processed % 25:
        return
    counts: dict[str, int] = {}
    for row in report["events"]:
        status = str(row.get("status") or "unknown")
        counts[status] = counts.get(status, 0) + 1
    checkpoint = output.with_suffix(".checkpoint.json")
    checkpoint.parent.mkdir(parents=True, exist_ok=True)
    temporary = checkpoint.with_suffix(".checkpoint.tmp")
    payload = {**report, "progress": {"processed": processed, "total": total, "complete": complete, "counts": counts}}
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(checkpoint)
    print(json.dumps({"progress": f"{processed}/{total}", "counts": counts, "checkpoint": str(checkpoint)}, ensure_ascii=False), flush=True)


def feedback_entry(event: dict[str, Any], resolution: dict[str, Any], env_name: str,
                   validation: dict[str, Any]) -> dict[str, Any] | None:
    if resolution.get("resolved"):
        return None
    coordinates = resolution.get("coordinates") or {}
    candidates = resolution.get("candidates") or []
    best = candidates[0] if candidates else {}
    return {
        "event_tmp_id": int(event["id"]),
        "event_url": public_event_url(env_name, validation.get("event_unique_id")),
        "reason": "Créer ou rattacher le lieu sans bloquer la publication de l'événement",
        "venue_name": event.get("place") or event.get("location_text"),
        "city": event.get("city_name") or event.get("resolved_city_string_id"),
        "address": event.get("address") or event.get("location_text"),
        "latitude": coordinates.get("latitude"), "longitude": coordinates.get("longitude"),
        "source_url": event.get("source_url"),
        "best_candidate": f"{best.get('type', '')}:{best.get('string_id', '')} {best.get('name', '')}".strip(),
        "best_score": best.get("score"), "location_type": "", "location_string_id": "",
        "status": "pending", "notes": "",
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.browser_fallback and args.env == "prod" and not args.allow_prod_browser_fallback:
        raise RuntimeError(
            "--browser-fallback avec l'API production exige "
            "--allow-prod-browser-fallback (le navigateur reste local)."
        )
    env = IZILIFE_ENVS[args.env]
    token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("IZILIFE_AGENT_TOKEN non défini.")
    if not env["verify_ssl"]:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    client = EventValidatorClient(env["base_url"], token, env["verify_ssl"])
    # La résolution est exclusivement serveur et se fait, plus bas, via
    # agentResolveEventLocation pour chaque EventTmp. L'ancien evtn_liste.xlsx
    # n'est plus une file d'état parallèle et n'est jamais lu ni réécrit.
    reconciliation = {"skipped": "feedback_workbook_retired"}
    corrections = {"skipped": "feedback_workbook_retired"}
    reused: dict[int, dict[str, Any]] = {}
    if args.reuse_report:
        previous = json.loads(args.reuse_report.read_text(encoding="utf-8"))
        reused = {int(row["tmp_id"]): row.get("proposal") or {} for row in previous.get("events", []) if row.get("proposal")}
    report: dict[str, Any] = {
        "generated_at": datetime.now().astimezone().isoformat(),
        "environment": args.env, "mode": args.mode, "location_reconciliation": reconciliation,
        "feedback_corrections": corrections, "events": [],
    }
    ai_calls = 0
    candidates = client.candidates(
        args.city_id,
        args.limit,
        args.tmp_id,
        args.from_date,
        args.include_representations,
    )
    if args.source_domain:
        domains = tuple(value.strip().lower() for value in args.source_domain if value.strip())
        candidates = [
            event for event in candidates
            if any(domain in str(event.get("source_url") or "").lower() for domain in domains)
        ]
    total = len(candidates)
    validated_representation_keys: set[str] = set()
    for processed, event in enumerate(candidates, 1):
        event_date = str(event.get("start_date") or event.get("end_date") or "")[:10]
        if args.from_date and event_date and event_date < args.from_date:
            continue
        entry: dict[str, Any] = {
            "tmp_id": int(event["id"]), "title": event.get("title"),
            "source_url": event.get("source_url"), "status": "reviewed",
            "for_place_id": event.get("for_place_id"),
            "for_shop_id": event.get("for_shop_id"),
            "place_string_id": event.get("place_string_id"),
        }
        representation_key = str(
            event.get("representation_key")
            or event.get("representation_title")
            or event.get("title")
            or ""
        ).strip().casefold()
        # Chaque EventTmp doit être confirmé côté serveur. Deux dates portant le
        # même titre ne sont pas nécessairement matérialisées par le même appel ;
        # les sauter ici laissait silencieusement des séances dans la file.
        try:
            resolution_response = client.resolve_location(int(event["id"]), dry_run=args.mode == "review")
            resolution = resolution_response.get("resolution") or {}
            event = {**event, **(resolution_response.get("event") or {})}
            existing_blockers = resolution_response.get("blockers") or []
            entry["location_resolution"] = resolution
            entry["current_blockers"] = existing_blockers
            if args.list_only:
                entry["status"] = "listed"
                report["events"].append(entry)
                progress_checkpoint(report, args.output, processed, total)
                continue
            if not existing_blockers:
                entry["status"] = "ready_without_ai"
                entry["provider"] = None
                entry["model"] = None
                if args.mode != "review":
                    if (str(event.get("content_kind") or "").upper() == "REPRESENTATION" and args.mode == "validate"):
                        representation = client.validate_representation(int(event["id"]))
                        applied = {"validation": {
                            "auto_validated": bool(representation.get("validated")),
                            **representation,
                        }}
                        if representation.get("validated") and representation_key:
                            validated_representation_keys.add(representation_key)
                    else:
                        applied = client.apply(int(event["id"]), {}, args.mode == "validate")
                    entry["application"] = applied
                    entry["status"] = "validated" if applied.get("validation", {}).get("auto_validated") else "enriched"
                report["events"].append(entry)
                progress_checkpoint(report, args.output, processed, total)
                continue

            if args.deterministic_only:
                applied = None
                if args.mode != "review":
                    applied = client.apply(int(event["id"]), {}, args.mode == "validate")
                    entry["application"] = applied
                    entry["status"] = "validated" if applied.get("validation", {}).get("auto_validated") else "enriched"
                else:
                    entry["status"] = "deterministic_review"
                report["events"].append(entry)
                progress_checkpoint(report, args.output, processed, total)
                continue

            # Missing media is resolved from page metadata, not by a second LLM
            # pass. Playwright is only a local fallback for protected/dynamic pages.
            if "image" in existing_blockers and args.mode != "review":
                image_url = fetch_source_image(str(event.get("source_url") or ""), env["verify_ssl"])
                image_source = "http_metadata"
                if not image_url and args.browser_fallback:
                    image_url = fetch_source_image_browser(str(event.get("source_url") or ""))
                    image_source = "playwright_metadata"
                if image_url:
                    image_application = client.apply(
                        int(event["id"]), {"primary_image_url": image_url}, False)
                    entry["image_recovery"] = {
                        "source": image_source, "url": image_url,
                        "blockers": image_application.get("blockers") or [],
                    }
                    existing_blockers = image_application.get("blockers") or existing_blockers
                    entry["current_blockers"] = existing_blockers
                    if not existing_blockers:
                        if (str(event.get("content_kind") or "").upper() == "REPRESENTATION"
                                and args.mode == "validate"):
                            representation = client.validate_representation(int(event["id"]))
                            applied = {"validation": {
                                "auto_validated": bool(representation.get("validated")),
                                **representation,
                            }}
                            if representation.get("validated") and representation_key:
                                validated_representation_keys.add(representation_key)
                        else:
                            applied = client.apply(int(event["id"]), {}, args.mode == "validate")
                        entry["application"] = applied
                        entry["status"] = "validated" if applied.get("validation", {}).get("auto_validated") else "enriched"
                        report["events"].append(entry)
                        progress_checkpoint(report, args.output, processed, total)
                        continue

            ai_blockers = sorted(set(existing_blockers) & AI_SOLVABLE_BLOCKERS)
            if not ai_blockers:
                entry["status"] = "needs_manual"
                entry["not_applied_reason"] = "no_ai_solvable_blocker"
                report["events"].append(entry)
                progress_checkpoint(report, args.output, processed, total)
                continue

            reused_proposal = reused.get(int(event["id"]))
            if reused_proposal:
                source_mode = "reused_report"
                analysis = {"provider": None, "model": None, "proposal": reused_proposal}
            else:
                if not args.allow_ai:
                    entry["status"] = "needs_ai"
                    entry["not_applied_reason"] = "ai_disabled"
                    report["events"].append(entry)
                    progress_checkpoint(report, args.output, processed, total)
                    continue
                source_text = fetch_source_text(str(event.get("source_url") or ""), env["verify_ssl"])
                source_mode = "http"
                if args.browser_fallback:
                    browser_text = fetch_source_text_browser(str(event.get("source_url") or ""))
                    if browser_text:
                        source_text = browser_text
                        source_mode = "playwright"
                ai_calls += 1
                analysis = client.analyze(event, source_text)
            entry.update({
                "provider": analysis.get("provider"), "model": analysis.get("model"),
                "source_mode": source_mode,
                "current_blockers": existing_blockers,
                "proposal": analysis.get("proposal", {}),
            })
            proposal = apply_time_fallbacks(
                event, analysis.get("proposal") or {}, existing_blockers
            )
            entry["proposal"] = proposal
            # Some otherwise valid compact responses omit the optional numeric
            # confidence.  Treating that omission as an explicit confidence of
            # zero left valid EventCategory string_ids pending forever.  The BO
            # remains the authority: it checks that the proposed string_id
            # exists and keeps the blocker when it does not.
            raw_confidence = proposal.get("confidence")
            proposed_category = str(proposal.get("event_category_ref") or "").strip()
            category_only_blockers = bool(existing_blockers) and all(
                blocker in {"categorie", "categorie_generique_interdite"}
                for blocker in existing_blockers
            )
            if raw_confidence in (None, "") and proposed_category and category_only_blockers:
                confidence = 1.0
                proposal["confidence"] = confidence
                entry["proposal"] = proposal
            else:
                confidence = float(raw_confidence or 0)
            doubts = proposal.get("doubts") or []
            relevant_doubts = blocking_doubts(doubts, existing_blockers)
            entry["blocking_doubts"] = relevant_doubts
            if args.mode != "review" and confidence >= args.min_confidence and not relevant_doubts:
                # La proposition enrichit d'abord EventTmp. La matérialisation
                # groupée d'une représentation reste confiée à sa route dédiée.
                applied = client.apply(int(event["id"]), proposal, False)
                remaining_blockers = applied.get("blockers") or []
                if (str(event.get("content_kind") or "").upper() == "REPRESENTATION"
                        and args.mode == "validate" and not remaining_blockers):
                    representation = client.validate_representation(int(event["id"]))
                    applied["validation"] = {
                        "auto_validated": bool(representation.get("validated")),
                        **representation,
                    }
                    if representation.get("validated") and representation_key:
                        validated_representation_keys.add(representation_key)
                elif args.mode == "validate":
                    applied = client.apply(int(event["id"]), {}, True)
                entry["application"] = applied
                entry["status"] = "validated" if applied.get("validation", {}).get("auto_validated") else "enriched"
            elif args.mode != "review":
                entry["status"] = "needs_review"
                entry["not_applied_reason"] = "confidence_or_doubts"

        except Exception as exc:  # keep processing the batch; report every failure
            entry["status"] = "error"
            entry["error"] = str(exc)
        report["events"].append(entry)
        progress_checkpoint(report, args.output, processed, total)
    report["ai_calls"] = ai_calls
    report["feedback_workbook"] = None
    report["feedback_workbook_status"] = "retired"
    progress_checkpoint(report, args.output, total, total, complete=True)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Agent IA de validation EventTmp")
    parser.add_argument("--env", choices=sorted(IZILIFE_ENVS), default="local")
    parser.add_argument("--mode", choices=("review", "apply", "validate"), default="review")
    parser.add_argument("--city-id", type=int)
    parser.add_argument("--tmp-id", type=int)
    parser.add_argument(
        "--source-domain", action="append", default=[],
        help="Limite le lot aux URL source contenant ce domaine (option répétable).",
    )
    parser.add_argument(
        "--limit", type=int, default=DEFAULT_CANDIDATE_LIMIT,
        help=("Nombre maximal d'EventTmp traites pendant cette execution "
              f"(defaut et plafond API : {DEFAULT_CANDIDATE_LIMIT})"),
    )
    parser.add_argument("--from-date", help="Date de début minimale incluse (YYYY-MM-DD)")
    parser.add_argument(
        "--include-representations",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=("Inclut par défaut les propositions REPRESENTATION afin de "
              "matérialiser leur structure même sans séance datée."),
    )
    parser.add_argument("--zone", default="global", help="Zone du classeur de suivi")
    parser.add_argument("--min-confidence", type=float, default=0.90)
    parser.add_argument("--browser-fallback", action="store_true",
                        help="Secours Playwright pour le rodage local uniquement")
    parser.add_argument(
        "--allow-prod-browser-fallback",
        action="store_true",
        help=("Autorise explicitement le navigateur local à compléter des EventTmp "
              "de production; sans ce drapeau, la protection reste active."),
    )
    parser.add_argument("--list-only", action="store_true",
                        help="Liste les bloqueurs sans ouvrir de source et sans appeler l'IA")
    parser.add_argument("--deterministic-only", action="store_true",
                        help="Résolution/règles locales uniquement, sans nouvel appel IA")
    parser.add_argument("--allow-ai", action="store_true",
                        help="Autorise explicitement les appels IA payants")
    parser.add_argument("--skip-location-reconciliation", action="store_true",
                        help="Ne rejoue pas le classeur des lieux lorsqu'il vient d'être réconcilié")
    parser.add_argument("--reuse-report", type=Path,
                        help="Réutilise les propositions d'un rapport précédent sans nouvel appel IA")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    args.output = args.output or (
        local_agent_workspace_root(args.env) / "reports" /
        f"event_validation_{datetime.now():%Y%m%d_%H%M%S}.json"
    )
    report = run(args)
    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    counts: dict[str, int] = {}
    for row in report["events"]:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    print(json.dumps({"report": str(output), "counts": counts}, ensure_ascii=False))
    return 0 if not counts.get("error") else 1


if __name__ == "__main__":
    raise SystemExit(main())
