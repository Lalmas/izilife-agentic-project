from __future__ import annotations
import argparse, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "offers"))
from offer_agent_common import create_workbook, drive_workspace_root, normalize_zone, process

FILE, SHEET = "experiences.xlsx", "Experiences"
COLUMNS = [
    ("title", "offer"), ("experience_string_id", "scope"), ("city_ref", "scope"),
    ("description", "offer"), ("short_description", "offer"), ("experience_type_ref", "offer"),
    ("experience_theme", "offer"), ("principal_activity_category_ref", "offer"),
    ("access_type_ref", "access"), ("booking_needed_ref", "access"), ("access_link", "access"),
    ("price_text", "access"), ("basic_price", "access"), ("duration", "access"),
    ("duration_measurement_unity_id", "access"), ("place_ref", "scope"), ("shop_ref", "scope"),
    ("phone_number", "access"), ("exterior", "bpr"), ("with_equipment", "bpr"),
    ("equipment_gived", "bpr"), ("is_nocturnal", "bpr"), ("noise_level", "bpr"),
    ("participation_mode", "bpr"), ("minimal_age", "bpr"),
    ("minimal_number_of_people", "bpr"), ("maximal_number_of_people", "bpr"),
    ("is_for_kids", "bpr"), ("accessible_for_kids", "bpr"),
    ("is_insolite", "bpr"), ("is_nocturnal", "bpr"), ("experience_in_all_city", "bpr"),
    ("place_visit", "bpr"), ("source_url", "access"), ("status", "result"),
    ("notes", "result"), ("last_result", "result"),
]


def payload(row: dict) -> dict:
    return {key: row.get(key) for key, _ in COLUMNS if key not in {"status", "notes", "last_result"}}


def main() -> None:
    parser = argparse.ArgumentParser(description="Création/upsert manuel d'expériences, une ligne Excel par expérience.")
    parser.add_argument("--zone", required=True)
    parser.add_argument("--env", choices=["local", "staging", "prod"], default="local")
    parser.add_argument("--init", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max", type=int, default=100)
    args = parser.parse_args()
    path = drive_workspace_root(args.env) / "izilife" / "experiences" / normalize_zone(args.zone) / FILE
    if args.init:
        example = {
            "title": "Expérience exemple", "experience_string_id": "experience-exemple", "city_ref": "lille",
            "description": "", "short_description": "", "experience_type_ref": "",
            "experience_theme": "sortie", "principal_activity_category_ref": "",
            "access_type_ref": "", "booking_needed_ref": "", "access_link": "", "price_text": "",
            "basic_price": "0", "duration": "1", "duration_measurement_unity_id": "2",
            "exterior": "non", "with_equipment": "non", "equipment_gived": "non",
            "is_nocturnal": "non", "noise_level": "0", "participation_mode": "individual",
            "minimal_age": "", "minimal_number_of_people": "", "maximal_number_of_people": "",
            "place_ref": "", "shop_ref": "", "phone_number": "", "is_for_kids": "non",
            "accessible_for_kids": "non", "is_insolite": "non", "is_nocturnal": "non",
            "experience_in_all_city": "oui", "place_visit": "non", "source_url": "",
            "status": "skip", "notes": "Renseigner les string_id des types/référentiels. URL conservée comme source. Création inactive pour contrôle BO.",
            "last_result": "",
        }
        create_workbook(path, SHEET, COLUMNS, example, {
            "is_for_kids": ["oui", "non"], "accessible_for_kids": ["oui", "non"],
            "exterior": ["oui", "non"], "with_equipment": ["oui", "non"],
            "equipment_gived": ["oui", "non"], "is_nocturnal": ["oui", "non"],
            "is_insolite": ["oui", "non"],
            "experience_in_all_city": ["oui", "non"], "place_visit": ["oui", "non"],
            "participation_mode": ["individual", "private_group", "open_group"],
            "status": ["pending", "done", "error", "skip"],
        })
        return
    process(path, SHEET, args.env, "/scraper/agentUpsertExperience", payload, args.dry_run, args.max)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from agent_excel_logger import run_logged
    run_logged("experiences", "experiences", main)
