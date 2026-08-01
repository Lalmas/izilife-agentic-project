# 00 — Architecture générale des agents

## Objectif

Le dossier `scripts/` contient les agents Python qui automatisent la collecte, la génération, l'insertion et la préparation de contenu pour izilife et l'agence.

Le BO PHP reste le système métier. Les agents ne remplacent pas le BO : ils l'alimentent via des endpoints agents protégés par token.

## Structure cible

```text
scripts/
  .env                         # secrets globaux agents uniquement

  core/
    paths.py                    # chemins, env, zones, workspaces

  izilife/
    .env.izilife                # defaults agents izilife
    places/
    events/
    social/
    objects/

  agence/
    .env.agence                 # defaults agents agence
    social/

  config/
    izilife/
      zones/
        lille/
          social.env
    agence/
      clients/
        volfoni/
          social.env

  docs/
```

## Principes

- Les secrets ne vont jamais sur le Drive.
- Le Drive contient uniquement les fichiers de travail : Excel, inputs, outputs, logs.
- Les scripts lisent les fichiers du Drive puis appellent le BO.
- Les environnements `local`, `staging`, `prod` sont séparés.
- Une zone se passe toujours en CLI sous forme simple : `--zone=lille`.
- Le dossier réel devient automatiquement `lille-zone`.

## Flux général

```text
Excel / inputs / description.txt
  → agent Python
  → LLM / image / parsing / structuration
  → BO PHP via endpoint agent
  → BDD ou fichier de validation
  → logs / outputs
```
