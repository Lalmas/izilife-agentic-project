# Agent — Calendrier (CelebrationDay & CalendarOccurrence)

> Charger aussi : izilife-global.md, dev/agents-socle.md, dev/architecture.md

## Rôle
Générer automatiquement les `CalendarOccurrence` pour l'année suivante.
Maintenir à jour les jours fériés, vacances scolaires et fêtes.
Déclencher la création des campagnes izilife liées aux `CelebrationDay`.

## Déclenchement
- Cron annuel : 1er décembre → génère les occurrences de l'année suivante
- Manuel : quand on ajoute une nouvelle `HolidayRule` ou `CelebrationDay`
- Agent : peut aussi être appelé ponctuellement pour un pays/ville

## Ce que fait l'agent

### 1. Génération CalendarOccurrence depuis HolidayRule
Pour chaque `HolidayRule` active :
- `date_rule = fixed` → calcule la date depuis `fixed_day` + `fixed_month` + année cible
- `date_rule = computed` → utilise `computation_key` (ex: `easter+1` pour lundi de Pâques)
- `date_rule = imported` → appelle l'API source (`service-public.fr`, `education.gouv.fr`)
- Insère dans `CalendarOccurrence` avec les bons scopes

### 2. Vérification des campagnes izilife à créer
Pour chaque `CelebrationDay` avec des `CampainType = campagne-izilife` récurrents :
- Vérifie si une `Campain` existe pour l'année cible
- Si non → crée un draft `Campain` lié à la `CelebrationDay`
- Notifie via Google Sheets pour planification éditoriale

### 3. Sources externes
- API `service-public.fr` → jours fériés France officiels
- API `education.gouv.fr` → vacances scolaires zones A/B/C
- `CalendarSource.string_id` = `service-public-fr` ou `education-gouv-fr`

## Outils
- PHP cron OVH — 0 token Claude pour la génération de dates
- Claude API (optionnel) — si besoin de résoudre des computation_key complexes
- Google Sheets — rapport des occurrences créées + campagnes à valider

## CelebrationDay importantes pour les campagnes izilife
(à compléter dans le fichier — exemples)
- `saint-valentin` → 14/02, family: commercial → campagne lieux romantiques
- `fete-de-la-musique` → 21/06, family: cultural → campagne concerts/events
- `noel` → 25/12, family: religious → campagne lieux + events festifs
- `nouvel-an` → 01/01, family: civil → campagne soirées
- `halloween` → 31/10, family: commercial → campagne lieux/events
- `saint-patrick` → 17/03, family: religious → campagne bars
- `fete-des-peres`, `fete-des-meres` → family: commercial

## Output
- Nouvelles `CalendarOccurrence` en BDD
- Draft `Campain` à valider dans BO
- Rapport Google Sheets

## Cron OVH staging
```
0 6 1 12 *  php /scripts/agents/agent-calendrier.php --year=next
```
