import json
from pathlib import Path

root = Path(r"C:\Users\alcamara\Documents\agentic_Workspace\outputs\intelligent_improver_20261112")
data = json.loads((root / "preparation_report.json").read_text(encoding="utf-8"))
seen = set()
targets = []
for item in data["resolved"]:
    key = (item["type"], item["string_id"])
    if key in seen:
        continue
    seen.add(key)
    targets.append({
        "scope_type": item["type"],
        "scope_ref": item["string_id"],
        "source_urls": [],
        "min_confidence": 0.8,
        "with_ai": True,
        "with_web_search": True,
        "source_cell": f"{item['source_column']}{item['source_row']}",
    })
output = root / "intelligent_targets.json"
output.write_text(json.dumps({
    "enabled_stages": ["google_hours", "intelligent"],
    "intelligent_targets": targets,
}, ensure_ascii=False, indent=2), encoding="utf-8")
print(output)
print(len(targets))
print(targets[:7])
