-- Contre-audit strict et en lecture seule après la purge manuelle des XP.
-- Résultat attendu pour déclarer le bloc terminé :
-- backup_rows = 43, remaining_rows = 0, deleted_rows = 43.

SELECT
    (SELECT COUNT(*) FROM backup_Experience_purge_20261109) AS backup_rows,
    (
        SELECT COUNT(*)
        FROM Experience e
        INNER JOIN backup_Experience_purge_20261109 b ON b.id = e.id
    ) AS remaining_rows,
    (
        SELECT COUNT(*)
        FROM backup_Experience_purge_20261109 b
        LEFT JOIN Experience e ON e.id = b.id
        WHERE e.id IS NULL
    ) AS deleted_rows;

-- Les doublons obsolètes 68 et 122 font partie de la purge.
-- Les fiches canoniques 74 et 123 doivent rester présentes et actives.
SELECT
    (SELECT COUNT(*) FROM Experience WHERE id IN (68, 122))
        AS obsolete_duplicates_remaining,
    (SELECT COUNT(*) FROM Experience WHERE id IN (74, 123) AND is_active = 1)
        AS canonical_active;
-- Résultat attendu : obsolete_duplicates_remaining = 0, canonical_active = 2.

-- Inventaire exact des tables de sauvegarde du lot et nombre de lignes.
-- Cette requête ne modifie que des variables de la session SQL.
SET SESSION group_concat_max_len = 1000000;
SELECT GROUP_CONCAT(
    CONCAT(
        'SELECT ', QUOTE(TABLE_NAME), ' AS backup_table, COUNT(*) AS backup_rows FROM `',
        REPLACE(TABLE_NAME, '`', '``'), '`'
    )
    SEPARATOR ' UNION ALL '
) INTO @xp_backup_audit_sql
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = DATABASE()
  AND (
      TABLE_NAME = 'backup_Experience_purge_20261109'
      OR TABLE_NAME LIKE 'backup\_purge\_20261109\_%'
  );

SET @xp_backup_audit_sql = COALESCE(
    @xp_backup_audit_sql,
    'SELECT ''aucune sauvegarde trouvée'' AS backup_table, 0 AS backup_rows'
);
PREPARE xp_backup_audit_stmt FROM @xp_backup_audit_sql;
EXECUTE xp_backup_audit_stmt;
DEALLOCATE PREPARE xp_backup_audit_stmt;
