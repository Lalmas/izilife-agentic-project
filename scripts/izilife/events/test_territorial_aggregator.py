import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch

from territorial_aggregator import (
    Candidate, canonical_url, discover_links, extract_jsonld_events, fingerprint,
    iso_date, iso_hour, send_new,
)


class TerritorialAggregatorTest(unittest.TestCase):
    def test_jds_source_starts_from_agenda_and_loads_more(self):
        config_path = Path(__file__).parent / "territorial_sources" / "lille-zone.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        jds = next(source for source in config["sources"] if source["name"] == "jds-lille")

        self.assertEqual("https://www.jds.fr/lille/agenda/", jds["url"])
        self.assertEqual(["Afficher plus de sorties à Lille"], jds["browser_actions"]["load_more_texts"])
        self.assertGreater(jds["browser_actions"]["max_rounds"], 1)

    def test_lille_config_contains_filtered_digital_platforms(self):
        config_path = Path(__file__).parent / "territorial_sources" / "lille-zone.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        sources = {source["name"]: source for source in config["sources"]}
        self.assertIn("fr--lille", sources["meetup-lille"]["url"])
        self.assertTrue(sources["meetup-lille"]["require_city"])
        self.assertIn("/ville/lille", sources["helloasso-lille"]["url"])
        self.assertTrue(sources["helloasso-lille"]["require_city"])

    def test_canonical_url_removes_tracking_and_fragment(self):
        self.assertEqual(
            canonical_url("https://Example.org/event/42/?utm_source=x&keep=1#buy"),
            "https://example.org/event/42?keep=1",
        )

    def test_fingerprint_keeps_different_sessions_distinct(self):
        first = Candidate("source", "https://e/1", "Même spectacle", "2026-12-01", "18:00", place_name="Salle")
        second = Candidate("source", "https://e/2", "Même spectacle", "2026-12-01", "21:00", place_name="Salle")
        self.assertNotEqual(fingerprint(first), fingerprint(second))

    def test_extract_jsonld_event(self):
        html = '''<script type="application/ld+json">{
          "@context":"https://schema.org","@type":"Event","name":"Concert test",
          "startDate":"2026-12-05T20:30:00+01:00","url":"https://example.org/e/1",
          "location":{"@type":"Place","name":"Le Lieu"},
          "offers":{"url":"https://tickets.example.org/1"}}
        </script>'''
        items = extract_jsonld_events(html, "https://example.org", "source", "lille")
        self.assertEqual(1, len(items))
        self.assertEqual("2026-12-05", items[0].start_date)
        self.assertEqual("20:30", items[0].start_hour)
        self.assertEqual("Le Lieu", items[0].place_name)

    def test_jsonld_city_overrides_default_city(self):
        html = '''<script type="application/ld+json">{
          "@type":"Event", "name":"Concert", "startDate":"2026-11-10T20:00:00",
          "url":"https://example.test/event/1",
          "location":{"name":"Salle", "address":{"addressLocality":"Roubaix"}}
        }</script>'''
        item = extract_jsonld_events(
            html, "https://example.test/event/1", "test", "Lille"
        )[0]
        self.assertEqual("Roubaix", item.city)

    def test_detail_links_are_prioritized(self):
        html = '''
          <a href="/evenements/categorie">Catégorie</a>
          <a href="/associations/source/evenement-concert-lille-9002569">Concert</a>
        '''
        links = discover_links(
            html, "https://www.infolocale.fr/evenements",
            ["/evenement-"], 1, r"/evenement-[^/?]+-\d+(?:$|\?)",
        )
        self.assertEqual(
            ["https://www.infolocale.fr/associations/source/evenement-concert-lille-9002569"],
            links,
        )

    def test_infolocale_compact_date_and_nested_city(self):
        self.assertEqual("2026-10-31", iso_date("20261031T200000"))
        self.assertEqual("20:00", iso_hour("20261031T200000"))
        html = '''<script type="application/ld+json">{
          "@type":"event", "name":"Mike D", "startDate":"20261031T200000",
          "url":"https://example.test/event/1",
          "location":{"name":"L'Aéronef", "address":{"addressLocality":{"nom":"Lille"}}}
        }</script>'''
        item = extract_jsonld_events(html, "https://example.test/event/1", "infolocale")[0]
        self.assertEqual("2026-10-31", item.start_date)
        self.assertEqual("20:00", item.start_hour)
        self.assertEqual("Lille", item.city)

    def test_send_new_uses_normalized_scraper_contract(self):
        item = Candidate(
            source="jds-lille",
            source_url="https://example.test/event",
            title="Test event",
            start_date="2026-11-07",
            detail_html="<html>event</html>",
            match_status="NEW",
            fingerprint="a" * 64,
        )
        captured = {}

        class Response:
            @staticmethod
            def raise_for_status():
                return None

            @staticmethod
            def json():
                return {"success": True, "results": [{
                    "success": True, "tmp_id": 42, "status": "pending_review",
                }]}

        def fake_post(url, **kwargs):
            captured["url"] = url
            captured.update(kwargs)
            return Response()

        with patch.dict(os.environ, {"IZILIFE_AGENT_TOKEN": "test-token"}), \
                patch("territorial_aggregator.resolve_city_id", return_value=1), \
                patch("territorial_aggregator.requests.post", side_effect=fake_post):
            self.assertEqual(1, send_new([item], "prod", "lille"))

        self.assertTrue(captured["url"].endswith("/scraper/agentUploadEventSources/1"))
        self.assertEqual(item.source_url, captured["data"]["source_urls[]"])
        self.assertIn("sources[]", captured["files"])
        self.assertEqual("SENT_TO_SCRAPER", item.match_status)
        self.assertIn("LLM", item.match_reason)


if __name__ == "__main__":
    unittest.main()
