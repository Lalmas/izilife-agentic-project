from __future__ import annotations

import mimetypes
import os
import re
import tempfile
from pathlib import Path
from urllib.parse import urljoin

import requests


DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"
PHOTO_URL = "https://maps.googleapis.com/maps/api/place/photo"
UPLOAD_URL = "https://www.izilife.co/izilife-admin/scraper/agentAddScopedMedia"

TARGETS = [
    ("PLACE", "le-flow-centre-euroregional-des-cultures-urbaines", "ChIJs4I0HpTVwkcRrLj0rtST6mM"),
    ("PLACE", "wag-studio-dance-ecole-de-danse-lille", "ChIJex_mHF3VwkcRSmO4olUcZ08"),
    ("PLACE", "arawak-21-galerie-d-art-itinerante", "ChIJATtN1XHVwkcR5r9AwSug-hU"),
    ("PLACE", "prison-island-lille-lesquin", "ChIJY99svnrXwkcRg1cusKQqzSU"),
    ("PLACE", "bump-games-lille-lezennes", "ChIJWTp4HjzXwkcRPPTmrPIPpkY"),
]

OFFICIAL_FALLBACKS = {
    "arawak-21-galerie-d-art-itinerante": "https://www.arawak21.fr/",
}


def main() -> None:
    api_key = os.environ["GOOGLE_KEY_API"].strip()
    token = os.environ["IZILIFE_AGENT_TOKEN"].strip()
    headers = {"X-Agent-Token": token, "Accept": "application/json"}
    for scope_type, scope_ref, place_id in TARGETS:
        details_response = requests.get(
            DETAILS_URL,
            params={"place_id": place_id, "fields": "name,photos", "language": "fr", "key": api_key},
            timeout=60,
        )
        details_response.raise_for_status()
        body = details_response.json()
        photos = (body.get("result") or {}).get("photos") or []
        source_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
        if photos:
            photo_reference = photos[0].get("photo_reference")
            image_response = requests.get(
                PHOTO_URL,
                params={"maxwidth": 1200, "photoreference": photo_reference, "key": api_key},
                timeout=90,
            )
        else:
            source_url = OFFICIAL_FALLBACKS.get(scope_ref, "")
            if not source_url:
                print(scope_ref, "NO_PHOTO", body.get("status"))
                continue
            page = requests.get(source_url, timeout=60)
            page.raise_for_status()
            meta_match = re.search(
                r'<meta[^>]+(?:property|name)=["\'](?:og:image|twitter:image)["\'][^>]+content=["\']([^"\']+)',
                page.text,
                re.I,
            )
            if not meta_match:
                meta_match = re.search(
                    r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\'](?:og:image|twitter:image)["\']',
                    page.text,
                    re.I,
                )
            image_url = meta_match.group(1) if meta_match else ""
            if not image_url:
                image_match = re.search(r'<img[^>]+src=["\']([^"\']+)', page.text, re.I)
                image_url = image_match.group(1) if image_match else ""
            if not image_url:
                print(scope_ref, "NO_OFFICIAL_PHOTO")
                continue
            image_response = requests.get(urljoin(source_url, image_url), timeout=90)
        image_response.raise_for_status()
        mime = image_response.headers.get("Content-Type", "image/jpeg").split(";", 1)[0]
        suffix = mimetypes.guess_extension(mime) or ".jpg"
        with tempfile.TemporaryDirectory(prefix="modifier_google_") as tmp:
            path = Path(tmp) / f"{scope_ref}{suffix}"
            path.write_bytes(image_response.content)
            with path.open("rb") as handle:
                upload_response = requests.post(
                    UPLOAD_URL,
                    data={
                        "scope_type": scope_type,
                        "scope_ref": scope_ref,
                        "belongs_to_scope": "oui",
                        "rights_confirmed": "oui",
                        "is_principal": "oui",
                        "title": (body.get("result") or {}).get("name") or scope_ref,
                        "source_url": source_url,
                    },
                    files={"media": (path.name, handle, mime)},
                    headers=headers,
                    timeout=240,
                )
            try:
                result = upload_response.json()
            except Exception:
                result = {"success": False, "error": upload_response.text[:300]}
            print(scope_ref, upload_response.status_code, result)


if __name__ == "__main__":
    main()
