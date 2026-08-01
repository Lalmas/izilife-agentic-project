# izilife — Documentation : `php spark calendar:run`

## Vue d'ensemble

`calendar:run` est la commande principale pour générer et maintenir le calendrier izilife.
Elle s'exécute en 4 étapes indépendantes, dans l'ordre.

```
php spark calendar:run [options]
```

---

## Options disponibles

| Option | Valeur | Description |
|--------|--------|-------------|
| `--year` | ex: `2027` | Année cible. Par défaut : **année suivante** |
| `--country` | ex: `FR` | Pays ISO pour les jours fériés (étape 2). Par défaut : `FR` |
| `--only` | voir ci-dessous | Exécuter **une seule** étape au lieu des 4 |
| `--school-year` | ex: `2025-2026` | Année scolaire pour les vacances (étape 4). Par défaut : année scolaire en cours |
| `--dry-run` | (flag) | **Simuler** sans rien insérer en BDD — affiche ce qui serait fait |

---

## Valeurs de `--only`

### `--only=occurrences`
Génère les **occurrences des CelebrationDay** pour l'année cible.

Ce que ça fait :
- Lit tous les `CelebrationDay` actifs avec `date_rule = fixed` ou `computed`
- Calcule la date pour l'année cible (ex: Pâques 2027 = 28/03/2027)
- Crée une entrée dans `CalendarOccurrence` si elle n'existe pas déjà

Exemples d'occurrences créées :
- Saint-Valentin 2027 → 2027-02-14
- Halloween 2027 → 2027-10-31
- Pâques 2027 → 2027-03-28 (calculé via algorithme)
- Black Friday 2027 → 2027-11-26 (4e jeudi de novembre + 1)
- Fête des mères 2027 → 2027-05-30 (dernier dimanche de mai)

Ne crée **pas** les jours fériés officiels (ça c'est `--only=holidays`).

```bash
php spark calendar:run --year=2027 --only=occurrences
php spark calendar:run --year=2027 --only=occurrences --dry-run
```

---

### `--only=holidays`
Importe les **jours fériés officiels** depuis les APIs gouvernementales + les **vacances scolaires**.

Sous-étapes :
1. **Jours fériés** — appelle `calendrier.api.gouv.fr` (FR) ou `date.nager.at` (autres pays)
2. **Vacances scolaires** — appelle `data.education.gouv.fr` pour la France (zones A/B/C)

Exemples créés :
- 2027-01-01 : Jour de l'an (country, France, férié + chômé)
- 2027-05-06 : Ascension (country, France, férié + chômé)
- Zone A : Vacances de Toussaint 2025-10-18 → 2025-11-03
- Zone B : Vacances d'hiver 2026-02-14 → 2026-03-01

> ⚠️ **En local (XAMPP Windows)** : les appels API externes sont souvent bloqués.
> Les jours fériés seront à 0. **Ce n'est pas un bug** — importe-les manuellement
> depuis le BO (`/boCelebrationDay` → bouton "Importer") ou lance depuis OVH staging.

```bash
# Jours fériés + vacances scolaires année scolaire en cours
php spark calendar:run --year=2027 --only=holidays

# Forcer une année scolaire précise
php spark calendar:run --year=2027 --only=holidays --school-year=2026-2027

# Autre pays
php spark calendar:run --year=2027 --only=holidays --country=BE
```

**`--school-year` expliqué :**
L'année scolaire ne correspond pas à l'année calendaire. Ex :
- `2025-2026` = rentrée sept 2025, fin juin 2026
- Pour voir les vacances qui tombent **en 2026**, il faut `2025-2026` ET `2026-2027`
- Par défaut le script calcule l'année scolaire en cours automatiquement

---

### `--only=campains`
Crée les **Campain drafts** pour les CelebrationDay qui ont `auto_create_campain = 1`.

Ce que ça fait :
- Calcule la date de l'occurrence pour l'année cible
- Crée une Campain avec `is_active = 0` (draft — validation humaine requise)
- `campain_start_date` = date occurrence - `alert_days_before` jours (défaut : 14j avant)
- `campain_end_date` = date de l'occurrence

CelebrationDay avec `auto_create_campain = 1` (configuré en BDD) :
- Saint-Valentin, Halloween, Noël, Saint-Nicolas, Chandeleur, Mardi gras
- Fête des mères, Fête des pères, Fête des grands-mères
- Black Friday, Cyber Monday
- Fête de la musique, Journées du patrimoine, Journée mondiale de la musique

> Les jours fériés "civils" (Toussaint, Ascension, 14 juillet...) n'ont **pas**
> de campagne automatique — ils sont des jours off mais pas des moments commerciaux.

```bash
php spark calendar:run --year=2027 --only=campains
php spark calendar:run --year=2027 --only=campains --dry-run
```

**Pour activer/désactiver une campagne automatique :**
```sql
-- Activer
UPDATE CelebrationDay SET auto_create_campain = 1 WHERE string_id = 'saint-patrick';
-- Désactiver
UPDATE CelebrationDay SET auto_create_campain = 0 WHERE string_id = 'cyber-monday';
```

---

## Combinaisons courantes

### Générer une année complète (tout d'un coup)
```bash
# Simulation d'abord
php spark calendar:run --year=2027 --dry-run

# Pour de vrai
php spark calendar:run --year=2027
```

### Workflow recommandé (ordre à respecter)
```bash
# 1. Occurrences en premier (les campains en dépendent pour les dates)
php spark calendar:run --year=2027 --only=occurrences

# 2. Jours fériés (depuis staging/OVH — pas depuis local)
php spark calendar:run --year=2027 --only=holidays

# 3. Vacances scolaires (année scolaire qui couvre l'année cible)
php spark calendar:run --year=2027 --only=holidays --school-year=2026-2027

# 4. Campains en dernier (besoin des occurrences pour calculer les dates)
php spark calendar:run --year=2027 --only=campains
```

### Préparer une année depuis zéro (staging)
```bash
php spark calendar:run --year=2026 --dry-run   # vérifier
php spark calendar:run --year=2026             # créer

php spark calendar:run --year=2027 --dry-run   # vérifier
php spark calendar:run --year=2027             # créer
```

---

## Crons OVH recommandés

```cron
# 1er décembre : générer l'année suivante complète
0 7 1 12 *   php /path/to/spark calendar:run >> /logs/agents/calendar.log 2>&1

# 1er août : mettre à jour les vacances scolaires de la rentrée
0 7 1 8 *    php /path/to/spark calendar:run --only=holidays >> /logs/agents/calendar.log 2>&1
```

---

## Ce qui est créé dans la BDD

| Étape | Table alimentée |
|-------|----------------|
| `occurrences` | `CalendarOccurrence` (occurrence_kind = celebration) |
| `holidays` jours fériés | `CalendarOccurrence` (occurrence_kind = public_holiday) |
| `holidays` vacances | `SchoolHolidayOccurrence` |
| `campains` | `Campain` (is_active = 0, is_published = 0) |

---

## Dédup — pas de doublon

Chaque étape vérifie l'existence avant d'insérer :
- Occurrences : `celebration_day_id + date_start + scope_level`
- Jours fériés : `string_id` unique (ex: `ferie-fr-20270101`)
- Vacances : `zone_id + period_type_id + school_year`
- Campains : `celebration_id + YEAR(campain_start_date)`

**Tu peux relancer sans risque — jamais de doublons.**

---

## Résolution des problèmes courants

| Symptôme | Cause | Solution |
|----------|-------|----------|
| Jours fériés = 0 | XAMPP bloque les appels HTTPS | Importer depuis le BO ou lancer depuis OVH |
| SKIP "déjà existante" | L'occurrence existe déjà | Normal — pas un bug |
| "impossible de calculer la date" | computation_key non supportée | Vérifier le format dans `CelebrationDay.computation_key` |
| Campains = 0 | `auto_create_campain = 0` sur tous les CD | Vérifier en BDD, lancer la migration `migration_calendar_auto_campain.sql` |
| Vacances = zone inconnue | Académie non mappée | Ajouter l'académie dans `_mapAcademieToZone()` du helper |
