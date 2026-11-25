import importlib.util
from pathlib import Path

MODULE = Path(__file__).with_name("validate_unmapped_pois.py")
SPEC = importlib.util.spec_from_file_location("validate_unmapped_pois", MODULE)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def test_import_requires_existing_category():
    ok, reason = mod.validate_proposal({
        "action": "IMPORT", "destination": "PLACE", "confidence": .99, "doubts": []
    }, .85)
    assert not ok and reason == "categorie_incomplete"


def test_deterministic_ignore_is_applicable():
    ok, reason = mod.validate_proposal({
        "action": "IGNORE", "confidence": 1, "doubts": []
    }, .85)
    assert ok and reason == ""


def test_doubts_block_apply():
    ok, reason = mod.validate_proposal({
        "action": "IMPORT", "destination": "SHOP", "category_string_id": "restaurant",
        "confidence": .99, "doubts": ["ambigu"],
    }, .85)
    assert not ok and reason == "doutes"


def test_extracts_official_website_only():
    assert mod.source_url({"json_payload": '{"websiteUri":"https://example.org/place"}'}) == "https://example.org/place"
    assert mod.source_url({"json_payload": '{"websiteUri":"javascript:alert(1)"}'}) == ""


def test_builds_google_maps_search_for_ambiguous_poi():
    url = mod.google_maps_url({"name":"Justice de Paix", "address":"Place du Général de Gaulle", "city_name":"Lille"})
    assert url.startswith("https://www.google.com/maps/search/")
    assert "Justice+de+Paix" in url
