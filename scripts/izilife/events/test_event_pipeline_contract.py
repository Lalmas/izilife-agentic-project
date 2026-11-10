import os
import unittest
from pathlib import Path


ADMIN_ROOT = Path(os.environ.get("IZILIFE_ADMIN_ROOT", r"C:\xampp\htdocs\izilife-admin"))


@unittest.skipUnless(ADMIN_ROOT.exists(), "izilife-admin source tree is not available")
class EventPipelineContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = (ADMIN_ROOT / "app/Libraries/AIWorkflow_lib.php").read_text(encoding="utf-8")
        cls.scraper = (ADMIN_ROOT / "app/Controllers/Scraper.php").read_text(encoding="utf-8")
        cls.object_conversion = (ADMIN_ROOT / "app/Controllers/ObjectConversion.php").read_text(encoding="utf-8")
        cls.experience_validator = (ADMIN_ROOT / "app/Models/Agents/AgentExperienceValidator_model.php").read_text(encoding="utf-8")

    def test_first_call_forbids_collective_and_party_music_fallbacks(self):
        self.assertIn("N'utilise jamais activite-collective comme valeur de secours", self.workflow)
        self.assertIn("« fête et musique » n'est jamais une catégorie de secours", self.workflow)
        self.assertIn("manual_collective_activity_approval", self.experience_validator)
        self.assertIn("activite_collective_validation_manuelle", self.experience_validator)

    def test_first_call_requires_apc_and_specialized_taxonomies(self):
        self.assertIn("Stage, cours, atelier, workshop, salon et festival exigent une activité principale précise", self.workflow)
        for field in (
            "principal_activity_category_string_id",
            "sport_string_id",
            "dance_string_id",
            "music_style_string_id",
            "artisan_technique_string_id",
        ):
            self.assertIn(field, self.workflow)

    def test_multiday_workshop_visit_course_rule_is_present(self):
        self.assertIn("Atelier, workshop, visite et cours ne couvrent jamais artificiellement", self.workflow)
        self.assertIn("occurrences_a_separer_ou_reclasser", self.scraper)

    def test_contextual_end_hour_is_the_only_missing_end_fallback(self):
        self.assertIn("private function _estimatedEventEndHour", self.scraper)
        self.assertNotIn("?? '23:59'", self.scraper)
        self.assertNotIn("?: '23:59'", self.scraper)
        self.assertNotIn("si absent tu peux mettre 23:59", self.workflow)
        self.assertIn("$this->_estimatedEventEndHour($startHour", self.scraper)
        self.assertIn("$this->_estimatedEventEndHour((string)$program['start_hour']", self.scraper)

    def test_one_shot_audit_uses_equipment_and_stored_source_context(self):
        validator = (ADMIN_ROOT / "app/Models/Agents/AgentEventValidator_model.php").read_text(encoding="utf-8")
        self.assertIn("e.event_equipment", validator)
        self.assertIn("$this->qualityVenueKey($row)", validator)
        self.assertIn("(string)($event['description']??'')", validator)
        self.assertIn("(string)($event['scrapping_json']??'')", validator)
        self.assertNotIn("concert|musique|dj|festival", validator)
        self.assertIn("concert|musique|musical|dj|fanfare|batucada|orchestre", validator)

    def test_duplicate_cleanup_supports_address_fallback_and_logical_archive(self):
        validator = (ADMIN_ROOT / "app/Models/Agents/AgentEventValidator_model.php").read_text(encoding="utf-8")
        routes = (ADMIN_ROOT / "app/Config/Routes.php").read_text(encoding="utf-8")
        self.assertIn("private function qualityVenueKey", validator)
        self.assertIn("'C'.(int)$event['city_id'].'|A'.$address", validator)
        self.assertIn("public function archiveDuplicateEvent", validator)
        self.assertIn("'is_active'=>0,'listable'=>0", validator)
        self.assertIn("_duplicate_archive", validator)
        self.assertIn("agentArchiveDuplicateEvent", routes)

    def test_event_tmp_city_is_joined_once(self):
        validator = (ADMIN_ROOT / "app/Models/Agents/AgentEventValidator_model.php").read_text(encoding="utf-8")
        self.assertEqual(validator.count("->join('City c', 'c.id=e.city_id', 'left')"), 1)

    def test_conversion_manifest_resolves_stable_references(self):
        self.assertIn("target_category_ref", self.object_conversion)
        self.assertIn("equipment_category_ref", self.object_conversion)
        self.assertIn("equipment_parent_ref", self.object_conversion)
        self.assertIn("resolveReferenceId('EventCategory','event_category_string_id'", self.object_conversion)
        self.assertIn("resolveReferenceId('EquipmentCategory','string_id'", self.object_conversion)
        self.assertIn("['PLACE'=>['Place','place_string_id'],'SHOP'=>['Shop','shop_string_id']]", self.object_conversion)
        self.assertIn("$s->meet_place", self.object_conversion)
        self.assertIn("$s->meet_shop", self.object_conversion)


if __name__ == "__main__":
    unittest.main()
