# Inventaire Agent 2 — agents iziLife

Date : 2026-11-05. Périmètre inspecté : `scripts/core`, `scripts/izilife`, contrôleurs et modèles PHP de la copie staging, classeurs versionnés et conventions Drive de `core.paths`. Le validateur Event est volontairement hors chantier.

| Agent demandé | Script / contrôleur existant | Pilote actuel | Écart factuel | Test réel à effectuer |
|---|---|---|---|---|
| Curate Places + résolution partagée | `places/createur_lieux.py`, `core/paths.py`, PHP `Scraper::agentFetchAndStoreOnePlace` | `curate_places.xlsm`, par zone/env | Le précontrôle Playwright existait dans le créateur seulement. Identité URL/social/string_id non mutualisée. | Classeur local, établissement existant puis absent : vérifier zéro appel payant pour rejet/doublon et un appel uniquement pour création. |
| Créateur Page direct | `agent_pages.py`, PHP `Scraper::agentAddPage` | `pages.xlsx`, par zone/env | Création directe déjà conforme, aucun passage `PlaceTmp`. Normalisation URL était locale ; antidoublon multiclés à raccorder au contrat PHP. | Créer une Page locale, rejouer avec même site/social/string_id et vérifier `created=false`. |
| Validateur Event | `events/validate_event_tmp.py`, `curate_events.xlsx` | zone/env | Hors chantier Agent 2 sur instruction explicite. | Aucun ici. |
| Améliorateur Event | Extraction Event riche dans `Scraper`, `events/ingest_manual_curate.py`, modèles `AgentEventPackage_model` / `AgentEventValidator_model` | Aucun classeur dédié à l’enrichissement d’un Event existant | Agent et pilote dédiés absents ; il faut cibler `string_id` ou `unique_id`, enrichir sans créer. | Local : `unique_id=90e3cd185643a0892c92264a81a9dee0`, source `https://larose.fr/spectacles/le-bal-arrange`, contrôler titre/texte/dates/prix/médias et absence de nouvelle fiche. |
| ExternalOffer + ElementNewsPost + veille | `offers/offer_agent_common.py`, `special_offer.py`, PHP `AgentOffer_model`; modèles BO `ExternalOffer`/`ElementNewsPost` présents | Pas de classeur commun identifié | Agent commun absent. Pilote requis à 3 onglets : offres ponctuelles, news ponctuelles, sources permanentes avec reprise/antidoublon. Payloads exacts à dériver du PHP avant écriture. | Local : une URL site, un post/carrousel Instagram, puis deux relances d’une source permanente sans doublon. |
| Enrichisseur / maintenance / fermeture | `places/enrichisseur.py`, `google_hours_agent.py`, `intelligent_enricher.py`, `enrichisseur_contenus.py`, `medias/media_curator.py`, PHP `AgentLocationMaintenance_model` | `ameliorateur.xlsx`, `enrichisseur_contenus.xlsx`, rapports JSON/XLSX séparés | Fermeture définitive et inactivité sont déjà gérées : ne pas créer un agent de fermeture. Il manque l’orchestrateur, la règle média→cover, la priorité description officielle et le vocabulaire restaurant complet. | Local, une Place et un Shop : fermeture, horaires, tags, sous-type restaurant, description, contenu, média existant sans principal puis principal posé. |
| Transféreur piloté Excel | `commercial_centers/location_transfer.py`, PHP `LocationTypeTransfer` + `LocationTypeTransfer_model` | CLI + plan JSON ; pas de classeur générique | Brique Place/Shop existante, mais pilote Excel source/type/destination et capacités Event/Page/Equipment/Experience absents ou non prouvés. Ne pas confondre avec maintenance. | Local : Place→Shop création, Shop→Place fusion existante, puis audit Event↔Experience/Serie/Annual/Representation avant cas Event. |
| Extraction complète / pilotage | `site_package.py`, `places/site_content_package.py`, `experiences/site_experience_package.py`, `events/*package*`, `structured_configuration_agent.py` | Paquets JSON + CLI multiples | Moteurs présents ; orchestrateur global Event/AnnualCelebration/EventSerie/Experience et pilote unifié manquent. Les contenus fins restent dans `enrichisseur_contenus.py`. | Source locale/HTTP réelle → JSON complet → validate → plan → apply local → relecture graphe créé/mis à jour. |
| Agent territorial | `events/territorial_aggregator.py`, `events/territorial_sources/lille-zone.json` | JSON zone ; rapports JSON/XLSX | Architecture JSON conforme. Vérifier que les sites locaux restent limités à leur zone. Aucun classeur de pilotage à ajouter. | Lancer Lille en local, contrôler filtrage territorial, matching et reprise. |
| Caractéristiques éditoriales Event | Prompts/ingestion dans PHP `Scraper`, modèles Event/Annual/Serie et tables éditoriales | JSON EventTmp / packages | Références existantes à confirmer dans tous les prompts Hub/OCR ; ingestion seulement si référence connue. Ne pas fragiliser OpenAgenda. | Fixture avec MusicStyle valide + inconnue : seule la valide est liée ; test OpenAgenda inchangé. |

## Contraintes vérifiées

- `core.paths` sépare `local`, `staging`, `prod` et normalise les dossiers `{zone}-zone`.
- Les classeurs canoniques vivent sous `$AGENTIC_DRIVE_ROOT/agentic_workspace[_local|_staging]/izilife/...` ; aucune copie suffixée `(1)` ne doit être choisie automatiquement.
- Facebook et Shotgun ont leurs scripts spécialisés et leurs répertoires dédiés ; ils restent hors modifications et hors planification.
- Le worktree contenait déjà de nombreuses modifications et suppressions sans rapport avec ce chantier. Elles doivent être préservées.

## Premier écart corrigé

- Ajout de `scripts/core/place_resolution.py` : précontrôle Maps gratuit, normalisation URL, identité partagée (`google_place_id`, `string_id`, site, réseaux sociaux) et motif de doublon.
- `createur_lieux.py` consomme désormais le résolveur `core` tout en conservant son API publique historique.
- `agent_pages.py` consomme la normalisation URL partagée.
