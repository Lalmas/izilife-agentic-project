# 11 — Events

## Flux

Les events collectés vont dans :

```text
scraping_event_tmp
```

Puis validation humaine dans le BO.

## Revue

La revue events est filtrable par AdministrativeDivision.

## Règles

- Pas d'insertion directe des events standards sans validation.
- Les EventSeries et AnnualCelebrations pourront utiliser `validation_request` ou des agents dédiés plus tard.
