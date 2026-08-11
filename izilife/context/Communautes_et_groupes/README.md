# Communautés, groupes et activités collectives

> Mise à jour du 10 août 2026 : `DECISIONS_FEED_2026-08-10.md` remplace toute règle antérieure imposant un groupe `Général`. Chaque Community et chaque UserGroup possède son propre feed/canal d'annonces.

Dernière mise à jour : 8 août 2026.

Ce dossier fixe progressivement le domaine Community/UserGroup. Il évite de transformer `Event`, `LocalEvent`, `Experience`, `Booking` ou `Ticket` en objets génériques pour toutes les interactions sociales.

## 1. Identité métier et Page

- `Community` porte l'identité, les membres et les règles communautaires.
- `UserGroup` porte un groupe autonome ou un sous-groupe d'une Community.
- `CommunityMember` et `UserGroupMember` portent les adhésions.
- Une éventuelle `Page` est seulement une façade publique ou marketing facultative.
- Une Community ou un UserGroup doit pouvoir fonctionner sans Page.
- Une Page ne doit jamais devenir la source de vérité des membres, des droits ou des RSVP.

## 2. Trois objets à ne pas confondre

### Activité interne légère

Exemples : « On va boire un verre ? », sortie proposée par un membre, entraînement informel ou choix collectif d'un lieu/d'une date.

Cette activité n'est pas nécessairement un Event iziLife et ne doit pas polluer `LocalEvent`. Elle peut commencer par un sondage, puis référencer un Place, un Shop, une Experience ou un Event existant.

Une future entité légère, provisoirement nommée `CommunityActivity`, devra pouvoir porter :

- Community ou UserGroup propriétaire ;
- auteur ;
- titre et texte court ;
- état `proposal / scheduled / cancelled / completed` ;
- date/heure facultatives ;
- Place, Shop, Event ou Experience référencé ;
- Survey éventuel pour choisir date ou lieu ;
- RSVP interne une fois l'activité planifiée ;
- passage facultatif vers une réservation réelle chez un lieu.

Elle ne doit pas créer artificiellement un Event tant que le groupe n'a besoin ni d'une fiche Event publique, ni de billetterie, ni des fonctions éditoriales d'un Event.

### Experience autonome à séances

Une Experience existe indépendamment d'une date et d'un lieu précis. Elle décrit un concept ou une activité reproductible : Blabla Run, cours collectif, entraînement, visite ou atelier.

Elle peut porter une récurrence, des Sessions, plusieurs lieux proches selon les Sessions, une billetterie ou une simple information et un rattachement Community/UserGroup.

Exemple : « Blabla Run Lille » peut avoir une séance à Lille le lundi et à Villeneuve-d'Ascq le samedi. Chaque occurrence porte son lieu réel, mais l'Experience reste indexée dans son bassin local.

Pour la V2, des antennes réellement indépendantes à Lille, Paris, Toulouse et Marseille utilisent des Experiences locales distinctes. Cette limite évite de faire des SCC une seconde couche implicite de scopes géographiques, d'administration et de recherche. Une future relation de modèle/réseau pourra relier ces Experiences si la mutualisation éditoriale devient nécessaire.

Conséquence de schéma à préserver : le lieu ne peut pas exister uniquement au niveau Experience. Session/SCC doit pouvoir résoudre un `session_place`, `session_shop` ou une adresse avec coordonnées, et éventuellement une configuration de réservation/lieu adaptée.

### Event daté

Un Event est l'existence datée d'un concept sur un lieu. Il n'existe pas de la même manière hors de sa date ou occurrence.

- `EventSerie` mutualise un concept éditorial entre plusieurs Events.
- `AnnualCelebration` explique une récurrence calendaire annuelle.
- un Event peut être créé par une Community/UserGroup lorsqu'il s'agit réellement d'un événement ;
- un Event communautaire peut rester privé ou devenir visible publiquement ;
- une sortie interne qui pointe vers un Event public existant reste une CommunityActivity référant cet Event, et ne crée pas un doublon.

Le rattachement `Event.community_id` ou `Event.user_group_id` reste pertinent pour les vrais Events créés par une communauté. Il ne signifie pas que toutes les sorties de groupe doivent devenir des Events.

## 3. Visibilité et billetterie sont indépendantes

Le rattachement Community/UserGroup change la visibilité dans What To Do, Home Builder, les rails Home, les suggestions, la recherche et les flux communautaires. Il ne désactive pas la billetterie.

Ordre fonctionnel :

1. déterminer si l'utilisateur peut découvrir la proposition ;
2. déterminer s'il est membre de la Community ou d'un de ses UserGroup ;
3. déterminer le parcours d'accès normal de l'objet ;
4. si une réservation ou billetterie est requise, appliquer Booking/EAP/Ticket ;
5. utiliser CommunityRSVP uniquement lorsqu'il n'existe pas de parcours de réservation prioritaire.

Ainsi :

- Event ou Experience payant : la billetterie reprend le dessus ;
- gratuit sur réservation iziLife : Booking et Ticket à 0 €, pas un simple RSVP ;
- activité collective sans réservation : RSVP `Oui / Non / Peut-être` ;
- utilisateur non membre : message « Vous devez rejoindre ce groupe » ; aucun workflow d'adhésion n'est encore déclenché.

Un RSVP ne réserve jamais une capacité commerciale et ne produit ni Ticket ni QR code.

## 4. Membership vérifié dans la première version

Pour une activité liée directement à un UserGroup, l'utilisateur doit être connecté et une ligne UserGroupMember acceptée et non bannie doit exister.

Pour une activité liée à une Community, une ligne CommunityMember acceptée et non bannie suffit, ou une adhésion acceptée à l'un des UserGroup de cette Community.

Sinon le FO affiche uniquement : « Vous devez rejoindre ce groupe ».

Le futur workflow `demande -> modération/abonnement éventuel -> acceptation` sera ajouté entre ce message et l'état membre. Il ne fait pas partie du premier RSVP.

## 5. CommunityRSVP

`CommunityRSVP` conserve une réponse par utilisateur et occurrence : `yes`, `no` ou `maybe`.

Il peut viser un Event, une Session manuelle d'Experience ou une occurrence virtuelle SCC identifiée par contenu, date et heure.

Le SQL est regroupé à la fin de `izilife-admin/statics/izilife_new_version/021_Next_Improves.sql`.

## 6. Règles anti-duplication

- Ne pas créer un Event interne pour une simple proposition ou un sondage.
- Ne pas copier un Event public lorsqu'un groupe décide d'y aller : le référencer.
- Ne pas dupliquer une Experience pour deux lieux proches d'un même programme local : localiser les Sessions.
- Créer une Experience locale distincte lorsque l'antenne/groupe, l'administration et le bassin de découverte sont distincts.
- Ne pas créer de Booking pour un RSVP sans capacité réservée.
- Ne pas créer de Ticket pour un simple « Oui ».
- Ne pas utiliser Page comme table d'adhésion.

## 7. Décisions encore ouvertes

- nom définitif de `CommunityActivity` ;
- visibilité exacte d'une activité strictement privée dans les recherches publiques ;
- transformation ou liaison d'une CommunityActivity vers une réservation Place/Shop ;
- possibilité future pour un non-membre de demander à rejoindre depuis la fiche ;
- rôle d'une Page marketing associée à une Community ;
- relation future de modèle/réseau entre plusieurs Experiences locales partageant un même concept.

Ces décisions ne doivent pas bloquer le premier RSVP réservé aux membres existants.

## 8. Modèle et déclinaisons locales d'Experience

Une Experience locale peut référencer une Experience modèle avec `model_experience_id`.
Le bouton BO « Déclinaison locale » crée un brouillon autonome : il copie le contenu
éditorial et les taxonomies, mais jamais les Sessions/SCC, lieux, EAP, capacités,
Bookings, Tickets, transactions, RSVP, Community ou UserGroup.

La copie est un instantané. Une modification ultérieure du modèle ne se propage pas
automatiquement aux déclinaisons. Lille, Paris ou Toulouse administrent donc leurs
propres horaires et inscriptions sans mélanger leurs données.

La géographie distingue deux niveaux :

- `city_id`, `administrative_division_id` et `experience_in_all_city` décrivent le
  périmètre de découverte de l'Experience ;
- `session_place_id`, `session_shop_id` ou l'adresse libre décrivent le lieu réel de
  chaque séance ou règle SCC.

`meet_place` et `meet_shop` ne sont qu'un repli pour les anciennes Experiences sans
lieu de séance explicite. Ils ne doivent pas remplacer les lieux opérationnels d'une
Experience multi-lieux.
# État du socle BO (9 août 2026)

Le BO minimal gère la création d'une Community avec administrateur humain, Partner légal facultatif, Community mère facultative et groupe Général automatique. Les groupes sont administrés depuis la Community et n'ont pas de menu ni de compte de versement autonome. Voir `SOCLE_V2_2026-08-08.md` pour les décisions détaillées.
# Règle de hiérarchie validée

Le modèle V2 autorise exactement deux niveaux de communautés, suivis d'un seul
niveau plat de groupes. Exemple : `Fitlife` → `Fitlife Europe` → groupes
`Général`, `Hauts-de-France`, `Lille`. Il n'existe ni troisième niveau de
Community ni sous-groupe.

La page publique minimale, l'adhésion, les groupes, l'agenda et le RSVP sont
décrits dans `SOCLE_V2_2026-08-08.md`.
