# V2 — checklist Event et Experience

## SQL à exécuter

Exécuter le bloc ajouté à la fin de `izilife-admin/statics/izilife_new_version/021_Next_Improves.sql` sur chaque environnement.

Cette évolution ajoute `Experience.participation_mode` :

- `individual` : quantité de personnes de la réservation ;
- `private_group` : groupe privé apporté par le client ;
- `open_group` : groupe public, dont la jauge réelle appartient aux séances.

Blabla Run est migré en `open_group`. `CommunityRSVP` est livré et reste distinct de `Booking` : il stocke Oui/Peut-être/Non par occurrence, sans billet ni QR code.

## Configuration serveur

Dans le `.env` du front ou les variables d'environnement du serveur :

```ini
IZILIFE_ALLOWED_EXTERNAL_TICKETING_HOSTS = shotgun.live,billetweb.fr,www.billetweb.fr,weezevent.com,www.weezevent.com
```

Ce sont des noms d'hôtes séparés par des virgules, sans `https://` ni chemin.

## Tests Event

- Une occurrence sans `event_access_type` affiche l'accès hérité du parent récurrent puis de l'EventSerie.
- Une nouvelle occurrence recopie l'accès du parent.
- Un événement terminé pendant la nuit précédente ne reste pas actif le lendemain.
- La liste BO affiche une plage début/fin pour un événement multi-jour ; les dates ne sont pas ajoutées au titre.
- Les cartes de recherche affichent `Billetterie en pause`, `Billetterie clôturée`, `Complet` ou le stock faible à partir de 15 places.
- Une billetterie externe non autorisée reste un lien ordinaire.
- Un pack de deux Tarif 1 et deux Tarif 2 consomme ces quatre composants pour chaque pack sélectionné.
- Le plafond du pack limite les packs ; le plafond global Event limite les admissions réelles.
- Une réservation gratuite passe par l'orchestrateur, sans appel PSP.

## Tests Experience

- `Libre & Gratuit`, sans réservation : aucune carte tarif, aucun achat à 0 €, séances et contact seulement.
- Les séances informatives restent affichées lorsque la billetterie iziLife est désactivée.
- Une configuration hebdomadaire mardi/jeudi à 19 h produit les prochaines dates.
- Une séance sans heure de fin utilise la durée de l'Experience pour la calculer.
- `Gratuit sur réservation` + billetterie iziLife crée une vraie Booking à 0 € sans PSP.
- `Payant` + billetterie iziLife affiche les EAP avec compteurs moins/plus.
- Le parcours décide séparément : sans date, date seule, séance/créneau ou choix après paiement.
- Une configuration de parcours vide est supprimable ; elle n'est pas obligatoire pour une Experience informative.
- Le BO refuse les EAP sur `Libre & Gratuit` et refuse un tarif payant sur `Gratuit sur réservation`.
- Le résumé des participants varie selon `participation_mode`; la capacité vendable reste celle de la séance.

## Règles Home contextuelles

- Terrasse et guinguette restent pertinentes le dimanche à 18 h 33 si la période locale terrasse est active, si la météo convient et si le coucher du soleil n'est pas dépassé.
- Elles sont retirées après la fenêtre liée au coucher du soleil.
- Une soirée festive générique n'est pas inventée : elle remonte selon le contexte ou par un Event réellement éligible.

## RSVP communautaire livré

`CommunityRSVP` gère `présent / peut-être / absent` par occurrence, sans billet ni QR. L'agrégation dans « Mes activités » reste à terminer. Les sondages de groupe restent indépendants du RSVP.
# Ajouts de validation du 9 août 2026

- [ ] Création autonome Event/Experience depuis leur liste, avec `CITY-id` obligatoire.
- [ ] Création autonome Place/Shop depuis leur liste, avec `CITY-id` obligatoire.
- [ ] Aucune création manuelle Place/Shop/Event/Experience proposée depuis une fiche Ville.
- [ ] Une modification de ville demande confirmation et synchronise `city_id`, ville et code postal.
- [ ] Une division administrative n'est jamais transformée en ville technique.
- [ ] Une XP Lille peut avoir une SCC/séance à Seclin sans changer son `city_id`.
- [ ] Une Community possède un administrateur humain et un groupe Général créé atomiquement.
- [ ] Le FO n'affiche qu'un seul « Proposé par » selon la priorité groupe, Community, Page, Partner.
# Communautés et calendrier SCC

- [ ] SQL `SessionRecurrenceOverride`, `CommunityRSVP`, `CommunityActivity` et ALTER Community installé.
- [ ] Deux niveaux de Community maximum contrôlés en BO ; aucun sous-groupe.
- [ ] Communauté inactive/non revendiquée visible en information, sans adhésion ni RSVP.
- [ ] Adhésion ouverte/demande/invitation et groupe Général vérifiés.
- [ ] RSVP Oui/Peut-être/Non enregistré par occurrence, sans doublon.
- [ ] Billetterie payante prioritaire sur le RSVP.
- [ ] Pause/remplacement SCC répercuté sur fiche XP et agenda communautaire.
- [ ] Occurrence avec Booking matérialisée et inscrits avertis.
