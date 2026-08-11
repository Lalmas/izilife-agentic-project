# Accès, séances, réservations et participations

Ce document fixe le contrat métier commun aux Events, Experiences et futurs parcours Place/Shop.

## Principes

Les notions sont orthogonales :

1. **AccessType** décrit le droit et le prix : libre et gratuit, gratuit sur réservation, payant, abonnement, etc.
2. **Billetterie iziLife** (`use_izilife_paiement`) dit si iziLife réalise l'inscription ou la vente. Si elle est désactivée, les séances restent informatives et un lien/contact peut être affiché.
3. **Booking needed** dit si une capacité doit réellement être réservée.
4. **Parcours de vente** précise quand choisir la date : aucune date, date seule, séance/créneau ou choix après paiement.
5. **Session** décrit une occurrence et porte sa capacité totale. Elle existe indépendamment de la billetterie.
6. **ElementAccessPrice (EAP)** décrit un tarif ou un pack. Il n'est pas autorisé pour « Libre & Gratuit ».
7. **Booking** représente une réservation réelle de capacité. Une simple information de séance n'en crée pas.
8. **CommunityRSVP** représente `présent / peut-être / absent` par occurrence, sans billet ni QR. Un sondage de groupe reste une autre notion.

## Experience : modes de participation

`Experience.participation_mode` désambiguïse `minimal_number_of_people` et `maximal_number_of_people` :

- `individual` : minimum/maximum de personnes qu'un même utilisateur peut inclure dans sa réservation ; la capacité totale reste sur la Session.
- `private_group` : le client vient avec son propre groupe privé, compris entre le minimum et le maximum.
- `open_group` : groupe public ou collectif ; le maximum est une indication éditoriale, la Session porte la jauge réelle.

Exemples :

- Blabla Run : `open_group`, séances mardi/jeudi, aucune réservation iziLife actuellement.
- Escapade urbaine publique limitée à 8 participants au total : `open_group`, Session capacité 8.
- Réservation individuelle de 1 à 4 places dans une séance de 20 personnes : `individual`, min 1, max 4, Session capacité 20.
- Expérience privée pour 4 à 10 proches : `private_group`, min 4, max 10.

## Matrice d'affichage Experience

| Accès | Billetterie iziLife | Affichage |
|---|---:|---|
| Libre & Gratuit | non/oui incohérent | Séances, lieu, horaires, contact ; aucun tarif ni achat |
| Gratuit sur réservation | oui | Séance éventuelle, quantité, réservation à 0 €, aucun PSP |
| Gratuit sur réservation | non | Séances et lien externe/contact |
| Payant | oui | EAP avec compteurs −/+, choix temporel selon le parcours, PayHub |
| Payant | non | Prix indicatif éventuel et lien externe autorisé |

## Parcours FO adaptatif Experience

L'interface ne doit pas imposer un tunnel unique à toutes les Experiences. Le resolver commun au FO et au serveur choisit la branche applicable :

- `NO_DATE` : aucun choix temporel. Les EAP sont affichés directement et l'achat ne crée pas de réservation datée. Exemple : dégustation organisée ensuite directement avec le prestataire.
- `ARRIVAL_DATE` : le calendrier est affiché avant les EAP ; les EAP ne deviennent achetables qu'après le choix du jour.
- `SESSION` avec choix avant paiement : cascade stricte `date -> séance -> EAP`. Une date dont toutes les séances sont complètes reste signalée « Complet » et n'est pas sélectionnable. Une séance complète reste visible, grisée/rouge, mais ne peut pas être choisie.
- choix différé après achat : l'EAP est acheté comme un droit à planifier avant une échéance. L'écran dédié applique ensuite la même cascade date puis séance, uniquement si la configuration de ce droit exige une séance.
- Experience informative ou « Libre & Gratuit » sans réservation iziLife : aucun EAP ni achat à 0 €. Les prochaines séances restent affichées sous forme de cartes informatives.

Un EAP unique limité par `maximum_quantity_per_user = 1` représente un achat unitaire : il est présélectionné à une unité et l'interface ne montre pas de compteur `- / +`. Le serveur conserve la même limite. L'existence d'un seul EAP ne suffit pas à déduire cette règle : la limite doit être configurée explicitement.

Les cartes et sélecteurs de séances utilisent la même projection des récurrences :

- la configuration courante fournit le planning normal ;
- une configuration temporaire applicable à une période remplace la récurrence normale sur cette période ;
- une `Session` matérialisée liée à un SCC représente l'exception (modification ou annulation) et masque l'occurrence virtuelle correspondante ;
- hors période temporaire, la récurrence courante redevient visible.

Cette règle vaut pour les Experience informatives comme pour les Experience payantes. Une séance informative ne crée jamais de `Booking`.

Une configuration de sessions n'a pas à couvrir les sept jours de la semaine pour être activée. Elle est valide dès qu'elle contient au moins un horaire actif et qu'elle ne contient pas de conflit de jours. Une programmation limitée au mardi et au jeudi est donc complète.

### Portée géographique V2

Pour éviter de transformer la recherche en moteur multi-occurrences prématuré, une Experience reste locale dans la V2. Plusieurs séances peuvent utiliser des lieux différents dans le même bassin de vie, mais le lieu d'un SCC est un lieu opérationnel et non un nouveau scope d'indexation national.

Un concept exploité par des groupes indépendants à Lille, Paris, Toulouse et Marseille utilise une Experience locale par groupe/zone. Une future relation de modèle, réseau ou marque pourra relier ces Experiences sans modifier Session, Booking, EAP ou Ticket. La recherche ne doit donc pas, dans ce chantier, dupliquer une Experience nationale dans chaque ville déduite de ses SCC.

### Placement du bloc informatif

Sur la fiche Experience, le bloc « Séances / Réservation » conserve la cohérence visuelle de l'application :

1. résumé textuel de la récurrence actuellement applicable ;
2. cartes des prochaines séances ;
3. cartes tarifaires informatives ;
4. contact ou lien de réservation externe.

Les tarifs restent donc présentés en cartes même lorsqu'ils ne sont pas achetables sur iziLife. En revanche, aucun contrôle de formulaire, compteur ou faux bouton de réservation n'est affiché si iziLife ne peut pas exécuter l'action.

### RSVP communautaire

Le CTA « Rejoindre le groupe » et les réponses RSVP appartiennent à `CommunityRSVP`, pas à `Booking` ni à la billetterie. Le FO propose `présent / peut-être / absent` aux membres pour une occurrence, sans Ticket ni QR code. L'agrégation dans « Mes activités » reste un chantier distinct.

Le module rattache directement une Experience ou un Event à zéro ou une `Community`, ou zéro ou un `UserGroup`. Il n'introduit aucune table intermédiaire ni politique d'accès supplémentaire.

La première version applique une règle unique :

- utilisateur connecté déjà membre de la Community, ou membre d'un de ses UserGroup : boutons `Oui / Non / Peut-être` ;
- utilisateur non connecté ou non membre : message `Vous devez rejoindre ce groupe` ;
- non-membre : accès à la page communautaire et demande d'adhésion selon la politique ouverte ou validée ; les invitations avancées restent différées.

Lorsque l'activité est directement liée à un UserGroup, l'appartenance est vérifiée dans UserGroupMember. Lorsqu'elle est liée à une Community, l'appartenance est vérifiée dans CommunityMember ou dans un UserGroup appartenant à cette Community. Les futures règles d'adhésion pourront plus tard s'intercaler entre « rejoindre » et « membre accepté » sans modifier CommunityRSVP.

Ce module fait partie de la mission de recette Experience décrite dans le PDF. Il ne doit pas être reclassé comme une évolution facultative. La conception doit néanmoins réutiliser `Community`, `CommunityMember`, `UserGroup` et `UserGroupMember`, sans créer une seconde notion concurrente de communauté.

Une `Page` éventuelle reste une façade éditoriale/marketing. Elle ne doit porter ni l'adhésion, ni les droits, ni les RSVP. Une Community peut donc fonctionner sans Page ; si une Page lui est associée plus tard, elle restera une projection visible facultative et non l'identité métier de la communauté.

Le SQL du module est regroupé à la fin de `izilife-admin/statics/izilife_new_version/021_Next_Improves.sql`. Il ajoute les rattachements Event/Experience, `CommunityRSVP`, `CommunityActivity`, les attributs publics de Community et `SessionRecurrenceOverride`. `Page` reste indépendante.

La distinction complète entre CommunityActivity, Experience à séances et Event daté est documentée dans `context/Communautes_et_groupes/README.md`. Le rattachement communautaire agit sur la visibilité des propositions ; il ne masque jamais une billetterie requise. Booking/EAP/Ticket reste prioritaire sur CommunityRSVP.

### Gratuit sur réservation iziLife

Une inscription gratuite qui réserve réellement une capacité produit un `Booking`. Le montant nul supprime uniquement le passage PSP ; il ne supprime pas la réservation métier. Un `Ticket` à 0 € peut alors fournir un QR code et alimenter le contrôle d'accès, l'annulation et « Mes activités ».

À l'inverse :

- une inscription gratuite `NO_DATE` qui crée seulement un droit peut produire un Ticket sans Booking daté ;
- une information libre sans engagement ne produit ni Booking ni Ticket ;
- un RSVP communautaire ne produit ni Booking ni Ticket.

La volumétrie n'est pas un motif pour détourner le modèle : les identifiants `BIGINT UNSIGNED` sont dimensionnés pour conserver les réservations réelles, et cette conservation donne précisément l'historique fonctionnel attendu.

## Affichage des séances informatives

Une Experience sans billetterie iziLife n'affiche pas une longue liste de dates si
l'utilisateur ne peut agir sur aucune occurrence. Le FO affiche la récurrence humaine,
le ou les lieux utiles, les cartes tarifaires informatives et le contact externe.

Les cartes d'occurrences sont conservées lorsqu'elles servent réellement à une action :
sélection avant réservation/paiement iziLife ou réponse RSVP d'un membre de groupe.
Le principe reste : ne présenter un contrôle que si l'utilisateur peut agir dessus.

Une configuration temporaire datée remplace la configuration courante sur sa période,
puis la récurrence normale revient automatiquement. Une occurrence ponctuelle peut être
annulée ou déplacée depuis l'action « Exception » du contenu SCC en BO.

## Events

- Une occurrence dont `event_access_type` est NULL hérite du parent récurrent, puis de l'EventSerie.
- La création d'une occurrence doit copier l'accès du parent ; l'héritage à la lecture protège les anciennes données.
- Une carte de recherche est une aide à la décision : elle affiche billetterie en pause, clôturée, complet, ou le stock faible à partir de 15 places restantes.
- Un événement multi-jour affiche une plage de dates séparée du titre. Le titre doit rester sémantique et ne pas embarquer les dates.

## Packs et limites

- `ElementAccessPrice.maximum_quantity_per_user` sur un pack limite le **nombre de packs**.
- `Event.maximum_tickets_per_user` limite le nombre réel d'admissions obtenu.
- Le stock des composants est consommé par `nombre de packs × quantité du composant`.

Exemple : un pack contient 2 Tarif 1 + 2 Tarif 2. Deux packs consomment 4 Tarif 1, 4 Tarif 2 et 8 admissions. S'il ne reste que 2 billets de chaque tarif, un seul pack est disponible.

## Billetteries externes

Dans le `.env` du front (ou dans les variables d'environnement du serveur) :

```ini
IZILIFE_ALLOWED_EXTERNAL_TICKETING_HOSTS = shotgun.live,billetweb.fr,www.billetweb.fr,weezevent.com,www.weezevent.com
```

Valeur : liste séparée par des virgules de noms d'hôtes autorisés, sans protocole ni chemin. Une URL dont l'hôte n'est pas dans cette liste reste affichée comme simple lien et n'est pas promue comme billetterie partenaire.

## SQL à exécuter

Le SQL de cette évolution est regroupé dans `izilife-admin/statics/izilife_new_version/021_Next_Improves.sql`. Il ajoute `participation_mode`, classe Blabla Run comme groupe ouvert et contient le bloc RSVP communautaire.

## Mes activités (suite V2)

La vue utilisateur agrégera sans fusionner les écritures : Bookings, billets Event réellement achetés/réservés, RSVP communautaires et éléments ajoutés manuellement à l'agenda. Les événements réellement réservés doivent être prioritaires sur les suggestions éditoriales.
# Clarification lieux et portée (2026-08-09)

- `city_id` reste obligatoire et constitue l'unique scope de découverte de l'Experience.
- Le BO expose un unique champ `Ville cœur`, qui renseigne directement `city_id`.
- Aucun scope administratif ou communautaire ne complète ou ne remplace ce rattachement dans la V2.
- Une AdministrativeDivision ne peut pas se substituer à cette ville : sa colonne `city_id` n'est pas une ville-centre universelle et concerne notamment des subdivisions locales comme certains quartiers.
- La structure normale reste Pays → divisions administratives selon le pays → City → éventuelles subdivisions locales. Les intercommunalités utilisent leur liste dédiée de villes et ne sont pas injectées artificiellement dans cette chaîne.
- Une Experience rattachée à Lille peut avoir des SCC/séances à Lille et Seclin ; cela ne change pas sa ville cœur. Les moteurs qui exploitent les lieux de séance le feront explicitement sans réécrire le socle des recherches par `city_id`.
- `experience_in_all_city` signifie que l'activité se déroule à travers la ville. Cela n'annule jamais un lieu de rendez-vous.
- `meet_place` / `meet_shop` restent le lieu général ou le rendez-vous de l'Experience.
- `locations_by_session = 1` signifie que les lieux opérationnels sont portés par chaque `SessionConfigurationContent`/`Session`.
- Une Experience en mode lieux par séance ne peut être activée/listée sans configuration active et sans lieu ou adresse sur chacun de ses contenus actifs.
- Une Experience informative affiche des cartes hebdomadaires jour/horaire/lieu ; les cartes datées servent uniquement lorsqu'une action porte réellement sur une occurrence.
- Le BO sépare `Proposé par (Partner/Page)` de `Communauté/Groupe` pour ne jamais mélanger identité commerciale et rattachement communautaire.
- Le FO affiche une seule ligne « Proposé par » avec priorité UserGroup (et sa Community), Community, Page, Partner.
# Règle géographique ferme

- `Experience.city_id` reste obligatoire et constitue l'unique ville cœur utilisée par la découverte et les recherches existantes.
- Une `AdministrativeDivision` ne fournit jamais un `city_id` de remplacement. Sa colonne `city_id` n'a pas une sémantique universelle de ville-centre ; elle concerne notamment certains niveaux sous la ville. Les intercommunalités conservent leur relation dédiée aux villes.
- Le scope d'une Community n'altère pas `Experience.city_id`.
- Les lieux opérationnels de `SessionConfigurationContent` et `Session` peuvent se trouver dans une ville voisine. Exemple : Experience rattachée à Lille, séance à Seclin.
- En mode `locations_by_session`, les contenus actifs doivent tous porter leur lieu/adresse. Le lieu de l'Experience ne doit pas masquer une configuration de séance incomplète.

# Création BO autonome

- Event, Experience, Place et Shop se créent depuis leur liste, sans passer par une fiche Ville et sans `city_id` imposé dans l'URL.
- Le formulaire exige une proposition d'autocomplétion typée `CITY-id`; le serveur recharge la vraie ligne City.
- `city_id`, nom de ville et code postal sont enregistrés ensemble depuis cette ligne. Une saisie libre ou un code postal ne peut jamais devenir un `city_id`.
- Une modification de ville affiche une confirmation explicite. Le serveur refuse une référence invalide et met les champs dénormalisés à jour atomiquement.
- Les anciens liens d'ajout Place/Shop/Event/Experience depuis une fiche Ville sont retirés du parcours BO.
- L'autocomplétion internationale d'adresse ne doit pas interroger silencieusement Nominatim depuis le navigateur. Elle devra passer par un proxy iziLife avec quota/cache et information utilisateur. En attendant, la ville typée est obligatoire et latitude/longitude restent des champs explicites ; le composant historique français des adresses de séance n'est pas présenté comme international.
# Exceptions de calendrier Experience

Deux mécanismes complémentaires sont retenus :

1. `SessionRecurrenceOverride` modifie virtuellement une SCC ou toute sa
   SessionConfiguration sur une période datée, ou chaque année entre deux mois.
   Le type `pause` supprime les occurrences ; `replace` fournit jours, heures et
   lieu temporaires. Aucune Session n'est créée lorsqu'il n'existe aucun Booking.
   Une pause peut viser toute la configuration. Un remplacement doit viser une
   SCC précise afin de ne jamais dupliquer les occurrences de plusieurs contenus.
2. Une annulation ou un déplacement ponctuel est matérialisé dans `Session` avec
   `session_conf_content_id`. Une ligne inactive neutralise l'occurrence SCC ;
   une seconde ligne active représente la séance déplacée. Le déplacement peut
   modifier la date, les horaires et le lieu opérationnel (Place, Shop ou adresse).

Lorsqu'une exception touche des Booking existants, les occurrences concernées
sont matérialisées sans doublon et les inscrits Booking ainsi que les RSVP
`yes`/`maybe` de l'occurrence reçoivent un courriel. Le resolver FO et
l'agenda communautaire consomment la même résolution, donc une occurrence
annulée ne doit jamais réapparaître dans l'un des deux écrans.
