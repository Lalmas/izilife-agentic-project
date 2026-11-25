# 30 — Agent Expériences

## Flux

```text
experiences.xlsx
  → ligne avec source_url + city_ref, titre vide : extraction URL vers scraping_experience_tmp
  → ligne avec les champs métier remplis : création/upsert manuel inactif pour contrôle BO
```

Les fiches GetYourGuide et Funbooker sont acceptées dans `source_url`. Une URL
de fiche est traitée seule : l'agent ne parcourt pas le catalogue du fournisseur.

L'automatisation territoriale utilise le second onglet `Sources automatiques`
du même `experiences.xlsx`. Une ligne correspond à un site générique :

```text
label | url | city_ref | mode | max_items | enabled | notes
```

`mode: catalog` autorise la découverte des fiches du site. `mode: item` traite
uniquement l'URL indiquée. Un site désactivé reste configuré mais n'est pas lancé.

## Commandes

```powershell
python scripts/izilife/experiences/experience.py --zone=lille --env=local --init
python scripts/izilife/experiences/experience.py --zone=lille --env=local --dry-run --max=5
python scripts/izilife/experiences/experience.py --zone=lille --env=local --max=5
python scripts/izilife/experiences/territorial_experience_agent.py --zone=lille --env=local
```
