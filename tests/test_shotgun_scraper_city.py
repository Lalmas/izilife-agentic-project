import importlib.util
import unittest
from unittest.mock import Mock, patch
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "izilife" / "events" / "shotgun_scraper.py"
SPEC = importlib.util.spec_from_file_location("shotgun_scraper", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def event_html(locality=None, latitude=None, longitude=None):
    address = "" if locality is None else f'"address": {{"addressLocality": "{locality}"}}'
    geo = "" if latitude is None else f', "geo": {{"latitude": {latitude}, "longitude": {longitude}}}'
    return f'''<html><head><script type="application/ld+json">
    {{"@type": "Event", "name": "Test", "location": {{{address}{geo}}}}}
    </script></head></html>'''


class ShotgunCityFilterTest(unittest.TestCase):
    def test_accepts_matching_lille_locality(self):
        self.assertEqual(MODULE.event_matches_city(event_html("Lille"), "lille"), (True, ["Lille"]))

    def test_accepts_accent_and_case_variants(self):
        self.assertEqual(MODULE.normalize_place_name("Saint-Étienne"), "saint-etienne")

    def test_rejects_bordeaux_for_lille(self):
        self.assertEqual(MODULE.event_matches_city(event_html("Bordeaux"), "lille"), (False, ["Bordeaux"]))

    def test_rejects_saint_etienne_for_lille(self):
        self.assertEqual(MODULE.event_matches_city(event_html("Saint-Étienne", 45.4397, 4.3872), "lille"), (False, ["Saint-Étienne"]))

    def test_accepts_lille_metropolitan_area(self):
        self.assertEqual(MODULE.event_matches_city(event_html("Englos", 50.625, 2.956), "lille"), (True, ["Englos"]))
        self.assertEqual(MODULE.event_matches_city(event_html("Pecq", 50.686, 3.337), "lille"), (True, ["Pecq"]))

    def test_missing_locality_does_not_drop_event(self):
        self.assertEqual(MODULE.event_matches_city(event_html(), "lille"), (True, []))

    @patch.object(MODULE.requests, "post")
    def test_pending_urls_are_loaded_before_upload(self, post):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "success": True,
            "events": [
                {"source_url": "https://shotgun.live/fr/events/already-there"},
                {"source_url": ""},
            ],
        }
        post.return_value = response
        self.assertEqual(
            MODULE.pending_source_urls("https://admin.test", 1, True),
            {"https://shotgun.live/fr/events/already-there"},
        )


if __name__ == "__main__":
    unittest.main()
