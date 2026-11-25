import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).parents[1] / "scripts" / "izilife" / "places" / "enrichment_validation_agent.py"
SPEC = importlib.util.spec_from_file_location("enrichment_validation_agent", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PayloadDecisionTest(unittest.TestCase):
    def test_confidence_only_is_rejected(self):
        self.assertFalse(MODULE.has_business_changes({"confidence": 0.9}))
        self.assertFalse(MODULE.has_business_changes({"confidence_score": 0.5, "scalar": {}, "satellites": {}}))
        self.assertFalse(MODULE.has_business_changes({"principal_characteristics": {"play_music": 0}}))
        self.assertFalse(MODULE.has_business_changes({"suggested_new_tags": ["inventé"]}))

    def test_business_values_are_applied(self):
        self.assertTrue(MODULE.has_business_changes({"principal_characteristics": {"play_music": 1}}))
        self.assertTrue(MODULE.has_business_changes({"satellites": {"Atmosphere": [{"string_id": "cosy"}]}}))
        self.assertTrue(MODULE.has_business_changes({"scalar": {"short_description": "Adresse conviviale"}}))

    def test_false_principal_value_is_not_actionable(self):
        self.assertFalse(MODULE.has_business_changes({"principal_characteristics": {"have_terrace": False}}))

    def test_place_website_is_not_actionable_because_place_has_no_column(self):
        payload = {"scalar": {"website": "https://example.test"}}
        self.assertFalse(MODULE.has_business_changes(payload, "PLACE"))
        self.assertTrue(MODULE.has_business_changes(payload, "SHOP"))


if __name__ == "__main__":
    unittest.main()
