from __future__ import annotations

import json
import os

import requests


BASE = "https://www.izilife.co/izilife-admin/scraper"
CHANGES = [
    ("SHOP", "buvette-rouge", "phalempin"),
    ("SHOP", "le-potager-des-demoiselles", "vendeville"),
    ("SHOP", "bar-myst", "faches-thumesnil"),
    ("SHOP", "les-enfants-gourmands", "phalempin"),
    ("SHOP", "lame-au-vert-restaurant-avelin", "avelin"),
    ("PLACE", "gulli-parc-lille-vendeville", "vendeville"),
]


def call(path: str, payload: dict[str, object], token: str, *, form_payload: bool = False) -> dict[str, object]:
    request_body = {"data": {"payload": json.dumps(payload, ensure_ascii=False)}} if form_payload else {"json": payload}
    response = requests.post(
        f"{BASE}/{path}",
        headers={"X-Agent-Token": token, "Accept": "application/json"},
        timeout=60,
        **request_body,
    )
    body = response.json()
    if response.status_code >= 400 or not body.get("success"):
        raise RuntimeError(f"{path}: HTTP {response.status_code}: {body}")
    return body


def main() -> None:
    token = os.environ.get("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise SystemExit("IZILIFE_AGENT_TOKEN absent")
    results = []
    for scope_type, scope_ref, city_ref in CHANGES:
        applied = call(
            "agentMaintainLocation",
            {"scope_type": scope_type, "scope_ref": scope_ref, "city_ref": city_ref},
            token,
            form_payload=True,
        )
        inspected = call(
            "agentCurationSyncInspect",
            {"scope_type": scope_type, "scope_ref": scope_ref},
            token,
        )
        actual = ((inspected.get("graph") or {}).get("identity") or {}).get("city_ref")
        if actual != city_ref:
            raise RuntimeError(f"{scope_type}/{scope_ref}: ville attendue {city_ref}, obtenue {actual}")
        results.append({"scope": f"{scope_type}/{scope_ref}", "city_ref": actual, "apply": applied})
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
