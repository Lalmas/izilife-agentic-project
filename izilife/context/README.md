# izilife — Répertoire de contexte agents

Ce répertoire contient tous les fichiers de contexte pour piloter
les agents et les conversations Claude autour du projet izilife.

## Règle d'or
Toute nouvelle conversation Claude commence par charger le(s) fichier(s)
correspondant au chantier. Coller le contenu en début de conversation.

## Structure

```
izilife-context/
│
├── README.md                      ← ce fichier
├── izilife-global.md              ← TOUJOURS charger en premier
│
├── dev/
│   ├── architecture.md            ← tables, controllers, méthodes
│   ├── scrapping.md               ← scripts existants, hubs, règles API
│   └── agents-socle.md            ← postIngestJson, classe Agent, variable LLM
│
├── agents/
│   ├── inspecteur-ville.md        ← audit ville, Places API, 0 token
│   ├── greffier.md                ← intégration lieux manquants
│   ├── enrichisseur.md            ← amélioration fiches (CIC, Max 200€)
│   ├── chasseur-events.md         ← curation events toutes sources
│   ├── chasseur-promos.md         ← HH, codes promos, deals
│   ├── community-manager.md       ← réseaux sociaux izilife + clients
│   └── redacteur-blog.md          ← blog izilife RSS → article
│
├── social/
│   ├── izilife-style.md           ← ton, posture fédérateur, formats
│   └── planning-template.md       ← structure Google Sheets éditorial
│
├── events/
│   ├── animateur.md               ← rôle organisateur, types d'events
│   └── generateur-contenu.md      ← quiz, blind test, bingo, flyers
│
├── wordpress/
│   ├── clients.md                 ← modèle agence, workflow Claude Code
│   └── clients/                   ← 1 fichier .md par client
│       └── protect-solaire.md     ← (à créer)
│
├── infra/
│   └── orchestration.md           ← crons, Sheets hub, PC local, OVH
│
└── Docs/
    └── navigation-taxonomie-2026-09-10.md ← synthèse de 01_navigation.sql
```

## Quel fichier charger selon le chantier ?

| Chantier | Fichiers à charger |
|----------|--------------------|
| Dev PHP / BDD / API | `izilife-global.md` + `dev/architecture.md` |
| Curation réutilisable / API interne V0 | `izilife-global.md` + `dev/curation-et-api-interne-v0.md` |
| Extraction ponctuelle d'un site complexe | `dev/BRIEF_EXTRACTION_SITES_COMPLEXES.md` + `scripts/izilife/places/README_site_content_package.md` |
| Catalogue Services et EAP | `CATALOGUE_SERVICES_EAP.md` + `CATALOGUE_PRODUCT_HANDOFF.md` |
| Scrapping / hubs | `izilife-global.md` + `dev/scrapping.md` |
| Construire un agent | `izilife-global.md` + `dev/agents-socle.md` + `agents/[nom].md` |
| Agrégateurs territoriaux d'événements | `agents/AGREGATEURS_EVENTS_JDS_INFOLOCALE.md` |
| Extraction intelligente d'un événement, festival, PDF ou agenda/carrousel | `agents/EVENT_GRAPH_PACKAGE.md` + `agents/event-package-v1.schema.json` |
| Amélioration sémantique d'une fiche | `agents/AMELIORATEUR_INTELLIGENT.md` |
| Conversion contrôlée Shop vers Place | `agents/TRANSFERT_SHOP_VERS_PLACE.md` |
| Conversions BO Event / XP / EventSerie | `agents/CONVERSIONS_EVENT_XP_SERIE.md` |
| État opérationnel Agents 5 | `agents/POST_LIVRAISON_AGENTS_5.md` |
| Réseaux sociaux | `izilife-global.md` + `social/izilife-style.md` + `agents/community-manager.md` |
| Events & animation | `izilife-global.md` + `events/animateur.md` + `events/generateur-contenu.md` |
| Site WordPress client | `izilife-global.md` + `wordpress/clients.md` + `wordpress/clients/[client].md` |
| Infra / orchestration | `izilife-global.md` + `infra/orchestration.md` |
| Navigation / taxonomie / moteurs | `izilife-global.md` + `Docs/navigation-taxonomie-2026-09-10.md` |

## À compléter
- [ ] Ajouter les vrais noms de tables depuis tables.sql
- [ ] Ajouter les vrais noms de controllers et méthodes
- [ ] Créer `wordpress/clients/protect-solaire.md`
- [ ] Créer `agents/cm-clients/` avec un .md par client agence
- [ ] Compléter les sources RSS dans `agents/redacteur-blog.md`
- [ ] Ajouter les nouveaux objets métier quand confirmés
# Mise à jour V2 du 9 août 2026

Les décisions actives sur la géographie Event/Experience/Place/Shop, les lieux par séance et le socle Community/UserGroup sont consolidées dans `Experience$/BOOKING_ACCESS_SESSIONS_DOMAIN.md` et `Communautes_et_groupes/SOCLE_V2_2026-08-08.md`. Elles priment sur toute ancienne note proposant de déduire `Experience.city_id` depuis une division administrative.
