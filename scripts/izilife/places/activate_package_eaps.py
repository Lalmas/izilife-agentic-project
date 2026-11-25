#!/usr/bin/env python3
"""Active les EAP d'un paquet JSON déjà importé, après comparaison BO."""
from __future__ import annotations

import argparse
import json
import os
from decimal import Decimal
from pathlib import Path
import requests

from site_content_package import izilife_post, load_env, normalize_env
from objects.object_agent_common import IZILIFE_ENVS


def lookup(target: dict, env: str) -> dict:
    config = IZILIFE_ENVS[env]
    response = requests.post(
        config['base_url'].rstrip('/') + '/scraper/agentInternalDataV0Lookup',
        json={'items': [{'type': target['scope_type'], 'string_id': target['scope_ref']}],
              'include_graph': True},
        headers={'X-Agent-Token': os.environ['IZILIFE_AGENT_TOKEN']},
        verify=config.get('verify_ssl', True), timeout=90,
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--file', required=True)
    parser.add_argument('--env', required=True, choices=['local', 'staging', 'prod'])
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    package = json.loads(Path(args.file).read_text(encoding='utf-8'))
    target = package['target']
    eaps = [obj for obj in package['objects']
            if obj.get('kind') == 'eap' and obj.get('review_status') == 'approved']
    if not eaps or len({obj['item']['name'] for obj in eaps}) != len(eaps):
        raise SystemExit('Liste EAP vide ou noms dupliqués dans le paquet.')
    load_env()
    env = normalize_env(args.env)
    result = (lookup(target, env).get('items') or [{}])[0]
    if result.get('status') != 'found':
        raise SystemExit('Cible introuvable dans l’API de lecture.')
    existing = {row['name']: row for row in result['graph']['eap']}
    if set(existing) != {obj['item']['name'] for obj in eaps}:
        raise SystemExit('Les EAP de la cible ne correspondent pas exactement au paquet.')
    for obj in eaps:
        item = obj['item']
        row = existing[item['name']]
        if Decimal(str(row['price'])) != Decimal(str(item['price'])):
            raise SystemExit('Prix différent dans le BO : ' + item['name'])
    print(json.dumps({'environment': env, 'scope': target, 'eap_matched': len(eaps),
                      'inactive_before': sum(int(row['is_active']) == 0 for row in existing.values()),
                      'apply': args.apply}, ensure_ascii=False))
    if not args.apply:
        return
    for obj in eaps:
        item = dict(obj['item'])
        item['is_active'] = 1
        item['need_to_be_confirmed_manually'] = 1
        response = izilife_post('/scraper/agentIngestSiteItem', {
            'payload': json.dumps({'kind': 'eap', 'scope_type': target['scope_type'],
                                   'scope_ref': target['scope_ref'], 'source_url': obj['source_url'],
                                   'item': item}, ensure_ascii=False)
        }, env, timeout=90)
        if not response.get('success') or response.get('created'):
            raise SystemExit('Activation interrompue sur ' + item['name'] + ': ' + str(response))
    checked = lookup(target, env)
    rows = checked['items'][0]['graph']['eap']
    active = sum(int(row['is_active']) == 1 for row in rows)
    print(json.dumps({'active_after': active, 'expected': len(eaps)}, ensure_ascii=False))
    if active != len(eaps):
        raise SystemExit('Activation incomplète dans le BO.')


if __name__ == '__main__':
    main()
