# izilife — Guide : Configurer les vacances scolaires par pays

## Principe général

Les vacances scolaires sont stockées dans 4 tables liées :
```
SchoolHolidaySystem     → un système par pays (ex: "Vacances scolaires France")
  └── SchoolHolidayZone → les zones du système (Zone A, B, C pour la France)
        └── SchoolHolidayZoneAdministrativeDivision → départements de chaque zone
              └── SchoolHolidayOccurrence → les dates réelles par zone et année scolaire
```

---

## France (Zones A / B / C)

### Structure déjà configurée par le SQL
- Système : `fr-vacances-scolaires` (type `zoned`)
- Zones : `zone-a`, `zone-b`, `zone-c`
- Départements par zone : configurés dans le SQL de migration

### Import automatique via l'API
```bash
# Importer les vacances de l'année scolaire 2025-2026
php spark calendar:run --only=holidays --school-year=2025-2026

# Importer pour 2026-2027
php spark calendar:run --only=holidays --school-year=2026-2027
```

L'agent appelle `data.education.gouv.fr` et parse automatiquement les zones A/B/C.

### Import manuel (si l'API ne répond pas)
1. Aller sur https://www.education.gouv.fr/calendrier-scolaire-100148
2. Trouver les dates pour chaque zone et chaque période (Toussaint, Noël, Hiver, Printemps, Été)
3. Dans phpMyAdmin → table `SchoolHolidayOccurrence`, insérer :

```sql
-- Exemple : Toussaint 2025-2026, Zone A
INSERT INTO SchoolHolidayOccurrence (zone_id, period_type_id, school_year, date_start, date_end, source_id, is_manual_override)
SELECT z.id, pt.id, '2025-2026', '2025-10-18', '2025-11-03',
       (SELECT id FROM CalendarSource WHERE string_id='education-gouv-fr'), 1
FROM SchoolHolidayZone z
JOIN SchoolHolidaySystem sys ON sys.id = z.system_id
JOIN Country c ON c.id = sys.country_id AND c.iso = 'FR'
JOIN SchoolHolidayPeriodType pt ON pt.string_id = 'toussaint'
WHERE z.string_id = 'zone-a';
```

### Vérifier qu'une zone est bien liée à ses départements
```sql
-- Voir les départements de la Zone C
SELECT z.name AS zone, ad.name AS departement, ad.slug
FROM SchoolHolidayZoneAdministrativeDivision zad
JOIN SchoolHolidayZone z ON z.id = zad.zone_id
JOIN AdministrativeDivision ad ON ad.id = zad.administrative_division_id
WHERE z.string_id = 'zone-c'
ORDER BY ad.slug;
```

---

## Belgique (national)

### Pas d'API — saisie manuelle
Source officielle : https://www.belgium.be/fr/education/conges_scolaires

La Belgique n'a pas de zones — un seul système national.

```sql
-- Vérifier que le système BE existe
SELECT s.*, z.name AS zone FROM SchoolHolidaySystem s
JOIN SchoolHolidayZone z ON z.system_id = s.id
JOIN Country c ON c.id = s.country_id AND c.iso = 'BE';
```

Insérer les vacances :
```sql
INSERT INTO SchoolHolidayOccurrence (zone_id, period_type_id, school_year, date_start, date_end, source_id, is_manual_override)
SELECT z.id, pt.id, '2025-2026', '2025-10-28', '2025-11-02',
       (SELECT id FROM CalendarSource WHERE string_id='izilife-manual'), 1
FROM SchoolHolidayZone z
JOIN SchoolHolidaySystem sys ON sys.id = z.system_id
JOIN Country c ON c.id = sys.country_id AND c.iso = 'BE'
JOIN SchoolHolidayPeriodType pt ON pt.string_id = 'toussaint'
WHERE z.string_id = 'national';
```

---

## Allemagne (régional par Land)

### API date.nager.at disponible
```bash
# Vérifier l'API manuellement
curl https://date.nager.at/api/v3/SchoolHolidays/2026/DE
```

L'Allemagne n'a pas encore de zones configurées dans le SQL (placeholder `national`).
Pour ajouter les Länder :
```sql
-- Ajouter un Land (ex: Bavaria)
INSERT INTO SchoolHolidayZone (system_id, country_id, name, string_id)
SELECT s.id, c.id, 'Bavaria', 'bavaria'
FROM SchoolHolidaySystem s JOIN Country c ON c.id = s.country_id AND c.iso = 'DE';
```

---

## Luxembourg (national)

### Saisie manuelle
Source : https://portal.education.lu/restopsi/CONGES

Même principe que la Belgique — zone `national`, saisie manuelle.

---

## Suisse (cantonal)

### Saisie manuelle ou par canton
La Suisse n'a pas d'API nationale. Chaque canton a ses dates.
Source de référence : https://www.ict-berufsbildung.ch/fr/formation-professionnelle/calendrier-scolaire/

Pour chaque canton, créer une zone :
```sql
INSERT INTO SchoolHolidayZone (system_id, country_id, name, string_id)
SELECT s.id, c.id, 'Vaud', 'vaud'
FROM SchoolHolidaySystem s JOIN Country c ON c.id = s.country_id AND c.iso = 'CH';
```

---

## Vérifier ce qui est importé

```sql
-- Voir toutes les vacances importées pour une année scolaire
SELECT co.iso, z.string_id AS zone, pt.name AS periode,
       sho.date_start, sho.date_end, sho.school_year
FROM SchoolHolidayOccurrence sho
JOIN SchoolHolidayZone z ON z.id = sho.zone_id
JOIN SchoolHolidaySystem sys ON sys.id = z.system_id
JOIN Country co ON co.id = sys.country_id
JOIN SchoolHolidayPeriodType pt ON pt.id = sho.period_type_id
WHERE sho.school_year = '2025-2026'
ORDER BY co.iso, z.string_id, sho.date_start;
```

---

## Commandes spark utiles

```bash
# Tout générer pour 2027 (occurrences + fériés + campagnes)
php spark calendar:run --year=2027

# Simulation (ne rien insérer)
php spark calendar:run --year=2027 --dry-run

# Seulement les jours fériés + vacances scolaires FR
php spark calendar:run --year=2027 --only=holidays

# Seulement les vacances scolaires d'une année précise
php spark calendar:run --year=2027 --only=holidays --school-year=2026-2027

# Seulement les campagnes draft
php spark calendar:run --year=2027 --only=campains
```

---

## Crons recommandés

```cron
# 1er décembre : générer l'année suivante complète
0 7 1 12 *  php spark calendar:run --year=next >> /logs/agents/calendar.log 2>&1

# 1er août : mettre à jour les vacances scolaires de la rentrée
0 7 1 8 *   php spark calendar:run --only=holidays --school-year={current}-{next} >> /logs/agents/calendar.log 2>&1
```
