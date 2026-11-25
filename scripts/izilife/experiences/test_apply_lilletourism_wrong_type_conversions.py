import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("apply_lilletourism_wrong_type_conversions.py")
SPEC = importlib.util.spec_from_file_location("lilletourism_conversion", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class ManifestTests(unittest.TestCase):
    def test_real_manifest_uses_only_stable_references(self):
        manifest = MODULE.load_manifest(MODULE.DEFAULT_MANIFEST)
        self.assertEqual(4, len(manifest["items"]))
        self.assertEqual(
            {"EVENT_SERIE", "EQUIPMENT"},
            {item["target_type"] for item in manifest["items"]},
        )

    def test_payload_is_audit_by_default(self):
        item = {
            "experience_id": 206,
            "target_type": "EVENT_SERIE",
            "target_category_ref": "soiree-jeux",
        }
        payload = MODULE.build_payload(item, False)
        self.assertFalse(payload["apply"])
        self.assertEqual("soiree-jeux", payload["target_category_ref"])
        self.assertNotIn("target_category", payload)

    def test_numeric_taxonomy_id_is_rejected(self):
        bad = {
            "items": [
                {
                    "experience_id": 1,
                    "target_type": "EVENT_SERIE",
                    "target_category_ref": "spectacle",
                    "target_category_id": 9,
                }
            ]
        }
        workspace_tmp = Path(__file__).resolve().parents[3] / "tmp"
        workspace_tmp.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=workspace_tmp) as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps(bad), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "IDs de nomenclature"):
                MODULE.load_manifest(path)


if __name__ == "__main__":
    unittest.main()
