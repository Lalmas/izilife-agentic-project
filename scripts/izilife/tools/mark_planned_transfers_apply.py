from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from openpyxl import load_workbook


PILOT = Path(r"G:\Mon Drive\agentic_workspace\izilife\transfers\lille-zone\transfers.xlsx")


def main() -> None:
    backup = PILOT.with_name(
        f"{PILOT.stem}.backup-before-apply-{datetime.now():%Y%m%d-%H%M%S}{PILOT.suffix}"
    )
    shutil.copy2(PILOT, backup)

    workbook = load_workbook(PILOT)
    sheet = workbook["Transferts"]
    headers = {
        str(cell.value).strip().upper(): cell.column
        for cell in sheet[1]
        if cell.value is not None
    }

    selected = []
    for row in range(2, sheet.max_row + 1):
        if str(sheet.cell(row, headers["CAN_APPLY"]).value).strip().upper() != "OUI":
            continue
        if str(sheet.cell(row, headers["STATUS"]).value).strip().lower() != "planned":
            continue
        sheet.cell(row, headers["ACTION"], "APPLY")
        sheet.cell(row, headers["STATUS"], "pending")
        selected.append(str(sheet.cell(row, headers["SOURCE_REF"]).value))

    workbook.save(PILOT)
    print(f"backup={backup}")
    print(f"selected={len(selected)}")
    for ref in selected:
        print(ref)


if __name__ == "__main__":
    main()
