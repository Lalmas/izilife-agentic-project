# 02 — Environnements

## Environnements supportés

```text
local
staging
prod
```

## Workspaces Drive

```text
local   → G:/Mon Drive/agentic_workspace_local
staging → G:/Mon Drive/agentic_workspace_staging
prod    → G:/Mon Drive/agentic_workspace
```

## URLs BO

Définies dans `core/paths.py` ou surchargées par variables serveur :

```env
IZILIFE_LOCAL_URL=https://localhost:4443/izilife-admin
IZILIFE_STAGING_URL=https://www.staging.izilife.co/izilife-admin
IZILIFE_PROD_URL=https://www.izilife.co/izilife-admin
```

## Usage CLI

```powershell
python script.py --zone=lille --env=local
python script.py --zone=lille --env=staging
python script.py --zone=lille --env=prod
```
