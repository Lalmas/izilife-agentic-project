import unittest

from core.place_resolution import MapsResolution, PlaceIdentity, normalize_url


class PlaceResolutionTest(unittest.TestCase):
    def test_tracking_is_removed_but_business_query_is_preserved(self):
        self.assertEqual(
            "https://example.org/lieu?lang=fr",
            normalize_url("HTTPS://EXAMPLE.ORG/lieu/?utm_source=x&lang=fr#bloc"),
        )

    def test_duplicate_priority_uses_stable_identifiers_then_urls(self):
        current = PlaceIdentity.build(
            google_place_id="ChIJ-1", string_id="Le Bal Arrangé",
            urls=["https://larose.fr/spectacles/le-bal-arrange", "https://instagram.com/la.rose/"],
        )
        self.assertEqual("google_place_id", current.duplicate_reason(
            PlaceIdentity.build(google_place_id="ChIJ-1")))
        self.assertEqual("string_id", current.duplicate_reason(
            PlaceIdentity.build(string_id="le-bal-arrange")))
        self.assertEqual("website_url", current.duplicate_reason(
            PlaceIdentity.build(urls=["https://larose.fr/spectacles/le-bal-arrange/?utm_medium=x"])))
        self.assertEqual("social_url", current.duplicate_reason(
            PlaceIdentity.build(urls=["https://www.instagram.com/la.rose"])))

    def test_closed_maps_result_is_explicit(self):
        result = MapsResolution("Lieu", "Lieu", "maps_heading", business_status="CLOSED_PERMANENTLY")
        self.assertTrue(result.is_permanently_closed)

    def test_name_address_and_coordinates_are_shared_duplicate_keys(self):
        left = PlaceIdentity.build(name="Palais des Beaux-Arts", address="Place de la République", latitude=50.63107, longitude=3.06269)
        by_address = PlaceIdentity.build(name="Palais des Beaux Arts", address="Place de la Republique")
        nearby = PlaceIdentity.build(name="Palais des Beaux-Arts", latitude=50.63110, longitude=3.06272)
        self.assertEqual("name_address", left.duplicate_reason(by_address))
        self.assertEqual("name_coordinates", left.duplicate_reason(nearby))

    def test_lookup_payload_is_canonical(self):
        value = PlaceIdentity.build(name="Musée Test", city="Lille", string_id="Musée Test", urls=["https://www.example.test/?utm_source=x"])
        self.assertEqual("musee-test", value.lookup_payload()["string_id"])
        self.assertEqual(["https://example.test/"], value.lookup_payload()["urls"])


if __name__ == "__main__":
    unittest.main()
