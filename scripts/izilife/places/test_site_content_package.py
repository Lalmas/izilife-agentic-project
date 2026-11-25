import json
import unittest
from pathlib import Path

from cryotera_catalogue_snapshot import build
from site_content_package import issues


class SiteContentPackageTest(unittest.TestCase):
    def test_cryotera_snapshot_has_every_verified_offer(self):
        package = build()
        self.assertEqual(issues(package), [])
        services = {x['item']['name'] for x in package['objects'] if x['kind'] == 'element_service'}
        eaps = [x['item'] for x in package['objects'] if x['kind'] == 'eap']
        self.assertEqual(len(services), 7)
        self.assertEqual(len(eaps), 22)
        names = {item['name'] for item in eaps}
        for item in eaps:
            self.assertIn(item['service_name'], services)
            for part in item.get('pack_composition', []):
                self.assertIn(part['name'], names)
        media = [m for obj in package['objects'] for m in obj['media']]
        self.assertEqual(len(media), 7)
        for image in media:
            self.assertTrue((Path(__file__).parent / image['local_file']).is_file())

    def test_approved_tariff_without_price_is_rejected(self):
        package = build()
        eap = next(obj for obj in package['objects'] if obj['kind'] == 'eap')
        eap['review_status'] = 'approved'
        eap['item'].pop('price')
        self.assertTrue(any('prix EAP explicite' in message for message in issues(package)))


if __name__ == '__main__':
    unittest.main()
