import unittest
import tempfile
from datetime import date
from pathlib import Path
from unittest.mock import patch

from local_event_ocr import (
    complete_missing_fields, estimated_end_hour, extract_event_fields,
    extract_title_candidate, ocr_image,
)


class LocalEventOcrTest(unittest.TestCase):
    def test_contextual_missing_end_hour(self):
        self.assertEqual("18:00", estimated_end_hour("10:00", "visite"))
        self.assertEqual("18:00", estimated_end_hour("14:30", "atelier"))
        self.assertEqual("19:00", estimated_end_hour("16:30", "rencontre"))
        self.assertEqual("23:59", estimated_end_hour("19:00", "concert"))
        self.assertEqual("02:00", estimated_end_hour("20:00", "soirée karaoké au bar"))

    def test_estimated_nightlife_end_moves_to_next_day(self):
        with patch("local_event_ocr.ocr_image", return_value=("14 novembre 2026 à 20h", "test")):
            result = complete_missing_fields(
                {"title": "Soirée karaoké"}, Path("poster.jpg"), date(2026, 11, 9)
            )
        self.assertEqual("02:00", result["end_hour"])
        self.assertEqual("2026-11-15", result["end_date"])

    def test_title_candidate_ignores_agenda_and_date(self):
        text="AGENDA DE NOVEMBRE\nCONCERT DE JAZZ\nSamedi 14 novembre 2026\n19h à 23h"
        self.assertEqual("CONCERT DE JAZZ",extract_title_candidate(text))

    def test_explicit_french_date_and_range(self):
        result = extract_event_fields("Samedi 14 novembre 2026 de 19h à 23h", date(2026, 11, 9))
        self.assertEqual("2026-11-14", result["start_date"])
        self.assertEqual("19:00", result["start_hour"])
        self.assertEqual("23:00", result["end_hour"])
        self.assertFalse(result["ambiguous"])

    def test_manual_values_are_never_overwritten(self):
        with patch("local_event_ocr.ocr_image", return_value=("15 novembre 2026 de 10h à 12h", "test")):
            result = complete_missing_fields({"start_date": "2026-12-01", "start_hour": "09:00"}, Path("poster.jpg"), date(2026, 11, 9))
        self.assertEqual("2026-12-01", result["start_date"])
        self.assertEqual("09:00", result["start_hour"])
        self.assertEqual("12:00", result["end_hour"])

    def test_multiple_dates_are_flagged_not_guessed(self):
        result = extract_event_fields("14 novembre 2026 puis 15 novembre 2026 à 19h", date(2026, 11, 9))
        self.assertNotIn("start_date", result)
        self.assertTrue(result["ambiguous"])
        self.assertIn("multiple_dates", result["reasons"])

    def test_missing_ocr_keeps_row_for_server_fallback(self):
        with patch("local_event_ocr.ocr_image", return_value=("", "")):
            result = complete_missing_fields({"title": "Concert"}, Path("poster.jpg"))
        self.assertEqual("Concert", result["title"])
        self.assertEqual("unavailable", result["local_ocr_status"])

    def test_real_local_ocr_image(self):
        from PIL import Image, ImageDraw, ImageFont
        workspace_tmp = Path(__file__).resolve().parents[3] / "tmp"
        workspace_tmp.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=workspace_tmp) as folder:
            path = Path(folder) / "poster.png"
            image = Image.new("RGB", (1500, 500), "white")
            draw = ImageDraw.Draw(image)
            font_path = Path("C:/Windows/Fonts/arial.ttf")
            font = ImageFont.truetype(str(font_path), 72) if font_path.exists() else ImageFont.load_default()
            draw.text((50, 80), "SAMEDI 14 NOVEMBRE 2026", fill="black", font=font)
            draw.text((50, 220), "DE 19H A 23H", fill="black", font=font)
            image.save(path)
            text, engine = ocr_image(path)
            self.assertTrue(text.strip())
            self.assertEqual("rapidocr", engine)
            parsed = extract_event_fields(text, date(2026, 11, 9))
            self.assertEqual("2026-11-14", parsed.get("start_date"))
            self.assertEqual("19:00", parsed.get("start_hour"), text)
            self.assertEqual("23:00", parsed.get("end_hour"), text)


if __name__ == "__main__":
    unittest.main()
