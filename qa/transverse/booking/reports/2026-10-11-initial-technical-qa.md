# Booking — QA technique initiale du 11 octobre 2026

## Verdict

**BLOCKED_ENVIRONMENT** pour les tests d'intégration avec fixtures. **PASS** pour les 12 contrats techniques exécutables sans base.

MariaDB local ne démarre pas. Le journal `C:\xampp\mysql\data\mysql_error.log` indique une corruption Aria : absence de checkpoint, échec de récupération Aria, puis impossibilité de charger `mysql.plugin`. Aucune réparation destructive n'a été tentée.

## Applications et composants traversés

- FO `izilife` : routes et contrôleur Reservation, BookingJourneyService, BookingGuestValidationService, BookingAjaxAuthenticationService, BookingConflictGuard, ServiceRequestService et Reservation_model.
- Partner Space `izilife-partner-admin` : ReservationManagement, contrôle des droits et de la portée, BC/BCC, composition, politique d'acceptation et privatisation.
- BO `izilife-admin` : formulaires et mutations BC/BCC, catégories groupées, schéma d'acceptation et privatisation.
- Paiement : PayHub, Stripe et IziCredits ont été inventoriés. Le nouveau parcours Booking de lieu ne les appelle pas encore ; les scénarios monétaires sont donc non applicables dans cette version et ne sont pas simulés par un autre produit.

## Fixtures

Les aliases demandés ont été enregistrés dans le profil local ignoré par Git, mais leurs IDs restent non résolus faute de connexion BDD : Soultrain, Disco Volante, La Luck, HUN, Follow Park, Hall U Need, Disco Volante Lille et les deux Users QA.

Aucune donnée QA existante n'a été modifiée. Aucune ligne Booking, Transaction, Payment, allocation, Grant, Redemption ou AccountValidation n'a été créée.

## Exécution

Run : `booking-qa-20261011-103136-884c1d13`.

Commande :

```powershell
./run.ps1 -Environment local -Scenario all
```

Résultat : 12 contrats réussis, base `BLOCKED_ENVIRONMENT`.

Contrats couverts :

- différence STANDARD heure d'arrivée/créneau fixe ;
- routes POST, CSRF et erreurs publiques ;
- composition facultative et persistance du segment ;
- privatisation acceptée et préférence de placement TABLE ;
- OTP Booking dédié dans AccountValidation, SMS pays proches, fallback e-mail, message contextualisé, expiration et limitation des tentatives ;
- schéma de politique d'acceptation ;
- sécurité des mutations BO ;
- portée multi-catégories BO ;
- composition et mutations Partner ;
- portée catégorie/lieu et conflits de privatisation Partner ;
- terminologie STANDARD sans confusion avec les sessions XP ;
- CSRF, XSS et contrôle de propriété Partner.

## Point OTP e-mail/SMS

Le code est présent : motif `booking_guest`, code à six chiffres, expiration dix minutes, cinq essais, SMS pour FR/BE/DE/NL/IT/ES/GB/LU/CH/MC/AD, fallback e-mail en cas d'échec SMS, et message « valider votre réservation chez <établissement> ». La réception réelle n'est pas validée : elle exige MariaDB puis des identifiants Twilio/SES opérationnels.

## Scénarios bloqués

- résolution des fixtures et état initial ;
- migrations effectives ;
- appels des vrais contrôleurs/services avec sessions authentifiées ;
- écritures et assertions BDD ;
- capacités, concurrence et chevauchements réels ;
- acceptation/refus de privatisation ;
- isolation entre Partners avec données réelles ;
- affichage User/Partner alimenté par la BDD ;
- émission OTP réelle ;
- tous les scénarios PSP/crédits, en plus non raccordés au Booking actuel.

## Nettoyage

Aucun nettoyage nécessaire : le run n'a réalisé aucune mutation.

## Validation manuelle propriétaire produit

- caractéristiques éditoriales, liens, images/XML et quotas ;
- libellés, compréhension et ergonomie des cartes/modales ;
- responsive ;
- réception effective e-mail/SMS ;
- redirections externes Stripe lorsqu'un paiement Booking existera.

## Suite requise

Réparer ou restaurer MariaDB/Aria, démarrer la base puis relancer le même runner. La résolution des aliases et tous les scénarios avec fixtures doivent rester bloqués jusqu'à cette remise en état.
