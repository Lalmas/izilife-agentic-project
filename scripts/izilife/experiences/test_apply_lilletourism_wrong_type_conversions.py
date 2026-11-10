import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


PATH = Path(__file__).with_name("apply_lilletourism_wrong_type_conversions.py")
SPEC = importlib.util.spec_from_file_location("conversion", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class ConversionManifestTests(unittest.TestCase):
    def test_manifest_contains_the_four_stable_ref_conversions(self):
        manifest = MODULE.load_manifest(MODULE.MANIFEST)
        self.assertEqual(4, len(manifest["items"]))
        self.assertEqual({"EVENT_SERIE", "EQUIPMENT"}, {row["target_type"] for row in manifest["items"]})

    def test_audit_payload_does_not_apply(self):
        row = {"experience_id": 206, "target_type": "EVENT_SERIE", "target_category_ref": "spectacle"}
        value = MODULE.payload(row, False)
        self.assertFalse(value["apply"])
        self.assertNotIn("target_category", value)

    def test_numeric_taxonomy_is_rejected(self):
        bad = {"items": [{"experience_id": 1, "target_type": "EVENT_SERIE", "target_category_ref": "spectacle", "target_category_id": 9}]}
        root = Path(__file__).resolve().parents[3] / "tmp"
        root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=root) as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps(bad), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "IDs de nomenclature"):
                MODULE.load_manifest(path)


if __name__ == "__main__":
    unittest.main()
