"""Résolution gratuite et identité partagée des lieux/pages iziLife.

Ce module ne réalise aucun appel Google Places payant. Il fournit le précontrôle
Google Maps via Playwright et une identité canonique réutilisable par les agents.
"""
from __future__ import annotations

import re
import unicodedata
from math import asin, cos, radians, sin, sqrt
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from urllib.parse import parse_qsl, quote_plus, urlencode, urlsplit, urlunsplit


TRACKING_PREFIXES = ("utm_", "igsh")
SOCIAL_HOSTS = {
    "facebook.com": "facebook",
    "www.facebook.com": "facebook",
    "instagram.com": "instagram",
    "www.instagram.com": "instagram",
    "tiktok.com": "tiktok",
    "www.tiktok.com": "tiktok",
    "linkedin.com": "linkedin",
    "www.linkedin.com": "linkedin",
}


def normalize_string_id(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", _fold(value)).strip("-")


def _fold(value: str) -> str:
    value = unicodedata.normalize("NFKD", str(value or ""))
    return "".join(char for char in value if not unicodedata.combining(char)).casefold()


def normalize_url(value: str) -> str:
    """Normalise une URL sans détruire le chemin qui identifie le compte/page."""
    value = str(value or "").strip()
    if not re.match(r"^https?://", value, re.I):
        return ""
    parsed = urlsplit(value)
    host = parsed.netloc.casefold().split("@")[-1]
    if host.startswith("www."):
        host = host[4:]
    if host.endswith(":80") and parsed.scheme.casefold() == "http":
        host = host[:-3]
    if host.endswith(":443") and parsed.scheme.casefold() == "https":
        host = host[:-4]
    query = urlencode([
        (key, val) for key, val in parse_qsl(parsed.query, keep_blank_values=True)
        if not key.casefold().startswith(TRACKING_PREFIXES)
    ])
    path = re.sub(r"/{2,}", "/", parsed.path).rstrip("/") or "/"
    return urlunsplit((parsed.scheme.casefold(), host, path, query, ""))


@dataclass(frozen=True)
class PlaceIdentity:
    google_place_id: str = ""
    string_id: str = ""
    name: str = ""
    address: str = ""
    city: str = ""
    latitude: float | None = None
    longitude: float | None = None
    website_urls: frozenset[str] = field(default_factory=frozenset)
    social_urls: frozenset[str] = field(default_factory=frozenset)

    @classmethod
    def build(cls, *, google_place_id: str = "", string_id: str = "", name: str = "",
              address: str = "", city: str = "", latitude=None, longitude=None,
              urls: list[str] | tuple[str, ...] = ()) -> "PlaceIdentity":
        websites: set[str] = set()
        socials: set[str] = set()
        for raw in urls:
            url = normalize_url(raw)
            if not url:
                continue
            host = urlsplit(url).netloc
            (socials if host in SOCIAL_HOSTS else websites).add(url)
        return cls(
            google_place_id=str(google_place_id or "").strip(),
            string_id=normalize_string_id(string_id),
            name=re.sub(r"[^a-z0-9]+", " ", _fold(name)).strip(),
            address=re.sub(r"[^a-z0-9]+", " ", _fold(address)).strip(),
            city=normalize_string_id(city),
            latitude=cls._coordinate(latitude), longitude=cls._coordinate(longitude),
            website_urls=frozenset(websites),
            social_urls=frozenset(socials),
        )

    def duplicate_reason(self, other: "PlaceIdentity") -> str:
        if self.google_place_id and self.google_place_id == other.google_place_id:
            return "google_place_id"
        if self.string_id and self.string_id == other.string_id:
            return "string_id"
        if self.website_urls & other.website_urls:
            return "website_url"
        if self.social_urls & other.social_urls:
            return "social_url"
        same_name = bool(self.name and self.name == other.name)
        if self.address and self.address == other.address and (same_name or not self.name or not other.name):
            return "name_address" if same_name else "address"
        distance = self.distance_meters(other)
        if same_name and distance is not None and distance <= 80:
            return "name_coordinates"
        return ""

    @staticmethod
    def _coordinate(value) -> float | None:
        try:
            return float(value) if value not in (None, "") else None
        except (TypeError, ValueError):
            return None

    def distance_meters(self, other: "PlaceIdentity") -> float | None:
        if None in (self.latitude, self.longitude, other.latitude, other.longitude):
            return None
        lat1, lon1, lat2, lon2 = map(radians, (self.latitude, self.longitude, other.latitude, other.longitude))
        dlat, dlon = lat2-lat1, lon2-lon1
        value = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
        return 12_742_000 * asin(sqrt(value))

    def lookup_payload(self) -> dict:
        return {key:value for key,value in {
            "google_place_id":self.google_place_id, "string_id":self.string_id,
            "name":self.name, "query":self.name, "address":self.address, "city":self.city,
            "latitude":self.latitude, "longitude":self.longitude,
            "urls":sorted(self.website_urls | self.social_urls),
        }.items() if value not in (None, "", [])}


@dataclass(frozen=True)
class MapsResolution:
    requested_name: str
    canonical_name: str = ""
    status: str = "unresolved"
    google_place_id: str = ""
    address: str = ""
    latitude: float | None = None
    longitude: float | None = None
    business_status: str = "UNKNOWN"
    maps_url: str = ""

    @property
    def is_permanently_closed(self) -> bool:
        return self.business_status == "CLOSED_PERMANENTLY"


class MapsNameResolver:
    """Précontrôle gratuit du nom public avant tout appel Google Places payant."""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self._manager = self._browser = self._page = None
        self.last_city_confirmed = False
        self.last_result = MapsResolution(requested_name="", status="disabled" if not enabled else "unresolved")

    def __enter__(self):
        if not self.enabled:
            return self
        from playwright.sync_api import sync_playwright
        self._manager = sync_playwright().start()
        self._browser = self._manager.chromium.launch(
            headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = self._browser.new_context(locale="fr-FR", timezone_id="Europe/Paris")
        self._page = context.new_page()
        self._page.set_default_timeout(5_000)
        self._page.set_default_navigation_timeout(20_000)
        return self

    def __exit__(self, exc_type, exc, traceback):
        if self._browser:
            self._browser.close()
        if self._manager:
            self._manager.stop()

    @staticmethod
    def _clean_title(value: str) -> str:
        value = re.sub(r"\s+", " ", str(value or "")).strip()
        return re.sub(r"\s*[-–—]\s*Google Maps\s*$", "", value, flags=re.I).strip()

    @staticmethod
    def names_are_compatible(requested: str, candidate: str) -> bool:
        def normalized(value: str) -> str:
            value = re.sub(r"[^a-z0-9]+", " ", _fold(value)).strip()
            value = re.sub(r"\bhotel de ville\b", "mairie", value)
            return re.sub(r"\bbibliotheque(?: municipale)?\b", "mediatheque", value)
        left, right = normalized(requested), normalized(candidate)
        if not left or not right:
            return False
        if "," in str(requested):
            left = normalized(str(requested).split(",", 1)[1])
        if left in right or right in left:
            return True
        left_tokens, right_tokens = set(left.split()), set(right.split())
        shared = left_tokens & right_tokens
        token_score = len(shared) / max(1, min(len(left_tokens), len(right_tokens)))
        generic = {"centre", "maison", "espace", "salle", "mediatheque", "bibliotheque", "municipale"}
        stopwords = {"de", "du", "des", "la", "le", "les", "d", "et"}
        initials = "".join(token[0] for token in right.split() if token not in stopwords)
        acronyms = {token for token in left.split() if 2 <= len(token) <= 6}
        return (SequenceMatcher(None, left, right).ratio() >= .68
                or (token_score >= .66 and bool(shared - generic))
                or initials in acronyms
                or "mediatheque" in left_tokens & right_tokens)

    @staticmethod
    def needs_city_confirmation(requested: str, candidate: str) -> bool:
        tokens = lambda value: set(re.sub(r"[^a-z0-9]+", " ", _fold(value)).split())
        generic = {"centre", "culturel", "maison", "espace", "salle", "municipal", "municipale",
                   "mediatheque", "bibliotheque", "mairie", "hotel", "ville", "de", "du", "des",
                   "la", "le", "les", "d", "et"}
        return not bool((tokens(requested) & tokens(candidate)) - generic)

    @staticmethod
    def _is_invalid_candidate(value: str) -> bool:
        cleaned = str(value or "").strip()
        if not cleaned or cleaned.casefold() in {"sponsorisé", "sponsorise", "résultats", "results", "google maps"}:
            return True
        return bool(re.match(r"^\d+\s+(?:rue|avenue|boulevard|place|allée|allee|chemin)\b", cleaned, re.I))

    def resolve(self, name: str, city: str, notes: str = "") -> tuple[str, str]:
        if not self.enabled or self._page is None:
            self.last_result = MapsResolution(requested_name=name, canonical_name=name, status="disabled")
            return name, "disabled"
        url = "https://www.google.com/maps/search/?api=1&query=" + quote_plus(
            " ".join(part for part in (name, city) if str(part).strip()))
        try:
            self.last_city_confirmed = False
            self._page.goto(url, wait_until="domcontentloaded", timeout=20_000)
            self._page.wait_for_timeout(1_200)
            for label in ("Tout accepter", "Accepter tout"):
                button = self._page.get_by_role("button", name=label)
                if button.count():
                    button.first.click(timeout=2_000)
                    self._page.wait_for_timeout(500)
                    break
            try:
                self._page.locator("h1.DUwDvf, a.hfpxzc").first.wait_for(state="attached", timeout=5_000)
            except Exception:
                pass
            selected_label = ""
            selected_href = ""
            # Une recherche Maps peut rester sur une liste. Sélectionner le lien
            # compatible sans l'ouvrir : son URL contient déjà l'identité Maps
            # et évite une seconde navigation fragile/inutile.
            if not self._page.locator("h1.DUwDvf").count():
                results = self._page.locator("a.hfpxzc")
                for index in range(min(results.count(), 8)):
                    link = results.nth(index)
                    label = (link.get_attribute("aria-label") or "").strip()
                    if label and self.names_are_compatible(name, label):
                        selected_label = label
                        selected_href = link.get_attribute("href") or ""
                        break
            body_text = re.sub(r"\s+", " ", self._page.locator("body").inner_text())
            current_url = selected_href or self._page.url
            place_id = ""
            candidate_urls = [current_url, *self._page.locator("a[href*='query_place_id=']").evaluate_all("els => els.map(e => e.href)")]
            canonical = self._page.locator("link[rel='canonical']")
            if canonical.count():
                candidate_urls.append(canonical.first.get_attribute("href") or "")
            for candidate_url in candidate_urls:
                match = re.search(r"(?:query_place_id=|!1s)([^&!]+)", str(candidate_url))
                if match:
                    from urllib.parse import unquote
                    decoded = unquote(match.group(1)).strip()
                    if decoded.startswith("ChIJ"):
                        place_id = decoded
                        break
            if not place_id:
                pid_nodes = self._page.locator("[data-pid]")
                for index in range(min(pid_nodes.count(), 20)):
                    value = (pid_nodes.nth(index).get_attribute("data-pid") or "").strip()
                    if value.startswith("ChIJ"):
                        place_id = value
                        break
            if not place_id:
                html_source = self._page.content()
                embedded = re.search(r'\bChIJ[A-Za-z0-9_-]{12,}\b', html_source)
                if embedded:
                    place_id = embedded.group(0)
            address = ""
            for selector in ("button[data-item-id='address']", "[data-item-id='address']"):
                locator = self._page.locator(selector)
                if locator.count():
                    address = re.sub(r"^Adresse\s*:\s*", "", locator.first.get_attribute("aria-label") or locator.first.inner_text()).strip()
                    if address:
                        break
            # Les coordonnées `/@lat,lon` et `og:image?center=` désignent souvent
            # la caméra/zone de recherche, pas l'établissement. Seuls les
            # paramètres internes `!3d...!4d...` identifient le point précis.
            coordinate_match = re.search(r"!3d(-?\d+(?:\.\d+)?)!4d(-?\d+(?:\.\d+)?)", current_url)
            latitude = float(coordinate_match.group(1)) if coordinate_match else None
            longitude = float(coordinate_match.group(2)) if coordinate_match else None
            folded_body = _fold(body_text)
            business_status = ("CLOSED_PERMANENTLY" if any(marker in folded_body for marker in
                ("ferme definitivement", "definitivement ferme", "permanently closed")) else
                "CLOSED_TEMPORARILY" if any(marker in folded_body for marker in
                ("ferme temporairement", "temporarily closed")) else "OPERATIONAL")
            self.last_city_confirmed = re.sub(r"[^a-z0-9]+", " ", _fold(city)).strip() in re.sub(
                r"[^a-z0-9]+", " ", _fold(body_text)).strip()
            for selector in ("h1.DUwDvf", "div[role='main'] h1", "h1"):
                locator = self._page.locator(selector)
                if locator.count():
                    candidate = self._clean_title(locator.first.inner_text(timeout=2_000))
                    if not self._is_invalid_candidate(candidate):
                        self.last_result = MapsResolution(name, candidate, "maps_heading", place_id, address,
                                                          latitude, longitude, business_status, current_url)
                        return candidate, "maps_heading"
            candidate = self._clean_title(selected_label or (self._page.title() if address or place_id else ""))
            if not self._is_invalid_candidate(candidate):
                self.last_result = MapsResolution(name, candidate, "maps_title", place_id, address,
                                                  latitude, longitude, business_status, current_url)
                return candidate, "maps_title"
            if "aucun résultat" in body_text.casefold() or "no results" in body_text.casefold():
                self.last_result = MapsResolution(name, status="no_result", maps_url=current_url)
                return "", "no_result"
            self.last_result = MapsResolution(name, status="unresolved", maps_url=current_url)
            return "", "unresolved"
        except Exception as exc:
            self.last_result = MapsResolution(name, status=f"browser_error:{type(exc).__name__}")
            return "", f"browser_error:{type(exc).__name__}"
