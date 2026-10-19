# Lot de corrections FO / BO / Partner — 16 août 2026

## Horaires

- horaires courants séparés entre ouverture générale et cuisine ;
- horaire de cuisine hebdomadaire indépendant ; exceptions limitées à l'ouverture générale ;
- remplacement de la ligne du jour au lieu d'une ligne en doublon ;
- mention « horaire exceptionnel » complétée par le jour férié détecté ;
- avertissement de jour férié sans exception fournie ;
- accordéons fermés au chargement et statuts directs par activité.

## Commercial et réservation

- règles de rémunération disponibles sur Event, EventSerie, AnnualCelebration, Experience et Partner ;
- un Partner peut porter une règle Event, Experience, ou les deux ;
- le PayHub conserve un plan de split audité, sans exécution PSP tant que son commutateur de sécurité est désactivé ;
- réservations distinguées entre configuration générale et activité secondaire ;
- offres ciblables par catégorie ou applicables à tout le lieu ;
- menus regroupés sous « Produits & menus ».

## Liens externes

Un lien Event n'est public que si `show_external_booking_link=1`, si l'Event est payant et si la billetterie iziLife n'est pas utilisée. La liste de domaines concurrents interdits reste prioritaire.

## Navigation et rendu

- intentions accessibles sur desktop ;
- header mobile compact de 48 px, sans disparition temporisée ni espace fantôme ;
- avis centrés sur desktop avec CSS limité à `#reviews` ;
- suppression de la sortie de debug WTD ;
- navigation culturelle séparée en Théâtre, Humour & Comedy clubs et Expositions sous Art ;
- rendu corrigé des caractéristiques visuelles sans HTML brut.

## SQL local appliqué

Les colonnes `Hourly.service_scope`, `HourlyContent.service_scope`, `LocalEvent.show_external_booking_link`, `Offer.shop_category_id` et `Offer.place_type_id` sont présentes dans `izilife2`. Les drapeaux LGBT des lieux/commerces ont été remis à `0` ; ils l'étaient déjà dans la base locale.

## Conditions d'utilisation des avantages

- trois modes exclusifs : selon les horaires, heure limite, ou créneaux précis ;
- fermeture réelle du Shop/Place toujours bloquante, exceptions horaires comprises ;
- après une heure limite du soir, indisponibilité jusqu'à 06h ;
- présentation compacte repliable, avec jours consécutifs regroupés (`Mar–Sam · avant 23h`) ;
- anciennes règles contenant simultanément créneaux et heure limite normalisées par le SQL final.

## News par édition

- une édition Event peut porter ses propres News sans redirection vers son AnnualCelebration ;
- FAQ et HISTORY restent réservées aux parents EventSerie et AnnualCelebration ;
- gestion globale avec recherche polymorphe, y compris Equipment localisable ;
- formulaire média allégé et options secondaires repliées ;
- limite d'upload fournie par le mode : 1 en média unique, 8 sinon.
## Avantages de Plans et conditions d’utilisation

- Les avantages de type `plan` affichés sur les lieux sont limités à `USER_PASS` et `USER_PRIME`, uniquement lorsque le Plan correspondant existe et est actif.
- Les références numériques de Plan ne sont pas supposées stables entre les bases : la règle métier repose sur `Plan.string_id`, jamais sur un `plan_id` codé en dur.
- Les contraintes horaires sont mutualisées par objet et temporalité. Elles sont rendues une seule fois, après les avantages Pass/Prime, sous le libellé discret « conditions d’utilisation ».
- En l’absence de créneau explicite, la condition commune est « Selon les horaires du lieu ». Les créneaux explicites et une heure limite restent mutuellement exclusifs.
- Les créations effectuées par l’agent Scraper et les modifications BO réutilisent/synchronisent la contrainte commune de la temporalité afin d’éviter une condition différente pour Pass et Prime.

## Éditions, communautés, News et médias

- AnnualCelebration : une nouvelle édition est refusée si sa période chevauche une édition existante du même parent, y compris une édition inactive.
- EventSerie : un chevauchement au même lieu déclenche un avertissement et exige une confirmation explicite ; un autre lieu reste autorisé.
- Event : Communauté et Groupe se sélectionnent par autocomplétion. Un Groupe impose côté navigateur et côté serveur sa Communauté réelle ; les identifiants numériques ne sont plus saisis manuellement.
- Les champs Prix & Accès Event restent sur une seule ligne aux largeurs desktop ; la grille Lieu/Organisateur/Communauté/Visibilité Experience suit la même règle sans CSS générique.
- `EVENT_MAP` est le type dédié au plan d’un événement. Il impose une présentation média unique et ne demande pas de corps d’article ; le terme `PLAN` reste réservé aux abonnements iziLife.
- Les médias internes d’une édition se gèrent depuis le pilotage central filtré sur le scope Event. Les médias externes d’une édition AnnualCelebration/EventSerie restent portés par son parent.
- Les modales Ajouter/Modifier du pilotage média conservent le scope et l’URL de retour, afin d’éviter les erreurs de contexte après enregistrement.
