# Catalogue, familles et références produit

## Règles de domaine

- `ProductCategory` organise les produits localement dans un Place ou un Shop.
- `ProductFamily` décrit la nature canonique du produit : Pizza, Cocktail, Cola, Smartphone, Robe, etc.
- Une famille n'est ni une activité du lieu, ni une catégorie de menu, ni une marque.
- Un `Product` local reste propriétaire de son prix, de sa disponibilité, de ses canaux, de ses options et de ses médias.
- L'activation globale du `Product` décide s'il est utilisable. Quand `ACTIVE_MULTI_CANALITY=true`, seules les méthodes `sur-place`, `a-emporter` et `livraison` ajoutent une restriction. `ONLINE` est une consultation, et un kiosque est un point de commande : aucun des deux n'est un `OrderMethod`.
- Une référence commune est également un `Product`, avec `is_reference = 1`. Elle ne doit jamais apparaître seule dans le Catalogue public.
- `reference_product_id` permet au produit local d'hériter des informations communes absentes localement.
- Une référence conditionnée correspond à une identité précise, éventuellement un GTIN : canette 33 cl et bouteille 1,5 L sont deux références différentes.
- Une quantité locale fixe reste sur le produit. Plusieurs contenances ou formats sélectionnables utilisent les groupes et valeurs d'options tarifés.
- Un pack commercial reste un produit composé. `ProductPackaging` n'est plus alimenté par les importateurs modernes.

## Administration

- Structure : dernier bloc de `021_Next_Improves.sql`.
- Données initiales : `022_ProductFamily_Data.sql`.
- Le fichier 022 est uniquement un jeu de données réexécutable (`INSERT ... ON DUPLICATE KEY UPDATE`) : aucune évolution de structure n'y est mélangée.
- BO : `/product/families` pour rechercher, ajouter, modifier, hiérarchiser, valider ou désactiver.
- BO : `/product/references` pour les produits de référence sans scope local.
- Partner Space : sélection d'une famille validée ; si elle manque, proposition d'un candidat `PENDING` pour validation BO.

## Imports

Les imports BO, Partner et l'agent Python utilisent le même contrat :

- `product_family_id` ou `primary_product_family_id` si l'identifiant est connu ;
- sinon `product_family_name` ou `family_name` ;
- à défaut, proposition issue de la catégorie ou du nom, créée en `PENDING` ;
- `option_groups` pour les formats multiples et leurs prix ;
- champs de quantité du `Product` pour un format unique ;
- aucune nouvelle écriture dans `ProductPackaging`.

## Front Office

- Un Catalogue charge au maximum 20 produits par catégorie, puis continue par Ajax.
- L'aperçu affiche des rails par catégorie ; les catégories sont de vrais panneaux, un seul est visible à la fois. `?overview_version=1` sélectionne les rails horizontaux (20 produits maximum) et `?overview_version=2` la grille courte de six produits. Les produits possédant un média sont prioritaires dans les aperçus.
- La navigation du Catalogue reprend le composant visuel des fiches Place/Shop (`nav-pills`, défilement horizontal, sticky pleine largeur). Elle recentre latéralement l'onglet choisi. En fin de catégorie, le prochain lot est chargé puis la catégorie suivante est activée après un défilement utilisateur.
- Les groupes `ProductHighlightGroup` publiés dans le Catalogue apparaissent avant les catégories sous « En ce moment ».
- Produit, Service et EAP utilisent des cartes illustrées et une modale riche.
- Une modale Produit affiche prix dynamique, description, options et composition, puis permet d'ouvrir la fiche Produit.
- Un Service possède une fiche publique de vente (média, prix, description, options et caractéristiques) ; un EAP reste intégré au Place/Shop et n'utilise pas de page autonome dans le parcours V1.
- Les parcours EAP Event et Experience ne sont pas remplacés par le Catalogue.
- La fiche Produit V1 reprend la structure iziLife des fiches Place/Shop : en-tête `bg_image`, résumé, navigation avec `Aperçu` actif par défaut, puis Composition, Photos et Avis selon les données. La maquette e-commerce à miniatures latérales est réservée à une V2 ultérieure.
- Le retour depuis une fiche Produit conserve l'URL et l'ancre de la catégorie du Catalogue d'origine.
- Les styles Catalogue sont centralisés dans `statics/css/catalogue.css` et ne sont pas déclarés dans les vues.

## Routage

Le projet utilise l'auto-routing CodeIgniter. Aucune route manuelle Catalogue n'est ajoutée.
