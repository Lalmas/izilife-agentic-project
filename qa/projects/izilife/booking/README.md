# QA FO Booking

Contrôler les routes `reservation/*`, le résolveur de parcours, les disponibilités, la création Booking, les conflits, l'identité invitée, l'OTP, la connexion AJAX et l'espace User.

Les scénarios avec mutation doivent traverser le contrôleur ou le service métier puis comparer l'état BDD avant/après. Une insertion SQL directe ne constitue jamais une preuve de fonctionnement du parcours.

La recette navigateur est décrite dans `qa/transverse/booking/browser-scenarios.json`. Chaque scénario doit produire une capture avant action, une capture du résultat et une assertion BDD ou réponse HTTP archivée. Les mêmes identifiants de scénarios sont rejoués en local puis en staging avec des aliases, jamais avec des IDs locaux codés en dur.

La recette manuelle couvre les parcours habituels. L'automatisation doit prioritairement prouver les cas coûteux à reproduire : capacité souple et dure, chevauchement, distance, journée privatisée, BCC composable et isolation des comptes.
