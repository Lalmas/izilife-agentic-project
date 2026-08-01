# Guide — Initialiser une nouvelle zone izilife

## Prérequis (une seule fois)

```powershell
pip install anthropic openai openpyxl requests
$env:ANTHROPIC_API_KEY = "sk-ant-xxx"
$env:OPENAI_API_KEY    = "sk-xxx"
```

## Créer une nouvelle zone

```powershell
cd C:\Users\alcamara\Documents\agentic_Workspace
python .\scripts\izilife\social\cm_izilife.py --init valenciennes
```

Ça crée automatiquement :
```
G:\Mon Drive\agentic_workspace\izilife\zones\valenciennes\
  ├── planning_valenciennes.xlsx   ← ton planning hebdo
  └── outputs\                     ← les posts générés

C:\Users\alcamara\Documents\agentic_Workspace\context\social\izilife\zones\
  └── valenciennes.md              ← spécificités de la zone
```

## Remplir le contexte zone

Ouvre `context/social/izilife/zones/valenciennes.md` et remplis :
- Ville principale + villes autour
- Hashtags locaux (#valenciennes, #valenciennois...)
- Compte Instagram (@izilife_valenciennes)
- Événements locaux incontournables
- Lieux emblématiques

## Lancer le script

```powershell
python .\scripts\izilife\social\cm_izilife.py --zone valenciennes
```

## Lister les zones

```powershell
python .\scripts\izilife\social\cm_izilife.py --list
```

## Migrer Lille (zone existante)

La zone Lille existe déjà dans `izilife/social/`.
Pour la migrer vers le nouveau système :

```powershell
python .\scripts\izilife\social\cm_izilife.py --init lille
```

Puis copie ton planning existant dans :
`G:\Mon Drive\agentic_workspace\izilife\zones\lille\planning_lille.xlsx`

## Architecture complète

```
G:\Mon Drive\agentic_workspace\izilife\zones\
  ├── lille\
  │   ├── planning_lille.xlsx
  │   └── outputs\
  ├── valenciennes\
  │   ├── planning_valenciennes.xlsx
  │   └── outputs\
  └── arras\...

C:\...\context\social\izilife\
  ├── izilife-social-strategy.md   (commun toutes zones)
  ├── community-manager.md         (commun toutes zones)
  └── zones\
      ├── lille.md                 (spécificités Lille)
      ├── valenciennes.md
      └── ...
```
