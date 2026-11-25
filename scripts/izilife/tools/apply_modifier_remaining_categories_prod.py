from __future__ import annotations

import json
import os

import requests


BASE = "https://www.izilife.co/izilife-admin/scraper"
CHANGES = [
    ("SHOP", "so-jump-trampoline-park-lille-lesquin", "salle-de-sport"),
    ("SHOP", "le-fronton-citi", "salle-de-sport"),
]


def call(path: str, payload: dict[str, object], token: str, *, form_payload: bool = False) -> dict[str, object]:
    body = {"data": {"payload": json.dumps(payload, ensure_ascii=False)}} if form_payload else {"json": payload}
    response = requests.post(
        f"{BASE}/{path}",
        headers={"X-Agent-Token": token, "Accept": "application/json"},
        timeout=60,
        **body,
    )
    result = response.json()
    if response.status_code >= 400 or not result.get("success"):
        raise RuntimeError(f"{path}: HTTP {response.status_code}: {result}")
    return result


def main() -> None:
    token = os.environ.get("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise SystemExit("IZILIFE_AGENT_TOKEN absent")
    results = []
    for scope_type, scope_ref, category_ref in CHANGES:
        applied = call(
            "agentMaintainLocation",
            {"scope_type": scope_type, "scope_ref": scope_ref, "primary_category_ref": category_ref},
            token,
            form_payload=True,
        )
        inspected = call("agentCurationSyncInspect", {"scope_type": scope_type, "scope_ref": scope_ref}, token)
        identity = ((inspected.get("graph") or {}).get("identity") or {})
        actual = identity.get("primary_category_ref")
        if actual != category_ref:
            raise RuntimeError(f"{scope_type}/{scope_ref}: catégorie attendue {category_ref}, obtenue {actual}")
        results.append({"scope": f"{scope_type}/{scope_ref}", "category_ref": actual, "apply": applied})
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
