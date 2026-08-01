# 20 — CM Izilife

## Commandes

```powershell
python scripts/izilife/social/cm_izilife.py --zone=lille --env=local --init
python scripts/izilife/social/cm_izilife.py --zone=lille --env=local --dry-run
python scripts/izilife/social/cm_izilife.py --zone=lille --env=local
```

## Planning

Colonnes utiles :

```text
DATE
RÉSEAU
TYPE
VILLE
LIEU
THÈME / SUJET
SÉRIE
ARTISTE / DJ / ASSO
STYLE
DATA / INFOS
DATE EVENT
HEURE / DURÉE
INPUT_ID
IMAGE_PROMPT
POST OUTPUT
IMAGE OUTPUT
IMAGE STATUS
STATUT
```

## Rôle des colonnes

- `STYLE` : ton, angle, directive LLM, prompt direct.
- `DATA / INFOS` : faits, punchlines, infos à intégrer.
- `ARTISTE / DJ / ASSO` : liste fournie par le fondateur, jamais inventée.
- `INPUT_ID` : dossier dans `inputs/`.
- `IMAGE_PROMPT` : consigne image optionnelle.

## Post Types

Configuration par type :

```text
POST_TYPE
CONTENT_TYPE
TEMPLATE_LOCAL
TEMPLATE_SOURCE
TEMPLATE_REF
IMAGE_MODE
NOTES
```

Pas de provider, pas de modèle, pas de clé dans Excel.
