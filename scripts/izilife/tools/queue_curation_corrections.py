from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from openpyxl import load_workbook


WORKBOOK = Path(r"G:\Mon Drive\agentic_workspace\izilife\places\lille-zone\ameliorateur.xlsx")


def main() -> None:
    backup = WORKBOOK.with_name(
        f"{WORKBOOK.stem}.backup-{datetime.now():%Y%m%d-%H%M%S}{WORKBOOK.suffix}"
    )
    shutil.copy2(WORKBOOK, backup)

    workbook = load_workbook(WORKBOOK)
    sheet = workbook["Prioritaires"]
    headers = {
        str(cell.value).strip().upper(): cell.column
        for cell in sheet[1]
        if cell.value is not None
    }

    queued = [
        {
            "STRING_ID": "les-toiles-du-nord",
            "TYPE": "PLACE",
            "IS_ACTIVE": 0,
            "LISTABLE": 0,
            "NOTES": "Désactivation demandée le 2026-11-07",
        },
        {
            "STRING_ID": "burger-king",
            "TYPE": "SHOP",
            "PRIMARY_CATEGORY_REF": "restaurant-rapide",
            "CATEGORY_REFS": "restaurant-rapide",
            "OTHER_CATEGORIES_MODE": "KEEP",
            "NOTES": "Catégorie existante ShopCategory #42",
        },
    ]

    for offset, values in enumerate(queued, start=2):
        for key, value in values.items():
            sheet.cell(row=offset, column=headers[key], value=value)
        sheet.cell(row=offset, column=headers["STATUT"], value="pending")
        sheet.cell(row=offset, column=headers["LAST_RESULT"], value=None)

    workbook.save(WORKBOOK)
    print(f"queued={len(queued)} backup={backup}")


if __name__ == "__main__":
    main()
