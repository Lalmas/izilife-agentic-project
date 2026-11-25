import unittest
from pathlib import Path
from unittest.mock import patch

import ingest_manual_curate as curate


class ManualCurateCarouselTest(unittest.TestCase):
    def test_separate_flyers_are_kept_and_cover_is_ignored(self):
        paths=[Path("cover.jpg"),Path("event1.jpg"),Path("event2.jpg")]
        outputs={
            "cover.jpg":{"local_ocr_status":"completed"},
            "event1.jpg":{"local_ocr_status":"completed","title":"Concert","start_date":"2099-11-14"},
            "event2.jpg":{"local_ocr_status":"completed","title":"Atelier","start_date":"2099-11-15"},
        }
        with patch.object(curate,"complete_missing_fields",side_effect=lambda row,path:dict(row,**outputs[path.name])):
            rows=curate.carousel_event_rows(paths,{"event_category_ref":"concert","included_img_indexes":"1,2,3"})
        self.assertEqual(["event1.jpg","event2.jpg"],[path.name for path,_ in rows])
        self.assertEqual([2,3],[row["img_index"] for _,row in rows])

    def test_included_and_excluded_indexes_limit_analysis(self):
        paths=[Path("cover.jpg"),Path("event.jpg"),Path("other.jpg")]
        with patch.object(curate,"complete_missing_fields",return_value={"local_ocr_status":"completed","title":"Concert","start_date":"2099-11-14"}) as ocr:
            rows=curate.carousel_event_rows(paths,{"included_img_indexes":"1,2","excluded_img_indexes":"1"})
        self.assertEqual(1,ocr.call_count)
        self.assertEqual(2,rows[0][1]["img_index"])

    def test_carousel_defaults_to_first_slide_without_ocr(self):
        with patch.object(curate,"complete_missing_fields",side_effect=AssertionError("OCR should not run")):
            rows=curate.carousel_event_rows([Path("first.jpg"),Path("second.jpg")],{})
        self.assertEqual(["first.jpg"],[path.name for path,_ in rows])
        self.assertEqual(1,rows[0][1]["img_index"])

    def test_manual_single_event_is_created_once(self):
        with patch.object(curate,"complete_missing_fields",return_value={"local_ocr_status":"unavailable"}):
            rows=curate.carousel_event_rows([Path("a.jpg"),Path("b.jpg")],{"title":"Soirée","start_date":"2099-11-14"})
        self.assertEqual(1,len(rows))

    def test_manual_image_index_selects_only_requested_slide(self):
        paths=[Path("cover.jpg"),Path("friday.jpg"),Path("saturday.jpg")]
        rows=curate.carousel_event_rows(paths,{"img_index":"2","title":"Vendredi","start_date":"2099-11-14"})
        self.assertEqual(["friday.jpg"],[path.name for path,_ in rows])

    def test_planning_instagram_mode_ignores_caption_for_indexed_slide(self):
        row={"img_index":"2","instagram_content_mode":"PLANNING_INSTAGRAM"}
        with patch.object(curate,"complete_missing_fields",side_effect=lambda value,_path:value):
            payload=curate.manual_event_payload(row,"https://instagram.test/p/planning",Path("slide2.jpg"))
        self.assertEqual("PLANNING_INSTAGRAM",payload["instagram_content_mode"])
        self.assertFalse(curate.should_use_instagram_caption(row))
        self.assertTrue(curate.should_use_instagram_caption({"img_index":"2"}))
        self.assertFalse(curate.should_use_instagram_caption({"instagram_content_mode":"PLANNING_INSTAGRAM"}))

    def test_planning_requires_explicit_slide_selection(self):
        valid,error=curate.validate_instagram_planning_selection({"instagram_content_mode":"PLANNING_INSTAGRAM"})
        self.assertFalse(valid)
        self.assertIn("sélection",error)
        for selection in ({"img_index":"2"},{"included_img_indexes":"1,3"},{"excluded_img_indexes":"1"}):
            valid,_=curate.validate_instagram_planning_selection(dict(selection,instagram_content_mode="PLANNING_INSTAGRAM"))
            self.assertTrue(valid)

    def test_planning_exclusions_only_process_remaining_slides(self):
        paths=[Path("cover.jpg"),Path("event1.jpg"),Path("event2.jpg")]
        parsed={"local_ocr_status":"completed","title":"Event","start_date":"2099-11-14"}
        with patch.object(curate,"complete_missing_fields",side_effect=lambda _row,_path:dict(parsed)) as ocr:
            rows=curate.carousel_event_rows(paths,{"instagram_content_mode":"PLANNING_INSTAGRAM","excluded_img_indexes":"1"})
        self.assertEqual(2,ocr.call_count)
        self.assertEqual([2,3],[row["img_index"] for _,row in rows])

    def test_regular_carousel_indexes_are_one_event_flyers(self):
        paths=[Path("one.jpg"),Path("two.jpg"),Path("three.jpg")]
        selected=curate.selected_event_flyers(paths,{"img_index":"1,2,3"})
        self.assertEqual(paths,selected)
        selected=curate.selected_event_flyers(paths,{"included_img_indexes":"1,3","excluded_img_indexes":"1"})
        self.assertEqual([Path("three.jpg")],selected)

    def test_past_manual_slide_is_ignored(self):
        rows=curate.carousel_event_rows([Path("old.jpg"),Path("new.jpg")],{"img_index":"1","title":"Ancien","start_date":"2020-01-01"})
        self.assertEqual([],rows)

    def test_complete_manual_core_skips_ocr(self):
        row={"title":"Soirée test","description":"Une soirée de test.","start_date":"2026-11-14","start_hour":"19:00","end_hour":"23:00","event_category_ref":"soiree","target_string_id":"la-luck"}
        with patch.object(curate,"complete_missing_fields",side_effect=AssertionError("OCR should not run")):
            payload=curate.manual_event_payload(row,"https://instagram.test/p/1",Path("event.jpg"))
        self.assertEqual("Une soirée de test.",payload["description"])
        self.assertTrue(payload["manual_ai_request"])

    def test_overnight_event_ends_next_day(self):
        self.assertEqual("2026-11-13",curate.inferred_end_date("2026-11-12","18:30","01:00"))


if __name__=="__main__":unittest.main()
