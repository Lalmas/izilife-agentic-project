# 10 — Places / Shops

## Flux historiques

- Création de lieux depuis Google Maps.
- Si le lieu n'existe pas : insertion directe.
- Si ambigu / doublon / incomplet : `scraping_unmapped_poi`.
- Enrichissement : `validation_request`.

## Règles

- `city=lille`, pas `city_id=1` dans les scripts.
- `--zone=lille`, pas `--zone=lille-zone` côté utilisateur.
- Les logs vont dans `{zone}-zone/logs/Wxx/`.

## Validation Request

Le scope VR scraper est réservé aux agents :

```text
requester_type = AI_AGENT
```

Les modals spécialisés sont dans :

```text
common_components/vr_modals/
```
