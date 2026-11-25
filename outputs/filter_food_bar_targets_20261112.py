from __future__ import annotations

import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

import openpyxl

ROOT = Path(r"C:\Users\alcamara\Documents\agentic_Workspace\outputs\intelligent_improver_20261112")
CONFIG = ROOT / "intelligent_targets.json"
OUTPUT = ROOT / "intelligent_targets_food_bar.json"
SOURCE = Path(r"C:\Users\alcamara\AppData\Local\Packages\sandbox.{d59ce699-2cf2-4dd8-bfce-0c0769eebb89}\AC\Temp\browser-use\exports\Curation - Démarchage.xlsm-d1747791-1fd5-4a1e-b8e9-c0c61da5c8f2.xlsx")
INVENTORY = Path(r"G:\Mon Drive\inventaire_maps_seclin_alentours.xlsx")

FOOD_GOOGLE_TERMS = (
    "restaurant", "food", "cafe", "bakery", "bar", "meal takeaway",
    "meal delivery", "night club",
)


def norm(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(ch for ch in text if not unicodedata.combining(ch)).lower()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


source = openpyxl.load_workbook(SOURCE, data_only=True)["Lieux Clean, Cur (Hor, Ph, ..)"]
inventory = openpyxl.load_workbook(INVENTORY, data_only=True)["Inventaire"]
headers = [str(cell.value or "").strip() for cell in inventory[1]]
pos = {name: index + 1 for index, name in enumerate(headers)}
identity_by_name: dict[str, list[tuple[str, str]]] = defaultdict(list)
for row in range(2, inventory.max_row + 1):
    name = norm(inventory.cell(row, pos["NOM"]).value)
    families = norm(inventory.cell(row, pos["FAMILLES_RECHERCHE"]).value)
    google_types = norm(inventory.cell(row, pos["GOOGLE_TYPES"]).value)
    if name:
        identity_by_name[name].append((families, google_types))

config = json.loads(CONFIG.read_text(encoding="utf-8"))
kept, excluded = [], []
for target in config["intelligent_targets"]:
    cell = str(target.get("source_cell") or "")
    match = re.fullmatch(r"([HI])(\d+)", cell)
    value = ""
    if match:
        column = 9 if match.group(1) == "I" else 8
        value = str(source.cell(int(match.group(2)), column).value or "").strip()

    include = False
    reason = ""
    if target["scope_type"] != "SHOP":
        reason = "scope_non_shop"
    elif cell.startswith("I"):
        include = target["scope_ref"] != "acropolis-bowling"
        reason = "priorite_I_alimentaire_bar" if include else "loisir_bowling"
    elif match and match.group(1) == "H" and int(match.group(2)) <= 50:
        # Ce premier bloc H avait déjà été préparé explicitement comme liste de
        # commerces de bouche. Les PLACE sont exclus par la règle ci-dessus.
        include = True
        reason = "bloc_H_commerces_bouche"
    else:
        identities = identity_by_name.get(norm(value), [])
        google_evidence = " ".join(types for _, types in identities)
        include = any(term in google_evidence for term in FOOD_GOOGLE_TERMS)
        reason = google_evidence if include else "google_type_non_alimentaire"

    row = target | {"source_value": value, "selection_reason": reason}
    (kept if include else excluded).append(row)

# Le Grenier vient d’être créé et appartient explicitement à la priorité I.
if not any(row["scope_ref"] == "le-grenier" for row in kept):
    kept.insert(3, {
        "scope_type": "SHOP", "scope_ref": "le-grenier", "source_urls": [],
        "min_confidence": 0.8, "with_ai": True, "with_web_search": True,
        "source_cell": "I5", "source_value": "Le grenier",
        "selection_reason": "priorite_I_restaurant",
    })

payload = {
    "google_hours_python": config["google_hours_python"],
    "continue_on_error": True,
    "enabled_stages": ["google_hours", "intelligent"],
    "intelligent_targets": kept,
}
OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
(ROOT / "excluded_non_food_bar.json").write_text(json.dumps(excluded, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"kept": len(kept), "excluded": len(excluded), "output": str(OUTPUT)}, ensure_ascii=False))
