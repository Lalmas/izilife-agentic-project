import json,tempfile,unittest
from pathlib import Path
from site_event_package import issues,plan

class SiteEventPackageTest(unittest.TestCase):
    def setUp(self):
        self.path=Path(__file__).parent/"examples"/"annual_celebration_package.json"
        self.package=json.loads(self.path.read_text(encoding="utf-8"))
    def test_annual_package_is_valid(self):self.assertEqual([],issues(self.package))
    def test_plan_counts_root_events_media_and_sources(self):
        value=plan(self.package,self.path);self.assertEqual("ANNUAL_CELEBRATION",value["root_type"]);self.assertEqual(1,value["events"]);self.assertEqual(1,value["media"]);self.assertEqual(1,value["sources"])
    def test_creation_requires_date(self):
        self.package["events"][0]["data"].pop("start_date");self.assertTrue(any("start_date" in x for x in issues(self.package)))
    def test_description_is_required_by_backend(self):
        self.package["events"][0]["data"].pop("description");self.assertTrue(any("description" in x for x in issues(self.package)))
    def test_event_category_is_required_by_backend(self):
        self.package["events"][0]["data"].pop("event_category_ref");self.assertTrue(any("event_category_ref" in x for x in issues(self.package)))
    def test_backend_contract_requires_exactly_one_root_edition(self):
        self.package["events"][0]["relation"]="ANNUAL_EDITION"
        self.assertTrue(any("exactement une ROOT_EDITION" in x for x in issues(self.package)))
    def test_editorial_agenda_forbids_root(self):
        self.package["package_kind"]="EDITORIAL_AGENDA"
        self.assertTrue(any("interdit root" in x for x in issues(self.package)))
if __name__=="__main__":unittest.main()
