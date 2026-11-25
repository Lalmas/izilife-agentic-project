from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests
from openpyxl import load_workbook


WORKBOOK = Path(r"G:\Mon Drive\Curation - Démarchage.xlsm")
ENDPOINT = "https://www.izilife.co/izilife-admin/scraper/agentCurationSyncInspect"


def url_identity(value: object) -> tuple[str, str] | None:
    text = str(value or "").strip()
    match = re.search(r"/(place|shop)/page/([^/?#]+)", urlparse(text).path, re.I)
    if not match:
        return None
    return match.group(1).upper(), match.group(2)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    token = os.environ.get("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise SystemExit("IZILIFE_AGENT_TOKEN absent")
    sheet = load_workbook(WORKBOOK, data_only=True, keep_vba=True)["Modifier"]
    results: list[dict[str, object]] = []
    for row in range(2, sheet.max_row + 1):
        identity = url_identity(sheet.cell(row, 1).value)
        if not identity:
            continue
        scope_type, scope_ref = identity
        response = requests.post(
            ENDPOINT,
            json={"scope_type": scope_type, "scope_ref": scope_ref},
            headers={"X-Agent-Token": token, "Accept": "application/json"},
            timeout=60,
        )
        body = response.json()
        graph = body.get("graph") or {}
        identity_data = graph.get("identity") or {}
        results.append(
            {
                "row": row,
                "scope_type": scope_type,
                "scope_ref": scope_ref,
                "instruction": sheet.cell(row, 2).value,
                "detail": sheet.cell(row, 3).value,
                "http": response.status_code,
                "success": body.get("success"),
                "match_status": body.get("match_status"),
                "identity": {
                    key: identity_data.get(key)
                    for key in (
                        "name", "is_active", "listable", "closed_state_ref",
                        "primary_category_ref", "city_ref", "in_on_place",
                        "principal_picture", "principal_cover", "cover_picture",
                    )
                },
                "counts": graph.get("counts") or {},
                "hours_count": len((graph.get("hours") or {}).get("sets") or []),
                "other_categories": graph.get("other_categories") or [],
            }
        )
    for item in results:
        identity = item["identity"]
        other_refs = [
            value
            for row in item["other_categories"]
            for key, value in row.items()
            if key.endswith("_ref") and value
        ]
        print(
            item["row"], item["scope_type"], item["scope_ref"],
            "instruction=", repr(item["instruction"]),
            "active=", identity.get("is_active"),
            "listable=", identity.get("listable"),
            "closed=", identity.get("closed_state_ref"),
            "category=", identity.get("primary_category_ref"),
            "other=", other_refs,
            "city=", identity.get("city_ref"),
            "media=", item["counts"].get("media"),
            "cover=", identity.get("principal_cover") or identity.get("cover_picture") or identity.get("principal_picture"),
            "hours=", item["hours_count"],
        )


if __name__ == "__main__":
    main()
