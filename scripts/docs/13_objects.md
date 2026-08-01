# 13 — Agents objets

## Objets prévus

```text
experiences
circuits
pages
local_habits
local_tips
outing_ideas
links
external_media
```

## Règle générale

Chaque objet a son workspace par zone :

```text
izilife/{object}/{zone}-zone/
```

## Flux

- Experience → `scraping_experience_tmp`, validation humaine.
- Circuit → curate sheet puis insertion directe en draft/review avec anti-doublon.
- Page → insertion directe avec anti-doublon.
- LocalHabit / LocalTip / OutingIdea → insertion directe, owner izilife.
- Link → insertion directe dans `Link`.
- ExternalMedia → insertion directe dans `ElementExternalMedia`.
