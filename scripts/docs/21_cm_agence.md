# 21 — CM Agence

## Principe

Même moteur que CM Izilife, mais par client.

## Structure Drive

```text
agence/clients/{client}/
  planning_{client}.xlsx
  inputs/
  outputs/
  templates/
```

## Structure contexte local

```text
scripts/agence/.env.agence
scripts/config/agence/clients/{client}/social.env
agence/context/community-manager-{client}.md
```

## Règles

- Le client peut utiliser les clés globales agence.
- Le client peut avoir ses propres clés si nécessaire, mais elles restent serveur.
- Les providers/modèles ne sont jamais dans l'Excel.
- La charte client est dans le contexte client et les templates.
