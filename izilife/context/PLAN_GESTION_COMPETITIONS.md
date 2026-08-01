# izilife — Plan de gestion des compétitions sportives

## État des lieux — Fichiers à garder

### Fichiers actifs (à conserver et installer)

| Fichier | Destination | Rôle |
|---------|-------------|------|
| `CompetitionRun_v2.php` | `app/Commands/CompetitionRun.php` | Spark command — gère éditions + import via API-Football |
| `CompetitionImport_ApiFootball_lib.php` | `app/Libraries/` | Import via API-Football (foot + rugby + basket + MMA) |
| `CompetitionImport_lib.php` | `app/Libraries/` | Import via scraping HTML + LLM — fallback si pas d'API |
| `SportCompetition_model_final.php` | `app/Models/SportCompetition_model.php` | Model complet |
| `BoSportCompetition_final.php` | `app/Controllers/BoSportCompetition.php` | Controller BO |
| `competitions_final.php` | `app/Views/bo_sport_competition/competitions.php` | Vue liste |
| `fetch_competition_schedule.py` | `scripts/` | Script Playwright — import ponctuel CDM/Euros |
| `migration_sportmatch_api_football.sql` | SQL à passer | Ajoute api_football_id, logos, scores sur SportMatch |
| `postImportCompetitionSchedule_v3.php` | méthode dans `Scraper.php` | Bouton Import BO → API-Football |

### Fichiers obsolètes (ne pas installer)

| Fichier | Raison |
|---------|--------|
| `CompetitionRun.php` (ancienne version) | Remplacé par v2 |
| `Scraper_importCompetitionScheduleDirect.php` | Remplacé par API-Football |
| `Scraper_competition_agent_methods.php` | Remplacé par API-Football |
| `postImportCompetitionSchedule_fixed.php` | Remplacé par v3 |
| `Scraper_importCompetitionSchedule.php` | Remplacé par v3 |
| `agent_competition_monthly.php` | Intégré dans CompetitionRun_v2 |
| `agent_competition_seasons.php` | Intégré dans CompetitionRun_v2 |

---

## Comment CompetitionRun_v2 fonctionne

```
php spark competition:run
```

**Étape 1 — Créer les éditions**
- Lit les compétitions avec `auto_create_edition = 1`
- Crée l'édition de la saison si elle n'existe pas encore
- Ex: Ligue 1 2025/2026, Premier League 2025/2026

**Étape 2 — Import matchs**
- Si `API_FOOTBALL_KEY` configurée ET `api_football_league_id` présent → **API-Football**
- Sinon → **CompetitionImport_lib** (scraping HTML via FetchFallback → Direct → BrightData → Playwright)

---

## Plan de gestion annuel

### Début de saison (août-septembre)

```bash
# 1. Activer API-Football ($15/mois pendant 1-2 mois max)
# Ajouter dans .env : API_FOOTBALL_KEY=ta_clé

# 2. Créer les éditions + importer tous les championnats
php spark competition:run

# 3. Couper l'abonnement API-Football après import
# Les matchs sont en BDD, plus besoin jusqu'à la saison prochaine
```

Championnats couverts automatiquement :
- Ligue 1, Ligue 2 (league_id: 61, 62)
- Premier League (39)
- La Liga (140)
- Bundesliga (78)
- Serie A (135)
- Champions League (2)
- Ligue Europa (3)
- Top 14 (rugby via v1.rugby.api-sports.io)
- NBA (via v2.nba.api-sports.io)

### Compétitions ponctuelles (CDM, Euros, JO)

Ces compétitions ont `auto_create_edition = 0` — saisie manuelle de l'édition dans le BO.

```bash
# 1. Créer l'édition dans le BO : /boSportCompetition/editions/{id}
# 2. Importer les matchs via le script Python Playwright
python scripts/fetch_competition_schedule.py --edition=1 --env=local

# Ou depuis staging/prod :
python scripts/fetch_competition_schedule.py --edition=1 --env=staging
```

**CDM 2026** — 72 matchs déjà importés ✅
Les phases finales seront importées au fur et à mesure en relançant le script.

### Mise à jour phases finales (quarts, demis, finale)

Quand les équipes qualifiées sont connues (après les phases de groupes) :

```bash
# Relancer le script — les matchs existants sont mis à jour (dédup par titre+date)
python scripts/fetch_competition_schedule.py --edition=1 --env=local

# Ou forcer via CompetitionRun
php spark competition:run --competition=3 --force
```

### Scores en temps réel (futur)

Quand tu voudras les scores (pour les passionnés) :
```bash
# CompetitionImport_ApiFootball_lib a déjà updateScores($editionId)
# À appeler depuis un cron quotidien pendant la compétition
# 0 22 * * * php spark competition:updateScores >> /logs/scores.log
```

---

## Configuration api_football_league_id

À configurer dans la table `Competition` :

| Compétition | league_id |
|-------------|-----------|
| Coupe du monde | 1 |
| Euro | 4 |
| Champions League | 2 |
| Ligue Europa | 3 |
| Ligue 1 | 61 |
| Ligue 2 | 62 |
| Premier League | 39 |
| La Liga | 140 |
| Bundesliga | 78 |
| Serie A | 135 |

---

## Endpoints API-Sports par sport

| Sport | Endpoint | Note |
|-------|----------|------|
| Football | `v3.football.api-sports.io` | ✅ Principal |
| Rugby | `v1.rugby.api-sports.io` | À venir |
| Basketball | `v1.basketball.api-sports.io` | À venir |
| MMA | `v1.mma.api-sports.io` | À venir |
| Formule 1 | `v1.formula-1.api-sports.io` | À venir |
| NBA | `v2.nba.api-sports.io` | À venir |

Même clé API pour tous. Il suffira d'ajouter un champ `api_sport_endpoint` sur `Competition` et d'adapter `CompetitionImport_ApiFootball_lib` pour changer l'URL de base.

---

## Commandes utiles

```bash
# Import complet
php spark competition:run

# Simulation
php spark competition:run --dry-run

# Une seule compétition
php spark competition:run --competition=3

# Forcer reimport
php spark competition:run --competition=3 --force

# Seulement créer les éditions
php spark competition:run --only=editions

# Seulement importer les matchs
php spark competition:run --only=matches

# Import ponctuel CDM via Playwright
python scripts/fetch_competition_schedule.py --edition=1 --env=local
python scripts/fetch_competition_schedule.py --edition=1 --env=staging
```

---

## Crons OVH

```cron
# 1er du mois — import matchs du mois
0 7 1 * *   php /path/to/spark competition:run --only=matches >> /logs/competition.log 2>&1

# 1er août — créer les éditions de la nouvelle saison
0 7 1 8 *   php /path/to/spark competition:run --only=editions >> /logs/competition.log 2>&1
```
