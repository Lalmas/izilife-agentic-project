import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from intelligent_enricher import (build_apply_payload, classify_restaurant, compact_current_izilife,
                                  compact_references, review_required, validate_proposal)


class IntelligentEnricherTest(unittest.TestCase):
    def test_unknown_references_are_rejected(self):
        refs = {
            "tags": [{"string_id": "familial"}],
            "principal_characteristics": ["is_accessible"],
            "editorial": {"MusicStyle": [{"string_id": "jazz"}]},
        }
        proposal = {
            "tags": [{"string_id": "familial"}, {"string_id": "invente"}],
            "principal_characteristics": [{"field": "is_accessible", "value": 1}],
            "editorial": {"MusicStyle": [{"string_id": "jazz"}, {"string_id": "metal-invente"}]},
        }
        result = validate_proposal(proposal, refs)
        self.assertEqual(1, len(result["tags"]))
        self.assertEqual(1, len(result["principal_characteristics"]))
        self.assertEqual(1, len(result["editorial"]["MusicStyle"]))
        self.assertEqual(2, len(result["rejected"]))

    def test_apply_payload_keeps_only_confident_validated_values(self):
        proposal = {
            "tags": [
                {"string_id": "terrasse", "confidence": 0.91},
                {"string_id": "bruyant", "confidence": 0.55},
            ],
            "principal_characteristics": [
                {"field": "have_terrace", "value": 1, "confidence": 0.9},
            ],
            "editorial": {
                "MusicStyle": [
                    {"string_id": "jazz", "confidence": 0.88},
                    {"string_id": "rock", "confidence": 0.6},
                ],
            },
        }
        payload = build_apply_payload(proposal, "SHOP", "test-shop", 0.8)
        self.assertEqual(["terrasse"], payload["tags"])
        self.assertEqual({"have_terrace": 1}, payload["principal_characteristics"])
        self.assertEqual({"MusicStyle": ["jazz"]}, payload["editorial"])

    def test_live_evidence_must_be_an_exact_non_speculative_quote(self):
        refs = {
            "tags": [],
            "principal_characteristics": ["adapted_to_family", "is_for_children"],
            "editorial": {},
        }
        pages = [{
            "url": "https://example.test/service",
            "text": "Cette prestation est accessible aux familles. Réservée aux adultes uniquement.",
        }]
        proposal = {
            "principal_characteristics": [
                {"field": "adapted_to_family", "value": 1, "source_url": pages[0]["url"],
                 "evidence": "Cette prestation est accessible aux familles."},
                {"field": "is_for_children", "value": 0, "source_url": pages[0]["url"],
                 "evidence": "No mention of children services."},
            ]
        }
        result = validate_proposal(proposal, refs, pages)
        self.assertEqual(["adapted_to_family"],
                         [row["field"] for row in result["principal_characteristics"]])
        self.assertEqual("preuve absente ou déductive", result["rejected"][0]["reason"])

    def test_prompt_inputs_are_compacted(self):
        refs = {
            "tags": [{"string_id": "familial", "name": "Familial", "tag_types": "SHOP"}],
            "principal_characteristics": ["adapted_to_family"],
            "editorial": {"MusicStyle": [{"string_id": "jazz", "name": "Jazz",
                                              "scope_types": "PLACE,SHOP"}]},
        }
        self.assertEqual(["familial | Familial"], compact_references("SHOP", refs)["tags"])
        compact = compact_current_izilife({"type": "SHOP", "data": {"name": "Test", "mail": "x@y"},
                                           "counts": {"media": 1}, "graph": {"media": [1], "ambiences": [2]}})
        self.assertEqual("Test", compact["identity"]["name"])
        self.assertNotIn("mail", compact["identity"])
        self.assertNotIn("media", compact["editorial_state"])

    def test_restaurant_profiles_are_not_conflated(self):
        gastro=classify_restaurant([{"text":"Notre restaurant gastronomique propose un menu dégustation.","url":"https://x"}])
        fast=classify_restaurant([{"text":"Restauration rapide, commande au comptoir et à emporter.","url":"https://x"}])
        table=classify_restaurant([{"text":"Un service à table est assuré chaque soir.","url":"https://x"}])
        self.assertEqual("restaurant-gastronomique",gastro["primary_category_ref"])
        self.assertEqual("restaurant-rapide",fast["primary_category_ref"])
        self.assertEqual("restaurant",table["primary_category_ref"])

    def test_confidence_alone_never_requires_human_review(self):
        self.assertFalse(review_required({"rejected":[],"warnings":[],"tags":[{"confidence":.51}]}))
        self.assertTrue(review_required({"rejected":[{"reason":"référence inconnue"}],"warnings":[]}))


if __name__ == "__main__":
    unittest.main()
