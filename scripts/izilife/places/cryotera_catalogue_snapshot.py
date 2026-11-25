#!/usr/bin/env python3
"""Transcription vérifiable des offres Cryotera affichées le 28/10/2026.

Ce fichier ne fait aucune requête et aucun import. Les tarifs sont ceux conseillés
sur le site du réseau, et restent à valider pour le centre destinataire.
"""
import json
from pathlib import Path

TARIFF_URL = 'https://cryotera.fr/les-tarifs'
BASE = 'https://cryotera.fr/prestations/'
TARGET = {'scope_type': 'SHOP', 'scope_ref': 'cryotera-pole-de-cryotherapie-lille'}

# nom, URL, prix d'une séance, description brève, offres: libellé/prix/type/nombre
SERVICES = [
    ('Cryothérapie Corps Entier', 'cryotherapie-corps-entier', 42,
     'Immersion à -90 °C en chambre de cryothérapie corps entier.', [
         ('Séance découverte', 30, 'single', 1), ('1 séance', 42, 'single', 1),
         ('5 séances', 190, 'pack', 5), ('10 séances', 350, 'pack', 10),
         ('2 séances / mois', 65, 'subscription', 2),
         ('4 séances / mois', 100, 'subscription', 4),
         ('8 séances / mois', 185, 'subscription', 8)]),
    ('Cryothérapie Localisée', 'cryotherapie-localisee', 45,
     'Application ciblée du froid sur une zone du corps.', [
         ('1 séance', 45, 'single', 1), ('5 séances', 195, 'pack', 5),
         ('10 séances', 350, 'pack', 10), ('4 séances / mois', 110, 'subscription', 4)]),
    ('Pressothérapie', 'pressotherapie', 25,
     'Drainage mécanique destiné à stimuler la circulation lymphatique.', [
         ('1 séance', 25, 'single', 1), ('10 séances', 150, 'pack', 10),
         ('4 séances / mois', 50, 'subscription', 4)]),
    ('Cryolipolyse', 'cryolipolyse', 200,
     'Traitement par le froid des zones ciblées.', [
         ('1 zone · 1 séance', 200, 'single', 1),
         ('1 zone · 3 séances', 550, 'pack', 3),
         ('2 zones · 1 séance', 385, 'single', 1),
         ('2 zones · 3 séances', 985, 'pack', 3)]),
    ('Soin du visage', 'soin-du-visage', 45,
     'Soin du visage associant froid localisé et masque en bio-cellulose.', [
         ('1 séance', 45, 'single', 1), ('5 séances', 195, 'pack', 5),
         ('10 séances', 350, 'pack', 10), ('4 séances / mois', 110, 'subscription', 4)]),
    ('Suivi en nutrition', 'suivi-en-nutrition', None,
     'Accompagnement par un professionnel de la nutrition ; tarif sur devis.', []),
]
PHOTO_FILES = {
    'cryotherapie-corps-entier': 'cryotherapie-corps-entier.jpeg',
    'cryotherapie-localisee': 'cryotherapie-localisee.jpeg',
    'pressotherapie': 'pressotherapie.png',
    'cryolipolyse': 'cryolipolyse.jpeg',
    'soin-du-visage': 'soin-du-visage.jpeg',
    'suivi-en-nutrition': 'suivi-en-nutrition.jpeg',
}


def entry(kind, url, item, status='pending', warnings=None):
    return {'kind': kind, 'source_url': url, 'item': item,
            'review_status': status, 'media': [], 'warnings': warnings or []}


def build():
    objects = []
    for service_name, slug, base_price, description, offers in SERVICES:
        service_url = BASE + slug
        service_item = {'name': service_name, 'description': description,
                        'service_type_ref': 'beaute-et-bien-etre', 'price_unit_ref': 'fixe',
                        'currency': 'EUR', 'status': 1,
                        'source_evidence': service_name}
        if base_price is not None:
            service_item['price'] = base_price
        service_entry = entry('element_service', service_url, service_item,
                              warnings=['Droits de réutilisation du visuel à confirmer'])
        service_entry['media'] = [{'source_url': service_url,
                                   'local_file': 'cryotera_media/' + PHOTO_FILES[slug],
                                   'role': 'cover', 'rights_confirmed': False}]
        objects.append(service_entry)
        # Les tarifs de base sont placés avant les packs qui les référencent.
        for label, price, offer_type, count in sorted(offers, key=lambda x: x[2] != 'single'):
            eap_name = f'{service_name} — {label}'
            access = 'abonnement' if offer_type == 'subscription' else 'lieu'
            price_model = 'abonnement-recurrent' if offer_type == 'subscription' else 'ticket-unitaire'
            eap_item = {'name': eap_name, 'service_name': service_name, 'price': price,
                        'currency': 'EUR', 'access_type_ref': access,
                        'price_model_ref': price_model, 'is_active': 0,
                        'need_to_be_confirmed_manually': 1,
                        'conditions_description': label,
                        'description': 'Tarif conseillé du réseau Cryotera ; centre de Lille à confirmer.'}
            if offer_type == 'pack':
                base_label = '2 zones · 1 séance' if label.startswith('2 zones') else (
                    '1 zone · 1 séance' if service_name == 'Cryolipolyse' else '1 séance')
                eap_item['is_pack_access'] = 1
                eap_item['pack_composition'] = [
                    {'name': f'{service_name} — {base_label}', 'quantity': count}]
            objects.append(entry('eap', TARIFF_URL, eap_item,
                                 warnings=['Tarif conseillé ; conditions commerciales du centre à confirmer',
                                           'Abonnement à configurer avant vente'] if offer_type == 'subscription'
                                 else ['Tarif conseillé ; conditions commerciales du centre à confirmer']))
    bilan = entry('element_service', BASE + 'cryotherapie-corps-entier',
                         {'name': 'Bilan personnalisé offert', 'description': 'Bilan personnalisé sans engagement.',
                          'price': 0, 'currency': 'EUR', 'service_type_ref': 'beaute-et-bien-etre',
                          'price_unit_ref': 'fixe', 'status': 1,
                          'source_evidence': 'Votre bilan personnalisé offert'},
                         warnings=['Vérifier la disponibilité au centre de Lille',
                                   'Droits de réutilisation du visuel à confirmer'])
    bilan['media'] = [{'source_url': BASE + 'cryotherapie-corps-entier',
                       'local_file': 'cryotera_media/bilan-personnalise.jpeg',
                       'role': 'cover', 'rights_confirmed': False}]
    objects.append(bilan)
    return {'schema_version': 'izilife.site_content.v1',
            'source': {'site': 'https://cryotera.fr/', 'tariff_url': TARIFF_URL,
                       'tariff_scope': 'tarifs conseillés dans le réseau de centres indépendants Cryotera',
                       'observed_at': '2026-10-28'},
            'target': TARGET, 'objects': objects}


if __name__ == '__main__':
    destination = Path(__file__).with_name('cryotera_lille_draft.json')
    destination.write_text(json.dumps(build(), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(SERVICES)} prestations, 22 tarifs et 1 bilan : {destination}')
