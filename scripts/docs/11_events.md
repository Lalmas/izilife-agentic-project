# 11 — Events

## Flux

Les events collectés vont dans :

```text
scraping_event_tmp
```

Puis validation humaine ou validation automatique contrôlée par
`events/validate_event_tmp.py`. Les représentations restent en validation
humaine. Le document de référence du pipeline est
`100_road_to_production_agents.md`.

## Revue

La revue events est filtrable par AdministrativeDivision.

## Règles

- Pas d'insertion directe des events standards sans passage par les contrôles
  du validateur EventTmp.
- Les EventSeries et AnnualCelebrations pourront utiliser `validation_request` ou des agents dédiés plus tard.
