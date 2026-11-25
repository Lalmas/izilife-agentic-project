#!/usr/bin/env python3
"""Paquet de curation vérifiable, indépendant de la collecte et de l'import."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from objects.object_agent_common import izilife_post, load_env, normalize_env

VERSION = 'izilife.site_content.v1'
KINDS = {'element_service', 'eap', 'product', 'equipment'}


def http_url(value):
    parsed = urlparse(str(value or ''))
    return parsed.scheme in {'http', 'https'} and bool(parsed.netloc)


def from_analysis(report, scope_type, scope_ref):
    """Convertit le rapport --analyze-only existant sans nouvelle requête externe."""
    rows = json.loads(Path(report).read_text(encoding='utf-8')).get('results', [])
    found = {}
    for row in rows:
        if row.get('scope_type') != scope_type or row.get('scope_ref') != scope_ref:
            continue
        for entry in row.get('items', []):
            if not isinstance(entry, dict) or entry.get('kind') not in KINDS:
                continue
            item = entry.get('item')
            if not isinstance(item, dict) or not str(item.get('name') or '').strip():
                continue
            key = (entry['kind'], str(item['name']).strip().casefold(), str(row.get('url') or ''))
            if key not in found or len(json.dumps(item, ensure_ascii=False)) > len(json.dumps(found[key]['item'], ensure_ascii=False)):
                found[key] = {'kind': entry['kind'], 'source_url': row.get('url'),
                              'item': item, 'review_status': 'pending', 'media': [],
                              'warnings': row.get('warnings', [])}
    return {'schema_version': VERSION, 'target': {'scope_type': scope_type, 'scope_ref': scope_ref},
            'objects': list(found.values())}


def issues(package):
    problems = []
    if package.get('schema_version') != VERSION:
        problems.append('schema_version incorrect')
    target = package.get('target') or {}
    if target.get('scope_type') not in {'PLACE', 'SHOP'} or not target.get('scope_ref'):
        problems.append('target: PLACE/SHOP et scope_ref requis')
    objects = package.get('objects')
    if not isinstance(objects, list):
        return problems + ['objects doit être une liste']
    for n, obj in enumerate(objects, 1):
        prefix = f'objects[{n}]'
        if not isinstance(obj, dict):
            problems.append(f'{prefix}: objet JSON attendu'); continue
        kind = obj.get('kind'); item = obj.get('item')
        if kind not in KINDS or not isinstance(item, dict) or not str(item.get('name') or '').strip():
            problems.append(f'{prefix}: kind ou item.name invalide'); continue
        if not http_url(obj.get('source_url')):
            problems.append(f'{prefix}: source_url HTTP(S) requis')
        if obj.get('review_status') not in {'pending', 'approved', 'excluded', 'needs_review'}:
            problems.append(f'{prefix}: review_status invalide')
        if kind == 'element_service' and obj.get('review_status') == 'approved':
            for field in ('service_type_ref', 'price_unit_ref'):
                if not item.get(field):
                    problems.append(f'{prefix}: {field} requis')
        if kind == 'eap' and obj.get('review_status') == 'approved':
            price = item.get('price')
            if price is None or price == '' or isinstance(price, bool):
                problems.append(f'{prefix}: prix EAP explicite requis (0 seulement si gratuit confirmé)')
            else:
                try:
                    if float(str(price).replace(',', '.')) < 0:
                        raise ValueError()
                except ValueError:
                    problems.append(f'{prefix}: prix EAP invalide')
            for field in ('access_type_ref', 'price_model_ref'):
                if not item.get(field):
                    problems.append(f'{prefix}: {field} requis')
        if kind == 'equipment':
            if not str(item.get('category_ref') or '').strip():
                problems.append(f'{prefix}: category_ref Equipment requis')
            instances = item.get('instances') or []
            if not isinstance(instances, list):
                problems.append(f'{prefix}: instances Equipment doit être une liste')
            else:
                instance_codes = []
                for position, instance in enumerate(instances, 1):
                    if not isinstance(instance, dict):
                        problems.append(f'{prefix}: instances[{position}] doit être un objet')
                        continue
                    code = str(instance.get('instance_code') or '').strip()
                    if not code:
                        problems.append(f'{prefix}: instances[{position}].instance_code requis')
                    else:
                        instance_codes.append(code)
                if len(instance_codes) != len(set(instance_codes)):
                    problems.append(f'{prefix}: instance_code Equipment dupliqué')
        for media in obj.get('media', []):
            if not isinstance(media, dict) or not http_url(media.get('source_url')) or not media.get('local_file'):
                problems.append(f'{prefix}: source_url et local_file du média requis')
            if obj.get('review_status') == 'approved' and kind not in {'element_service', 'eap'}:
                problems.append(f'{prefix}: fichier média direct géré seulement pour Service/EAP')
    return problems


def apply_package(package, env, package_path):
    """Envoi explicite des objets approuvés et de leurs images locales."""
    errors = issues(package)
    if errors:
        raise SystemExit('Paquet invalide:\n' + '\n'.join(errors))
    for index, obj in enumerate(package['objects'], 1):
        if obj['review_status'] != 'approved':
            continue
        for media in obj.get('media', []):
            if media.get('rights_confirmed') is not True:
                raise SystemExit(f'Objet {index}: droits du média non confirmés; aucun envoi.')
            media_path = (Path(package_path).resolve().parent / media['local_file']).resolve()
            if not media_path.is_file():
                raise SystemExit(f'Objet {index}: fichier média absent: {media_path}; aucun envoi.')
    load_env(); env = normalize_env(env)
    target = package['target']
    result = izilife_post('/scraper/agentGetPlaceByStringId',
                          {'string_id': target['scope_ref'], 'entity_type': target['scope_type']}, env, timeout=60)
    if not result.get('success'):
        raise SystemExit(f"Cible introuvable: {target['scope_type']}/{target['scope_ref']}: {result.get('error', result)}")
    approved = [obj for obj in package['objects'] if obj['review_status'] == 'approved']
    preflight = izilife_post('/scraper/agentSiteContentPreflight', {
        'scope_type': target['scope_type'], 'scope_ref': target['scope_ref'],
        'requires_service_eap_link': 'oui' if any(
            obj['kind'] == 'eap' and obj['item'].get('service_name') for obj in approved) else 'non',
        'requires_null_service_price': 'oui' if any(
            obj['kind'] == 'element_service' and obj['item'].get('price') is None for obj in approved) else 'non',
    }, env, timeout=60)
    if not preflight.get('success'):
        raise SystemExit(f"Précontrôle BO bloquant, aucun envoi: {preflight.get('error', preflight)}")
    ordered = sorted(enumerate(package['objects'], 1), key=lambda pair: (
        pair[1].get('kind') != 'element_service',
        pair[1].get('kind') == 'eap' and bool(pair[1].get('item', {}).get('pack_composition'))))
    for index, obj in ordered:
        if obj['review_status'] != 'approved':
            print(f"SKIP {index} {obj['kind']} {obj['item']['name']}: {obj['review_status']}")
            continue
        item = dict(obj['item'])
        if obj['kind'] == 'eap':
            item['is_active'] = 0
            item['need_to_be_confirmed_manually'] = 1
        payload = {'kind': obj['kind'], 'scope_type': target['scope_type'],
                   'scope_ref': target['scope_ref'], 'source_url': obj['source_url'], 'item': item}
        response = izilife_post('/scraper/agentIngestSiteItem',
                                {'payload': json.dumps(payload, ensure_ascii=False)}, env, timeout=180)
        if not response.get('success'):
            raise SystemExit(f"Échec objet {index} {item['name']}: {response.get('error', response)}")
        print(json.dumps({'index': index, 'kind': obj['kind'], 'name': item['name'],
                          'created': response.get('created'), 'updated': response.get('updated'),
                          'ids': {key: value for key, value in response.items() if key.endswith('_id')}}, ensure_ascii=False))
        if obj['kind'] in {'element_service', 'eap'}:
            for media in obj.get('media', []):
                media_path = (Path(package_path).resolve().parent / media['local_file']).resolve()
                with media_path.open('rb') as file_handle:
                    image_response = izilife_post('/scraper/agentAttachSiteItemImage', {
                        'scope_type': target['scope_type'], 'scope_ref': target['scope_ref'],
                        'kind': obj['kind'], 'object_name': item['name'], 'rights_confirmed': 'oui',
                        'source_url': media['source_url'],
                    }, env, timeout=180, files={'media': (media_path.name, file_handle)})
                if not image_response.get('success'):
                    raise SystemExit(f"Échec image objet {index}: {image_response.get('error', image_response)}")
                print(json.dumps({'index': index, 'media_id': image_response.get('media_id'),
                                  'media_skipped': image_response.get('skipped', False)}, ensure_ascii=False))


def apply_media_only(package, env, package_path):
    """Rattache les images approuvées aux objets déjà présents, sans upsert Service/EAP."""
    problems = issues(package)
    if problems:
        raise SystemExit('Paquet invalide:\n' + '\n'.join(problems))
    target = package['target']
    images = []
    for index, obj in enumerate(package['objects'], 1):
        if obj['review_status'] != 'approved' or obj['kind'] not in {'element_service', 'eap'}:
            continue
        for media in obj.get('media', []):
            if media.get('rights_confirmed') is not True:
                raise SystemExit(f'Objet {index}: utilisation du média non confirmée; aucun envoi.')
            path = (Path(package_path).resolve().parent / media['local_file']).resolve()
            if not path.is_file():
                raise SystemExit(f'Objet {index}: fichier média absent: {path}; aucun envoi.')
            images.append((index, obj, media, path))
    if not images:
        raise SystemExit('Aucun média approuvé dans le paquet.')
    load_env(); env = normalize_env(env)
    result = izilife_post('/scraper/agentGetPlaceByStringId',
                          {'string_id': target['scope_ref'], 'entity_type': target['scope_type']}, env, timeout=60)
    if not result.get('success'):
        raise SystemExit(f"Cible introuvable: {target['scope_type']}/{target['scope_ref']}")
    for index, obj, media, path in images:
        with path.open('rb') as handle:
            response = izilife_post('/scraper/agentAttachSiteItemImage', {
                'scope_type': target['scope_type'], 'scope_ref': target['scope_ref'],
                'kind': obj['kind'], 'object_name': obj['item']['name'],
                'rights_confirmed': 'oui', 'source_url': media['source_url'],
            }, env, timeout=180, files={'media': (path.name, handle)})
        if not response.get('success'):
            raise SystemExit(f"Échec image {index} {obj['item']['name']}: {response.get('error', response)}")
        print(json.dumps({'index': index, 'name': obj['item']['name'],
                          'media_id': response.get('media_id'), 'skipped': response.get('skipped', False)},
                         ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    export = sub.add_parser('from-analysis')
    export.add_argument('--report', required=True); export.add_argument('--scope-type', choices=['SHOP', 'PLACE'], required=True)
    export.add_argument('--scope-ref', required=True); export.add_argument('--output', required=True)
    check = sub.add_parser('validate'); check.add_argument('--file', required=True)
    apply = sub.add_parser('apply'); apply.add_argument('--file', required=True)
    apply.add_argument('--env', choices=['local', 'staging', 'prod'], required=True)
    apply.add_argument('--confirm-write', action='store_true')
    media_only = sub.add_parser('media-only'); media_only.add_argument('--file', required=True)
    media_only.add_argument('--env', choices=['local', 'staging', 'prod'], required=True)
    media_only.add_argument('--confirm-write', action='store_true')
    args = parser.parse_args()
    if args.command == 'from-analysis':
        package = from_analysis(args.report, args.scope_type, args.scope_ref)
        output = Path(args.output)
        if output.exists():
            raise SystemExit(f'Fichier déjà existant: {output}')
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(package, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'{len(package["objects"])} objets exportés vers {output}; aucun import')
        return
    package = json.loads(Path(args.file).read_text(encoding='utf-8'))
    problems = issues(package)
    if args.command == 'validate':
        print(json.dumps({'objects': len(package.get('objects', [])), 'issues': problems}, ensure_ascii=False, indent=2))
        if problems:
            raise SystemExit(1)
        return
    if not args.confirm_write:
        raise SystemExit('Écriture désactivée: préciser --confirm-write.')
    if args.command == 'media-only':
        apply_media_only(package, args.env, args.file)
    else:
        apply_package(package, args.env, args.file)


if __name__ == '__main__':
    main()
