# 90 — Configuration IA / providers / modèles

## Principe

Aucun provider, modèle ou secret dans Excel.
Aucun secret sur le Drive.

La configuration IA est uniquement côté scripts.

## Structure

```text
scripts/
  .env
  izilife/.env.izilife
  agence/.env.agence
  config/
    izilife/zones/lille/social.env
    agence/clients/volfoni/social.env
```

## Création par init

`--init` doit créer les fichiers de configuration manquants avec des valeurs par défaut non sensibles.

## Ordre de chargement Izilife

```text
scripts/.env
↓
scripts/izilife/.env.izilife
↓
scripts/config/izilife/zones/{zone}/social.env
```

## Ordre de chargement Agence

```text
scripts/.env
↓
scripts/agence/.env.agence
↓
scripts/config/agence/clients/{client}/social.env
```

## scripts/.env

Secrets uniquement :

```env
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
IZILIFE_AGENT_TOKEN=
CANVA_API_KEY=
GOOGLE_API_KEY=
```

## .env.izilife / .env.agence / social.env

Config technique non sensible :

```env
TEXT_PROVIDER=anthropic
TEXT_MODEL=claude-sonnet-4-6

IMAGE_ENGINE=both
IMAGE_PROVIDER=openai
IMAGE_MODEL=gpt-image-1

CANVA_ENABLED=0

VIDEO_ENGINE=none
VIDEO_PROVIDER=
VIDEO_MODEL=
```

## Définitions

### TEXT_PROVIDER

Fournisseur texte :

```text
anthropic
openai
```

### TEXT_MODEL

Modèle texte : Claude, GPT, etc.

### IMAGE_ENGINE

Workflow image :

```text
none      → pas d'image
pillow    → composition locale sur template
llm       → génération image LLM
both      → Pillow + LLM pour comparaison
canva     → Canva API
```

### IMAGE_PROVIDER

Fournisseur image LLM/API :

```text
openai
canva
google
stable
```

### IMAGE_MODEL

Modèle image :

```text
gpt-image-1
imagen
flux
...
```

### VIDEO_ENGINE

Workflow vidéo, pour plus tard :

```text
none
llm
canva
runway
veo
```

### VIDEO_PROVIDER / VIDEO_MODEL

Provider et modèle vidéo. Non utilisé tant que `VIDEO_ENGINE=none`.
