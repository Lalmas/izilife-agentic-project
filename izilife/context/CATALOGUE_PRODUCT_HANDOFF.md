# Passation totale — Catalogue, menus, Produit, Service, EAP et MDM

Dernière mise à jour : 16 septembre 2026.

## Règles absolues

- Ce projet n'est pas neuf : avant de créer une vue, du CSS ou du JS, chercher et réutiliser Place/Shop et `common_components`.
- Ne pas consulter les fichiers `.env`.
- Ne pas modifier les anciens SQL. Ajouter les évolutions dans les scripts séquentiels `Next_Improves`/022.
- Le worktree contient beaucoup d'autres changements : ne rien réinitialiser, supprimer ou reformater hors périmètre.
- Centraliser le CSS Catalogue dans `statics/css/catalogue.css`, sans feuille spéciale par fiche.
- Ne jamais déclarer terminé uniquement parce que les lints PHP passent : validation visuelle et fonctionnelle obligatoire.

## Modèle Produit/MDM validé

- Une offre locale est un `Product` rattaché à Shop/Place/Page.
- Une référence canonique utilise aussi `Product`, avec `is_reference=1`, sans scope local ; l'offre pointe vers elle via `reference_product_id`.
- La référence porte identité, média commun, GTIN et données héritables. Exemple : `Coca-Cola servi au verre`; A vend 35 cl, B 33 cl.
- Les produits conditionnés figés restent distincts : canette 33 cl, bouteille 50 cl, bouteille 1,5 L, avec GTIN propre.
- Le B2B/prix professionnel n'est pas prioritaire.
- `ProductFamily` décrit ce qu'est le produit : Pizza, Burger, Cocktail, Cola, Espresso…
- Ne pas confondre avec `ProductCategory`, qui range l'offre dans le menu local.
- L'ancienne `ProductNature` (Naturel/Transformé/Industriel/Cuisiné) n'est pas utile ici et pourra disparaître.
- Famille principale + familles secondaires possibles. L'import résout une famille ou propose un candidat `PENDING`.
- `KnowedMeal`/`KnowedDrink` restent temporairement des données de curation, pas le nouveau référentiel.

## Options et formats

Socle moderne : `ProductOptionGroupAssignment`, `ProductOptionAssignmentValue`, `ProductOptionValuePrice`.

- Plusieurs volumes/prix : options.
- Supplément facultatif : checkbox.
- Choix unique obligatoire : radio.
- Prix absolu ou supplément : recalcul immédiat.
- Format unique figé : champs du produit/référence.
- Pack/composition : produit composé.
- `ProductPackaging` est un ancien mécanisme incomplet d'import, pas le socle futur.
- Exemple vérifié : Jupiler, 25 cl = 3,50 EUR par défaut ; 50 cl = 6,00 EUR, prix absolus.
- La Burrata des captures n'a aucune option.

## Fiche Produit V1 attendue

V1 alimentaire = fiche objet iziLife comme Place/Shop, pas le template e-commerce Phoenix.

### Header

- Vue : `app/Views/products/components/show_product_bg_image.php`.
- Même rythme que `show_place_bg_image.php`/`show_shop_bg_image.php`.
- Galerie obligatoirement via `common_components/show_object_header_gallery.php` ; ne pas recréer un swiper.
- En haut : rappels synthétiques seulement — nom, type/familles, configuration/conditionnement, prix, propriétaire.
- La description n'est jamais dans le header.

### Navigation/Aperçu

- Vue : `app/Views/products/components/show_product_navigation_menu.php`.
- Onglets V1 : Aperçu, Composition si présente, Photos si plusieurs médias.
- Pas d'onglet Avis pour le moment.
- Dans Aperçu, `À propos` réutilise `common_components/services_and_characteristics/show_description.php` (titre, ligne, Voir plus/moins).
- Ensuite : options, ingrédients, allergènes, caractéristiques et autres détails disponibles.
- Produit composé : blocs de choix obligatoires/facultatifs avec radios/checkboxes et impact tarifaire.

### Avis futurs

- Ne pas créer un second moteur.
- Réutiliser plus tard le socle `Review` avec destination `PRODUCT` et présentation/notation produit adaptée.
- Ne pas brancher maintenant les retours d'expérience sur 10 des lieux/événements.

### V2 future

- Template acheté : `C:/Users/alcamara/Documents/agentic_Workspace/phoenix-v1.22.0/public/apps/e-commerce/landing/product-details.html`.
- Pour électronique/habits/retail : grande image + miniatures latérales sur ordinateur.
- Ne pas le mélanger avec la V1 alimentaire.

## Menu/Catalogue attendu

### Navigation catégories

- Copier le rendu `navigation_menu` Place/Shop : pleine largeur, sticky, scroll horizontal, jamais de libellé sur 2–3 lignes.
- Mobile : garder l'onglet actif visible/repositionné vers le début.
- Fin de catégorie : charger la suite, puis sélectionner la catégorie suivante et déplacer la barre.

### Aperçu

- Défaut actuel décidé : `overview_version=2`.
- Six cartes normales par catégorie, contiguës, typiquement deux lignes de trois desktop, médias en priorité.
- Lien `Voir tout` au format iziLife, comme les blocs/swipers existants.
- `overview_version=1` reste une variante de comparaison. Si conservée, elle doit étendre le vrai système `overflow_swipers` pour `PRODUCT`, pas imiter un swiper localement.
- Liste complète : 20 produits puis `Voir plus` Ajax (30 pourra être décidé ensuite).
- Retour fiche Produit : URL et ancre exactes du menu/catégorie via `return_url`.

### État à ne pas survendre

Les derniers changements ont mis la grille 6 cartes par défaut et forcé largeur viewport/nowrap sur la navigation. Les captures antérieures montraient toujours une barre sur plusieurs lignes et une seule grande carte : revalider impérativement dans le navigateur réel avant d'annoncer la correction.

## Modale Produit attendue

- Largeur normale, pas `modal-lg`; tout le modal scrollable.
- Fermeture sans backdrop bloqué.
- Nom vert iziLife, casse normale; prix vert gras.
- Description petite, sans titre `Description`, Voir plus/moins.
- Bouton œil `Voir le produit`, comme `Voir le commerce` du live resume.
- Image, composition, options, suppléments, formats et compteur quantité.
- Radio obligatoire/unique, checkbox facultative, recalcul immédiat du prix.
- Le JS/options existait déjà : ne pas jeter ni dupliquer.

## Services et EAP/tarifs

- Service : carte + modale + page publique unique, style fiche iziLife; mêmes options/attributs, pas une page par type.
- EAP/tickets/tarifs : pas de page autonome en V1; intégrés dans l'onglet Tarifs/Menu/Catalogue du Place/Shop.
- Cartes avec image ou placeholder équipement; clic vers modale proche Produit.
- Conserver prix, description, conditions, validité, limites, prix groupes et contenu packs.
- Préparer sans activer de futures pages dédiées aux gros tickets.
- Event/Experience restent intacts. Centraliser le fond EAP sans casser leur affichage distinct.

## BO, Partner et imports

### BO

- `/product/families` et `/product/references` existent.
- Menu BO : section `MDM produits`, liens Familles/Références; liens croisés entre les deux écrans.
- Familles : recherche, hiérarchie, domaine, validation, activation, création/modification. Fusion/médias/ingrédients/allergènes plus tard.
- Références : Product sans scope, famille, parent, description, GTIN, statut.
- Formulaires Produit BO : famille et référence canonique.

### Partner

- Formulaires Produit : famille et référence; proposition de famille créée en `PENDING`.
- Canaux limités à `ON_SITE`, `TAKEAWAY`, `DELIVERY`.
- Ne pas maintenir une copie libre du scraper BO global. L'import partenaire doit utiliser un service contrôlé limité à ses objets.

### Import

- Faire converger import manuel BO et agent vers le même normaliseur final.
- Mettre à jour ou supprimer les anciens boutons/écrans qui alimentent l'ancien format.
- Le scraper BO résout/crée déjà `ProductFamily` en `PENDING`.
- Vérifier la parité Partner et `C:/Users/alcamara/Documents/agentic_Workspace/scripts/izilife` avant de déclarer le pipeline terminé.

## SQL

- Structure : fin de `C:/xampp/htdocs/izilife-admin/statics/izilife_new_version/021_Next_Improves.sql`.
- Inserts familles : `C:/xampp/htdocs/izilife-admin/statics/izilife_new_version/022_ProductFamily_Data.sql`.
- Le 022 doit devenir très complet : alimentation, boissons, retail, électronique, vêtements, etc., sans mélanger familles canoniques et catégories locales.

## Fichiers clés

### FO

- `app/Controllers/Product.php`
- `app/Libraries/Catalogue/CatalogueResolver.php`
- `app/Views/products/components/show_product_bg_image.php`
- `app/Views/products/components/show_product_navigation_menu.php`
- `app/Views/catalogue/product_page.php`
- `app/Views/catalogue/browse.php`
- `app/Views/catalogue/_product_card.php`
- `app/Views/catalogue/_product_modal_only.php`
- `app/Views/catalogue/_option_selector.php`
- `app/Views/catalogue/option_price_script.php`
- `app/Views/catalogue/product_modal_content.php`
- `app/Views/catalogue/product_preview_modal.php`
- `app/Views/catalogue/product_modal_loader.php`
- cartes/modales Service et EAP dans `app/Views/catalogue/`
- `statics/css/catalogue.css`
- layouts publics chargeant ce CSS.

### BO/Partner

- `C:/xampp/htdocs/izilife-admin/app/Controllers/Product.php`
- `C:/xampp/htdocs/izilife-admin/app/Controllers/Scraper.php`
- `C:/xampp/htdocs/izilife-admin/app/Views/products/families.php`
- `C:/xampp/htdocs/izilife-admin/app/Views/products/references.php`
- `C:/xampp/htdocs/izilife-admin/app/Views/layouts/content.php`
- `C:/xampp/htdocs/izilife-partner-admin/app/Controllers/Product.php`
- modèles/formulaires Produit BO et Partner associés.

## État réel

### Réalisé/amorcé

- ProductFamily/références, écrans BO et menu MDM.
- Champs famille/référence BO/Partner.
- Héritage FO d'une référence et exclusion des références du Catalogue.
- Résolution FO des options modernes.
- Pagination Ajax et retour contextuel.
- Cartes/modales Produit, Service et EAP amorcées.
- CSS Catalogue centralisé.
- Fiche Produit découpée en `bg_image` + navigation, swiper commun.
- À propos remis dans Aperçu via composant existant.
- Faux onglet Avis Produit retiré.

### À finir/valider

- Rendu exact de la fiche Produit après les derniers changements.
- Taille du swiper header avec un seul média.
- Navigation Menu pleine largeur/nowrap desktop et mobile.
- Six cartes réellement contiguës + Voir tout conforme.
- Vrai `overflow_swiper` PRODUCT si version 1 conservée.
- Modale options/composition/compteur/recalcul testée bout en bout.
- Scroll catégorie suivante et repositionnement mobile.
- Cartes/modales Service et EAP.
- Centralisation EAP/Event/Experience sans régression.
- Parité imports BO/Partner/Python.
- Tests FO/BO/Partner et documentation finale.

## Ordre de reprise recommandé

1. Lire ce brief et les composants Place/Shop, sans réinventer.
2. Ouvrir dans le navigateur réel Burrata + menu Soultrain Café.
3. Finir visuellement fiche Produit puis navigation/grille du Menu, desktop/mobile.
4. Tester une modale simple, Jupiler avec formats, puis un produit composé.
5. Tester retour catégorie + pagination Ajax.
6. Contrôler Service/EAP.
7. Auditer BO/Partner/imports, puis seulement annoncer la livraison.

## URLs de contrôle

- `https://localhost:4443/izilife/shop/menu/soultraincafe`
- `https://localhost:4443/izilife/product/page/shop/soultraincafe/43e555b1a7e4117a96ed53a854e9e943`
- `https://localhost:4443/izilife/shop/page/soultraincafe`
- Ajouter `?overview_version=2` pour la grille, `?overview_version=1` pour le rail.
