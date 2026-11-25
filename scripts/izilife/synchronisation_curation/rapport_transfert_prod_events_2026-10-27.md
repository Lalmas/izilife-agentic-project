# Rapport de transfert production — 27 octobre 2026

## Périmètre appliqué

- `EventTmp` pertinents provenant du local et du staging.
- `ExperienceTmp` pertinents.
- Représentations non-test et leurs `LocalEvent` rattachés par `representation_id`.
- Trois endpoints du Hub Lille : Comédie de Lille, MaVieLilloise — app et Spotlight Lille.
- L'endpoint OpenAgenda MEL existant en production n'a pas été modifié.

## Dédoublonnage

- 299 lignes `EventTmp` candidates ont été rapprochées entre local et staging.
- 180 événements uniques ont été retenus après élimination de 119 doublons source.
- 164 `EventTmp` ont été créés en production ; les 16 autres existaient déjà et ont été ignorés.
- 5 `ExperienceTmp` ont été créées. L'expérience staging identique à une ligne locale a été fusionnée.
- Les rapprochements n'utilisent jamais les identifiants numériques source.
- Les insertions utilisent des clés métier et des clauses `NOT EXISTS` pour ne pas recréer un objet déjà présent.

## Résultat production

- 164 `EventTmp` créés avec le statut `pending`.
- 5 `ExperienceTmp` créées avec le statut `pending`.
- 5 représentations créées.
- 11 séances futures `LocalEvent` créées et liées à leur représentation.
- 3 endpoints du Hub Lille créés et activés.

Répartition des séances :

- Ben H — Le mec en rose : 1.
- C'est décidé, je deviens une connasse : 1.
- Chéri, on se dit tout : 6.
- David Voinson en rodage : 3.
- Normal n'existe pas : 0 séance future disponible dans la source.

## Contrôles

- Import SQL complet exécuté avec succès : 204 requêtes.
- Aucune reprise des IDs local/staging.
- Aucune suppression et aucun écrasement des lignes production existantes.
- Les données contenant explicitement des marqueurs de test/QA ont été exclues. « Madame Meuf — Testostérone » est conservé : le mot fait partie du titre réel et ne constitue pas un marqueur de test.
- Les fichiers SQL d'exécution à usage unique ont été supprimés après application ; le générateur et ce rapport restent disponibles pour l'audit.
