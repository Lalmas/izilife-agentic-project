import importlib.util
import sys
import tempfile
import types
import unittest
from pathlib import Path


sys.modules.setdefault("requests", types.ModuleType("requests"))
sys.modules.setdefault("openpyxl", types.ModuleType("openpyxl"))

MODULE_PATH = Path(__file__).with_name("createur_lieux.py")
SPEC = importlib.util.spec_from_file_location("createur_lieux", MODULE_PATH)
createur_lieux = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(createur_lieux)


class NewnessSqlTest(unittest.TestCase):
    def test_work_queue_keeps_only_new_retry_and_error(self):
        class Cell:
            def __init__(self, value): self.value = value

        class Sheet:
            rows = [
                ["NOM", "VILLE", "TYPE_IMPOSE", "CATEGORY_STRING_ID", "NOTES", "STATUT"],
                ["Nouveau", "lille", "", "", "", "pending"],
                ["À reprendre", "lille", "", "", "", "error"],
                ["Relance", "lille", "", "", "", "retry"],
                ["Déjà au BO", "lille", "", "", "", "unmapped"],
                ["Terminé", "lille", "", "", "", "done"],
                ["Ignoré", "lille", "", "", "", "skip"],
            ]

            def __getitem__(self, index):
                return [Cell(value) for value in self.rows[index - 1]]

            def iter_rows(self, min_row=1, values_only=False):
                for row in self.rows[min_row - 1:]:
                    yield tuple(row) if values_only else [Cell(value) for value in row]

        rows = createur_lieux.read_pending_rows(Sheet())
        self.assertEqual(["Nouveau", "À reprendre", "Relance"], [row["nom"] for row in rows])

    def test_google_maps_title_is_canonicalized(self):
        self.assertEqual(
            "Médiathèque André-Malraux",
            createur_lieux.MapsNameResolver._clean_title(
                "Médiathèque André-Malraux - Google Maps"
            ),
        )

    def test_same_target_and_date_is_deduplicated(self):
        statements = [
            "UPDATE `Shop` SET `opening_date` = '2026-03-02', `is_new_in_city` = 1 WHERE `id` = 5439; /* Pigments LaM */",
            "UPDATE `Shop` SET `opening_date` = '2026-03-02', `is_new_in_city` = 1 WHERE `id` = 5439; /* Pigments au LaM */",
        ]

        safe, conflicts = createur_lieux.sanitize_newness_statements(statements)

        self.assertEqual(1, len(safe))
        self.assertEqual([], conflicts)

    def test_conflicting_dates_are_excluded(self):
        statements = [
            "UPDATE `Shop` SET `opening_date` = '2025-11-10', `is_new_in_city` = 1 WHERE `id` = 1789; /* Brunchit Lille */",
            "UPDATE `Shop` SET `opening_date` = '2025-03-03', `is_new_in_city` = 1 WHERE `id` = 1789; /* Tubrilles */",
            "UPDATE `Place` SET `opening_date` = '2026-07-06', `is_new_in_city` = 1 WHERE `id` = 253; /* LaM */",
        ]

        safe, conflicts = createur_lieux.sanitize_newness_statements(statements)

        self.assertEqual(1, len(safe))
        self.assertIn("`Place`", safe[0])
        self.assertEqual(1, len(conflicts))
        self.assertIn("Shop id=1789", conflicts[0])

    def test_sql_file_keeps_conflict_as_non_executable_comment(self):
        with tempfile.TemporaryDirectory(dir=MODULE_PATH.parent) as directory:
            curate_file = Path(directory) / "curate_places.xlsm"
            first = "UPDATE `Shop` SET `opening_date` = '2026-07-13', `is_new_in_city` = 1 WHERE `id` = 5349; /* Swyft 16 */"
            second = "UPDATE `Shop` SET `opening_date` = '2026-07-20', `is_new_in_city` = 1 WHERE `id` = 5349; /* Swyft 15 */"

            target = createur_lieux.write_newness_sql(curate_file, "Lieux", [first, second])
            content = target.read_text(encoding="utf-8")

            self.assertNotIn("UPDATE `Shop`", content)
            self.assertIn("-- CONFLICT EXCLUDED: Shop id=5349", content)
            self.assertTrue(content.startswith("START TRANSACTION;"))
            self.assertTrue(content.rstrip().endswith("COMMIT;"))


if __name__ == "__main__":
    unittest.main()
