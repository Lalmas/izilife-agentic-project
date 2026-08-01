# IziLife — Contexte Produit / Menu Digital / Offres / Campagnes

## 0. Objectif du document

Ce document sert de contexte pour les agents de développement et pour Codex.

Il décrit comment enrichir le système produit existant d’IziLife afin de gérer correctement :

- le menu numérique ;
- les menus multiples par lieu ;
- les catégories et sous-catégories d’affichage ;
- la disponibilité temporelle des produits, catégories et menus ;
- les mises en avant de produits : produit du moment, plat du jour, cocktail du moment, menu du jour, etc. ;
- l’intégration avec les offres, campagnes, happy hours et PlaceLiveResume.

Le principe général est simple :

> Ne pas recréer des objets qui existent déjà. Ajouter des couches propres au modèle existant.

---

## 1. Modèle existant à respecter

Le système produit IziLife possède déjà plusieurs briques importantes.

### Product

`Product` est l’objet central.

Il peut représenter :

- un produit simple ;
- un produit composé ;
- un produit groupé ;
- un service ;
- un produit de réservation ;
- un produit lié à un shop ;
- un produit lié à une place ;
- un produit lié à un event ;
- un produit lié à une page ;
- un produit lié à une sélection IziLife ou MeetZ.

Un produit possède notamment :

- `product_type` ;
- `product_order_type` ;
- `productCategory_id` ;
- `product_specific_type_id` ;
- `shop_id` ;
- `place_id` ;
- `partner_id` ;
- `network_id` ;
- `page_id` ;
- `price` ;
- `is_active` ;
- `status`.

### ProductType

`ProductType` distingue déjà :

- produit simple ;
- produit composé ;
- produit groupé.

Il ne faut pas créer un nouveau type pour “formule midi”, “brunch” ou “menu étudiant”.

Une formule est un produit composé.

### ProductCategory

`ProductCategory` possède déjà `parent_id`.

Cela permet déjà de gérer les sous-catégories.

Exemple :

- Cocktails
  - Cocktails signatures
  - Cocktails classiques
  - Cocktails sans alcool
  - Cocktails d’été

Il ne faut donc pas créer une table `ProductSubCategory`.

### ComposedProductSlot / ComposedProductSlotItem

Ces tables permettent déjà de gérer les produits composés.

Exemple : formule midi.

- Slot 1 : choisir un plat ;
- Slot 2 : choisir un dessert ;
- Slot 3 : choisir une boisson.

Une formule midi est donc un `Product` de type composé avec des slots.

---

## 2. Distinction importante

Il faut séparer quatre notions.

### 2.1 Produit

Ce qui est vendu.

Exemples :

- Mojito ;
- Burger maison ;
- Tiramisu ;
- Massage californien ;
- Menu enfant ;
- Formule déjeuner.

### 2.2 Catégorie / sous-catégorie

Ce qui organise le menu.

Exemples :

- Cocktails ;
- Plats ;
- Desserts ;
- Cocktails signatures ;
- Cocktails sans alcool.

### 2.3 Menu numérique

Ce qui sélectionne et présente des catégories dans un contexte donné.

Exemples :

- Menu Bar ;
- Menu Restaurant ;
- Menu Brunch ;
- Menu Soir ;
- Menu Event.

Un même lieu peut avoir plusieurs menus.

### 2.4 Mise en avant

Ce qui remonte certains produits ou menus dans des zones spéciales.

Exemples :

- Plat du jour ;
- Cocktail du moment ;
- Dessert du jour ;
- Menu du jour ;
- Nos signatures ;
- Coups de cœur ;
- Nouveautés.

---

## 3. Menu numérique

Un menu numérique est un conteneur.

Il n’est pas une catégorie.

Il ne remplace pas `ProductCategory`.

Il dit simplement :

> Dans ce menu, on affiche telles catégories, dans tel ordre, avec éventuellement un nom d’affichage différent.

Exemple :

### Menu Bar

- Cocktails
  - Cocktails signatures
  - Cocktails classiques
  - Sans alcool
- Bières
- Tapas

### Menu Restaurant

- Entrées
- Plats
- Desserts
- Boissons

### Menu Brunch

- Brunch
- Boissons chaudes
- Desserts

Un lieu bar-restaurant peut donc avoir :

- un menu bar ;
- un menu restaurant ;
- un menu brunch ;
- un menu spécial événement.

---

## 4. Sous-catégories

Les sous-catégories sont déjà couvertes par `ProductCategory.parent_id`.

À faire côté BO / espace partenaire :

- créer une catégorie ;
- créer une sous-catégorie ;
- déplacer une sous-catégorie ;
- ordonner les catégories ;
- ordonner les sous-catégories ;
- affecter des produits à une catégorie ou sous-catégorie.

Exemple attendu pour un bar :

- Cocktails
  - Cocktails signatures
  - Cocktails classiques
  - Cocktails sans alcool
  - Cocktails du moment
- Bières
  - Pressions
  - Bouteilles
- Tapas
  - Froides
  - Chaudes

Cette organisation doit être librement modifiable par le commerçant.

---

## 5. Disponibilité

La disponibilité est une couche transversale.

Elle doit pouvoir s’appliquer à :

- un produit ;
- une catégorie de produits ;
- un menu.

Exemples :

### Produit

Formule midi :

- lundi à vendredi ;
- 12h00 à 14h00.

### Catégorie

Carte des tapas :

- tous les jours ;
- 18h00 à 23h00.

### Menu

Menu brunch :

- dimanche ;
- 10h00 à 15h00.

Règle importante :

> Si aucune disponibilité n’est définie, l’objet est considéré comme disponible par défaut.

Si une disponibilité est définie, l’objet est disponible uniquement dans les fenêtres actives.

---

## 6. Offres et campagnes

Les offres et campagnes existent déjà dans le modèle IziLife.

Il ne faut pas recréer leur logique dans les produits.

### Happy Hour

Un happy hour n’est pas un produit.

C’est une offre / campagne spéciale.

Il possède :

- une période ;
- un horaire ;
- une mécanique de réduction ;
- une ou plusieurs cibles.

Les cibles peuvent être :

- une catégorie ;
- un produit ;
- une liste de produits ;
- un autre scope déjà prévu par le système d’offres.

Exemple :

Happy hour cocktails :

- Offer / SpecialCampaign type Happy Hour ;
- horaires : 18h00-20h00 ;
- target : catégorie Cocktails ;
- mécanique : -50% ou prix spécial.

### Formule midi

Une formule midi n’est pas une offre happy hour.

C’est un produit composé avec une disponibilité midi.

Exemple :

- Product type composé ;
- slots : plat, dessert, boisson ;
- disponibilité : lundi-vendredi 12h-14h.

---

## 7. Mises en avant

Une mise en avant ne doit pas être un simple champ texte sur `Product`.

Il faut gérer des groupes de mise en avant.

Pourquoi ?

Parce que certains groupes contiennent un seul produit, d’autres plusieurs.

Exemples :

- Plat du jour : 1 produit ;
- Dessert du jour : 1 produit ;
- Menu du jour : 1 produit composé ;
- Cocktails du moment : plusieurs produits ;
- Nos signatures : plusieurs produits ;
- Coups de cœur : plusieurs produits ;
- Nouveautés : plusieurs produits.

Le commerçant doit pouvoir nommer ses groupes.

Exemples :

- “Cocktails du moment” ;
- “Les signatures de la maison” ;
- “La reco du chef” ;
- “Menu express midi” ;
- “Nos pépites du moment”.

Mais EasyLife garde un `type_code` interne pour comprendre le comportement.

Exemples :

- `DISH_OF_DAY` ;
- `DESSERT_OF_DAY` ;
- `COCKTAIL_OF_MOMENT` ;
- `MENU_OF_DAY` ;
- `SIGNATURE` ;
- `FAVORITE` ;
- `NEW` ;
- `CUSTOM`.

---

## 8. ProductHighlightGroup

Un `ProductHighlightGroup` est une section de mise en avant.

Il peut être rattaché à :

- une place ;
- un shop ;
- un menu ;
- une catégorie de produits.

Exemples :

### Plat du jour

- title : Plat du jour ;
- type_code : DISH_OF_DAY ;
- max_items : 1 ;
- visible sur menu : oui ;
- visible sur PlaceLiveResume : oui.

### Cocktails du moment

- title : Cocktails du moment ;
- type_code : COCKTAIL_OF_MOMENT ;
- max_items : null ou configurable ;
- visible sur menu : oui ;
- visible sur PlaceLiveResume : oui.

### Nos signatures

- title : Nos signatures ;
- type_code : SIGNATURE ;
- max_items : null ;
- visible sur menu : oui ;
- visible sur PlaceLiveResume : éventuellement non.

---

## 9. ProductHighlightItem

Un `ProductHighlightItem` rattache un produit à un groupe de mise en avant.

Il peut avoir :

- un produit ;
- un ordre ;
- une période de validité ;
- des overrides de titre, description ou image.

Exemple :

Groupe : Cocktails du moment

- Mojito fraise ;
- Spritz passion ;
- Gin basilic.

Exemple :

Groupe : Plat du jour

- Poulet basquaise.

Avec `max_items = 1`, le BO doit empêcher plusieurs produits actifs simultanément.

---

## 10. Best-sellers

`Best-seller` ne doit pas être un highlight manuel.

Quand les commandes seront activées, EasyLife pourra calculer automatiquement :

- produits les plus vendus ;
- produits les plus commandés ;
- produits les plus consultés ;
- produits les plus ajoutés au panier ;
- produits les plus commandés par période.

Donc ne pas créer :

- `BEST_SELLER` manuel ;
- case à cocher “best-seller”.

Best-seller sera une vue calculée plus tard.

---

## 11. PlaceLiveResume

Le composant `PlaceLiveResume` ne doit pas afficher tous les objets.

Il doit afficher ce qui est pertinent maintenant ou bientôt.

Il peut remonter :

- happy hour en cours ;
- happy hour dans X heures ;
- formule déjeuner active ;
- brunch ce week-end ;
- plat du jour ;
- cocktail du moment ;
- événement ce soir ;
- offre active ;
- produit mis en avant ;
- menu actuellement disponible.

Exemple à midi :

- Formule déjeuner active ;
- Plat du jour ;
- Dessert du jour ;
- Offre EasyLife active.

Exemple à 18h :

- Happy hour dans 30 minutes ;
- Cocktails du moment ;
- DJ set ce soir.

Exemple dimanche :

- Brunch disponible ;
- Escapade / événement lié au lieu ;
- Menu brunch actif.

Objectif :

> montrer rapidement ce qui rend le lieu intéressant maintenant.

---

## 12. Règles d’affichage du menu digital

Le menu digital doit afficher :

1. les menus actifs ;
2. les catégories du menu ;
3. les sous-catégories ;
4. les produits simples ;
5. les produits composés ;
6. les groupes de mise en avant actifs ;
7. les produits disponibles selon l’heure et le jour.

Il doit masquer :

- les produits inactifs ;
- les produits indisponibles ;
- les catégories vides ;
- les menus indisponibles ;
- les highlights inactifs ou expirés.

---

## 13. Règle d’or

Ne pas créer des objets spécifiques à chaque cas.

Ne pas créer :

- `PlatDuJour` ;
- `CocktailDuMoment` ;
- `FormuleMidi` ;
- `HappyHourProduct` ;
- `MenuSoirSpecial` ;
- `BestSellerManual`.

Créer des mécanismes génériques :

- `Product` ;
- `ProductCategory` ;
- `ProductMenu` ;
- `ProductMenuCategory` ;
- `AvailabilityRule` ;
- `ProductHighlightGroup` ;
- `ProductHighlightItem` ;
- `Offer` / `SpecialCampaign`.

Chaque cas métier est une composition de ces briques.
