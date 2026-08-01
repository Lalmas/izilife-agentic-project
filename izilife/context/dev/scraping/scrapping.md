# izilife — Scripts de scrapping

> Charger aussi : izilife-global.md, dev/architecture.md

## Scripts existants
- Scrapping events depuis sites blogger/agenda
- Scrapping expériences
- Upload images events par URL
- `postFetchAndStoreOnePlace()` — fetch + store un lieu Google Places
- Parser page menu d'un lieu (source HTML — à migrer vers CIC)
- Nearby Search par catégorie + ville + rayon
- Place Details par place_id
- Photos par place_id

## Hubs de villes
- Un Hub = config d'une ville : sources, comptes Insta/FB, sites agenda, catégories Places
- Lancement hub par hub pour isoler les erreurs
- Sites non scrappables HTML → basculer vers CIC (désactivé jusqu'à Max 200€)

## Règles Google Places API
- Free tier : ~28 000 requêtes/mois (toutes villes confondues)
- Nearby Search : 1 requête par catégorie × rayon
- Place Details : 1 requête par lieu → stocker le JSON, ne plus rappeler
- Photos : 1 requête par lieu → stocker les URLs
- **Ne jamais relancer une ville déjà scannée**

## Objets sans script encore
- Circuit — à construire
- Match/Compétition — saisie manuelle, pas de scrapping
- Equipment/Transport — sources : Google Places (transit_station…), fichiers GTFS, collectivités
- Menu — script existant à migrer vers CIC
- LocalHabit, LocalTip, OutingIdea — saisie guidée ou CIC

## Déduplication (avant toute insertion en _tmp)
- Par URL source
- Par hash image
- Par google_place_id (lieux)

## Sites dynamiques (nécessitent CIC — désactivé jusqu'à Max 200€)
- Instagram events / comptes
- Facebook events
- Shotgun, Eventbrite
- TripAdvisor (enrichissement lieux)
- Sites restaurant avec menu en JS
