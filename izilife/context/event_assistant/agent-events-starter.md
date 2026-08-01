# Chantier — Agent Events izilife

> Charger avec : izilife-global.md + izilife-social-strategy.md
> Ce chantier est séparé du chantier CM réseaux sociaux.

---

## Ce que fait cet agent

Deux missions distinctes :

### Mission 1 — Communication event
Génère les posts Instagram/Facebook pour chaque event (caption + slides + image).

### Mission 2 — Préparation event
Aide à préparer le contenu de l'event :
- Sélectionne les questions quiz depuis la banque
- Génère les fiches Blind Test (extraits musicaux par thème)
- Construit les épreuves Izilympics
- Évite les répétitions avec les 4 events précédents

---

## Types d'events

### EVENT_SERIE — events izilife récurrents

| Event | Format | Complexité |
|-------|--------|-----------|
| Quiz Kahoot | Simple, smartphone, classement auto | ⭐ |
| Quiz izilife | Animé, manches variées (CG, visuels, défis, finale) | ⭐⭐⭐ |
| Blind Test classique | Titre/artiste/film | ⭐ |
| Blind Test izilife | Manches thématiques, Urban Old School / Pop Culture | ⭐⭐⭐ |
| Izilympics | Équipes mélangées, mises, bonus, boost — format le plus élaboré | ⭐⭐⭐⭐⭐ |
| Chill Apartment | Speakeasy moderne, lieu secret, artistes live, 1-2x/mois | ⭐⭐ |
| Wine Tasting | Dégustation, public afterwork | ⭐⭐ |
| Karaoké Battle | Compétitif, duel ou équipe, vote public | ⭐⭐ |
| Karaoké libre | Classique | ⭐ |
| Bingo Party | Chill, dimanche/mardi | ⭐ |
| Soirée Jeux | Time's Up, Dixit, Codenames... | ⭐ |
| Open Mic | Scène ouverte, musiciens + stand-up | ⭐⭐ |

### EVENT_ANIMATEUR — on paie le fondateur pour animer un lieu
Même types d'events mais pour un client externe.
Le fondateur est prestataire. Tarifs : 150-300€ selon format.

---

## Architecture multi-zones

Chaque zone (Lille, Valenciennes, Arras...) a :
- Sa propre banque de questions (onglets dans le Sheets)
- Son historique des 4 derniers events
- Ses organisateurs/bénévoles assignés
- BDD commune partagée entre zones

Structure Sheets :
```
Questions_Quiz.gsheet
  ├── Cinéma & Séries
  ├── Musique
  ├── Culture Générale
  ├── Géographie
  ├── Sport
  ├── Nordiste / Local
  └── [par zone si questions locales]

Historique_Events.gsheet
  ├── Lille
  ├── Valenciennes
  ├── Arras
  └── ...
```

---

## Règle anti-répétition

Avant de sélectionner des questions ou thèmes :
1. Lire les 4 derniers events de la zone concernée
2. Exclure toute question/thème déjà utilisé dans ces 4 events
3. Prioriser les catégories non utilisées récemment

---

## Générateur images event

| Type | Image |
|------|-------|
| Posts COM event | Template Canva par type (Quiz, Blind Test, Izilympics...) |
| Posts humour/histoire | Génération via LLM image (configurable : DALL-E, Canva Magic, Stable Diffusion...) |

Config image dans colonne DATA du planning :
- `IMAGE_LLM: description` → appelle le provider configuré (pas DALL-E spécifiquement)
- `IMAGE_CANVA: description` → appelle Canva Magic Media
- Rien → texte uniquement

Variable : `IMAGE_PROVIDER = "dalle" | "canva_magic" | "stable_diffusion"`

---

## Fichiers à créer dans ce chantier

- `context/events/agent-events.md` — system prompt agent
- `context/events/playbook-quiz-izilife.md` — règles Quiz izilife
- `context/events/playbook-blindtest-izilife.md` — règles Blind Test
- `context/events/playbook-izilympics.md` — règles Izilympics (le plus complexe)
- `scripts/events/prepare_event.py` — script préparation event
- `scripts/events/cm_event.py` — script communication event

---

## Docs sources à lire au démarrage de ce chantier

- `__PLAYBOOK_OFFICIEL___FUNNY_QUIZ.docx`
- `__Banque_officielle___IZI_Lympic_Games.docx`
- `Liste_IziLympic_Games.docx`
- `Description_des_events.docx`
- `Events_Animateur_de_Lieux_-_Catalogue.docx`
- `Event_Chill_Appartment.docx`
- Screenshot banque questions Sheets (Cinéma & Séries)

---

## À faire dans la prochaine conversation

1. Lire tous les docs sources
2. Construire playbook-quiz-izilife.md
3. Construire playbook-izilympics.md (le plus complexe)
4. Définir la structure Sheets historique par zone
5. Coder prepare_event.py
