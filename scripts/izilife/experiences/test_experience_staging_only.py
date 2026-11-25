from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent


class ExperienceStagingOnlyContractTest(unittest.TestCase):
    def test_excel_agent_uses_tmp(self):
        source = (ROOT / "experience.py").read_text(encoding="utf-8")
        self.assertIn('endpoint = "/scraper/agentStageExperience"', source)
        self.assertNotIn('endpoint = "/scraper/agentUpsertExperience"', source)

    def test_site_package_stages_complete_payload(self):
        source = (ROOT / "site_experience_package.py").read_text(encoding="utf-8")
        self.assertIn('_post("/scraper/agentStageExperience", item, env)', source)
        self.assertIn('item["additional_image_urls"]', source)
        self.assertIn('item["eaps"]', source)
        self.assertIn('item["session_packages"]', source)
        self.assertNotIn('_post("/scraper/agentUpsertExperience", item, env)', source)


if __name__ == "__main__":
    unittest.main()
