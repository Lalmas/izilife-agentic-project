import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "places" / "food_usage_classifier.py"
SPEC = importlib.util.spec_from_file_location("food_usage_classifier", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class FoodUsageClassifierTest(unittest.TestCase):
    def test_fast_onsite_maps_to_two_tags(self):
        tags, confidence, evidence, _ = MODULE.normalize({
            "consumption_onsite": "YES",
            "restaurant_style": "FAST",
            "confidence": 0.96,
            "evidence": [{"text": "Repas sur place et commande au comptoir", "url": "https://example.test"}],
        })
        self.assertEqual(["consommation-sur-place", "repas-sur-le-pouce"], tags)
        self.assertEqual(0.96, confidence)
        self.assertIn("commande au comptoir", evidence)

    def test_table_service_maps_to_moment_repas(self):
        tags, *_ = MODULE.normalize({
            "consumption_onsite": "YES", "restaurant_style": "TABLE_SERVICE",
            "confidence": 0.94, "evidence": [{"text": "Service à table"}],
        })
        self.assertEqual(["consommation-sur-place", "moment-repas-a-table"], tags)

    def test_negative_requires_explicit_evidence(self):
        tags, *_ = MODULE.normalize({
            "consumption_onsite": "NO", "restaurant_style": "FAST",
            "confidence": 0.91, "evidence": [{"text": "Aucune information sur une salle"}],
        })
        self.assertEqual(["repas-sur-le-pouce"], tags)

    def test_explicit_takeaway_only_can_be_negative(self):
        tags, *_ = MODULE.normalize({
            "consumption_onsite": "NO", "restaurant_style": "FAST",
            "confidence": 0.97, "evidence": [{"text": "Exclusivement à emporter"}],
        })
        self.assertEqual(["sans-consommation-sur-place", "repas-sur-le-pouce"], tags)


if __name__ == "__main__":
    unittest.main()
