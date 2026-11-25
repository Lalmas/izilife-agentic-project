import argparse
import unittest
from unittest.mock import patch

from validate_event_tmp import DEFAULT_CANDIDATE_LIMIT, apply_time_fallbacks, clean_html, main


class EventValidatorTests(unittest.TestCase):
    def test_contextual_end_fallback_and_overnight_date(self):
        proposal = apply_time_fallbacks(
            {"start_date": "2026-11-14", "start_hour": "20:00", "title": "Soirée blind test"},
            {}, ["heure_fin"],
        )
        self.assertEqual("02:00", proposal["end_hour"])
        self.assertEqual("2026-11-15", proposal["end_date"])

    def test_daytime_end_fallback_is_not_end_of_day(self):
        proposal = apply_time_fallbacks(
            {"start_date": "2026-11-14", "start_hour": "10:00", "title": "Visite guidée"},
            {}, ["heure_fin"],
        )
        self.assertEqual("18:00", proposal["end_hour"])

    def test_clean_html_removes_scripts_and_tags(self):
        self.assertEqual(clean_html('<h1>Concert</h1><script>bad()</script><p>20 h</p>'), 'Concert 20 h')

    def test_default_run_requests_the_full_backend_batch(self):
        captured = {}

        def fake_run(args: argparse.Namespace):
            captured['limit'] = args.limit
            captured['include_representations'] = args.include_representations
            return {'events': []}

        with patch('validate_event_tmp.run', side_effect=fake_run), \
                patch('validate_event_tmp.Path.write_text'), \
                patch('validate_event_tmp.Path.mkdir'), \
                patch('validate_event_tmp.sys.argv', ['validate_event_tmp.py']):
            self.assertEqual(main(), 0)

        self.assertEqual(captured['limit'], DEFAULT_CANDIDATE_LIMIT)
        self.assertTrue(captured['include_representations'])


if __name__ == '__main__':
    unittest.main()
