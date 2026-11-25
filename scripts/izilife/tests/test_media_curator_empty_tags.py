import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from medias.media_curator import upload


class MediaCuratorEmptyTagsTest(unittest.TestCase):
    @patch("medias.media_curator.requests.post")
    def test_empty_tags_are_not_sent(self, post):
        response = Mock()
        response.json.return_value = {"success": True, "created": True}
        post.return_value = response
        values = {
            "SCOPE_TYPE": "CITY",
            "SCOPE_REF": "lille",
            "RIGHTS_CONFIRMED": "OUI",
            "BELONGS_TO_SCOPE": "OUI",
            "TAG_REFS": None,
        }
        temp_root = Path(__file__).resolve().parents[3] / "tmp" / "media_curator_tests"
        temp_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temp_root) as directory:
            media = Path(directory) / "test.jpg"
            media.write_bytes(b"image")
            with patch.dict("os.environ", {"IZILIFE_AGENT_TOKEN": "test"}):
                upload(media, values, False, "prod")

        self.assertNotIn("tag_refs", post.call_args.kwargs["data"])


if __name__ == "__main__":
    unittest.main()
