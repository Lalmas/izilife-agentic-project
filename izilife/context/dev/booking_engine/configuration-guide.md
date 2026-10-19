# Guide de configuration des réservations

## Déclaration du parcours et conditions d'exécution

Le choix d'un comportement comme « Réservation de table » décrit uniquement la manière dont l'utilisateur devrait interagir avec ce lieu ou cette catégorie. Ce choix n'est ni une activation, ni une autorisation. Il reste sans effet si le reste du modèle ne le justifie pas.

Un parcours n'est visible et utilisable que si les conditions suivantes sont réunies :

1. la catégorie est compatible avec le type de réservation selon `EtablishmentType` et `BookableServiceProductType` ;
2. le plan autorise la Feature correspondante (`TABLE_BOOKING`, `STAY_BOOKING`, etc.) ;
3. une BC/BCC active, courante, publiée, non suspendue et exploitable existe sur le lieu ou sur les catégories choisies ;
4. le parcours déclaré est cohérent avec ces éléments.

Une catégorie compatible n'est donc jamais activée automatiquement par l'abonnement. Réciproquement, sélectionner « Réservation de table » ne fabrique pas une capacité absente et ne rend pas le parcours visible. La présence d'un Equipment reste informative lorsque son parcours n'est pas autorisé et publié.

## Classification des catégories

Le moteur ne teste jamais un nom comme Restaurant, Bar, Bowling, VR ou Escape Game. Il résout le `BookableServiceProductType` de l'`EtablishmentType` :

- `table-au-restaurant` : parcours TABLE ;
- `objet-reservable` : parcours Equipment/ressource ;
- `hebergement` : futur parcours STAY ;
- types de places : futurs parcours SEAT ;
- ticket, accès à la journée, abonnement, etc. : parcours d'accès EAP/EABC.

Pour `ShopCategory`, la classification propre de l'enfant est prioritaire. L'enfant n'hérite du parent que s'il n'a aucune classification propre. Une exception doit donc être exprimée dans le référentiel, jamais dans le code applicatif. Toute évolution du catalogue impose une passe de cohérence sur la catégorie, son parent et son `EtablishmentType`.

## Portée d'une BC

- Établissement non multi-catégorie : une BC/BCC sur l'établissement.
- Multi-catégorie en mode `unique-etablissement` : une BC/BCC commune ; les catégories décrivent le lieu mais ne créent pas artificiellement plusieurs tunnels.
- Multi-catégorie en mode `commerces-separes` : chaque catégorie publiée doit être explicitement rattachée à une BC via `BookingConfigurationCategory`.
- Plusieurs catégories aux mêmes règles peuvent partager une seule BC. Le tunnel demande alors la catégorie effective et l'enregistre dans `Booking`.
- Des horaires, capacités ou règles différents nécessitent des BC distinctes.
- Une catégorie sans rattachement explicite n'apparaît pas dans le résumé FO.

## Navigation des activités et Equipment

Le niveau affiché dépend d'abord du mode de gestion du lieu. Il ne faut ni
remonter tous les Equipment au premier niveau, ni transformer automatiquement
une `EquipmentCategory` en activité de premier niveau.

### Lieu multi-catégorie en mode commerces séparés

Le premier niveau présente les catégories métier du Place/Shop réellement
exploitables, par exemple Bar, Restaurant, Bowling, VR ou Salle d'arcade.

Les Equipment sont de préférence liés à la catégorie métier à laquelle ils
appartiennent. Ils apparaissent ensuite au deuxième niveau, après sélection de
la catégorie :

```text
Que voulez-vous réserver ?
├── Bar
├── Restaurant
├── Bowling
└── VR
    ├── Mission VR A
    ├── Mission VR B
    └── Arène VR
```

La catégorie peut porter sa propre BC/BCC lorsqu'elle est directement
réservable. Les Equipment affichés sous cette catégorie restent des objets
complets, informationnels ou réservables, avec leurs photos, descriptions,
localisation, QR codes, EAP et éventuelle BC/BCC propre.

La présence d'Equipment Bowling ne crée pas une seconde entrée Bowling au
premier niveau : l'entrée est portée par la catégorie Bowling et donne accès à
la liste de ses Equipment.

### Lieu mono-catégorie

Lorsque le lieu n'exploite qu'une seule catégorie pertinente, le tunnel ne doit
pas imposer une étape de choix inutile. Un lieu dédié à la VR peut afficher ou
proposer directement ses Equipment VR. Les missions restent au niveau des
Equipment ; elles ne deviennent pas chacune une catégorie du lieu.

### Exception : Equipment important au premier niveau d'un lieu multi-catégorie

Dans un lieu multi-catégorie, un Equipment peut être une nouveauté, une activité
emblématique ou une offre suffisamment autonome pour devoir apparaître au
premier niveau, même s'il n'est lié à aucune catégorie du lieu ou s'il est lié à
une catégorie trop générale qui le laisserait normalement au deuxième niveau.
Exemples : Duckpin, une arène VR particulière ou un concept de quiz autonome.

Cette remontée doit être une décision explicite portée par l'Equipment concerné,
par exemple avec un champ `show_as_primary_activity` désactivé par défaut. Elle
ne doit pas être portée globalement par `EquipmentCategory`, car cela ferait
remonter toutes les missions VR, toutes les pistes ou tous les Equipment d'une
même catégorie.

Le champ constitue une exception éditoriale locale :

- `0` : l'Equipment suit la navigation normale de sa catégorie ou de son lieu ;
- `1` : cet Equipment précis peut être présenté comme activité au premier
  niveau de ce lieu.

Cette exception ne crée pas un nouvel objet métier `Activity` et ne duplique pas
l'Equipment. L'entrée de premier niveau pointe vers sa fiche Equipment réelle.

### Visibilité et réservation restent orthogonales

`show_as_primary_activity` ne doit jamais :

- rendre automatiquement l'Equipment réservable ;
- créer ou activer une BC/BCC ;
- créer un lien `BookingConfigurationCategory` ;
- modifier ses EAP ;
- contourner EABC, les entitlements ou les règles de disponibilité.

Une catégorie ou un Equipment peut être visible sans être réservable. À
l'inverse, un Equipment réservable peut rester au deuxième niveau sous sa
catégorie. Le resolver de navigation décide du niveau d'affichage ; le resolver
de réservation décide séparément des parcours exploitables.

### Exemples de résolution

- Hall U Need — VR : VR apparaît au premier niveau parce que c'est une catégorie
  du lieu ; les missions VR liées apparaissent après sélection de VR.
- Lieu exclusivement VR : la catégorie étant implicite, la liste des Equipment
  VR peut être affichée directement.
- Hall U Need — Bowling : Bowling apparaît au premier niveau ; les pistes à thème
  apparaissent au deuxième niveau avec leurs informations et leur éventuelle
  réservation propre.
- Salle d'arcade : la catégorie apparaît au premier niveau et ses machines au
  deuxième ; certaines machines peuvent être réservables et d'autres seulement
  informationnelles.
- Follow Park — Duckpin : l'Equipment suit normalement sa catégorie, mais peut
  recevoir `show_as_primary_activity = 1` si le Duckpin doit être mis en avant
  comme activité autonome au premier niveau.

## Exemples

### Restaurant simple

Le plan autorise `TABLE_BOOKING`. Le Partner publie une BC TABLE et ses BCC. Le formulaire est affiché. Aucun EABC n'est requis.

### Bar-restaurant unique

Le lieu est géré comme un établissement unique : une BC TABLE et une BCC communes. Le FO présente un seul parcours.

### Bar et restaurant séparés, mêmes règles

Une BC TABLE est liée explicitement aux deux catégories. Le FO affiche une entrée « Réserver une table », puis demande Bar ou Restaurant dans le tunnel.

### Bar et restaurant séparés, règles différentes

Chaque catégorie possède sa BC/BCC. Le résumé FO présente deux parcours distincts.

### Multi-catégorie sans commerce de bouche

Aucune catégorie n'est compatible avec `table-au-restaurant`, donc aucune activation TABLE n'est proposée. Les parcours de loisir restent possibles selon leurs propres capacités et leur EABC éventuel.

### Commerce de bouche et loisirs

Restaurant/Bar utilisent TABLE. Bowling, VR ou Escape Game utilisent le type générique `objet-reservable`, jamais leur nom. Une BC peut porter le créneau générique et allouer une ressource d'un pool ; un Equipment thématique peut avoir sa propre BC/BCC et être choisi explicitement.

### Disney : billet puis choix du jour

EABC décrit le parcours d'accès et l'EAP vendu. La BC/BCC porte une disponibilité au jour sans imposer de créneau horaire.

### Billet puis jour et créneau

EABC impose l'achat/validation de l'EAP ; la BC/BCC fournit ensuite le jour et les créneaux. Une BC Equipment ne doit jamais permettre de contourner ce chemin d'accès.

## Contrat EABC

EABC orchestre les accès, EAP et parcours des lieux de loisir/Equipment. Il peut coexister avec TABLE sur le même lieu, mais TABLE reste indépendante : aucun type « réservation de table » n'est ajouté à EABC et l'absence d'EABC ne bloque jamais une réservation de table correctement autorisée, activée et configurée.

## Contenu spécial Brunch

Le Brunch est un contenu spécial d'une BC/BCC, pas une couverture standard des sept jours.

- une BC contenant uniquement un Brunch actif est activable sans compléter les autres jours ;
- le contenu Brunch doit néanmoins avoir au moins un jour, une heure de début et une heure de fin valides ;
- un seul contenu Brunch actif est admis par BC ;
- une BC standard sans Brunch reste soumise à la couverture des sept jours ;
- une BC générale est éligible si la catégorie principale **ou une catégorie secondaire** du lieu peut proposer un Brunch ;
- une BC ciblée sur une catégorie n'est éligible que si cette catégorie (ou son parent autorisé) peut proposer un Brunch ;
- les racines éligibles sont Restaurant, Bar, Salon de thé, Coffee shop/Café, Boulangerie, Pâtisserie, Food truck, Hôtel-restaurant et Bruncherie ; leurs catégories enfants héritent de l'éligibilité ; côté Place, Hôtel, Résidence hôtelière, Complexe hôtelier et Food court sont admis ;
- en BO, l'éligibilité est vérifiée sur la catégorie principale comme sur les catégories secondaires ; le Partner ne peut pas publier un Brunch hors de ce périmètre ;
- le bloc de détails Brunch n'est affiché que lorsque « spécial Brunch » est effectivement choisi ;
- activer une BC la publie également pour éviter un état BO actif mais invisible en FO.
