from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from openpyxl import load_workbook


AMELIORATEUR = Path(r"G:\Mon Drive\agentic_workspace\izilife\places\lille-zone\ameliorateur.xlsx")
TRANSFERS = Path(r"G:\Mon Drive\agentic_workspace\izilife\transfers\lille-zone\transfers.xlsx")


MAINTENANCE = [
    dict(STRING_ID="haze-franck", TYPE="SHOP", IS_ACTIVE=0, LISTABLE=0,
         FERME_DEFINITIVEMENT="oui", NOTES="Modifier ligne 38"),
    dict(STRING_ID="akaviva", TYPE="PLACE", IS_ACTIVE=0, LISTABLE=0,
         FERME_DEFINITIVEMENT="oui", NOTES="Modifier lignes 39/57 dédupliquées"),
    dict(STRING_ID="mosaic-le-jardin-des-cultures", TYPE="PLACE", IS_ACTIVE=0, LISTABLE=0,
         FERME_DEFINITIVEMENT="oui", NOTES="Modifier ligne 40"),
    dict(STRING_ID="l-atelier-du-gourmet-burger-friterie-evenementiel", TYPE="SHOP",
         IS_ACTIVE=0, LISTABLE=0, FERME_DEFINITIVEMENT="oui", NOTES="Modifier ligne 61"),
    dict(STRING_ID="l-albatros", TYPE="SHOP", PRIMARY_CATEGORY_REF="bar-tabac",
         CATEGORY_REFS="bar-tabac", OTHER_CATEGORIES_MODE="REPLACE", NOTES="Modifier ligne 16"),
    dict(STRING_ID="auberge-du-forgeron-restaurant-gastronomique-bistro-et-hotel-de-charme",
         TYPE="SHOP", PRIMARY_CATEGORY_REF="restaurant", CATEGORY_REFS="restaurant,bar,hotel",
         OTHER_CATEGORY_REFS="bar,hotel", OTHER_CATEGORIES_MODE="REPLACE",
         NOTES="Modifier ligne 18"),
    dict(STRING_ID="l-expresso", TYPE="SHOP", PRIMARY_CATEGORY_REF="brasserie",
         CATEGORY_REFS="brasserie", OTHER_CATEGORIES_MODE="REPLACE", NOTES="Modifier ligne 19"),
    dict(STRING_ID="hippopotamus-steakhouse-seclin", TYPE="SHOP", PRIMARY_CATEGORY_REF="restaurant",
         CATEGORY_REFS="restaurant", OTHER_CATEGORIES_MODE="REPLACE", NOTES="Modifier ligne 20"),
    dict(STRING_ID="maxipinball-flipper-flechette-babyfoot", TYPE="SHOP",
         PRIMARY_CATEGORY_REF="salle-de-jeux-videos", CATEGORY_REFS="salle-de-jeux-videos",
         OTHER_CATEGORIES_MODE="REPLACE", NOTES="Modifier ligne 21"),
    dict(STRING_ID="au-bureau-pub-et-brasserie", TYPE="SHOP", PRIMARY_CATEGORY_REF="brasserie",
         CATEGORY_REFS="brasserie,bar,pub", OTHER_CATEGORY_REFS="bar,pub",
         OTHER_CATEGORIES_MODE="REPLACE", NOTES="Modifier ligne 22"),
    dict(STRING_ID="zen-motor-s", TYPE="SHOP", PRIMARY_CATEGORY_REF="brasserie",
         CATEGORY_REFS="brasserie,bar", OTHER_CATEGORY_REFS="bar",
         OTHER_CATEGORIES_MODE="REPLACE", NOTES="Modifier ligne 23"),
    dict(STRING_ID="la-scene", TYPE="SHOP", PRIMARY_CATEGORY_REF="restaurant",
         CATEGORY_REFS="restaurant,bar", OTHER_CATEGORY_REFS="bar",
         OTHER_CATEGORIES_MODE="REPLACE", NOTES="Modifier ligne 24"),
    dict(STRING_ID="la-petite-terrasse-restaurant-brasserie", TYPE="SHOP",
         PRIMARY_CATEGORY_REF="restaurant", CATEGORY_REFS="restaurant",
         OTHER_CATEGORIES_MODE="REPLACE", NOTES="Modifier ligne 25"),
    dict(STRING_ID="buvette-rouge", TYPE="SHOP", PRIMARY_CATEGORY_REF="bar",
         CATEGORY_REFS="bar", OTHER_CATEGORIES_MODE="REPLACE",
         CITY_REF="phalempin", NOTES="Modifier ligne 27"),
    dict(STRING_ID="le-potager-des-demoiselles", TYPE="SHOP", PRIMARY_CATEGORY_REF="restaurant",
         CATEGORY_REFS="restaurant", OTHER_CATEGORIES_MODE="REPLACE",
         CITY_REF="vendeville", NOTES="Modifier ligne 28"),
    dict(STRING_ID="bar-myst", TYPE="SHOP", CITY_REF="faches-thumesnil", NOTES="Modifier ligne 33"),
    dict(STRING_ID="les-enfants-gourmands", TYPE="SHOP", CITY_REF="phalempin", NOTES="Modifier ligne 34"),
    dict(STRING_ID="lame-au-vert-restaurant-avelin", TYPE="SHOP", CITY_REF="avelin", NOTES="Modifier ligne 35"),
    dict(STRING_ID="gulli-parc-lille-vendeville", TYPE="PLACE", CITY_REF="vendeville", NOTES="Modifier ligne 36"),
    dict(STRING_ID="le-club-cafe", TYPE="SHOP", PRIMARY_CATEGORY_REF="cafe",
         CATEGORY_REFS="cafe", OTHER_CATEGORIES_MODE="REPLACE",
         NOTES="Modifier ligne 42; médias traités séparément"),
    dict(STRING_ID="l-orangerie", TYPE="SHOP", CLOSED_STATE_REF="ferme-temporairement",
         PRIMARY_CATEGORY_REF="cafe", CATEGORY_REFS="cafe,bar", OTHER_CATEGORY_REFS="bar",
         OTHER_CATEGORIES_MODE="REPLACE", NOTES="Modifier lignes 43/48 dédupliquées"),
    dict(STRING_ID="mirage", TYPE="SHOP", PRIMARY_CATEGORY_REF="bar-lounge",
         CATEGORY_REFS="bar-lounge", OTHER_CATEGORIES_MODE="REPLACE", NOTES="Modifier ligne 44"),
]


TRANSFERS_DATA = [
    dict(SOURCE_TYPE="SHOP", SOURCE_REF="iberica",
         DESTINATION_TYPE="PLACE", DESTINATION_MODE="CREATE", DESTINATION_NAME="Ibérica",
         DESTINATION_CATEGORY_REF="espace-evenementiel", ACTIVATE_DESTINATION="OUI"),
    dict(SOURCE_TYPE="SHOP", SOURCE_REF="cageot-bar-restaurants-en-circuit-court-a-lille",
         DESTINATION_TYPE="PLACE", DESTINATION_MODE="CREATE", DESTINATION_NAME="Cageot",
         DESTINATION_CATEGORY_REF="food-court", ACTIVATE_DESTINATION="OUI"),
    *[
        dict(SOURCE_TYPE="PLACE", SOURCE_REF=ref, DESTINATION_TYPE="EQUIPMENT",
             DESTINATION_MODE="CREATE", DESTINATION_NAME=name,
             DESTINATION_CATEGORY_REF="aire-de-jeux-enfants", ACTIVATE_DESTINATION="OUI")
        for ref, name in [
            ("aire-de-jeu-du-parc-lebas", "Aire de jeu du parc Lebas"),
            ("aire-de-jeux-du-centre-marcel-bertrand", "Aire de jeux du centre Marcel Bertrand"),
            ("aire-de-jeux-pour-enfants-de-la-plaine-des-vachers", "Aire de jeux de la plaine des Vachers"),
            ("terrain-de-jeu-du-square-augustin-laurent", "Terrain de jeu du square Augustin Laurent"),
            ("aire-de-jeux-parvis-wagner", "Aire de jeux du parvis Wagner"),
            ("aire-de-jeux-hlm-michelet", "Aire de jeux HLM Michelet"),
            ("aire-de-jeux-de-l-abbaye-de-loos", "Aire de jeux de l'abbaye de Loos"),
            ("aire-de-jeux-de-la-plaine-des-sports-grimonprez", "Aire de jeux de la plaine des sports Grimonprez"),
        ]
    ],
]


def backup(path: Path) -> Path:
    target = path.with_name(f"{path.stem}.backup-modifier-{datetime.now():%Y%m%d-%H%M%S}{path.suffix}")
    shutil.copy2(path, target)
    return target


def queue(path: Path, sheet_name: str, rows: list[dict]) -> tuple[Path, int]:
    saved = backup(path)
    wb = load_workbook(path)
    ws = wb[sheet_name]
    headers = {str(c.value).strip().upper(): c.column for c in ws[1] if c.value is not None}
    # Chaque lot remplace le précédent. Nettoyer toutes les cellules de données
    # évite qu'une catégorie, un statut ou un résultat d'un ancien objet soit
    # réutilisé silencieusement par une nouvelle ligne plus courte.
    for row_index in range(2, max(ws.max_row, len(rows) + 1) + 1):
        for column_index in headers.values():
            ws.cell(row_index, column_index).value = None
    for index, values in enumerate(rows, 2):
        for key, value in values.items():
            ws.cell(index, headers[key], value)
        ws.cell(index, headers["ACTION"], "PLAN") if "ACTION" in headers else None
        ws.cell(index, headers["STATUT" if "STATUT" in headers else "STATUS"], "pending")
        if "LAST_RESULT" in headers:
            ws.cell(index, headers["LAST_RESULT"], None)
    wb.save(path)
    return saved, len(rows)


def main() -> None:
    ameliorateur_backup, maintenance_count = queue(AMELIORATEUR, "Prioritaires", MAINTENANCE)
    transfers_backup, transfer_count = queue(TRANSFERS, "Transferts", TRANSFERS_DATA)
    print(f"maintenance={maintenance_count} backup={ameliorateur_backup}")
    print(f"transfers={transfer_count} backup={transfers_backup}")


if __name__ == "__main__":
    main()
