# Agent — Chasseur d'events

> Charger aussi : izilife-global.md, dev/agents-socle.md

## Rôle
Trouver et ingérer les events de la ville depuis toutes les sources.
Remplacer complètement le travail manuel de curation d'events.
Toujours via _tmp — jamais d'écriture directe en prod.

## Déclenchement
- **Dimanche** : run complet toutes sources (cron PC local)
- **WhatsApp partenaires** : 24h/24 via webhook (cron OVH)
- **Manuel** : à tout moment — image ou lien → même tuyau

## Sources
- Instagram (comptes suivis dans le Hub de la ville)
- Facebook events
- Shotgun, Eventbrite, BilletRéduc
- Sites agenda locaux
- WhatsApp partenaires (lieux qui envoient flyers/liens)
- Toi en curation manuelle (même tuyau JSON)

## Outils
- **CIC** : lit les pages dynamiques (Instagram, Facebook, Shotgun)
  → **désactivé jusqu'à Max 200€**
- **Cowork** : scroll + sauvegarde source HTML → PHP parse (version Pro 20€)
- **PHP webhook** : reçoit les messages WhatsApp Business API
- **Claude API** : OCR sur les flyers image (ponctuel)

## Workflow CIC (version Max 200€)
1. CIC ouvre chaque source du Hub de la ville
2. Lit et comprend la page : titre, date, lieu, image, lien billetterie
3. Construit le JSON event directement
4. Push via postIngestJson(type=event) → event_tmp

## Workflow Cowork (version Pro 20€ — actif maintenant)
1. Cowork ouvre Chrome, va sur le compte Instagram/FB
2. Scrolle, clique droit → "Enregistrer la source HTML"
3. Script PHP parse le HTML → extrait les données
4. Si image flyer → Claude API OCR → JSON
5. Push via postIngestJson(type=event) → event_tmp

## Workflow WhatsApp partenaires
1. Lieu envoie flyer (image) ou lien dans le channel WhatsApp Business
2. Webhook PHP reçoit le message
3. Si image → Claude API OCR → JSON event
4. Si lien → PHP fetch la page → extraire les données
5. Push via postIngestJson(type=event) → event_tmp

## Déduplication (avant toute insertion)
- Par URL source
- Par hash image (si flyer)
- Par couple (lieu_id + date + titre approximatif)

## JSON de sortie attendu
```json
{
  "type": "event",
  "source": "chasseur-events",
  "source_url": "https://...",
  "fields": {
    "titre": "Soirée Jazz au Bistrot",
    "date_debut": "2025-06-07 21:00",
    "date_fin": "2025-06-08 02:00",
    "place_id_izilife": 42,
    "google_place_id": "ChIJ...",
    "description": "...",
    "image_url": "https://...",
    "lien_billetterie": "https://...",
    "prix": "10€",
    "tags": ["jazz", "concert", "bar"]
  }
}
```

## Cron
```
# OVH staging — webhook WhatsApp (tourne en continu)
# PC local — run hebdo sources sociales
0 9 * * 0  php /scripts/agents/chasseur-events.php --mode=full
```
