# izilife — `php spark calendar:run` — Documentation complète

## Structure de données (comprendre avant tout)

```
CelebrationDay          = Définition intemporelle d'une fête
                          "St Valentin existe chaque année le 14 février"
                          Contient : nom, règle de date, famille, flags commerciaux

CalendarOccurrence      = Date réelle pour une année précise
                          "St Valentin 2027 = 2027-02-14"
                          Sans occurrence → invisible dans le calendrier et l'app

SchoolHolidayOccurrence = Période de vacances scolaires pour une zone et une année scolaire
                          "Zone A, Toussaint 2025-2026 : 18/10 → 03/11"

Campain                 = Campagne marketing liée à une fête
                          "Campagne St Valentin 2027 : 15 jan → 14 fév"
                          Créée en draft → validation humaine avant publication
```

---

## Les 4 étapes de `calendar:run`

### Étape 1 — `occurrences`
**Ce que c'est :** Calcule et crée les dates réelles des fêtes pour l'année cible.

**Source :** Lit les `CelebrationDay` actifs avec `date_rule = fixed` ou `computed`.

**Résultat dans :** Table `CalendarOccurrence` (`occurrence_kind = celebration`)

**Exemples créés pour 2027 :**
- St Valentin → 2027-02-14 (fixe : 14 février)
- Pâques → 2027-03-28 (calculé : algorithme de Butcher)
- Ascension → 2027-05-06 (calculé : Pâques + 39 jours)
- Black Friday → 2027-11-26 (calculé : 4e jeudi novembre + 1 jour)
- Fête des mères → 2027-05-30 (calculé : dernier dimanche de mai)
- Halloween → 2027-10-31 (fixe : 31 octobre)

**Commande :**
```bash
php spark calendar:run --year=2027 --only=occurrences
```

---

### Étape 2 — `holidays` (partie 1 : jours fériés)
**Ce que c'est :** Importe les jours fériés officiels depuis les APIs gouvernementales.

**Source :** `calendrier.api.gouv.fr` (France), `date.nager.at` (Belgique, Suisse, etc.)

**Résultat dans :** Table `CalendarOccurrence` (`occurrence_kind = public_holiday`, `is_public_holiday = 1`)

**Exemples créés pour FR 2027 :**
- 2027-01-01 : Jour de l'an (country/France, Férié + Chômé)
- 2027-04-05 : Lundi de Pâques (country/France)
- 2027-11-11 : Armistice (country/France)

> ⚠️ **Échoue en local XAMPP** (accès internet bloqué). Solution : importer depuis
> le BO → `/boCelebrationDay` → bouton "Importer" → choisir pays + année.
> Fonctionne automatiquement en staging/production OVH.

---

### Étape 2 — `holidays` (partie 2 : vacances scolaires)
**Ce que c'est :** Importe les vacances scolaires depuis l'API education.gouv.fr.

**Source :** `data.education.gouv.fr` (France zones A/B/C), manuel pour autres pays.

**Résultat dans :** Table `SchoolHolidayOccurrence`

**Exemples créés pour 2025-2026 :**
- zone-a : Toussaint 2025-10-18 → 2025-11-03
- zone-b : Vacances d'hiver 2026-02-14 → 2026-03-02
- zone-c : Vacances de printemps 2026-04-18 → 2026-05-04

**Commande :**
```bash
# Jours fériés + vacances scolaires (année scolaire auto-détectée)
php spark calendar:run --year=2027 --only=holidays

# Forcer une année scolaire précise
php spark calendar:run --only=holidays --school-year=2025-2026
```

> **`--school-year` vs `--year` :** Une année scolaire chevauche deux années civiles.
> `2025-2026` = rentrée sept 2025, fin juin 2026. Pour voir les vacances de
> l'été 2026, il faut `--school-year=2025-2026`.

---

### Étape 3 — `campains`
**Ce que c'est :** Crée les campagnes marketing draft pour les fêtes commerciales.

**Source :** CelebrationDay avec `auto_create_campain = 1` en BDD.

**Résultat dans :** Table `Campain` (`is_active = 0`, `is_published = 0` → draft)

**Fêtes qui génèrent une campagne automatiquement :**
St Valentin, Halloween, Noël, Saint-Nicolas, Chandeleur, Mardi gras,
Fête des mères, Fête des pères, Fête des grands-mères, Black Friday,
Cyber Monday, Fête de la musique, Journées du patrimoine.

**Fêtes sans campagne auto :**
Toussaint, Ascension, 14 juillet, 11 novembre, 1er mai... (jours off, pas commerciaux)

**Dates de la campagne :**
- Début = date occurrence - `alert_days_before` jours (défaut : 14j avant la fête)
- Fin = date de la fête

**Après le run :** Valider les campagnes dans le BO (`/boCampain`) avant publication.

**Commande :**
```bash
php spark calendar:run --year=2027 --only=campains
```

**Activer/désactiver une fête :**
```sql
UPDATE CelebrationDay SET auto_create_campain = 1 WHERE string_id = 'saint-patrick';
UPDATE CelebrationDay SET auto_create_campain = 0 WHERE string_id = 'cyber-monday';
```

---

## Commandes complètes

### Simulation (ne rien créer en BDD)
```bash
php spark calendar:run --year=2027 --dry-run
```

### Générer une année complète (tout d'un coup)
```bash
php spark calendar:run --year=2027
```
Lance les 4 étapes dans l'ordre.

### Étape par étape (recommandé pour contrôler)
```bash
# 1. Les fêtes de l'année (base de tout)
php spark calendar:run --year=2027 --only=occurrences

# 2. Jours fériés officiels (depuis OVH ou BO en local)
php spark calendar:run --year=2027 --only=holidays

# 3. Vacances scolaires (année scolaire précise)
php spark calendar:run --only=holidays --school-year=2026-2027

# 4. Campagnes marketing
php spark calendar:run --year=2027 --only=campains
```

### Préparer 2026 et 2027 depuis zéro
```bash
php spark calendar:run --year=2026 --dry-run   # vérifier
php spark calendar:run --year=2026             # créer

php spark calendar:run --year=2027 --dry-run   # vérifier
php spark calendar:run --year=2027             # créer
```

---

## Politique crons OVH

```cron
# 1er décembre à 7h — génère l'année suivante complète
0 7 1 12 *  php /var/www/html/izilife-admin/spark calendar:run >> /logs/agents/calendar.log 2>&1

# 1er août à 7h — vacances scolaires de la rentrée
0 7 1 8 *   php /var/www/html/izilife-admin/spark calendar:run --only=holidays >> /logs/agents/calendar.log 2>&1
```

**Pas de cron mensuel** pour le calendrier — une fois par an suffit.

---

## Dédup — jamais de doublon

Chaque étape vérifie avant d'insérer :

| Étape | Clé de dédup |
|-------|-------------|
| occurrences | `celebration_day_id + date_start + scope_level` |
| jours fériés | `string_id` unique (ex: `ferie-fr-20270101`) |
| vacances | `zone_id + period_type_id + school_year` |
| campains | `celebration_id + YEAR(campain_start_date)` |

**Tu peux relancer autant de fois que tu veux — rien ne sera dupliqué.**

---

## Résolution des problèmes

| Symptôme | Cause | Solution |
|----------|-------|----------|
| Jours fériés = 0 | XAMPP bloque HTTPS | Importer depuis le BO ou lancer depuis OVH |
| SKIP "déjà existante" | Occurrence déjà en BDD | Normal — pas un bug |
| "impossible de calculer la date" | computation_key non reconnue | Vérifier le format dans `CelebrationDay.computation_key` |
| Campains = 0 | `auto_create_campain = 0` partout | Lancer `migration_calendar_auto_campain.sql` |
| Fête absente du calendrier BO | Occurrence manquante | Lancer `--only=occurrences` pour l'année |
| Vacances = zone inconnue | Académie non mappée | Ajouter dans `_mapAcademieToZone()` du helper |
