import unittest
from unittest.mock import patch

from commercial_center_sync import belongs_to_center, build_plan, choose_google_candidate, official_category


class CommercialCenterSyncTest(unittest.TestCase):
    def test_maps_official_fashion_category(self):
        self.assertEqual("magasin-de-vetements", official_category({"name": "Example", "source_categories": ["mode-femme"]}))

    def test_rejects_homonym_outside_center(self):
        self.assertIsNone(choose_google_candidate("Miniso", [
            {"name": "MINISO Lille Flandres", "address": "Place de la Gare, 59800 Lille"},
        ], "lille", "LILLENIUM"))

    def test_accepts_lillenium_address(self):
        candidate = {"name": "NAYA", "address": "Centre commercial Lillenium, 2 rue du Faubourg des Postes, Lille"}
        self.assertEqual(candidate, choose_google_candidate("Naya", [candidate], "lille", "LILLENIUM"))

    def test_rejects_wrong_city_even_with_brand(self):
        self.assertFalse(belongs_to_center("Triumph Lillenium", "220 rue de l'Artisanat, Seclin", "lille", "LILLENIUM"))

    def test_accepts_v2_valmy_address(self):
        self.assertTrue(belongs_to_center("Bershka", "Boulevard de Valmy, Villeneuve-d'Ascq", "villeneuve-d-ascq", "AUSHOPPING V2"))

    def test_duplicate_google_place_is_not_applied_twice(self):
        class Api:
            def post(self, endpoint, payload):
                if payload.get("scope_type") == "PLACE":
                    return {"graph": {"identity": {"source_id": 82}}}
                if payload.get("google_place_id"):
                    return {"status": "missing"}
                return {"status": "google_candidates", "candidates": [{
                    "google_place_id": "same", "name": payload["query"],
                    "address": "Centre commercial Lillenium, Lille",
                }]}

        inventory = {"commerces": [
            {"center": "LILLENIUM", "inside_center": True, "center_scope_ref": "lillenium", "name": "Same", "candidates": []},
            {"center": "LILLENIUM", "inside_center": True, "center_scope_ref": "lillenium", "name": "Same", "candidates": []},
        ]}
        actions = build_plan(inventory, Api(), "prod", {"LILLENIUM"})["actions"]
        self.assertEqual("CREATE_OR_ATTACH_GOOGLE", actions[0]["action"])
        self.assertEqual("DUPLICATE_INVENTORY", actions[1]["action"])


if __name__ == "__main__":
    unittest.main()
