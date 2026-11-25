import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from medias import media_curator


class DummyBrowser:
    def new_context(self, **kwargs): return self
    def new_page(self): return self
    def close(self): pass


class DummyPlaywright:
    chromium = None
    def __init__(self): self.chromium = self
    def start(self): return self
    def launch(self, **kwargs): return DummyBrowser()
    def stop(self): pass


class InstagramChainTest(unittest.TestCase):
    def test_selected_post_is_downloaded_uploaded_and_keeps_provenance(self):
        test_root = ROOT / 'tmp_tests'; test_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=test_root) as tmp:
            root = Path(tmp)
            workbook = root / 'media.xlsx'
            wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Medias'; ws.append(media_curator.HEADERS)
            values = {header: '' for header in media_curator.HEADERS}
            values.update({'SCOPE_TYPE':'PLACE','SCOPE_REF':'demo','MEDIA_GROUP':'SIMPLE','SOURCE_TYPE':'INSTAGRAM','SOURCE_URLS':'https://www.instagram.com/p/demo/','RIGHTS_CONFIRMED':'OUI','BELONGS_TO_SCOPE':'OUI'})
            ws.append([values[h] for h in media_curator.HEADERS]); wb.save(workbook)
            downloaded = root / 'downloaded.jpg'; downloaded.write_bytes(b'fake-jpeg')
            captured = []
            downloader = types.SimpleNamespace(apply_stealth=lambda page: None, open_igram_session=lambda page: None, download_one_url=lambda *args: [downloaded])
            playwright = types.SimpleNamespace(sync_playwright=lambda: DummyPlaywright())
            def fake_upload(path, row, principal, env):
                captured.append(row.get('SOURCE_ORIGIN_URL')); return {'success':True,'created':True}
            real_temporary_directory = tempfile.TemporaryDirectory
            temporary_factory = lambda prefix=None: real_temporary_directory(prefix=prefix, dir=root)
            with patch.dict(sys.modules, {'media_downloader':downloader, 'playwright.sync_api':playwright}), patch.object(media_curator, 'load_env'), patch.object(media_curator, 'root_dir', return_value=root), patch.object(media_curator.tempfile, 'TemporaryDirectory', side_effect=temporary_factory), patch.object(media_curator, 'prepare_upload', side_effect=lambda path, tmp: path), patch.object(media_curator, 'upload', side_effect=fake_upload):
                media_curator.run('lille-zone','local',str(workbook),False,1)
            self.assertEqual(['https://www.instagram.com/p/demo/'], captured)
            checked = openpyxl.load_workbook(workbook)['Medias']
            headers = [c.value for c in checked[1]]
            self.assertEqual('done', checked.cell(2, headers.index('STATUS') + 1).value)
            self.assertIn('https://www.instagram.com/p/demo/', checked.cell(2, headers.index('LAST_RESULT') + 1).value)


if __name__ == '__main__': unittest.main()
