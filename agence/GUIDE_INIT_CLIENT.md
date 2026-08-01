# Guide — Initialiser un client agence

## Prérequis (une seule fois)

```powershell
pip install anthropic openai openpyxl requests
$env:ANTHROPIC_API_KEY = "sk-ant-xxx"   # si client sur Claude
$env:OPENAI_API_KEY    = "sk-xxx"       # si client sur GPT (défaut)
```

## Créer un nouveau client

```powershell
cd C:\Users\alcamara\Documents\agentic_Workspace
python .\scripts\agence\cm_agence.py --init nom_client
```

Exemple :
```powershell
python .\scripts\agence\cm_agence.py --init soultrain_lille
```

Ça crée automatiquement :
```
G:\Mon Drive\agentic_workspace\clients\soultrain_lille\
  ├── planning_soultrain_lille.xlsx   ← planning hebdo du client
  └── outputs\                        ← posts générés (séparés des autres clients)

C:\...\context\social\clients\
  ├── community-manager-soultrain_lille.md   ← ton, thèmes, hashtags du client
  └── .provider_soultrain_lille               ← "openai" ou "claude"
```

## Remplir le contexte client

Ouvre `context/social/clients/community-manager-soultrain_lille.md` et remplis :
- Nom, secteur, ville
- Compte Instagram + Facebook
- Ton & style (formel/décontracté, humour...)
- Thèmes éditoriaux
- Ce qu'on ne fait PAS
- Hashtags du client
- Exemples de posts passés qui ont bien marché

## Choisir le LLM

Par défaut : **OpenAI GPT-4o** (le client paie ses tokens ou toi tu factures)

Pour basculer sur Claude :
```
C:\...\context\social\clients\.provider_soultrain_lille
```
Ouvre ce fichier et remplace `openai` par `claude`.

## Lancer le script

```powershell
python .\scripts\agence\cm_agence.py --client soultrain_lille
```

## Lister les clients

```powershell
python .\scripts\agence\cm_agence.py --list
```

## Architecture complète

```
G:\Mon Drive\agentic_workspace\clients\
  ├── soultrain_lille\
  │   ├── planning_soultrain_lille.xlsx
  │   └── outputs\
  │       └── 20260614_post_event_dj_set\
  │           ├── caption.txt     ← à copier-coller Instagram
  │           ├── slides.txt      ← texte slides Canva
  │           └── post.txt        ← tout ensemble
  └── autre_client\...

C:\...\context\social\clients\
  ├── community-manager-soultrain_lille.md
  ├── .provider_soultrain_lille
  └── community-manager-autre_client.md
```

## Modèle de facturation suggéré

| Forfait | Ce que tu fournis | Prix |
|---------|------------------|------|
| Starter | Setup + 8 posts/mois | 150€/mois |
| Standard | Setup + 16 posts/mois | 250€/mois |
| Premium | Setup + 30 posts/mois + images | 400€/mois |

Le client paie ses tokens API séparément (ou inclus dans ton forfait Premium).
Coût réel tokens : ~0.02-0.05€ par post texte, ~0.04€ par image DALL-E.
