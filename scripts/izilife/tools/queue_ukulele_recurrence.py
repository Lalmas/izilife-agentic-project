from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from openpyxl import load_workbook


WORKBOOK = Path(r"G:\Mon Drive\agentic_workspace\izilife\events\lille-zone\event_structures.xlsx")


def main() -> None:
    backup = WORKBOOK.with_name(
        f"{WORKBOOK.stem}.backup-{datetime.now():%Y%m%d-%H%M%S}{WORKBOOK.suffix}"
    )
    shutil.copy2(WORKBOOK, backup)
    workbook = load_workbook(WORKBOOK)
    sheet = workbook["Structures"]
    headers = {str(cell.value).strip(): cell.column for cell in sheet[1] if cell.value is not None}
    for column in range(1, sheet.max_column + 1):
        sheet.cell(row=2, column=column).value = None
    values = {
        "object_type": "RECURRENT_EVENT",
        "unique_id": "7d578ab0d8133a988186cd68ffe0614f",
        "name": "UKULELE PARTY !",
        "event_category_ref": "jam-session",
        "is_active": "oui",
        "listable": "oui",
        "start_date": "2026-11-07",
        "start_hour": "15:00",
        "end_date": "2026-11-07",
        "end_hour": "23:59",
        "recurrence_frequency": "MONTHLY",
        "recurrence_interval": 1,
        "recurrence_days": "SA",
        "recurrence_rrule": "FREQ=MONTHLY;INTERVAL=1;BYDAY=SA;BYSETPOS=1",
        "timezone_id": "Europe/Paris",
        "status": "pending",
        "notes": "Chaque premier samedi du mois",
    }
    for key, value in values.items():
        sheet.cell(row=2, column=headers[key], value=value)
    sheet.cell(row=2, column=headers["last_result"], value=None)
    workbook.save(WORKBOOK)
    print(f"queued=1 backup={backup}")


if __name__ == "__main__":
    main()
