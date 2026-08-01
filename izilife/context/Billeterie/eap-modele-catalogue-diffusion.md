# EAP — modèle, instances, diffusion et feuille de route

Dernière mise à jour : 29 juillet 2026

## 1. Objet du document

Ce document fixe ce que devient `ElementAccessPrice` après l'audit de la billetterie Event et les échanges sur Experience, EventSerie, Partner et les lieux multi-catégories.

Il sert de référence avant toute nouvelle généralisation. Il évite de confondre :

- le tarif modèle ;
- le tarif réellement vendu sur un objet ;
- la copie d'un tarif ;
- le périmètre local dans lequel le tarif est utilisable ;
- `ElementService` et `Product`, qui pourront employer une mécanique de catalogue comparable sans devenir des EAP.

## 2. Définition métier de l'EAP

Un `ElementAccessPrice` est une offre tarifaire qui donne un droit d'accès à un objet ou à une ressource IziLife.

Exemples :

- entrée adulte ou enfant d'un Event ;
- billet gratuit sur réservation ;
- pack famille ;
- accès à une Experience ;
- accès à un Equipment ;
- pass ou carte d'accès à un Place/Shop.

`Tarif libre` et `tarif libre à partir de` ne sont pas des EAP. Ce sont des modes d'accès propres à l'Event. Le front construit un formulaire virtuel (montant par personne et nombre de personnes) et `EventBookingHandler` le valide sans rechercher une ligne `ElementAccessPrice`.

L'EAP n'est pas le Ticket délivré. Après réservation ou paiement, le pipeline produit les occurrences `Ticket` correspondant aux droits achetés.

L'EAP n'est pas non plus un `ElementService`. Un ES représente une prestation. Un EAP représente un droit d'accès. Ils peuvent partager des briques de catalogue, prix, Booking, panier et paiement sans être fusionnés.

## 3. Deux rôles pour un EAP

### 3.1 EAP modèle

Un EAP modèle sert de point de départ réutilisable. Il n'est normalement pas vendu directement dans le tunnel d'un Event.

Sources prévues :

- EventSerie ;
- Partner ;
- éventuellement Network dans une phase ultérieure.

Attributs structurants déjà prévus dans le schéma :

- `is_template = 1` ;
- `event_serie_id` ou `partner_id` ;
- aucun rattachement à une instance de vente locale.

### 3.2 EAP local

Un EAP local est installé sur l'objet qui le vend réellement :

- `event_id` ;
- `experience_id` ;
- `place_id` ;
- `shop_id` ;
- `equipment_id` ;
- etc.

Il possède ses propres prix, période de vente, limites éventuelles, état et dépendances. Le front et le handler de paiement utilisent l'EAP local, pas un modèle recherché dynamiquement dans une EventSerie ou un Partner.

`ElementAccessPrice.quantity` est facultatif. Lorsqu'il est renseigné, il limite cette offre ; il ne représente pas systématiquement la capacité réelle. La disponibilité peut être portée par l'Event, une Session, un Equipment, une ressource ou un créneau Booking, ou être illimitée. Un resolver de disponibilité doit combiner ces contraintes.

Lorsqu'il provient d'un modèle :

```text
is_template = 0
is_variant_of = ID de l'EAP modèle
```

## 4. Utiliser ou copier

Deux besoins doivent être proposés, sans les confondre.

### Créer une instance depuis un modèle

Le modèle est instancié sur l'objet. L'instance locale devient indépendante mais conserve sa provenance avec `is_variant_of`.

C'est le comportement recommandé pour :

- EventSerie vers une édition Event ;
- Partner vers un Event, une Experience, un Place ou un Shop ;
- duplication rapide d'un tarif local.

Une modification ultérieure du modèle ne modifie pas automatiquement les instances existantes.

Une table de déploiement pourra tracer explicitement : modèle source, objet cible, instance créée, date, auteur et version. Elle empêchera les doublons et permettra de proposer une nouvelle mise à jour. Elle ne remplacera pas l'EAP local vendu par l'objet.

Cette instanciation doit être centralisée dans un service commun et recopier de manière atomique les dépendances : tarifs groupés, composition de packs avec remappage des identifiants, médias et règles compatibles.

### Utiliser un même droit partagé

Cas particulier futur : un pass Partner ou Network réellement valable dans plusieurs objets.

Il ne s'agit alors pas d'une copie, mais d'un droit partagé avec une capacité, une validité et une consommation communes. Ce comportement nécessitera une liaison explicite EAP ↔ objets et ne doit pas être simulé en plaçant plusieurs clés étrangères sur la même ligne.

La synchronisation automatique modèle → instances est différée : elle exige des règles d'héritage champ par champ et une gestion des conflits.

## 5. EventSerie

Le système existe déjà partiellement :

- une EventSerie possède des EAP via `event_serie_id` ;
- le BO affiche une section « Tickets templates (EAP) » ;
- la publication d'une édition propose « Copier tickets templates (EAP) » ;
- le contrôleur recopie les EAP vers le nouvel Event.

Points à corriger :

- marquer les EAP de série comme modèles ;
- renseigner `is_variant_of` lors de la copie ;
- copier les tarifs groupés ;
- copier les compositions de packs en remappant les identifiants ;
- copier les autres dépendances compatibles ;
- éviter les doublons lors d'une nouvelle importation ;
- permettre de choisir quels EAP copier ;
- indiquer dans l'Event la série et le modèle d'origine ;
- permettre une duplication locale indépendante.

Le tunnel Event continue de ne vendre que les EAP ayant `event_id = Event courant`.

## 6. Catalogue Partner

Le catalogue Partner n'est pas un préalable au lancement Event/XP, mais il est une cible structurante.

Il permettra à un organisateur, une association ou un réseau de préparer des offres réutilisables pour plusieurs objets.

Version minimale :

- créer et modifier un EAP modèle ;
- voir les objets du Partner compatibles ;
- sélectionner un ou plusieurs objets cibles ;
- créer des copies locales ;
- conserver `is_variant_of` ;
- afficher où le modèle a été déployé ;
- ne pas synchroniser automatiquement les copies.

Évolution future : pass partagé entre plusieurs objets, mise à jour contrôlée des variantes et catalogue Network.

## 7. Périmètre local Place/Shop

Une fois l'EAP rattaché à un Place ou Shop, son périmètre local peut être :

- tout le lieu/commerce ;
- une catégorie secondaire ;
- plusieurs catégories secondaires ;
- certains équipements ou animations.

Les liaisons existantes sont :

- `LocationEAPUseForCategory` ;
- `LocationEAPUseForEquipment`.

La notion actuelle de « diffusion » doit être renommée en « Périmètre d'application » lorsqu'elle concerne les catégories et ressources internes.

L'identité de `LocationOtherCategory` reste composite :

```text
Place : place_id + place_type_id
Shop  : shop_id + shop_category_id
```

Une clé artificielle n'est pas nécessaire. Les références typées `PLACE-{id}` et `SHOP-{id}` doivent devenir le seul format accepté par le code concerné.

### Souplesse retenue

- même prix et mêmes règles sur plusieurs catégories : un seul EAP avec plusieurs liaisons ;
- prix, limite d'offre ou règles différents : EAP distincts ;
- action « Dupliquer » pour accélérer la création d'un EAP indépendant ;
- choix « Tout l'objet » ou « Catégories sélectionnées » dans l'ajout et la modification ;
- badge de périmètre dans la liste.

## 8. Experience et Sessions

Le moteur générique accepte déjà `EXPERIENCE` et la table EAP possède `experience_id`. La page BO Experience ne charge cependant pas encore la gestion commune des EAP.

Le branchement XP devra apporter :

- bloc EAP sur la page Experience ;
- ajout, modification, pack et tarif groupé via les composants communs ;
- rattachement EAP ↔ Session ou `SessionConfigurationContent` ;
- contrôle des capacités de Session ;
- choix du créneau avant ou après achat selon `ElementAccessAndBookingConf` ;
- handler serveur dédié ou généralisation maîtrisée du pipeline Event ;
- génération des Tickets et/ou Booking correspondants.

## 9. ElementService et Product

`ElementService` suivra la même idée de catalogue et de provenance, mais gardera ses propres règles : service, durée, options, réservation et exécution de prestation.

Le catalogue Partner pourra donc contenir plusieurs familles :

```text
Catalogue Partner
├── modèles EAP
├── modèles ElementService
├── modèles Product
└── éventuellement modèles Offer
```

Pour Product, la diffusion est plus complexe : prix multiples, variantes, options, stocks, menus et canaux de vente. Elle ne doit pas être généralisée avant d'avoir stabilisé EAP puis ES. Le mécanisme commun à mutualiser sera limité au catalogue, à la provenance et au déploiement ; la copie détaillée restera propre à chaque famille.

## 10. Ordre du chantier transversal validé

Le chantier est mené dans les fiches Back Office avant son portage dans l'espace Partner :

1. Centraliser le scope commun : tout l'objet ou catégories sélectionnées.
2. Adapter l'ajout et la modification des EAP.
3. Afficher clairement le périmètre dans la liste des EAP.
4. Installer le composant EAP commun sur Experience.
5. Installer les accès ElementService manquants, notamment Shop et XP.
6. Étendre le même contrat de scope à Hourly, ElementMenu, Offer, BPR de type Plan, Product et ElementService.
7. Brancher EAP + Sessions pour la vente des Experiences.

À l'intérieur de ces étapes, les EAP Event restent la référence fonctionnelle et le mécanisme d'instanciation EventSerie/AnnualCelebration doit être fiabilisé avant d'être réutilisé par XP. Tout ce qui concerne l'espace Partner (gestion des objets, catalogue Partner et déploiements) est préparé ici mais réalisé dans la conversation Partner.

## 11. À transférer dans la conversation espace Partner

Les éléments suivants appartiennent explicitement au chantier Partner :

- gestion des EAP Event depuis l'espace Partner ;
- création/modification/activation des EAP ;
- packs et tarifs groupés ;
- pause, reprise et clôture des réservations ;
- réservations, ventes, participants et chiffre d'affaires ;
- installation des EAP sur Experience et Sessions ;
- choix du périmètre multi-catégorie Place/Shop ;
- accès aux ElementServices de Place, Shop, Page, Partner, XP et Equipment selon droits ;
- catalogue Partner de modèles EAP ;
- sélection des objets appartenant au Partner ;
- copie d'un modèle vers les objets choisis ;
- affichage de la provenance et des déploiements ;
- duplication indépendante ;
- plus tard, pass partagé entre plusieurs objets ;
- plus tard, catalogues ES, Product et Offer ;
- permissions fines par employé Partner et par objet ;
- empêcher toute administration d'un objet hors périmètre du Partner.

## 12. Principes non négociables

- Un Event vend ses EAP locaux ; il ne dépend pas d'une résolution dynamique fragile vers EventSerie/Partner.
- Toute copie issue d'un modèle conserve sa provenance.
- Copier et partager sont deux opérations différentes.
- La limite éventuelle d'un EAP local ne doit pas être mélangée à celle d'un modèle ; la capacité réelle reste résolue sur la cible ou la ressource.
- Le périmètre catégorie ne crée pas un nouveau Place/Shop.
- EAP, ElementService et Product partagent des infrastructures, pas leur identité métier.
- Le serveur reste l'autorité pour prix, capacités, disponibilités et droits Partner.
