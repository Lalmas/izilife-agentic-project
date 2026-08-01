# Agent — Chasseur d'Events (Sources Non-Scrappables)

> Charger aussi : izilife-global.md, dev/agents-socle.md

---

## Rôle et périmètre

Cet agent **ne remplace pas le Hub de scraping**.

Le Hub s'occupe déjà des sources scrappables automatiquement : sites de mairies, Zénith, salles de spectacle, gros référenceurs. Une Spark command le fait tourner chaque semaine.

Cet agent s'occupe **uniquement des plateformes qui bloquent le scraping automatique** :
- Instagram
- Facebook Events
- Shotgun
- Dice, Resident Advisor, Eventbrite, et toute future plateforme bloquante

Son rôle n'est pas d'extraire les données — c'est de **collecter les sources** (liens, images, HTML) et de les déposer dans la file Google Sheet. Un script PHP côté izilife fait le reste sans consommer de tokens.

**Principe fondamental : séparer navigation (tokens légers) et traitement (0 token PHP).**

---

## Zone de lancement

Lille + zone ~30km : Roubaix, Tourcoing, Villeneuve-d'Ascq, Arras, Béthune, Valenciennes et petites villes alentour.

Dans Google Sheet : un fichier par zone géographique (ex. `izilife-events-lille-zone`).

---

## Deux versions

### Version Pro 20€ — active maintenant

**Ce que fait l'agent (Claude in Chrome / Cowork) :**
1. Ouvre la plateforme (FB, Shotgun, Instagram)
2. Scrolle et identifie les events
3. Pour chaque event : vérifie **uniquement** si le lien ou l'image est déjà dans le Sheet
4. Si absent → dépose dans le Sheet :
   - FB / Shotgun : l'URL de l'event
   - Instagram : screenshot du post/flyer → dépose dans Google Drive → lien Drive dans le Sheet
5. Ne lit pas la date, ne génère pas de JSON → **0 token d'analyse**

**Ce que fait le script PHP (côté izilife, 0 token) :**
1. Lit le Sheet, prend les lignes au statut `TODO`
2. Pour les URLs (FB/Shotgun) : fetch la source HTML → appelle `postScrapEventsFromBloggerWebsite()` ou `postUploadEventSources()`
3. Pour les images Drive (Instagram) : télécharge le fichier → appelle `postUploadEventImages()` → OCR LLM côté izilife → JSON → `scraping_event_tmp`
4. Filtre les dates passées (pas l'agent — le script)
5. Met à jour le statut dans le Sheet : `OK` / `FAILED` / `DUPLICATE`

**Ce que fait la curation manuelle (toi) :**
- Même tuyau exactement
- FB/Shotgun : tu colles l'URL dans le Sheet
- Instagram : tu prends le screenshot sur mobile → tu le déposes dans le bon dossier Google Drive → tu colles le lien Drive dans le Sheet
- Statut `TODO` → le script prend le relais automatiquement

### Version Max 200€ — future

Claude in Chrome fait tout en une session :
1. Scrolle la plateforme
2. Lit et comprend le contenu de chaque event (date, lieu, description, image)
3. Construit le JSON directement
4. Push via `postIngestJson(type=event)` → `scraping_event_tmp`

Avantage : plus rapide, zéro script intermédiaire.
Activation : dès passage au plan Max 200€.

---

## Comptes nécessaires

| Plateforme | Compte requis | Notes |
|---|---|---|
| Shotgun | Non (à vérifier) | Pages events publiques |
| Facebook | Oui — compte dédié agent | Pas le compte perso |
| Instagram | Oui — compte dédié agent | Liste de comptes locaux à suivre |

La liste des comptes Instagram à surveiller est maintenue dans le Hub de la zone (Google Sheet, onglet `Sources`).

---

## Instagram — cas spécial

Instagram ne se scrape pas par lien utile. Le contenu est souvent un **flyer image** ou un **carousel**.

Workflow :
- L'agent fait un **screenshot** du post (ou de chaque slide si carousel)
- Le screenshot est déposé dans **Google Drive** dans le dossier de la zone (`Drive/izilife-events/lille-zone/instagram/YYYY-MM/`)
- Dans le Sheet : lien Drive + hash SHA1 calculé par le script PHP (pas par toi)
- Le script PHP télécharge l'image, calcule le fingerprint, appelle `postUploadEventImages()`, l'OCR est fait côté izilife

**Carousel / agenda multi-events :**
- Si le carousel contient plusieurs events distincts (programme semaine, line-up) → un screenshot par slide
- Chaque slide = une ligne dans le Sheet
- Le script PHP les traite indépendamment

---

## Google Sheet — structure

```
Google Drive/
└── izilife-events/
    ├── lille-zone/
    │   ├── 2026-06.gsheet   ← fichier du mois
    │   ├── 2026-07.gsheet
    │   └── instagram/       ← dossier images screenshots
    │       └── 2026-06/
    ├── paris-zone/
    └── dunkerque-zone/
```

**Structure d'un fichier mensuel :**
- Un onglet par semaine : `W23`, `W24`, `W25`, `W26`

**Colonnes d'un onglet :**

| Colonne | Description |
|---|---|
| `url` | URL de l'event (FB, Shotgun) ou lien Google Drive (Instagram image) |
| `platform` | `FACEBOOK` / `INSTAGRAM` / `SHOTGUN` / `MANUAL` |
| `status` | `TODO` / `OK` / `FAILED` / `DUPLICATE` / `SKIP` / `NEEDS_REVIEW` |
| `source` | `AGENT` / `HUMAN` |
| `city` | Ville principale de l'event |
| `image_fingerprint` | SHA1 calculé par le script PHP (pas rempli à la saisie) |
| `tmp_id` | ID inséré dans `scraping_event_tmp` si OK |
| `note` | Erreur, remarque, raison du SKIP |
| `processed_at` | Date de traitement par le script |

---

## Déduplication

Effectuée par le **script PHP**, pas par l'agent :
- URL déjà présente dans le Sheet (même colonne `url`)
- `image_fingerprint` déjà présent dans le Sheet ou dans `scraping_event_tmp.file_fingerprint`
- `scraping_event_tmp.urlRecentlyScraped()` — 7 jours
- `scraping_event_tmp.fileRecentlyScraped()` — 14 jours

L'agent vérifie **uniquement** si l'URL/lien est déjà dans le Sheet avant d'ajouter une ligne (vérification légère, pas d'appel BDD).

---

## Déclenchement

| Mode | Qui | Quand |
|---|---|---|
| Run complet agent | Claude in Chrome (PC local) | Dimanche matin |
| Curation manuelle | Toi | N'importe quand |
| Traitement Sheet | Script PHP (OVH ou local) | Après chaque ajout, ou cron horaire |
| WhatsApp partenaires | Webhook PHP (OVH) | 24h/24 — pipeline séparé |

---

## WhatsApp partenaires (pipeline séparé)

Le lieu envoie un flyer (image) ou un lien dans le channel WhatsApp Business.
Webhook PHP reçoit → si image → `postUploadEventImages()` → OCR côté izilife → `scraping_event_tmp`.
Ce pipeline ne passe pas par le Sheet — il injecte directement.

---

## Évolution par plateforme

Dès qu'une nouvelle plateforme bloque le scraping automatique :
1. Créer le script PHP parser dédié côté izilife (basé sur la structure HTML du site)
2. Ajouter la valeur dans la colonne `platform` du Sheet
3. L'agent n'a rien à changer — il dépose juste l'URL dans le Sheet

Si la structure HTML du site change et que le script plante :
1. Analyser la nouvelle structure
2. Mettre à jour le script PHP uniquement
3. L'agent continue sans modification

---

## Ce que cet agent ne fait PAS

- Il ne génère pas de JSON
- Il ne lit pas les dates (délégué au script PHP)
- Il n'écrit jamais directement dans `scraping_event_tmp`
- Il ne valide jamais un event en prod
- Il ne gère pas les sources scrappables (c'est le Hub + Spark command)
