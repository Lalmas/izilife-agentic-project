import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "izilife"))
from objects.object_agent_common import izilife_post

fixture = json.loads(Path(__file__).with_name("fixture.json").read_text(encoding="utf-8"))
entries = next(iter(fixture["sources"].values()))
result = {"checked": 0, "media_ok_or_existing": 0, "errors": []}
for entry in entries:
    payload = {
        "kind": "product", "scope_type": "SHOP", "scope_ref": "la-braise",
        "source_url": "https://www.labraiseseclin.com/menu", "item": entry["item"],
    }
    response = izilife_post("/scraper/agentIngestSiteItem", {"payload": json.dumps(payload, ensure_ascii=False)}, "prod", timeout=180)
    stats = response.get("stats", {}) if isinstance(response, dict) else {}
    errors = stats.get("media_errors", []) or []
    result["checked"] += 1
    if not errors:
        result["media_ok_or_existing"] += 1
    else:
        result["errors"].append({"name": entry["item"]["name"], "errors": errors})
print(json.dumps(result, ensure_ascii=False, indent=2))
