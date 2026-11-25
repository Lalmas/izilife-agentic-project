import tempfile
import unittest
import sys
from pathlib import Path
from unittest.mock import patch

SCRIPTS_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SCRIPTS_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from openpyxl import Workbook, load_workbook

from external_content_agent import discovered_urls, init_workbook, promo_source_string_id, run, upload_images


class ExternalContentWatchTest(unittest.TestCase):
    def test_social_origins_use_manual_business_source(self):
        self.assertEqual("manual", promo_source_string_id("instagram"))
        self.assertEqual("manual", promo_source_string_id("facebook"))
        self.assertEqual("dealabs", promo_source_string_id("dealabs"))

    def test_initializer_has_complete_manual_schema(self):
        test_root=Path(__file__).resolve().parents[3]/"tmp";test_root.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=test_root) as tmp:
            path=Path(tmp)/"external.xlsx";init_workbook(path);wb=load_workbook(path)
            self.assertEqual(["ExternalOffer","ElementNewsPost","Veille","Historique","ModeEmploi"],wb.sheetnames)
            self.assertIn("USE_LLM_IF_MISSING",[cell.value for cell in wb["ExternalOffer"][1]])
            self.assertIn("IMAGE_URLS",[cell.value for cell in wb["ElementNewsPost"][1]])

    def test_optional_ai_is_called_only_when_row_requests_it(self):
        test_root=Path(__file__).resolve().parents[3]/"tmp";test_root.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=test_root) as tmp:
            path=Path(tmp)/"external.xlsx";init_workbook(path);wb=load_workbook(path)
            ws=wb["ElementNewsPost"];headers=[cell.value for cell in ws[1]]
            row={"SOURCE_URL":"https://example.test/news/ai","SOURCE_TYPE":"website","STATUS":"pending","SCOPE_TYPE":"PLACE","SCOPE_REF":"demo","USE_LLM_IF_MISSING":"oui"}
            ws.append([row.get(header,"") for header in headers]);wb.save(path)
            import external_content_agent as agent
            with patch.object(agent,"extracted",return_value={"title":"","description":"","image_url":"","hash":"x","content":"Texte source"}), \
                 patch.object(agent,"ai_complete",return_value={"success":True,"result":{"title":"Titre","content":"Contenu"}}) as ai_mock, \
                 patch.object(agent,"post",return_value={"success":True,"created":True,"id":7}):
                run(path,"local",False,1)
            self.assertEqual(1,ai_mock.call_count)

    def test_complete_manual_offer_does_not_fetch_source(self):
        test_root=Path(__file__).resolve().parents[3]/"tmp";test_root.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=test_root) as tmp:
            path=Path(tmp)/"external.xlsx";init_workbook(path);wb=load_workbook(path)
            ws=wb["ExternalOffer"];headers=[cell.value for cell in ws[1]]
            row={"SOURCE_URL":"https://www.instagram.com/p/test/","SOURCE_TYPE":"instagram","STATUS":"pending","TITRE":"Offre","DESCRIPTION":"Description","SCOPE_TYPE":"GLOBAL","USE_LLM_IF_MISSING":"non"}
            ws.append([row.get(header,"") for header in headers]);wb.save(path)
            import external_content_agent as agent
            with patch.object(agent,"extracted",side_effect=AssertionError("source should not be fetched")), \
                 patch.object(agent,"post",return_value={"success":True,"created":True,"id":8}):
                run(path,"local",False,1)
            self.assertEqual("done",load_workbook(path)["ExternalOffer"]["C2"].value)

    def test_external_offer_upload_keeps_only_first_image(self):
        import external_content_agent as agent
        response = unittest.mock.Mock()
        response.content = b"image"
        response.headers = {"Content-Type": "image/jpeg"}
        response.raise_for_status.return_value = None
        upload = unittest.mock.Mock()
        upload.json.return_value = {"success": True, "created": True}
        with patch.object(agent.requests, "get", return_value=response) as get_mock, \
             patch.object(agent.requests, "post", return_value=upload) as post_mock, \
             patch.dict(agent.IZILIFE_ENVS, {"local": {"base_url": "http://localhost", "verify_ssl": False}}), \
             patch.dict(agent.os.environ, {"IZILIFE_AGENT_TOKEN": "test"}):
            result = upload_images("EXTERNAL_OFFER", 9, ["https://example.test/a.jpg", "https://example.test/b.jpg"], "local")
        self.assertEqual(1, len(result))
        self.assertEqual(1, get_mock.call_count)
        self.assertEqual(1, post_mock.call_count)

    def test_discovery_is_same_host_and_destination_filtered(self):
        html='''<a href="/actualites/nouvelle-expo">News</a><a href="/contact">Contact</a>
        <a href="https://other.test/news/x">Other</a>'''
        self.assertEqual(
            ["https://example.test/actualites/nouvelle-expo"],
            discovered_urls("https://example.test/", html, "ELEMENT_NEWS_POST"),
        )

    def test_instagram_watch_discovers_posts_and_reels(self):
        html='<a href="/p/ABC123/">Post</a><a href="/reel/XYZ789/">Reel</a><a href="/stories/demo/1">Story</a>'
        self.assertEqual(["https://instagram.com/p/ABC123","https://instagram.com/reel/XYZ789"],discovered_urls("https://www.instagram.com/demo/",html,"ELEMENT_NEWS_POST"))

    def test_watch_creates_persistent_history(self):
        test_root=Path(__file__).resolve().parents[3]/"tmp"
        test_root.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=test_root) as tmp:
            path=Path(tmp)/"watch.xlsx";wb=Workbook();ws=wb.active;ws.title="ExternalOffer"
            ws.append(["SOURCE_URL","SOURCE_TYPE","STATUS","RESULTAT","ERREUR"])
            news=wb.create_sheet("ElementNewsPost");news.append(["SOURCE_URL","SOURCE_TYPE","SCOPE_TYPE","SCOPE_REF","STATUS","RESULTAT","ERREUR"])
            watch=wb.create_sheet("Veille");watch.append(["SOURCE_URL","SOURCE_TYPE","DESTINATION_TYPE","SCOPE_TYPE","SCOPE_REF","ACTIF","LAST_CHECK","LAST_HASH","STATUS","RESULTAT"])
            watch.append(["https://example.test/","website","ELEMENT_NEWS_POST","PAGE","demo","oui"]);wb.save(path)
            import external_content_agent as agent
            original=agent.fetch
            agent.fetch=lambda _: '<a href="/actualites/article-1">Article</a><title>Accueil</title>'
            try:run(path,"local",True,10)
            finally:agent.fetch=original
            result=load_workbook(path)
            self.assertIn("Historique",result.sheetnames)
            self.assertEqual("baseline",result["Historique"]["F2"].value)
            self.assertEqual("initialized",result["Veille"]["I2"].value)

    def test_import_updates_history_with_object_id(self):
        test_root=Path(__file__).resolve().parents[3]/"tmp";test_root.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=test_root) as tmp:
            path=Path(tmp)/"import.xlsx";wb=Workbook();offers=wb.active;offers.title="ExternalOffer"
            offers.append(["SOURCE_URL","SOURCE_TYPE","STATUS","RESULTAT","ERREUR"]);offers.append(["https://example.test/offre/1","website","pending"])
            news=wb.create_sheet("ElementNewsPost");news.append(["SOURCE_URL","SOURCE_TYPE","STATUS","RESULTAT","ERREUR"])
            watch=wb.create_sheet("Veille");watch.append(["SOURCE_URL","SOURCE_TYPE","DESTINATION_TYPE","SCOPE_TYPE","SCOPE_REF","ACTIF","LAST_CHECK","LAST_HASH","STATUS","RESULTAT"])
            history=wb.create_sheet("Historique");history.append(["PARENT_URL","CONTENT_URL","DESTINATION_TYPE","FIRST_SEEN","LAST_SEEN","STATUS","OBJECT_ID","LAST_RESULT"]);history.append(["https://example.test/","https://example.test/offre/1","EXTERNAL_OFFER","x","x","queued"]);wb.save(path)
            import external_content_agent as agent
            with patch.object(agent,"extracted",return_value={"title":"Offre","description":"Promo","image_url":"","hash":"x","content":"Promo"}),patch.object(agent,"post",return_value={"success":True,"created":True,"id":42}):run(path,"local",False,1)
            result=load_workbook(path);self.assertEqual("imported",result["Historique"]["F2"].value);self.assertEqual(42,result["Historique"]["G2"].value)


if __name__ == "__main__": unittest.main()
