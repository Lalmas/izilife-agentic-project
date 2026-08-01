# Agent — Inspecteur de ville

> Charger aussi : izilife-global.md, dev/agents-socle.md, dev/architecture.md

## Rôle
Auditer une ville complète une seule fois.
Trouver les lieux manquants sur izilife.
Détecter les lieux probablement fermés.
Produire un rapport actionnable pour le Greffier et l'Enrichisseur.

## Déclenchement
- 1 fois par ville (passe initiale)
- Mensuel ensuite : comparaison légère avec la liste stockée (pas de nouvel appel Places API)
- Manuel : quand on veut couvrir une nouvelle ville

## Outils
- PHP + Google Places API (Nearby Search) — 0 token Claude
- Google Sheets pour le rapport

## Workflow
1. Charger les place_id déjà en BDD izilife pour cette ville (Place + Shop + Equipment)
2. Nearby Search par catégorie (restaurant, bar, museum, gym, **toilet, park, bicycle_store**…) + rayon
3. Stocker tous les place_id retournés dans une table de référence
4. Comparer avec BDD izilife → 3 listes :
   - **Manquants** → file de tâches Greffier
   - **Présents score bas** → file de tâches Enrichisseur
   - **Suspects fermés** (`business_status ≠ OPERATIONAL`) → rapport
5. Écrire le rapport dans Google Sheets (onglet "Inspecteur")

## Types Google Places à couvrir
Lieux classiques + **Équipements urbains** :
- `toilet` → toilettes publiques
- `park` → parcs (avec terrain de sport, street workout cage…)
- `bicycle_parking`, `bicycle_store` → mobilité vélo
- `transit_station`, `bus_station`, `subway_station`, `train_station` → transports
- `parking` → stationnement
- `electric_vehicle_charging_station` → bornes électriques

Ces types Google doivent être dans `google_maps_categories_helper.php` et mappés vers les
bonnes `EquipmentCategory`. Si pas mappé → `ScrapingUnmappedPoi` → classification manuelle.

## Règles
- Ne jamais relancer Nearby Search sur une ville déjà scannée
- Semaines suivantes : comparer liste stockée avec BDD, pas d'appel API
- Un lieu fermé n'est pas supprimé — signalé pour validation humaine
- Max ~28 000 requêtes/mois Google Places (toutes villes confondues)

## Output (Google Sheets — onglet "Inspecteur")
| place_id | nom | adresse | type | statut | action | date_détection |
|----------|-----|---------|------|--------|--------|----------------|

## Cron OVH staging
```
0 1 * * 1  php /scripts/agents/inspecteur.php --ville=lille --mode=maintenance
```
