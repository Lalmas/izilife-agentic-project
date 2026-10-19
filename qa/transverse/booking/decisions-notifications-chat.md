# Booking — notifications et conversation

## Politique de notification retenue

L'objectif est de protéger la disponibilité du client tout en transmettant les décisions qui modifient réellement son organisation.

| Événement | E-mail | SMS | Justification |
| --- | --- | --- | --- |
| Réservation confirmée automatiquement | Oui | Non | Le résultat est déjà affiché immédiatement dans le tunnel. |
| Demande envoyée et en attente | Oui | Non | Le client vient d'effectuer l'action et dispose du lien de suivi. |
| Demande acceptée par le partenaire | Oui | Oui | Décision attendue et temporellement importante. |
| Demande refusée par le partenaire | Oui | Oui | Le client doit pouvoir réorganiser rapidement son programme. |
| Annulation par le partenaire | Oui | Oui | Changement important d'une réservation déjà organisée. |
| Modification importante de date ou d'heure | Oui | Oui | Changement nécessitant une action ou une prise de connaissance rapide. |
| Message de conversation | Relais e-mail | Non | Éviter de transformer chaque échange en sollicitation SMS. |
| Rappel, QR code, présence/no-show | À définir | À définir | Chantier Partner/Kiosk ultérieur. |

Cette matrice doit être portée plus tard par une librairie de notification unique, capable d'arbitrer e-mail, SMS, notification mobile et temps réel. Le chantier Booking ne doit pas multiplier aujourd'hui les appels directs à Twilio.

## État réel de la conversation

La messagerie actuelle est limitée aux demandes et privatisations :

- `ServiceRequestMessage` stocke les messages ;
- le client écrit depuis sa page de suivi ;
- le partenaire répond depuis le Partner Space ;
- la réponse est relayée par e-mail sans divulguer les coordonnées.

Il n'existe pas encore de conversation générique utilisable par une `Booking` TABLE, STANDARD ou EQUIPMENT. La vue `follow_booking` est actuellement en lecture seule.

## Cible du chantier chat

Le futur socle doit être transversal et ne pas dépendre de `ServiceRequest` :

- une conversation rattachée à un contexte métier (`BOOKING`, `SERVICE_REQUEST`, puis autres objets) ;
- des participants User, BookingCustomer et PartnerEmployee ;
- des messages avec auteur, horodatage, statut de lecture et modération ;
- des endpoints AJAX communs FO/PS ;
- un composant JS réutilisable inspiré du thème Phoenix ;
- un relais via la librairie de notification, sans exposition des coordonnées privées.

Ce chantier implique un schéma générique. Il ne doit pas être simulé en détournant `ServiceRequestMessage`, et reste séparé de la contrainte actuelle « aucune nouvelle table » de la finalisation BookingCustomer/OTP.
