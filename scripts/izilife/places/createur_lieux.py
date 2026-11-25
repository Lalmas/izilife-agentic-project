"""
createur_lieux.py
-----------------
Curation manuelle de lieux — lit curate_places.xlsx depuis Google Drive par zone
et appelle postAgentFetchAndStoreOnePlace pour chaque lieu pending.

Le PHP fait tout : recherche Google Places, vérifie existence, importe.
Ce script ne fait qu'orchestrer les appels et tenir le fichier à jour.

Usage :
    python createur_lieux.py --zone=lille  --env=local --init
    python createur_lieux.py --zone=lille --env=local --city=lille --dry-run
    python createur_lieux.py --zone=lille --env=local --city=lille

Prérequis :
    pip install requests openpyxl python-dotenv
    Variable : IZILIFE_AGENT_TOKEN

Fichier canonique :
    $AGENTIC_DRIVE_ROOT/agentic_workspace/izilife/places/{zone}-zone/curate_places.xlsx
    Colonnes :
        nom          : Nom du lieu (obligatoire)
        ville        : Slug ville izilife (ex: roubaix). Si vide → ville du --city
        type_impose  : SHOP, PLACE ou EQUIPMENT (optionnel — laissé vide = Google décide)
        category_string_id : référence stable de ShopCategory/PlaceType/EquipmentCategory.
                        Obligatoire avec type_impose (ex: restaurant, musee)
        in_on_place_ref : Place.string_id du contenant (optionnel, ex: aushopping-v2)
        notes        : Tes notes perso
        statut       : pending/retry → done | error ; unmapped est transféré au BO puis archivé
"""

from __future__ import annotations

import os
import sys
import re
import time
import random
import argparse
import requests
import unicodedata
from difflib import SequenceMatcher
from datetime import datetime, date, timedelta
from pathlib import Path
from urllib.parse import quote_plus

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ─────────────────────────────────────────────
# CORE PATHS / CONFIG — migration safe
# ─────────────────────────────────────────────

def _ensure_core_import_path():
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "scripts" / "core" / "paths.py").exists():
            sys.path.insert(0, str(parent / "scripts"))
            return
        if (parent / "core" / "paths.py").exists():
            sys.path.insert(0, str(parent))
            return

_ensure_core_import_path()

try:
    from core.paths import IZILIFE_ENVS, ENV_GLOBAL, ENV_IZILIFE, izilife_places_zone, place_curate_file
    from core.place_resolution import MapsNameResolver as CoreMapsNameResolver, PlaceIdentity, normalize_url
    HAS_CORE_PATHS = True
except Exception:
    HAS_CORE_PATHS = False

CURRENT_ENV = "prod"

CITY_SLUG_ALIASES = {
    "annullin": "annœullin",
    "annoeullin": "annœullin",
    "marcq-en-barul": "marcq-en-baroeul",
    "mons-en-barul": "mons-en-baroeul",
}

def set_current_env(env_name: str):
    global CURRENT_ENV
    CURRENT_ENV = str(env_name or "prod").strip().lower()


def canonical_city_slug(value: str) -> str:
    slug = str(value or "").strip().lower()
    return CITY_SLUG_ALIASES.get(slug, slug)


# Agent credentials are supplied by the shell/process environment; never load local .env files.

try:
    import openpyxl
except ImportError:
    print("pip install openpyxl")
    sys.exit(1)

# ─────────────────────────────────────────────
# CHEMINS
# ─────────────────────────────────────────────

def get_drive_root() -> Path:
    value = os.environ.get("AGENTIC_DRIVE_ROOT", "").strip()
    if not value: raise RuntimeError("AGENTIC_DRIVE_ROOT non défini.")
    return Path(value).expanduser()


def get_curate_file(zone: str, workbook_name: str = "curate_places.xlsx") -> Path:
    if HAS_CORE_PATHS and Path(workbook_name).name == "curate_places.xlsx":
        return place_curate_file(zone, CURRENT_ENV)
    if HAS_CORE_PATHS:
        directory = izilife_places_zone(zone, CURRENT_ENV)
    else:
        directory = get_drive_root() / "agentic_workspace" / "izilife" / "places" / f"{zone}-zone"
    # Le pilote automatique utilise uniquement le classeur canonique. Un fichier
    # produit par Google Drive sous le nom "curate_places (1).xlsm" n'est jamais
    # sélectionné implicitement.
    # Un autre classeur doit toujours être demandé explicitement en CLI.
    return directory / Path(workbook_name).name


# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────

ENVS = IZILIFE_ENVS if HAS_CORE_PATHS else {
    "local":   {"base_url": "https://localhost:4443/izilife-admin",          "verify_ssl": False},
    "staging": {"base_url": "https://www.staging.izilife.co/izilife-admin", "verify_ssl": True},
    "prod":    {"base_url": "https://www.izilife.co/izilife-admin",          "verify_ssl": True},
}

AGENT_TOKEN = os.environ.get("IZILIFE_AGENT_TOKEN", "METTRE_TOKEN_ICI")
DELAY       = (2, 4)

# ─────────────────────────────────────────────
# UTILS
# ─────────────────────────────────────────────

def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def sleep_random(mn=2, mx=4):
    time.sleep(random.uniform(mn, mx))

def izilife_get(endpoint: str, env: dict) -> dict | None:
    try:
        r = requests.get(
            env["base_url"] + endpoint,
            headers={"X-Agent-Token": AGENT_TOKEN},
            verify=env["verify_ssl"], timeout=15,
        )
        r.encoding = "utf-8"
        return r.json() if r.status_code == 200 else None
    except Exception as e:
        log(f"  ❌ GET {endpoint} : {e}")
        return None

def izilife_post(endpoint: str, data: dict, env: dict) -> dict | None:
    try:
        r = requests.post(
            env["base_url"] + endpoint,
            json=data,
            headers={"X-Agent-Token": AGENT_TOKEN, "Accept": "application/json"},
            verify=env["verify_ssl"], timeout=30,
        )
        r.encoding = "utf-8"
        try:
            payload = r.json()
        except ValueError:
            payload = {"success": False, "error": r.text[:1000] or "Réponse HTTP non JSON"}
        if not isinstance(payload, dict):
            payload = {"success": False, "error": str(payload)[:1000]}
        payload.setdefault("http_status", r.status_code)
        if not r.ok:
            log(f"  ❌ HTTP {r.status_code} : {payload}")
        return payload
    except Exception as e:
        log(f"  ❌ POST {endpoint} : {e}")
        return None


def lookup_existing_place(name: str, city: str, env: dict, *, google_place_id: str = "",
                          address: str = "", latitude=None, longitude=None,
                          urls: list[str] | None = None) -> dict | None:
    """Recherche iziLife gratuite sur toutes les clés d'identité partagées."""
    identity = PlaceIdentity.build(name=name, string_id=name, city=city,
        google_place_id=google_place_id, address=address, latitude=latitude,
        longitude=longitude, urls=urls or [])
    result = izilife_post("/scraper/agentLocationIdentityCandidates", identity.lookup_payload(), env)
    if not result:
        return None
    candidates = result.get("candidates") or []
    decisive = [item for item in candidates if float(item.get("score") or 0) >= .94]
    if len(decisive) == 1:
        return decisive[0]
    if len(decisive) > 1 or candidates:
        return {"ambiguous": True, "candidates": candidates}
    return None

def resolve_city_id(city_slug: str, env: dict, strict: bool = True) -> int:
    r = izilife_get(f"/scraper/cityByStringId/{city_slug}", env)
    if r and r.get("success") and r.get("city"):
        city_id = int(r["city"]["id"])
        subdivision = r.get("subdivision") or {}
        if subdivision:
            log(
                f"Subdivision résolue : {city_slug} → "
                f"commune parente={r['city'].get('string_id')} (city_id={city_id})"
            )
        else:
            log(f"Ville résolue : {city_slug} → city_id={city_id}")
        return city_id
    log(f"❌ Ville ou subdivision introuvable : {city_slug}")
    if strict:
        sys.exit(1)
    return 0

# ─────────────────────────────────────────────
# LECTURE / ÉCRITURE XLSX
# ─────────────────────────────────────────────

def read_pending_rows(ws, allow_headerless: bool = False) -> list[dict]:
    first_values = [str(c.value or "").strip() for c in ws[1]]
    has_headers = any(value.lower() == "nom" for value in first_values)
    if not has_headers and not allow_headerless:
        raise ValueError("En-tête NOM absent. Utiliser --legacy-layout uniquement pour un ancien classeur sans en-têtes.")
    headers = [value.lower() for value in first_values] if has_headers else [
        "nom", "ville", "type_impose", "category_string_id", "notes", "statut", "age_semaines"
    ]
    rows = []
    min_row = 2 if has_headers else 1
    for row_idx, row in enumerate(ws.iter_rows(min_row=min_row, values_only=True), start=min_row):
        data = {headers[i]: str(v or "").strip() for i, v in enumerate(row) if i < len(headers)}
        for value in row:
            match = re.fullmatch(r"\s*(\d+)\s*semaines?\s*", str(value or ""), re.IGNORECASE)
            if match:
                data["weeks_ago"] = int(match.group(1))
                break
        # Le classeur est une file de création/reprise, pas le miroir des POI
        # non mappés du BO. Seuls les nouveaux et les échecs techniques sont
        # rejouables ici.
        if data.get("statut", "").lower() not in ("", "pending", "error", "retry"):
            continue
        if not data.get("nom", "").strip():
            continue
        data["row_idx"] = row_idx
        rows.append(data)
    return rows

def ensure_result_columns(ws) -> dict[str, int]:
    headers = [str(c.value or "").strip().lower() for c in ws[1]]
    result = {}
    for header in ("result_type", "entity_id", "tmp_id", "string_id", "last_result"):
        if header not in headers:
            ws.cell(row=1, column=len(headers) + 1, value=header.upper())
            headers.append(header)
        result[header] = headers.index(header) + 1
    return result


def update_row(ws, row_idx: int, new_status: str, row: dict | None = None):
    headers = [str(c.value or "").strip().lower() for c in ws[1]]
    if "nom" not in headers:
        ws.cell(row=row_idx, column=6).value = new_status
        return
    try:
        col = headers.index("statut") + 1
        ws.cell(row=row_idx, column=col).value = new_status
    except ValueError:
        pass
    if row is not None:
        columns = ensure_result_columns(ws)
        if new_status == "done":
            ws.cell(row=row_idx, column=columns["result_type"]).value = str(row.get("_result_type") or "")
            ws.cell(row=row_idx, column=columns["entity_id"]).value = int(row.get("_entity_id") or 0) or None
            ws.cell(row=row_idx, column=columns["string_id"]).value = str(row.get("_string_id") or "")
        result = str(row.get("_last_error") or "")
        if new_status == "unmapped":
            tmp_id = int(row.get("_tmp_id") or 0)
            ws.cell(row=row_idx, column=columns["tmp_id"]).value = tmp_id or None
            result = f"Transféré dans Valider Lieux (ScrapingUnmappedPoi #{tmp_id})"
        elif new_status == "done" and not result:
            result = "Créé ou déjà rattaché"
        canonical = str(row.get("_canonical_name") or "").strip()
        if canonical and canonical.casefold() != str(row.get("nom") or "").casefold():
            result = (result + " — " if result else "") + f"Nom Maps: {canonical}"
        ws.cell(row=row_idx, column=columns["last_result"]).value = result

# ─────────────────────────────────────────────
# TRAITEMENT D'UN LIEU
# ─────────────────────────────────────────────

class _LegacyMapsNameResolver:
    """Précontrôle gratuit du nom public avant l'appel Google Places payant."""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self._manager = None
        self._browser = None
        self._page = None
        self.last_city_confirmed = False

    def __enter__(self):
        if not self.enabled:
            return self
        from playwright.sync_api import sync_playwright
        self._manager = sync_playwright().start()
        self._browser = self._manager.chromium.launch(
            headless=True, args=["--disable-blink-features=AutomationControlled"]
        )
        context = self._browser.new_context(locale="fr-FR", timezone_id="Europe/Paris")
        self._page = context.new_page()
        return self

    def __exit__(self, exc_type, exc, traceback):
        if self._browser:
            self._browser.close()
        if self._manager:
            self._manager.stop()

    @staticmethod
    def _clean_title(value: str) -> str:
        value = re.sub(r"\s+", " ", str(value or "")).strip()
        value = re.sub(r"\s*[-–—]\s*Google Maps\s*$", "", value, flags=re.I)
        return value.strip()

    @staticmethod
    def names_are_compatible(requested: str, candidate: str) -> bool:
        """Interdit qu'une simple proximité géographique remplace l'identité du lieu."""
        def normalized(value: str) -> str:
            value = unicodedata.normalize("NFKD", str(value or ""))
            value = "".join(char for char in value if not unicodedata.combining(char))
            value = re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()
            value = re.sub(r"\bhotel de ville\b", "mairie", value)
            value = re.sub(r"\bbibliotheque(?: municipale)?\b", "mediatheque", value)
            return re.sub(r"\s+", " ", value)

        left, right = normalized(requested), normalized(candidate)
        if not left or not right:
            return False
        # Les lignes issues des sources utilisent souvent "VILLE, Nom du lieu".
        if "," in str(requested):
            left = normalized(str(requested).split(",", 1)[1])
        if left in right or right in left:
            return True
        left_tokens, right_tokens = set(left.split()), set(right.split())
        shared = left_tokens & right_tokens
        token_score = len(shared) / max(1, min(len(left_tokens), len(right_tokens)))
        sequence_score = SequenceMatcher(None, left, right).ratio()
        # Un terme générique isolé (centre, maison, médiathèque...) ne suffit pas.
        generic = {"centre", "maison", "espace", "salle", "mediatheque", "bibliotheque", "municipale"}
        distinctive_shared = shared - generic
        stopwords = {"de", "du", "des", "la", "le", "les", "d", "et"}
        right_initials = "".join(token[0] for token in right.split() if token not in stopwords)
        left_acronyms = {token for token in left.split() if 2 <= len(token) <= 6}
        acronym_match = right_initials in left_acronyms
        library_family = "mediatheque" in left_tokens and "mediatheque" in right_tokens
        return (
            sequence_score >= 0.68
            or (token_score >= 0.66 and bool(distinctive_shared))
            or acronym_match
            or library_family
        )

    @staticmethod
    def needs_city_confirmation(requested: str, candidate: str) -> bool:
        """Les familles génériques identiques ne prouvent pas l'identité du lieu."""
        def tokens(value: str) -> set[str]:
            value = unicodedata.normalize("NFKD", str(value or ""))
            value = "".join(char for char in value if not unicodedata.combining(char))
            return set(re.sub(r"[^a-z0-9]+", " ", value.casefold()).split())

        generic = {
            "centre", "culturel", "maison", "espace", "salle", "municipal", "municipale",
            "mediatheque", "bibliotheque", "mairie", "hotel", "ville", "de", "du", "des",
            "la", "le", "les", "d", "et",
        }
        return not bool((tokens(requested) & tokens(candidate)) - generic)

    @staticmethod
    def _is_invalid_candidate(value: str) -> bool:
        cleaned = str(value or "").strip()
        if not cleaned:
            return True
        if cleaned.casefold() in {"sponsorisé", "sponsorise", "résultats", "results", "google maps"}:
            return True
        # Un titre composé uniquement d'un numéro et d'une voie n'est pas un nom de lieu.
        return bool(re.match(r"^\d+\s+(?:rue|avenue|boulevard|place|allée|allee|chemin)\b", cleaned, re.I))

    def resolve(self, name: str, city: str, notes: str = "") -> tuple[str, str]:
        if not self.enabled or self._page is None:
            return name, "disabled"
        # Les notes sont des métadonnées internes (motif, coordonnées, EventTmp,
        # commentaires humains). Elles ne doivent jamais contaminer le nom public
        # recherché ni être renvoyées par le titre de la page Google Maps.
        query = " ".join(part for part in (name, city) if str(part).strip())
        url = "https://www.google.com/maps/search/?api=1&query=" + quote_plus(query)
        try:
            self.last_city_confirmed = False
            self._page.goto(url, wait_until="domcontentloaded", timeout=45_000)
            self._page.wait_for_timeout(1_200)
            for label in ("Tout accepter", "Accepter tout"):
                button = self._page.get_by_role("button", name=label)
                if button.count():
                    button.first.click(timeout=2_000)
                    self._page.wait_for_timeout(500)
                    break
            body_text = re.sub(r"\s+", " ", self._page.locator("body").inner_text())
            def normalized(value: str) -> str:
                value = unicodedata.normalize("NFKD", str(value or ""))
                value = "".join(char for char in value if not unicodedata.combining(char))
                return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()
            self.last_city_confirmed = normalized(city) in normalized(body_text)
            for selector in ("h1.DUwDvf", "div[role='main'] h1", "h1"):
                locator = self._page.locator(selector)
                if locator.count():
                    candidate = self._clean_title(locator.first.inner_text(timeout=2_000))
                    if not self._is_invalid_candidate(candidate):
                        return candidate, "maps_heading"
            candidate = self._clean_title(self._page.title())
            if not self._is_invalid_candidate(candidate):
                return candidate, "maps_title"
            body = body_text.lower()
            if "aucun résultat" in body or "no results" in body:
                return "", "no_result"
            return "", "unresolved"
        except Exception as exc:
            return "", f"browser_error:{type(exc).__name__}"


# Compatibilité publique : les imports/tests historiques continuent d'utiliser
# createur_lieux.MapsNameResolver, tandis que l'implémentation vit dans core.
MapsNameResolver = CoreMapsNameResolver if HAS_CORE_PATHS else _LegacyMapsNameResolver


def process_one(row: dict, default_city_slug: str, env: dict, dry_run: bool,
                maps: MapsNameResolver | None = None,
                blocked_categories: set[tuple[str, str]] | None = None) -> str:
    nom         = row.get("nom", "").strip()
    ville       = canonical_city_slug(row.get("ville", "").strip() or default_city_slug)
    type_impose = row.get("type_impose", "").strip().upper()
    category_string_id = (
        row.get("category_string_id", "").strip()
        or row.get("categorie_string_id", "").strip()
    )
    in_on_place_ref = row.get("in_on_place_ref", "").strip()
    # Une famille de recherche (ex. « salon de thé ») sert uniquement à trouver
    # des candidats. Elle ne doit jamais écraser le type réel renvoyé par Google.
    # Les curations éditoriales restent forcées par défaut ; les inventaires de
    # prospection déclarent explicitement cette colonne à oui.
    category_is_search_family = str(
        row.get("category_is_search_family", "")
        or row.get("categorie_est_famille_recherche", "")
    ).strip().casefold() in {"1", "true", "yes", "oui", "y", "o"}

    category_ref = (type_impose, category_string_id)
    if blocked_categories is not None and category_ref in blocked_categories:
        row["_last_error"] = (
            f"Référence absente en production déjà confirmée: "
            f"{type_impose}:{category_string_id}"
        )
        log(f"    ⚠️ Référence absente déjà confirmée — appel payant évité : {type_impose}:{category_string_id}")
        return "error"

    log(f"\n  → {nom} ({ville})")

    query_name = nom
    if maps is not None:
        canonical_name, maps_status = maps.resolve(nom, ville, row.get("notes", ""))
        row["_maps_status"] = maps_status
        if canonical_name:
            compatible = maps.names_are_compatible(nom, canonical_name)
            requires_city = maps.needs_city_confirmation(nom, canonical_name)
            if not compatible or (requires_city and not maps.last_city_confirmed):
                row["_last_error"] = (
                    f"Nom Maps ou commune incompatible: '{nom}' → '{canonical_name}'"
                )
                log(f"    ⚠️ Nom Maps incompatible — appel Google Places évité : {canonical_name}")
                return "error"
            query_name = canonical_name
            row["_canonical_name"] = canonical_name
            maps_result = getattr(maps, "last_result", None)
            if maps_result:
                row["_google_place_id"] = str(maps_result.google_place_id or "")
                row["_address"] = str(maps_result.address or "")
                row["_latitude"] = maps_result.latitude
                row["_longitude"] = maps_result.longitude
                row["_business_status"] = str(maps_result.business_status or "UNKNOWN")
                if maps_result.is_permanently_closed:
                    row["_last_error"] = "Google Maps indique une fermeture définitive"
                    log("    ⚠️ Établissement fermé définitivement — aucun appel Google Places")
                    return "error"
            if canonical_name.casefold() != nom.casefold():
                log(f"    🗺️ Nom Maps : {nom} → {canonical_name}")
        elif maps_status in {"no_result", "unresolved"}:
            row["_last_error"] = "Aucun établissement confirmé sur Google Maps"
            log("    ⚠️ Aucun résultat Maps certain — appel Google Places évité")
            return "error"
        else:
            row["_last_error"] = f"Précontrôle Maps indisponible ({maps_status})"
            log(f"    ⚠️ Précontrôle Maps indisponible ({maps_status}) — appel payant évité")
            return "error"

    if category_is_search_family:
        type_impose = ""
        category_string_id = ""
        category_ref = ("", "")

    if type_impose in ("SHOP", "PLACE", "EQUIPMENT") and not category_string_id:
        log("    ❌ TYPE_IMPOSE exige CATEGORY_STRING_ID (référence cible stable, jamais un ID numérique).")
        return "error"
    if category_string_id and type_impose not in ("SHOP", "PLACE", "EQUIPMENT"):
        log("    ❌ CATEGORY_STRING_ID exige TYPE_IMPOSE=SHOP, PLACE ou EQUIPMENT.")
        return "error"

    # Antidoublon iziLife avant la phase Google payante.
    if not dry_run:
        identity_urls = [row.get(key, "") for key in (
            "url", "url_website", "website", "site", "url_facebook", "facebook",
            "url_instagram", "instagram",
        ) if row.get(key)]
        existing = lookup_existing_place(
            query_name, ville, env,
            google_place_id=str(row.get("_google_place_id") or ""),
            address=str(row.get("_address") or row.get("address") or ""),
            latitude=row.get("_latitude"), longitude=row.get("_longitude"), urls=identity_urls,
        )
        if existing and existing.get("ambiguous"):
            row["_last_error"] = "Plusieurs fiches iziLife possibles : arbitrage requis"
            log("    ⚠️ Plusieurs doublons possibles dans iziLife — appel payant évité")
            return "error"
        if existing:
            row["_entity_id"] = int(existing.get("id") or 0)
            row["_result_type"] = str(existing.get("type") or "").upper()
            row["_string_id"] = str(existing.get("string_id") or "")
            log(f"    ℹ️ Déjà présent dans iziLife [{row['_result_type']}] id={row['_entity_id']} — appel payant évité")
            return "done"

    if dry_run:
        log(
            f"    [DRY RUN] → postAgentFetchAndStoreOnePlace/{ville} "
            f"query={query_name} destination={type_impose or 'AUTO'} "
            f"category_string_id={category_string_id or 'AUTO'} "
            f"in_on_place_ref={in_on_place_ref or 'NONE'}"
        )
        return "done"

    # Appel PHP — il cherche sur Google Places, vérifie existence, importe
    payload = {"query": query_name, "original_query": nom}
    if row.get("_google_place_id"):
        payload["google_place_id_hint"] = row["_google_place_id"]
    if type_impose in ("SHOP", "PLACE", "EQUIPMENT"):
        payload["destination"] = type_impose
        payload["category_string_id"] = category_string_id
    if in_on_place_ref:
        payload["in_on_place_ref"] = in_on_place_ref

    resp = izilife_post(f"/scraper/agentFetchAndStoreOnePlace/{ville}", payload, env)

    if not resp:
        log(f"    ❌ Pas de réponse du serveur")
        return "error"

    if resp.get("success"):
        result_type  = resp.get("result_type", "")
        name_created = resp.get("name", nom)
        if result_type == "unmapped":
            tmp_id = int(resp.get("tmp_id") or 0)
            if tmp_id <= 0:
                row["_last_error"] = "Réponse unmapped sans identifiant ScrapingUnmappedPoi vérifiable"
                log("    ❌ Unmapped non confirmé : aucun tmp_id renvoyé par le serveur")
                return "error"
            row["_tmp_id"] = tmp_id
            log(f"    ⚠️  Type non mappé → ScrapingUnmappedPoi : {name_created}")
            return "unmapped"
        row["_entity_id"] = int(resp.get("entity_id") or 0)
        row["_result_type"] = str(result_type).upper()
        row["_string_id"] = str(resp.get("string_id") or "")
        log(f"    ✅ Créé : {name_created} [{result_type}] id={resp.get('entity_id')}")
        return "done"
    else:
        err = resp.get("error", "Erreur inconnue")
        row["_last_error"] = err
        if (
            blocked_categories is not None
            and category_string_id
            and re.search(r"(?:introuvable|inexistante|unknown|not found)", str(err), re.I)
            and re.search(r"(?:PlaceType|ShopCategory|EquipmentCategory|cat[ée]gorie)", str(err), re.I)
        ):
            blocked_categories.add(category_ref)
            log(f"    ⚠️ Référence mémorisée comme absente : {type_impose}:{category_string_id}")
        google_status = resp.get("google_status")
        google_error = resp.get("google_error")
        if google_status and google_status != "UNKNOWN":
            err = f"Google Places status={google_status}: {err}"
        if google_error and google_error not in err:
            err = f"{err} — {google_error}"
        if resp.get("already_exists"):
            row["_entity_id"] = int(resp.get("entity_id") or 0)
            row["_result_type"] = str(resp.get("result_type") or type_impose).upper()
            row["_string_id"] = str(resp.get("string_id") or "")
            log(f"    ℹ️  Déjà existant — skip")
            return "done"
        log(f"    ❌ {err}")
        return "error"

# ─────────────────────────────────────────────
# INIT — créer le template xlsx
# ─────────────────────────────────────────────

def create_template(zone: str):
    pfile = get_curate_file(zone)
    pfile.parent.mkdir(parents=True, exist_ok=True)

    if pfile.exists():
        log(f"⚠️  Fichier déjà existant : {pfile}")
        return

    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.formatting.rule import FormulaRule

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Lieux"

    HDR_BG = "1F4E79"
    ALT_BG = "EBF3FB"
    thin   = Side(style="thin", color="BFBFBF")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    headers = [
        "NOM", "VILLE", "TYPE_IMPOSE", "CATEGORY_STRING_ID",
        "CATEGORY_IS_SEARCH_FAMILY", "IN_ON_PLACE_REF", "NOTES", "STATUT",
    ]
    widths  = [42,    18,      14,             24,                   28,                38,      14]
    for col, (h, w) in enumerate(zip(headers, widths), 1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.font      = Font(bold=True, color="FFFFFF", name="Arial", size=10)
        cell.fill      = PatternFill("solid", fgColor=HDR_BG)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border    = border
        ws.column_dimensions[cell.column_letter].width = w
    ws.row_dimensions[1].height = 22

    exemples = [
        ["Restaurant exemple", "lille",     "SHOP",  "restaurant", "aushopping-v2", "Exemple dans un centre", "pending"],
        ["Musée exemple",      "tourcoing", "PLACE", "musee",      "",              "Exemple avec référence vérifiée", "pending"],
        ["Planétarium exemple", "lille",    "EQUIPMENT", "planetarium", "",          "Exemple avec référence vérifiée", "pending"],
        ["",                         "",       "",      "",          "",              "", "pending"],
        ["",                         "",       "",      "",          "",              "", "pending"],
    ]
    for r, row_data in enumerate(exemples, 2):
        for c, val in enumerate(row_data, 1):
            cell = ws.cell(row=r, column=c, value=val)
            cell.font      = Font(name="Arial", size=10)
            cell.alignment = Alignment(vertical="center")
            cell.border    = border
            cell.fill      = PatternFill("solid", fgColor=ALT_BG if r % 2 == 0 else "FFFFFF")
        ws.row_dimensions[r].height = 18

    # Dropdown type_impose
    dv_type = DataValidation(type="list", formula1='"SHOP,PLACE,EQUIPMENT"',
                             allow_blank=True, showDropDown=False)
    dv_type.sqref = "C2:C500"
    ws.add_data_validation(dv_type)

    # Dropdown statut
    dv_status = DataValidation(type="list",
                               formula1='"pending,retry,error,skip"',
                               allow_blank=False, showDropDown=False)
    dv_status.sqref = "G2:G500"
    ws.add_data_validation(dv_status)

    # Mise en forme conditionnelle par statut
    for status, color in [("done","C6EFCE"),("error","FFC7CE"),
                          ("unmapped","FFEB9C"),("skip","D9D9D9")]:
        ws.conditional_formatting.add("A2:G500", FormulaRule(
            formula=[f'$G2="{status}"'],
            fill=PatternFill("solid", fgColor=color)
        ))

    ws.freeze_panes = "A2"

    wb.save(pfile)
    log(f"✅ Template créé : {pfile}")
    log(f"   Remplis le fichier puis lance :")
    log(f"   python createur_lieux.py --zone={zone} --env=local --city=<ville_par_defaut>")


# ─────────────────────────────────────────────
# ARCHIVE AUTO — déplacer les done vers logs/WXX/
# ─────────────────────────────────────────────

def get_log_file(zone: str, script: str = "createur_lieux") -> Path:
    today = date.today()
    week  = today.strftime("W%V")
    d = get_curate_file(zone).parent / "logs" / week
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{script}_{today.isoformat()}.xlsx"


def opening_monday(weeks_ago: int) -> date:
    today = date.today()
    this_monday = today - timedelta(days=today.weekday())
    return this_monday - timedelta(weeks=max(0, int(weeks_ago)))


NEWNESS_UPDATE_RE = re.compile(
    r"^UPDATE\s+`(?P<table>Shop|Place)`\s+SET\s+"
    r"`opening_date`\s*=\s*'(?P<date>\d{4}-\d{2}-\d{2})'\s*,\s*"
    r"`is_new_in_city`\s*=\s*1\s+WHERE\s+`id`\s*=\s*(?P<id>\d+)\s*;",
    re.IGNORECASE,
)


def sanitize_newness_statements(statements: list[str]) -> tuple[list[str], list[str]]:
    """Déduplique les nouveautés et neutralise les dates contradictoires.

    Une même entité peut apparaître plusieurs fois dans le classeur sous des
    libellés différents. Une date identique est un doublon inoffensif. Deux
    dates différentes sont ambiguës : aucune des lignes n'est exécutable tant
    que le conflit n'est pas résolu explicitement.
    """
    parsed: dict[tuple[str, int], dict[str, list[str]]] = {}
    passthrough: list[str] = []
    for raw in statements:
        statement = raw.strip()
        match = NEWNESS_UPDATE_RE.match(statement)
        if not match:
            if statement and statement not in passthrough:
                passthrough.append(statement)
            continue
        key = (match.group("table").capitalize(), int(match.group("id")))
        by_date = parsed.setdefault(key, {})
        by_date.setdefault(match.group("date"), []).append(statement)

    safe = list(passthrough)
    conflicts: list[str] = []
    for (table, entity_id), by_date in parsed.items():
        if len(by_date) == 1:
            # Même cible et même date : garder une seule requête, même si les
            # commentaires/libellés historiques diffèrent.
            safe.append(next(iter(by_date.values()))[0])
            continue
        dates = ", ".join(sorted(by_date))
        labels = " | ".join(
            statement.partition("/*")[2].rpartition("*/")[0].strip()
            for rows in by_date.values()
            for statement in rows
            if "/*" in statement
        )
        detail = f"{table} id={entity_id}: dates={dates}"
        if labels:
            detail += f"; lignes={labels}"
        conflicts.append(detail)
    return safe, conflicts


def write_newness_sql(curate_file: Path, sheet_name: str, statements: list[str]) -> Path | None:
    today = date.today()
    week = today.strftime("W%V")
    directory = curate_file.parent / "logs" / week
    directory.mkdir(parents=True, exist_ok=True)
    safe_sheet = re.sub(r"[^a-z0-9]+", "-", sheet_name.lower()).strip("-") or "sheet"
    target = directory / f"curate_places_newness_{safe_sheet}_{today.isoformat()}.sql"
    # Plusieurs passages le même jour alimentent le même lot. Ne jamais écraser
    # les requêtes produites par un passage précédent : fusionner les UPDATE en
    # conservant leur ordre et en éliminant uniquement les doublons exacts.
    previous: list[str] = []
    if target.exists():
        previous = [
            line.strip()
            for line in target.read_text(encoding="utf-8").splitlines()
            if line.strip().upper().startswith("UPDATE ")
        ]
    if not previous and not statements:
        return None
    merged, conflicts = sanitize_newness_statements([*previous, *statements])
    content = [
        "START TRANSACTION;",
        *merged,
        *([""] if conflicts else []),
        *[f"-- CONFLICT EXCLUDED: {conflict}" for conflict in conflicts],
        "COMMIT;",
        "",
    ]
    target.write_text("\n".join(content), encoding="utf-8")
    return target


def purge_done(zone: str, curate_file: Path | None = None, sheet_name: str | None = None) -> int:
    """Archive les lignes terminales hors du classeur de travail.

    Convention : on n'ajoute pas d'onglet Log dans curate_places.xlsx.
    Le fichier principal garde uniquement les lignes à suivre : pending, retry, error.
    Les unmapped sont déjà matérialisés dans la file TMP/BO et ne doivent pas
    être dupliqués dans curate_places.
    Retourne le nombre de lignes archivées.
    """
    pfile = curate_file or get_curate_file(zone)
    if not pfile.exists():
        log("Aucun fichier à purger.")
        return 0

    for _attempt in range(3):
        try:
            keep_vba = pfile.suffix.lower() == ".xlsm"
            wb = openpyxl.load_workbook(pfile, keep_vba=keep_vba)
            ws = wb[sheet_name] if sheet_name and sheet_name in wb.sheetnames else wb.active
            headers = [str(c.value or "").strip().lower() for c in ws[1]]
            if not headers:
                log("Aucun header dans le fichier principal.")
                return 0

            stat_col = (headers.index("statut") + 1) if "statut" in headers else 6
            done_rows = []
            keep_rows = []

            for row in ws.iter_rows(min_row=2, values_only=True):
                row_values = list(row)
                if not any(v is not None and str(v).strip() != "" for v in row_values):
                    continue
                status = str(row_values[stat_col - 1] or "").strip().lower()
                tmp_id = 0
                if "tmp_id" in headers:
                    try:
                        tmp_id = int(row_values[headers.index("tmp_id")] or 0)
                    except (TypeError, ValueError):
                        tmp_id = 0
                # Un ancien statut unmapped sans identifiant TMP n'est pas une
                # preuve suffisante : on le conserve pour reprise/contrôle.
                if status == "unmapped" and tmp_id <= 0:
                    row_values[stat_col - 1] = "error"
                    if "last_result" in headers:
                        row_values[headers.index("last_result")] = (
                            "Unmapped historique non vérifié : absence de tmp_id"
                        )
                    keep_rows.append(row_values)
                elif status in {"done", "unmapped", "skip"}:
                    done_rows.append(row_values)
                else:
                    keep_rows.append(row_values)

            if not done_rows:
                log("Aucune ligne terminale à archiver.")
                return 0

            # Écrire le log externe
            lf = get_log_file(zone, "createur_lieux")
            lb = openpyxl.Workbook()
            lws = lb.active
            lws.title = "Done"
            for col, h in enumerate(headers, 1):
                lws.cell(row=1, column=col, value=str(h).upper())
            for r, row in enumerate(done_rows, 2):
                for c, val in enumerate(row, 1):
                    lws.cell(row=r, column=c, value=val)
            lb.save(lf)
            log(f"✅ {len(done_rows)} ligne(s) done → {lf}")

            # Réécrire le fichier principal sans les done
            for row in ws.iter_rows(min_row=2):
                for cell in row:
                    cell.value = None
            for r, row in enumerate(keep_rows, 2):
                for c, val in enumerate(row, 1):
                    ws.cell(row=r, column=c, value=val)
            wb.save(pfile)
            log(f"✅ Fichier principal nettoyé — {len(keep_rows)} ligne(s) restante(s)")
            return len(done_rows)

        except PermissionError:
            time.sleep(3)

    log("❌ Fichier verrouillé — archivage impossible")
    return 0

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Créateur de lieux izilife — curation manuelle")
    parser.add_argument("--zone",    type=str, required=True,
                        help="Zone cible : lille, valenciennes, paris ...")
    parser.add_argument("--env",     choices=ENVS.keys(), default="local")
    parser.add_argument("--city",    type=str, default=None,
                        help="Ville par défaut si colonne 'ville' vide dans le xlsx")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--workbook", default="curate_places.xlsx",
                        help="Nom du classeur canonique dans le dossier de zone (défaut: curate_places.xlsx).")
    parser.add_argument("--sheet", default="Lieux",
                        help="Onglet à traiter (défaut: Lieux).")
    parser.add_argument("--legacy-layout", action="store_true",
                        help="Autoriser explicitement un ancien onglet sans ligne d'en-têtes.")
    parser.add_argument("--newness-sql", action="store_true",
                        help="Générer explicitement le SQL opening_date/is_new_in_city depuis les âges en semaines.")
    parser.add_argument("--no-maps-preflight", action="store_true",
                        help="Désactiver explicitement le précontrôle gratuit du nom dans Google Maps.")
    parser.add_argument("--clean-only", action="store_true",
                        help="Archiver les lignes terminales (done/unmapped/skip) sans appel API ni traitement.")
    parser.add_argument("--init",    action="store_true",
                        help="Créer le fichier xlsx template pour la zone")
    args = parser.parse_args()
    set_current_env(args.env)

    if args.init:
        create_template(args.zone)
        return


    if not args.city and not args.clean_only:
        print("❌ --city obligatoire sauf avec --init ou --clean-only")
        sys.exit(1)

    env     = ENVS[args.env]
    zone    = args.zone.lower().strip()
    dry_run = args.dry_run

    log(f"=== createur_lieux.py — zone={zone} env={args.env} city={args.city}" +
        (" [DRY RUN]" if dry_run else "") + " ===")

    if AGENT_TOKEN == "METTRE_TOKEN_ICI" and not dry_run and not args.clean_only:
        log("❌ IZILIFE_AGENT_TOKEN non défini.")
        sys.exit(1)

    curate_file = get_curate_file(zone, args.workbook)
    if not curate_file.exists():
        log(f"❌ Fichier introuvable : {curate_file}")
        log(f"   Lance : python createur_lieux.py --zone={zone} --init")
        sys.exit(1)

    keep_vba = curate_file.suffix.lower() == ".xlsm"
    wb = openpyxl.load_workbook(curate_file, keep_vba=keep_vba)
    if args.sheet and args.sheet not in wb.sheetnames:
        log(f"❌ Onglet introuvable : {args.sheet}. Disponibles : {', '.join(wb.sheetnames)}")
        sys.exit(1)
    ws = wb[args.sheet] if args.sheet else wb.active
    if args.clean_only:
        archived = purge_done(zone, curate_file=curate_file, sheet_name=ws.title)
        log(f"✅ Nettoyage terminé : {archived} ligne(s) terminale(s) archivée(s), aucun appel API.")
        return

    # Nettoie aussi les anciens unmapped encore présents : ils appartiennent
    # désormais exclusivement à la file Valider Lieux du BO.
    if not dry_run:
        purge_done(zone, curate_file=curate_file, sheet_name=ws.title)
        wb = openpyxl.load_workbook(curate_file, keep_vba=keep_vba)
        ws = wb[args.sheet] if args.sheet else wb.active
    rows = read_pending_rows(ws, allow_headerless=args.legacy_layout)

    if not rows:
        log("✅ Aucun lieu pending.")
        return

    # Valider toutes les références de ville avant le premier appel Google ou
    # la première écriture. La colonne VILLE et --city contiennent toujours un
    # City.string_id (jamais un libellé ni un id numérique).
    city_slugs = {
        canonical_city_slug(row.get("ville", "").strip() or args.city.strip())
        for row in rows
    }
    invalid_cities = set() if dry_run else {
        city_slug
        for city_slug in sorted(city_slugs)
        if resolve_city_id(city_slug, env, strict=False) <= 0
    }
    if invalid_cities:
        log("⚠️ Villes ignorées pour ce passage : " + ", ".join(sorted(invalid_cities)))

    log(f"{len(rows)} lieu(x) à traiter")
    stats = {"done": 0, "unmapped": 0, "errors": 0}
    newness_sql = []
    blocked_categories: set[tuple[str, str]] = set()

    with MapsNameResolver(enabled=not args.no_maps_preflight) as maps:
        for row in rows:
            row_city = canonical_city_slug(row.get("ville", "").strip() or args.city.strip())
            if row_city in invalid_cities:
                if not dry_run:
                    update_row(ws, row["row_idx"], "error", row)
                    wb.save(curate_file)
                stats["errors"] += 1
                continue
            new_status = process_one(
                row, canonical_city_slug(args.city), env, dry_run,
                maps=maps, blocked_categories=blocked_categories,
            )
            if not dry_run:
                update_row(ws, row["row_idx"], new_status, row)
                wb.save(curate_file)
                entity_id = int(row.get("_entity_id") or 0)
                result_type = str(row.get("_result_type") or "").upper()
                if new_status == "done" and entity_id > 0 and result_type in ("SHOP", "PLACE") and "weeks_ago" in row:
                    table = "Shop" if result_type == "SHOP" else "Place"
                    opened = opening_monday(int(row["weeks_ago"])).isoformat()
                    label = str(row.get("nom", "")).replace("*/", "")
                    newness_sql.append(
                        f"UPDATE `{table}` SET `opening_date` = '{opened}', `is_new_in_city` = 1 "
                        f"WHERE `id` = {entity_id}; /* {label} — {row['weeks_ago']} semaines */"
                    )
            stats[new_status if new_status in stats else "errors"] += 1
            if not dry_run:
                sleep_random(*DELAY)

    # Archivage automatique des done vers logs/WXX/ après traitement
    if not dry_run:
        if args.newness_sql:
            sql_file = write_newness_sql(curate_file, ws.title, newness_sql)
            if sql_file:
                log(f"✅ SQL nouveautés : {sql_file}")
        purge_done(zone, curate_file=curate_file, sheet_name=ws.title)

    log(f"\n=== Résultat ===")
    log(f"  Créés      : {stats['done']}")
    log(f"  Unmapped   : {stats['unmapped']}  (à traiter dans le BO)")
    log(f"  Erreurs    : {stats['errors']}")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from agent_excel_logger import run_logged
    run_logged("curate_manuel_lieux", "places", main)
