# Mes activités — TODO V2

Construire une vue utilisateur unifiée sans transformer `Booking` en table fourre-tout.

- Agréger les réservations `Booking` confirmées (Experience, Place, Shop et futurs services).
- Agréger les billets et commandes Event payés ou gratuits sur l'occurrence exacte.
- Agréger la source `CommunityRSVP` déjà livrée (`présent`, `peut-être`, `absent`) sans billet ni QR code.
- Garder les sondages de groupes séparés des RSVP : un sondage pose une question, un RSVP engage la présence à une occurrence.
- Ajouter les participations confirmées et RSVP `présent` à l'agenda personnel.
- Dans l'agenda, ne pas appliquer le ranking éditorial : afficher d'abord les occurrences auxquelles l'utilisateur participe réellement.
- Conserver les règles d'annulation propres à chaque source.
- Afficher l'origine et le statut : billet, réservation, participation communautaire ou ajout manuel.

Voir aussi `BOOKING_ACCESS_SESSIONS_DOMAIN.md`.
# Socle désormais disponible

- `CommunityActivity` porte les propositions et sorties légères personnelles ou communautaires sans polluer LocalEvent. Le nom SQL historique est conservé, mais `activity_scope` distingue `PERSONAL`, `COMMUNITY` et `USER_GROUP`.
- Une activité personnelle est toujours privée, partageable par `ActivityInvitation` ou lien non devinable, et absente de toutes les surfaces de découverte.
- La promotion vers Event/Experience conserve l'activité comme espace social (invités, RSVP, futur feed et historique).
- Une activité peut être rattachée à une Community ou un UserGroup, jamais les deux.
- Elle peut pointer vers un Place/Shop et évoluer ensuite vers LocalEvent/Experience.
- Le RSVP communautaire est stocké par occurrence.

# Suite volontairement différée

- sondage combiné date + lieu ;
- transformation en réservation commerçant en un clic ;
- espace complet de management communautaire côté FO ;
- mur/forum et modération ;
- workflow complet de revendication et vérification de propriétaire.

Ces évolutions doivent réutiliser CommunityActivity et Survey, sans introduire
une couche `CommunityProgram`.
