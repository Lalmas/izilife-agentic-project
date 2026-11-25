import unittest
from location_package import issues,approved_package,VERSION

class LocationPackageTest(unittest.TestCase):
    def test_conflicted_coordinates_cannot_be_approved(self):
        package={"schema_version":VERSION,"objects":[{"kind":"EQUIPMENT","review_status":"approved","source_url":"https://example.org/source","scope_type":"CITY","scope_ref":"gondecourt","category_ref":"restaurant-scolaire","internal_id":"restaurant-scolaire-de-gondecourt","name":"Restaurant Scolaire de Gondecourt","city_ref":"gondecourt","latitude":50.54564115613193,"longitude":2.9851193748727978,"coordinate_status":"verified","coordinate_conflict":{"other":[50.5446,3.0112]}}]}
        self.assertIn("objects[1]: conflit de coordonnées encore ouvert",issues(package))
    def test_needs_review_is_not_sent_to_apply(self):
        package={"schema_version":VERSION,"objects":[{"kind":"EQUIPMENT_CATEGORY","string_id":"restaurant-scolaire","name":"Restaurant scolaire","source_url":"https://example.org","review_status":"approved","coordinate_status":"verified"},{"kind":"EQUIPMENT","review_status":"needs_review"}]}
        self.assertEqual(1,len(approved_package(package)["objects"]))

if __name__=="__main__":unittest.main()
