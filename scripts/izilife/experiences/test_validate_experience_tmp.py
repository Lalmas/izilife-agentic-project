import unittest
from unittest.mock import patch

from validate_experience_tmp import sanitize_expired_schedule


class ExpiredScheduleSanitationTest(unittest.TestCase):
    @patch("validate_experience_tmp.date")
    def test_expired_schedule_is_archived_and_removed(self, mocked_date):
        mocked_date.today.return_value = __import__("datetime").date(2026, 11, 8)
        mocked_date.fromisoformat.side_effect = __import__("datetime").date.fromisoformat
        proposal = {"experience": {
            "title": "Atelier stable",
            "session_configuration": {"dates": ["2026-10-24"]},
            "session_contents": [{"day_list": [6], "hour_list": ["14:00"]}],
        }}
        result = sanitize_expired_schedule(proposal)["experience"]
        self.assertIsNone(result["session_configuration"])
        self.assertEqual([], result["session_contents"])
        self.assertEqual("all_explicit_dates_expired", result["ignored_expired_schedule"]["reason"])

    @patch("validate_experience_tmp.date")
    def test_future_schedule_is_preserved(self, mocked_date):
        mocked_date.today.return_value = __import__("datetime").date(2026, 11, 8)
        mocked_date.fromisoformat.side_effect = __import__("datetime").date.fromisoformat
        proposal = {"session_configuration": {"dates": ["2026-12-01"]}, "session_contents": [{"day_list": [2]}]}
        result = sanitize_expired_schedule(proposal)
        self.assertEqual({"dates": ["2026-12-01"]}, result["session_configuration"])
        self.assertNotIn("ignored_expired_schedule", result)

    def test_orphan_session_contents_are_removed(self):
        proposal = {"experience": {"session_configuration": None, "session_contents": [
            {"day_list": [1, 2], "hour_list": ["09:00", "18:00"]}
        ]}}
        result = sanitize_expired_schedule(proposal)["experience"]
        self.assertEqual([], result["session_contents"])
        self.assertIn("without an explicit session_configuration", result["session_warnings"][0])


if __name__ == "__main__":
    unittest.main()
