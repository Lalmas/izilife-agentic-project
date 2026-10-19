# Booking — preuve technique locale — 12 octobre 2026

## Exécution

- Commande : `php spark qa:booking`
- Résultat : PASS
- Écritures : transaction annulée en fin de test (`writes_rolled_back: true`)
- Fixture principale résolue : Disco Volante Lille
- Créneau exercé : 13 octobre 2026, 12:00–13:30

## Contrats effectivement exercés

- schéma Booking, privatisation, politique d'acceptation, segments BCC et modes d'accès ;
- création Booking et privatisation par les services métier ;
- lecture dans l'espace User ;
- conflit par chevauchement et garde-fou de distance ;
- capacité souple, plafond dur et créneau désactivé ;
- pause d'une configuration et journée bloquée par une privatisation acceptée ;
- TABLE mono-catégorie et Bar + Restaurant ;
- BCC composable : intervalle, heures fixes et service ;
- STANDARD glissant et fixe ;
- EQUIPMENT et SERVICE à jauge par départ ;
- invité : OTP SMS, vérification, expiration et repli e-mail après échec SMS ;
- connexion AJAX, vraie session et MFA différée pilotée par `IZILIFE_MFA_ACTIVATED`.

## Limite de cette preuve

Ce PASS prouve les services, règles et écritures/lectures en base. Il ne remplace pas la preuve visuelle. Celle-ci doit être produite par les scénarios de `qa/transverse/booking/browser-scenarios.json`, avec captures avant/résultat et assertion BDD ou HTTP associée.
