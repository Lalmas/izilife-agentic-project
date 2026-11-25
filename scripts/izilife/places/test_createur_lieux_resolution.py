import unittest
from unittest.mock import patch

import createur_lieux
from core.place_resolution import MapsResolution


class FakeMaps:
    last_city_confirmed = True

    def __init__(self, result):
        self.last_result = result

    def resolve(self, name, city, notes=""):
        return self.last_result.canonical_name, self.last_result.status

    names_are_compatible = staticmethod(lambda requested, candidate: True)
    needs_city_confirmation = staticmethod(lambda requested, candidate: False)


class CreateurLieuxResolutionTest(unittest.TestCase):
    def test_existing_izilife_object_stops_before_paid_endpoint(self):
        row = {"nom": "Musée Test", "ville": "lille", "type_impose": "PLACE",
               "category_string_id": "musee"}
        maps = FakeMaps(MapsResolution("Musée Test", "Musée Test", "maps_heading",
                                       google_place_id="ChIJ-test", business_status="OPERATIONAL"))
        with patch.object(createur_lieux, "lookup_existing_place", return_value={
            "id": 42, "type": "PLACE", "string_id": "musee-test"
        }), patch.object(createur_lieux, "izilife_post") as paid:
            self.assertEqual("done", createur_lieux.process_one(row, "lille", {}, False, maps))
            paid.assert_not_called()

    def test_missing_object_uses_maps_place_id_hint(self):
        row = {"nom": "Musée Test", "ville": "lille", "type_impose": "PLACE",
               "category_string_id": "musee"}
        maps = FakeMaps(MapsResolution("Musée Test", "Musée Test", "maps_heading",
                                       google_place_id="ChIJ-test", business_status="OPERATIONAL"))
        response = {"success": True, "result_type": "PLACE", "entity_id": 7,
                    "string_id": "musee-test", "name": "Musée Test"}
        with patch.object(createur_lieux, "lookup_existing_place", return_value=None), \
             patch.object(createur_lieux, "izilife_post", return_value=response) as paid:
            self.assertEqual("done", createur_lieux.process_one(row, "lille", {}, False, maps))
            self.assertEqual("ChIJ-test", paid.call_args.args[1]["google_place_id_hint"])

    def test_permanent_closure_stops_all_api_calls(self):
        row = {"nom": "Musée Fermé", "ville": "lille"}
        maps = FakeMaps(MapsResolution("Musée Fermé", "Musée Fermé", "maps_heading",
                                       business_status="CLOSED_PERMANENTLY"))
        with patch.object(createur_lieux, "lookup_existing_place") as lookup, \
             patch.object(createur_lieux, "izilife_post") as paid:
            self.assertEqual("error", createur_lieux.process_one(row, "lille", {}, False, maps))
            lookup.assert_not_called()
            paid.assert_not_called()


if __name__ == "__main__":
    unittest.main()
