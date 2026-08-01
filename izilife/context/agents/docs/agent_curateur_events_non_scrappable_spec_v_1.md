# Agent Curateur Events — Sources Non Scrappables (Facebook, Instagram, Shotgun, etc.)

## Objectif

Créer un agent semi-autonome capable de :

- parcourir des plateformes difficiles à scraper ;
- récupérer des événements publics ;
- sauvegarder sources et images ;
- détecter plusieurs événements dans un carousel/agenda ;
- injecter dans les tables temporaires existantes ;
- collaborer avec la curation humaine ;
- éviter les doublons ;
- produire des logs exploitables.

L’objectif n’est PAS :

- publier directement des événements ;
- modifier la prod ;
- remplacer totalement le jugement humain ;
- faire du scraping massif.

Le système doit rester :

- supervisable ;
- traçable ;
- évolutif ;
- compatible avec Facebook / Instagram / Shotgun / autres plateformes futures.

---

# Vision générale

Le système repose sur une logique :

```text
Curation humaine + Curation agentique
→ même file de traitement
→ mêmes scripts d’injection
→ mêmes tables temporaires
→ validation humaine finale
```

L’agent ne crée jamais directement les objets finaux.

Il :

- collecte ;
- extrait ;
- pré-remplit ;
- enrichit ;
- injecte dans *_tmp.

---

# Architecture globale

## Sources principales

### Facebook Events

Utilisation :

- Events publics ;
- sections “Meilleurs”, “Local”, “Cette semaine” ;
- événements visibles sans login si possible.

Actions agent :

- ouvrir la card ;
- récupérer URL ;
- screenshot si nécessaire ;
- détecter date/lieu ;
- récupérer image principale ;
- injecter source.

---

### Instagram

Utilisation :

- posts ;
- carousels ;
- stories sauvegardées ;
- agendas visuels.

Actions agent :

- détecter carousel ;
- parcourir chaque slide ;
- détecter s’il s’agit :
  - d’un agenda ;
  - d’un programme ;
  - de plusieurs événements ;
  - d’une simple galerie photo.

Puis :

- screenshot des slides ;
- OCR ;
- extraction structurée ;
- génération potentielle de plusieurs events.

---

### Shotgun

Utilisation :

- pages events ;
- listings publics ;
- pages organisateurs.

Actions agent :

- récupération URL ;
- récupération image ;
- extraction date ;
- récupération lieu.

---

### Autres plateformes futures

Architecture pensée pour :

- Resident Advisor ;
- Dice ;
- Eventbrite ;
- TikTok ;
- sites de bars ;
- sites de festivals ;
- newsletters ;
- blogs.

---

# Workflow général

## Étape 1 — File centrale de sources

Le système repose sur un Google Sheet partagé.

## Structure

Un fichier par mois.

Exemple :

```text
Izilife Event Sources - 2026-06
```

Un onglet par semaine.

Exemple :

```text
W23
W24
W25
```

---

# Colonnes minimales

| Colonne | Description |
|---|---|
| url | URL source |
| status | TODO / OK / FAILED / DUPLICATE / SKIP |
| source | HUMAN / AGENT |
| note | erreur ou remarque |
| processed_at | date de traitement |
| image_fingerprint | hash image si disponible |
| city | ville principale |
| platform | FACEBOOK / INSTAGRAM / SHOTGUN |

---

# Workflow humain

## Curation manuelle

L’humain :

- navigue sur Facebook/Instagram/Shotgun ;
- colle simplement les URLs intéressantes ;
- ne remplit rien d’autre.

Exemple :

```text
https://facebook.com/events/xxxxx
https://shotgun.live/events/yyyy
https://instagram.com/p/zzzzz
```

---

# Workflow agent

## Phase 1 — Traitement de la file

L’agent :

1. lit les lignes TODO ;
2. ouvre chaque URL ;
3. récupère contenu ;
4. sauvegarde screenshots/images ;
5. détecte doublons ;
6. lance les scripts existants ;
7. injecte dans *_tmp ;
8. met à jour le Sheet.

---

# États possibles

| Statut | Signification |
|---|---|
| TODO | À traiter |
| OK | Traitement réussi |
| FAILED | Erreur |
| DUPLICATE | Déjà traité |
| SKIP | Ignoré volontairement |
| NEEDS_REVIEW | Ambigu ou douteux |

---

# Phase 2 — Curation autonome

Une fois la file TODO vide :

l’agent peut commencer sa propre exploration.

Exemple :

```text
Facebook Events Lille
→ Local
→ Meilleurs
→ Cette semaine
```

L’agent :

- parcourt les cards ;
- ouvre les événements ;
- récupère URL ;
- vérifie si déjà présent ;
- ajoute au Sheet ;
- traite.

---

# Anti-doublons

## Vérifications minimales

Avant traitement :

- URL déjà présente ;
- image_fingerprint déjà présent ;
- google_place_id déjà lié ;
- event déjà existant.

---

# Instagram — Gestion des carousels

## Objectif

Détecter lorsqu’un carousel contient :

- plusieurs événements ;
- un agenda hebdomadaire ;
- un programme mensuel ;
- plusieurs dates.

---

# Cas 1 — Carousel simple

Exemple :

```text
Slide 1 → affiche event
Slide 2 → photo ambiance
Slide 3 → teaser
```

Résultat :

```text
1 seul événement
```

---

# Cas 2 — Agenda multi-events

Exemple :

```text
Slide 1 → Lundi
Slide 2 → Mardi
Slide 3 → Mercredi
Slide 4 → Jeudi
```

Ou :

```text
Programme Juin 2026
```

Résultat :

```text
Plusieurs événements détectés
```

L’agent doit :

- OCR chaque slide ;
- détecter les dates ;
- découper les événements ;
- générer plusieurs entrées.

---

# Heuristiques Instagram

## Détection agenda

Indices :

- jours de semaine ;
- dates multiples ;
- horaires multiples ;
- titres multiples ;
- grilles ;
- tableaux ;
- “programme” ;
- “line-up”.

---

# Fingerprint image

## Objectif

Détecter :

- reposts ;
- duplicates ;
- screenshots identiques ;
- mêmes affiches.

---

# Version simple

```text
sha1(image_file)
```

---

# Version avancée future

Perceptual hash :

```text
pHash
```

Permet :

- reconnaître une même image recadrée ;
- reconnaître screenshots différents.

---

# Dossiers de travail

## Workspace agent

```text
izilife-agent-workspace/
├── facebook_events/
│   ├── todo/
│   ├── done/
│   ├── failed/
│   └── screenshots/
│
├── instagram/
│   ├── screenshots/
│   ├── carousels/
│   └── extracted/
│
├── shotgun/
│   ├── screenshots/
│   └── extracted/
│
├── logs/
└── prompts/
```

---

# Insertion BO

## Principe

L’agent n’insère jamais directement un event final.

Il :

- utilise les méthodes autorisées ;
- remplit les tables temporaires ;
- laisse la validation humaine.

---

# Méthodes autorisées

## Events

```text
postScrapEventsFromBloggerWebsite()
postUploadEventImages()
postUploadEventSources()
postUploadEventSourcesReplacement()
```

Scopes :

```text
event_tmp:create_from_source
event_tmp:create_from_image
```

---

# Experiences

```text
postScrapExperiencesFromBloggerWebsite()
```

Scope :

```text
experience_tmp:create_from_source
```

---

# Places

```text
postFetchAndStoreOnePlace()
```

Scope :

```text
place_tmp:fetch_or_create
```

---

# Sécurité

## Comptes utilisés

Toujours :

- compte service dédié ;
- jamais compte perso ;
- jamais accès prod au début.

---

# Permissions

Les comptes service :

- peuvent créer du temporaire ;
- peuvent uploader des sources ;
- ne peuvent pas :
  - publier ;
  - supprimer ;
  - confirmer ;
  - modifier la prod.

---

# Cowork — rôle réel

Cowork agit comme :

```text
opérateur semi-autonome
```

Il :

- ouvre les plateformes ;
- navigue ;
- récupère ;
- screenshot ;
- OCR ;
- injecte ;
- log.

Il ne remplace pas encore :

- le jugement éditorial final ;
- la validation humaine ;
- la supervision.

---

# Première mission recommandée

## Agent Facebook Events Lille

Objectif :

- traiter 10 événements max ;
- Lille + alentours ;
- Facebook seulement.

Workflow :

```text
1. Lire TODO dans le Sheet.
2. Traiter les URLs.
3. Injecter dans *_tmp.
4. Mettre OK.
5. Puis seulement faire de la découverte autonome.
```

---

# Critères minimums d’un event acceptable

Au début :

approche large.

Ne rejeter que :

- spam évident ;
- événement sans date ;
- événement hors zone ;
- contenu déjà passé ;
- contenu illisible.

L’objectif est :

```text
volume + variété
```

avant :

```text
sélection éditoriale parfaite
```

---

# Évolution future

## Phase 1

Semi-automatique.

Humain fournit beaucoup d’URLs.

---

## Phase 2

Agent découvre des events lui-même.

---

## Phase 3

Classement intelligent :

- qualité ;
- ambiance ;
- popularité ;
- diversité ;
- cohérence locale.

---

## Phase 4

Réseau multi-villes :

- Lille ;
- Valenciennes ;
- Paris ;
- Marseille ;
- Toulouse.

---

# Conclusion

Le système n’est pas un “scraper classique”.

C’est :

```text
une chaîne de curation hybride humain + IA
```

avec :

- collecte ;
- screenshots ;
- OCR ;
- extraction ;
- anti-doublons ;
- injection temporaire ;
- validation humaine.

Le premier objectif n’est pas l’autonomie totale.

Le premier objectif est :

```text
supprimer le travail répétitif de collecte et d’injection
```

sans perdre le contrôle éditorial.

