-- Rollback manuel des états relevés avant le nettoyage production du 26/10/2026.
-- À exécuter uniquement si une restauration explicite est demandée.

UPDATE Place SET is_active = 1, listable = 1 WHERE id IN (74, 94, 109, 110, 279);

UPDATE Shop SET is_active = 1, listable = 1 WHERE id IN (
  633, 648, 651, 652, 659, 1377, 1441, 1516, 1689, 2318, 3652
);

UPDATE Shop SET is_active = 1, listable = 1 WHERE id = 10;

UPDATE Shop SET is_active = 0, listable = 0 WHERE id IN (17, 19, 59);
UPDATE Shop SET is_active = 0, listable = 1 WHERE id IN (18, 41, 42, 43);

-- Hall U Need : l'ancienne PLACE 96 n'est incluse qu'après consolidation vérifiée.
UPDATE Place SET is_active = 1, listable = 1 WHERE id = 96;
UPDATE Shop SET is_active = 1, listable = 1 WHERE id = 1263;
