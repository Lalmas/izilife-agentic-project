# Projet : Équipes d'Agents IA — Architecture & Roadmap

## Contexte

Je suis entrepreneur avec deux projets en parallèle :
- **Protect Solaire** (protect-solaire.com) — site e-commerce WordPress/WooCommerce en cours de refonte
- **izilife** — app de découverte de lieux, events et bons plans

Pour financer izilife, je développe une activité de **création et maintenance de sites WordPress** pour des clients. L'ensemble de ces projets doit être piloté et automatisé via des équipes d'agents IA.

Stack technique : PHP, WordPress/WooCommerce, XAMPP local, serveur OVH (SSH disponible), Claude Code, Claude.ai desktop app.

---

## Les 4 Équipes d'Agents

### Équipe 1 — Clients WordPress (Sites & Dev)

**Objectif** : Gérer la création, maintenance et développement sur mesure des sites WordPress clients sans intervention manuelle répétitive.

**Outils** : Claude Code (SSH sur serveurs clients), Git/GitHub par projet client

**Workflow** :
```
Demande client
→ Claude Code lit les fichiers via SSH
→ Génère / modifie le code
→ Push sur GitHub (branche par client)
→ Déploie sur le serveur client
```

**À construire** :
- Template de projet WordPress réutilisable
- Prompt système par client (contexte, accès SSH, chemin WP, identifiants Git)
- Workflow Git : branche dev → review → merge → deploy
- Script de sync serveur → GitHub pour les projets existants

---

### Équipe 2 — Réseaux Sociaux (Startup + Clients)

**Objectif** : Générer, programmer et publier du contenu pour izilife et les clients, uniquement pour générer du cash à court terme.

**Outils** : Claude (génération), Cowork (automatisation bureau), Claude in Chrome (navigation/scraping réseaux), Google Sheets (planning)

**Workflow** :
```
Google Sheets (planning éditorial)
→ Claude génère les posts (texte + prompt image)
→ Cowork programme la publication
→ Claude in Chrome publie si API indisponible
```

**Cas d'usage spécifiques** :
- Scraping d'events Instagram : Claude in Chrome clique "Partager" → récupère le lien → script télécharge l'image → OCR → extraction données
- Veille concurrents : Claude in Chrome + Perplexity MCP pour sources éparpillées
- Historique dans Google Sheets : déduplication par URL + hash image

---

### Équipe 3 — Pilotage Startup izilife

**Objectif** : M'aider à prendre des décisions, suivre les KPIs, prioriser les développements.

**Outils** : Cowork (fichiers/rapports), Claude Code (analyse données, scripts), Claude Chat (réflexion stratégique)

**Workflow** :
```
Données brutes (BDD, analytics, Sheets)
→ Claude Code extrait et formate
→ Claude analyse et recommande
→ Cowork génère les rapports / dashboards
```

**À construire** :
- Dashboard hebdomadaire automatique
- Script d'extraction KPIs depuis BDD izilife
- Prompt système "pilote startup" avec contexte business complet

---

### Équipe 4 — Curation d'Articles (Blog izilife)

**Objectif** : Trouver, filtrer et préparer des sources pour les articles de blog izilife de façon semi-automatique.

**Outils** : Script PHP (RSS), Perplexity MCP (recherche éparpillée), Claude API (résumé/rédaction), Google Sheets (hub central)

**Architecture** :
```
Sites avec RSS → Script PHP cron → Google Sheets
Sites sans RSS → Claude in Chrome → scrape → Google Sheets
Sujets ouverts → Perplexity MCP → synthèse → Google Sheets
        ↓
Claude résume / classe / rédige le brief
        ↓
Article publié sur izilife
```

**Règles** :
- Script PHP pour RSS = zéro token consommé
- Google Sheets = hub central avec historique
- Déduplication : par URL + hash image
- Claude intervient uniquement pour analyse/rédaction, pas pour la collecte brute

---

## Architecture Technique Globale

```
┌─────────────────────────────────────────────────────┐
│                  PIPELINE PRINCIPAL                  │
│                                                      │
│  Sites RSS ──→ Script PHP cron                       │
│  Sites statiques ──→ Script PHP/Python               │
│  Sites dynamiques ──→ Claude in Chrome               │
│  Recherche ouverte ──→ Perplexity MCP                │
│                    ↓                                 │
│           Google Sheets (hub central)                │
│                    ↓                                 │
│         Claude API (analyse / rédaction)             │
│                    ↓                                 │
│              BDD izilife / WordPress                 │
└─────────────────────────────────────────────────────┘
```

**Règle de choix d'outil** :

| Situation | Outil |
|-----------|-------|
| Site RSS disponible | Script PHP cron (0 token) |
| Site statique scrappable | Script PHP/Python direct |
| Site dynamique / JS / login | Claude in Chrome (ponctuel) |
| Recherche multi-sources éparpillées | Perplexity MCP |
| Contenu à analyser / résumer | API Claude dans le script |
| Automatisation bureau Windows | Cowork |
| Dev / SSH / fichiers serveur | Claude Code |

---

## MCP à Configurer

- **Perplexity MCP** — recherche web temps réel avec sources citées (clé API Perplexity requise)
- **GitHub MCP** — gestion des repos clients via Claude Code
- **Google Sheets MCP** — lecture/écriture du hub central (optionnel, peut se faire via API PHP)

---

## izilife — Features IA Produit (séparé des agents)

Ces features sont dans l'app izilife elle-même, appelées via l'API Claude/GPT/Mistral depuis le backend PHP :

| Feature | Déclencheur | LLM utilisé |
|---------|-------------|-------------|
| Flyer → Event | Partner upload image | OCR + Claude |
| Menu papier → Fiche | Partner upload PDF/image | OCR + Claude |
| Description naturelle → Event | Partner tape texte | Claude |
| Amélioration fiche lieu | Bouton BO / cron | Claude + scraping |
| Génération article blog | Cron hebdo | Claude |
| Recherche nouveautés lieu | Bouton BO / cron | Perplexity MCP |

**Note** : Ces features sont interchangeables avec un LLM propriétaire à terme.

---

## Ordre d'Attaque Recommandé

1. **Finir Protect Solaire** (en cours — conv dédiée)
2. **Équipe 1** — Premier site client WordPress avec Claude Code + Git
3. **Équipe 4** — Script RSS PHP + hub Google Sheets (quick win, 0 token)
4. **Perplexity MCP** — Brancher pour la veille et l'amélioration fiches
5. **Équipe 2** — Réseaux sociaux avec Google Sheets comme planning
6. **Équipe 3** — Dashboard pilotage izilife

---

## Notes Importantes

- OVH mutualisé : SSH disponible mais pas de npm/node → Claude Code doit tourner en **local**, pas sur le serveur
- Windows + XAMPP local pour le dev PHP
- Git configuré localement (`C:\Program Files\Git\bin\bash.exe` dans `CLAUDE_CODE_GIT_BASH_PATH`)
- Workflow de déploiement : Claude Code local → modifie fichiers → scp/ssh vers serveur OVH
- Claude in Chrome et Cowork : Instagram/Facebook peuvent bloquer les bots → prévoir délais et ne pas automatiser trop vite
