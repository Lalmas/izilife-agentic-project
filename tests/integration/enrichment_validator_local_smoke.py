from __future__ import annotations

import json
import os
import subprocess
import time
import uuid

import requests


MYSQL = r"C:\xampp\mysql\bin\mysql.exe"
BASE_URL = "https://localhost:4443/izilife-admin"
TOKEN = os.environ.get("IZILIFE_AGENT_TOKEN", "")


def sql(statement: str) -> str:
    result = subprocess.run(
        [MYSQL, "-u", "root", "-N", "-B", "-D", "izilife2", "-e", statement],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def quote(value: str) -> str:
    return "'" + value.replace("\\", "\\\\").replace("'", "''") + "'"


def insert_request(entity_type: str, entity_id: int, payload: dict) -> int:
    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    statement = f"""
        INSERT INTO validation_request
            (requester_type,agent_name,target_entity_type,action_type,target_entity_id,city_id,
             proposed_payload,risk_level,status,created_at,updated_at)
        VALUES
            ('AI_AGENT','enrichisseur',{quote(entity_type)},'ENRICH',{entity_id},1,
             {quote(encoded)},'MEDIUM','PENDING_REVIEW',NOW(),NOW());
        SELECT LAST_INSERT_ID();
    """
    return int(sql(statement).splitlines()[-1])


def post(endpoint: str, data: dict, expected_status: int = 200) -> dict:
    response = requests.post(
        BASE_URL + endpoint,
        data=data,
        headers={"X-Agent-Token": TOKEN},
        verify=False,
        timeout=60,
    )
    payload = response.json()
    if response.status_code != expected_status:
        raise AssertionError(f"{endpoint}: HTTP {response.status_code}, attendu {expected_status}: {payload}")
    return payload


def assert_equal(actual, expected, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: attendu {expected!r}, obtenu {actual!r}")


def main() -> None:
    if not TOKEN:
        raise RuntimeError("IZILIFE_AGENT_TOKEN non défini.")

    suffix = uuid.uuid4().hex[:10]
    shop_id = 0
    place_id = 0
    request_ids: list[int] = []
    try:
        shop_id = int(sql(f"""
            INSERT INTO Shop
                (name,shop_string_id,shop_type,shopCategory_id,self_delivery,city_id,is_active,listable,created)
            VALUES
                ('Codex validator smoke',{quote('codex-validator-' + suffix)},1,2,0,1,1,0,NOW());
            SELECT LAST_INSERT_ID();
        """).splitlines()[-1])
        place_id = int(sql(f"""
            INSERT INTO Place
                (name,place_string_id,place_type,address,zip_code,city_id,place_of_life,is_active,listable,created)
            VALUES
                ('Codex validator place',{quote('codex-validator-place-' + suffix)},1,'Test',59000,1,0,1,0,NOW());
            SELECT LAST_INSERT_ID();
        """).splitlines()[-1])

        confidence_id = insert_request("SHOP", shop_id, {"confidence": 0.9})
        applied_payload = {
            "scalar": {
                "short_description": "Description temporaire du test",
                "phone_number": "0102030405",
                "website": "https://example.test",
                "opening_hours_text": "Lundi 10h-18h",
            },
            "principal_characteristics": {"play_music": 1, "can_eat_here": 1, "wifi": 0},
            "satellites": {
                "Atmosphere": [{"string_id": "calme"}],
                "MusicStyle": [{"string_id": "afro"}],
                "BarType": [{"string_id": "bar-ambiance"}],
                "MealType": [{"string_id": "petit-dejeuner"}],
            },
            "confidence": 0.8,
        }
        applied_id = insert_request("SHOP", shop_id, applied_payload)
        duplicate_id = insert_request("SHOP", shop_id, applied_payload)
        invalid_id = insert_request("SHOP", shop_id, {
            "principal_characteristics": {"adapted_to_handicap": 1},
            "satellites": {"Atmosphere": [{"string_id": "reference-inexistante"}]},
            "confidence": 0.7,
        })
        obsolete_only_id = insert_request("SHOP", shop_id, {
            "satellites": {"Atmosphere": [{"string_id": "reference-inexistante"}]},
            "confidence": 0.7,
        })
        place_website_id = insert_request("PLACE", place_id, {
            "scalar": {"website": "https://place-without-column.test"},
            "confidence": 0.9,
        })
        child_payload = {
            "satellites": {
                "Equipment": [{"equipment_category_string_id": "table", "detectable": "smoke"}],
                "Terrace": [{
                    "waterfront": False, "roadside": True, "has_parasol": False,
                    "has_heater": False, "is_rooftop": False, "suggest_only": True,
                }],
            },
            "confidence": 0.8,
        }
        child_id = insert_request("SHOP", shop_id, child_payload)
        child_duplicate_id = insert_request("SHOP", shop_id, child_payload)
        request_ids = [
            confidence_id, applied_id, duplicate_id, invalid_id, obsolete_only_id, place_website_id,
            child_id, child_duplicate_id,
        ]

        candidates = post("/scraper/agentEnrichmentValidationCandidates", {"limit": 20, "city_id": 1})
        candidate_by_id = {int(item["id"]): item for item in candidates["items"]}
        for request_id in request_ids:
            if request_id not in candidate_by_id:
                raise AssertionError(f"Demande locale #{request_id} absente des candidats.")
        assert_equal(candidate_by_id[confidence_id]["has_business_changes"], False, "confidence-only")
        assert_equal(candidate_by_id[applied_id]["has_business_changes"], True, "payload métier")
        assert_equal(candidate_by_id[place_website_id]["has_business_changes"], False, "website PLACE non applicable")

        assert_equal(post("/scraper/agentProcessEnrichmentValidation", {"id": confidence_id})["decision"], "REJECTED", "rejet confidence")
        assert_equal(post("/scraper/agentProcessEnrichmentValidation", {"id": applied_id})["decision"], "APPLIED", "application métier")
        assert_equal(post("/scraper/agentProcessEnrichmentValidation", {"id": duplicate_id})["decision"], "APPLIED", "application idempotente")
        invalid_result = post("/scraper/agentProcessEnrichmentValidation", {"id": invalid_id})
        assert_equal(invalid_result["decision"], "APPLIED", "référence obsolète ignorée avec scalaire valide")
        obsolete_only_result = post("/scraper/agentProcessEnrichmentValidation", {"id": obsolete_only_id})
        assert_equal(obsolete_only_result["decision"], "REJECTED", "référence obsolète seule rejetée")
        assert_equal(post("/scraper/agentProcessEnrichmentValidation", {"id": place_website_id})["decision"], "REJECTED", "rejet champ non applicable")
        assert_equal(post("/scraper/agentProcessEnrichmentValidation", {"id": child_id})["decision"], "APPLIED", "création sous-demandes")
        assert_equal(post("/scraper/agentProcessEnrichmentValidation", {"id": child_duplicate_id})["decision"], "APPLIED", "déduplication sous-demandes")

        statuses = sql("SELECT CONCAT(id,':',status) FROM validation_request WHERE id IN (" + ",".join(map(str, request_ids)) + ") ORDER BY id")
        status_map = dict(line.split(":", 1) for line in statuses.splitlines())
        assert_equal(status_map[str(confidence_id)], "REJECTED", "statut confidence")
        assert_equal(status_map[str(applied_id)], "APPLIED", "statut applied")
        assert_equal(status_map[str(duplicate_id)], "APPLIED", "statut duplicate")
        assert_equal(status_map[str(invalid_id)], "APPLIED", "statut invalid partiel")
        assert_equal(status_map[str(obsolete_only_id)], "REJECTED", "statut obsolete-only")
        assert_equal(status_map[str(place_website_id)], "REJECTED", "statut place website")
        assert_equal(status_map[str(child_id)], "APPLIED", "statut child")
        assert_equal(status_map[str(child_duplicate_id)], "APPLIED", "statut child duplicate")

        shop = sql(f"SELECT short_description,phone_number,url_website,shop_hourly_text FROM Shop WHERE id={shop_id}").split("\t")
        assert_equal(shop, ["Description temporaire du test", "0102030405", "https://example.test", "Lundi 10h-18h"], "mapping scalaire")
        principal = sql(f"SELECT play_music,can_eat_here,wifi FROM PrincipalCharacteristics WHERE shop_id={shop_id}").split("\t")
        assert_equal(principal, ["1", "1", "0"], "caractéristiques principales")

        pivot_checks = {
            "ShopAtmosphere": "atmosphere_id=14",
            "ShopMusicStyle": "music_type_id=5",
            "ShopBarType": "bar_type_id=2",
            "ShopMealType": "meal_type_id=1",
        }
        for table, condition in pivot_checks.items():
            count = sql(f"SELECT COUNT(*) FROM {table} WHERE shop_id={shop_id} AND {condition}")
            assert_equal(count, "1", f"pivot {table} sans doublon")

        equipment_children = sql(f"""
            SELECT COUNT(*) FROM validation_request
            WHERE agent_name='enrichisseur' AND action_type='CREATE'
              AND target_entity_type='EQUIPMENT' AND target_entity_id={shop_id}
              AND proposed_payload LIKE '%equipment_category_string_id%table%'
        """)
        terrace_children = sql(f"""
            SELECT COUNT(*) FROM validation_request
            WHERE agent_name='enrichisseur' AND action_type='CREATE'
              AND target_entity_type='SHOP' AND target_entity_id={shop_id}
              AND proposed_payload LIKE '%_type%Terrace%'
        """)
        assert_equal(equipment_children, "1", "déduplication Equipment")
        assert_equal(terrace_children, "1", "déduplication Terrace")

        print(json.dumps({"success": True, "requests": request_ids}, ensure_ascii=False))
    finally:
        if shop_id:
            sql(f"DELETE FROM validation_request WHERE agent_name='enrichisseur' AND target_entity_id={shop_id}")
        if request_ids:
            sql("DELETE FROM validation_request WHERE id IN (" + ",".join(map(str, request_ids)) + ")")
        if shop_id:
            for table in ["ShopAtmosphere", "ShopMusicStyle", "ShopBarType", "ShopMealType"]:
                sql(f"DELETE FROM {table} WHERE shop_id={shop_id}")
            sql(f"DELETE FROM PrincipalCharacteristics WHERE shop_id={shop_id}")
            sql(f"DELETE FROM Shop WHERE id={shop_id}")
        if place_id:
            sql(f"DELETE FROM PrincipalCharacteristics WHERE place_id={place_id}")
            sql(f"DELETE FROM Place WHERE id={place_id}")


if __name__ == "__main__":
    main()
