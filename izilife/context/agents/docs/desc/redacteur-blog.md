# Agent — Rédacteur blog izilife

> Charger aussi : izilife-global.md, dev/agents-socle.md

## Rôle
Trouver des sources, préparer des briefs, rédiger des articles de blog izilife.
0 token sur la collecte. Claude uniquement pour la rédaction finale depuis brief validé.

## Déclenchement
- Cron hebdo (lundi matin)
- Manuel quand on veut publier un article spécifique

## Outils
- PHP cron (RSS → Sheets) — 0 token
- Perplexity API (recherche multi-sources) — 0 token Claude
- Claude API (rédaction depuis brief) — tokens uniquement ici
- WordPress API (publication en brouillon)

## Workflow
1. Script PHP fetch les flux RSS des sources dans la liste → insère dans Sheets
2. Claude API lit le Sheets, identifie les sujets pertinents pour izilife
3. Claude rédige un brief pour chaque sujet retenu
4. Validation humaine du brief requise
5. Sur validation → Claude rédige l'article complet
6. WordPress API publie en brouillon
7. Validation humaine avant publication finale

## Sources RSS (à compléter par ville)
- Blogs sortie locale
- Offices de tourisme
- Presse locale
- À compléter selon les villes couvertes

## Règles
- Claude ne rédige pas depuis les RSS bruts — seulement depuis les briefs validés
- Pas de copie de contenu existant — angle éditorial izilife toujours
- Chaque article renvoie vers les pages izilife correspondantes (lieux, events…)

## Cron OVH staging
```
0 8 * * 1  php /scripts/agents/redacteur-blog.php
```
