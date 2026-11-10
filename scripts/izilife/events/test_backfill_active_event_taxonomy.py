import argparse
import unittest
from unittest.mock import patch

from backfill_active_event_taxonomy import build_duplicate_pairs, filter_quality_events, has_occurrence_doubt


class ActiveEventTaxonomyBackfillTests(unittest.TestCase):
    def test_duplicate_pairs_are_collapsed_and_linked(self):
        rows = [
            {"id": 10, "title": "Heure du conte", "event_start_hour": "10:00", "event_end_hour": "10:30",
             "basic_price": 0, "is_free_event": 1, "bo_url": "https://bo/event/10", "event_media_count": 1,
             "quality_evidence": {"duplicate_candidates": [{"event_id": 11, "similarity": 1, "certainty": "certain"}]}},
            {"id": 11, "title": "Heure du conte", "event_start_hour": "10:00", "event_end_hour": "10:30",
             "basic_price": 0, "is_free_event": 1, "bo_url": "https://bo/event/11", "event_media_count": 0,
             "quality_evidence": {"duplicate_candidates": [{"event_id": 10, "similarity": 1, "certainty": "certain"}]}},
        ]
        pairs = build_duplicate_pairs(rows)
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0]["decision"], "ready_to_archive_duplicate")
        self.assertEqual(pairs[0]["recommended_keeper"]["event_id"], 10)

    def test_duplicate_conflict_requires_manual_merge(self):
        rows = [
            {"id": 20, "title": "Romain", "event_start_hour": "19:00", "event_end_hour": "23:59",
             "basic_price": 16, "is_free_event": 0, "quality_evidence": {"duplicate_candidates": [
                 {"event_id": 21, "similarity": 1, "certainty": "certain"}]}},
            {"id": 21, "title": "Romain", "event_start_hour": "19:00", "event_end_hour": "23:59",
             "basic_price": 20, "is_free_event": 0, "quality_evidence": {"duplicate_candidates": []}},
        ]
        pair = build_duplicate_pairs(rows)[0]
        self.assertIn("basic_price", pair["data_conflicts"])
        self.assertEqual(pair["decision"], "manual_merge_required")

    def test_occurrence_doubt_blocks_automatic_apply(self):
        self.assertTrue(has_occurrence_doubt({
            "doubts": [{"field": "occurrences", "reason": "dates_to_split_or_reclassify"}]
        }))

    def test_taxonomy_only_proposal_is_applicable(self):
        self.assertFalse(has_occurrence_doubt({
            "principal_activity_category_ref": "litterature", "doubts": []
        }))

    def test_named_quality_focuses_are_distinct(self):
        rows = [
            {"id": 1, "quality_reasons": ["probable_semantic_duplicate"]},
            {"id": 2, "quality_reasons": ["representation_media_missing"]},
            {"id": 3, "quality_reasons": ["paid_without_access_link"]},
            {"id": 4, "quality_reasons": ["false_free_with_commercial_evidence"]},
            {"id": 5, "quality_reasons": ["free_without_explicit_evidence"]},
        ]
        self.assertEqual([row["id"] for row in filter_quality_events(rows, "duplicates")], [1])
        self.assertEqual([row["id"] for row in filter_quality_events(rows, "representation-media")], [2])
        self.assertEqual([row["id"] for row in filter_quality_events(rows, "paid-without-link")], [3])
        self.assertEqual([row["id"] for row in filter_quality_events(rows, "false-free")], [4, 5])
        self.assertEqual([row["id"] for row in filter_quality_events(rows, "pricing")], [3, 4, 5])
        self.assertEqual(filter_quality_events(rows, "all"), rows)

    def test_pricing_candidates_are_repaired_not_only_reported(self):
        class Client:
            calls = []

            def __init__(self, *args):
                pass

            def quality_candidates(self, limit, event_id=None):
                return [{"id": 41, "quality_reasons": ["false_free_with_commercial_evidence"]}]

            def repair_event_pricing(self, event_id, dry_run):
                self.calls.append((event_id, dry_run))
                return {"event_id": event_id, "status": "ready" if dry_run else "repaired"}

        args = argparse.Namespace(
            env="local", mode="review", event_id=None, limit=10, allow_ai=False,
            taxonomy_only=False, quality_only=True, quality_focus="false-free",
            apply_duplicates=False, min_confidence=.9,
        )
        with patch("backfill_active_event_taxonomy.TaxonomyClient", Client), \
             patch.dict("backfill_active_event_taxonomy.IZILIFE_ENVS", {
                 "local": {"base_url": "http://example.test", "verify_ssl": True}
             }), patch.dict("backfill_active_event_taxonomy.os.environ", {"IZILIFE_AGENT_TOKEN": "test"}):
            report = __import__("backfill_active_event_taxonomy").run(args)
        self.assertEqual(Client.calls, [(41, True)])
        self.assertEqual(report["pricing_recovery"][0]["status"], "ready")


if __name__ == "__main__":
    unittest.main()
