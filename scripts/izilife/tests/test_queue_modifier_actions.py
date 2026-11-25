from __future__ import annotations

import importlib.util
from pathlib import Path

from openpyxl import Workbook, load_workbook


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "queue_modifier_actions_20261107.py"
SPEC = importlib.util.spec_from_file_location("queue_modifier_actions", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_queue_clears_stale_values(tmp_path: Path) -> None:
    path = tmp_path / "pilot.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Prioritaires"
    ws.append(["STRING_ID", "TYPE", "PRIMARY_CATEGORY_REF", "STATUT", "LAST_RESULT"])
    ws.append(["old", "SHOP", "restaurant", "done", "old result"])
    wb.save(path)

    MODULE.queue(path, "Prioritaires", [{"STRING_ID": "new", "TYPE": "PLACE"}])

    out = load_workbook(path)["Prioritaires"]
    assert out["A2"].value == "new"
    assert out["B2"].value == "PLACE"
    assert out["C2"].value is None
    assert out["D2"].value == "pending"
    assert out["E2"].value is None
