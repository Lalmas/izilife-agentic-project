# Catalogue Services et EAP — règle actuelle

État vérifié le 30 octobre 2026. Cette note décrit le rendu FO simple, avant ouverture du panier et de la réservation des Services.

## Trois portées à distinguer

- Un **EAP propre à un Service** porte directement `ElementAccessPrice.service_id` et garde son prix dans `ElementAccessPrice.price`. Il n'est pas simultanément propriétaire du Place/Shop/Partner parent. Il apparaît uniquement dans la modale de son Service.
- `LocationEAPUseForService(eap_id, service_id)` est réservée à la **diffusion descendante** : un EAP appartenant à un Place, Shop ou Partner supérieur peut donner accès à un ou plusieurs Services sans leur appartenir.
- Un **EAP du lieu ou du partenaire sans lien Service** conserve son rendu de tarif autonome.
- Un **EAP limité à une catégorie** conserve sa portée dans `LocationEAPUseForCategory`. Il reste distinct d'un EAP propre à un Service. Le futur affichage « Accessible grâce à XXXXX » sur un Service n'est pas encore décidé ni implémenté.

Le résolveur FO filtre les EAP liés à un Service dans sa liste des tarifs du lieu, et charge ces EAP dans le détail du Service. Le contrôle de présence accepte la casse renvoyée par MySQL Windows tout en utilisant le vrai nom `LocationEAPUseForService` dans les requêtes Linux.

`EapPrice` est une ancienne table de liaison : malgré son nom, elle ne contient aucun prix. Une ancienne liaison unique devient la propriété directe `ElementAccessPrice.service_id`. Seuls les EAP réellement partagés entre plusieurs Services sont migrés vers `LocationEAPUseForService`. Un prix différent selon le contexte reste porté par un EAP local distinct, éventuellement relié à un EAP modèle par `is_variant_of`. La table est déjà supprimée en local ; en production elle reste temporairement présente jusqu'au déploiement du FO/BO compatible, puis elle pourra être supprimée après contrôle.

La table de diffusion est many-to-many : un EAP supérieur peut être diffusé sur plusieurs Services lorsque son prix et ses règles sont strictement identiques. Les EAP propres à un Service n'utilisent pas cette table. Dès que le prix, la validité, la quantité ou les conditions changent, il faut créer une variante EAP distincte.

Dans le catalogue des Services, **une seule catégorie visible** ouvre directement sa grille : pas d'onglet Aperçu et pas de carrousel « Voir tout » qui répète cette même catégorie. Avec plusieurs catégories, la navigation Aperçu + catégories reste en place. Aucun équivalent de « service du moment » n'est implémenté actuellement ; si cette fonction apparaît, il faudra revoir cette condition avant de masquer l'aperçu.

## Prix et rendu

- `ElementService.price=NULL` : pas de prix direct. Ne jamais le présenter comme gratuit.
- `ElementService.price=0` : Service réellement gratuit.
- Prix positif : vente directe du Service, sans modifier le rendu historique.
- Si un Service a des EAP propres actifs, sa modale affiche son descriptif puis des cartes pleine largeur **nom, description et prix**. Le prix direct unique n'est pas affiché dans cette modale. Les compteurs et le bouton d'achat sont masqués pour ce cas. Il n'y a pas de calcul de panier dans cette version.
- Le pied de modale d'un Service est masqué dès le HTML initial pendant le chargement du détail : aucun compteur ne doit apparaître brièvement avant les cartes EAP. Une fois le détail chargé, le pied revient uniquement pour un Service sans EAP propre. L'en-tête des cartes est « Tarifs ».
- Les EAP génériques et les autres Services conservent leur rendu existant.

`ElementService.status=1` signifie brouillon ; le FO demande `status=2` (publié) et `is_active=1`. L'import agent peut enregistrer `price=NULL`, mais le formulaire BO actuel convertit encore un champ Prix vide en `0` : point à corriger avant de l'utiliser pour un Service sans prix direct. La modale FO évite désormais d'afficher `NULL` comme 0 €.

## Cryotera local et livraison

Fiche fictive locale `SHOP cryotera-test-local` (`izilife2`, shop ID 323) : 7 Services publiés et 22 EAP actifs portant chacun directement leur `service_id`. `LocationEAPUseForService` contient 0 ligne pour Cryotera, car il ne s'agit pas d'une diffusion. Les 5 Services avec EAP propres ont `price=NULL` ; « Suivi en nutrition » reste à `NULL` ; « Bilan personnalisé offert » reste à `0`.

Contrôle HTTP local : `/shop/offer/cryotera-test-local` affiche les Services sans section Tarifs ; la prévisualisation « Cryothérapie Corps Entier » répond 200 avec 7 cartes, dont 30 € et 42 €. Vérifications de syntaxe PHP effectuées sur les trois fichiers FO modifiés.
Le catalogue local `/shop/services/cryotera-test-local` a une seule catégorie et affiche directement les sept Services, sans onglet Aperçu ni lien « Voir tout ».
Contrôle de non-régression : `/shop/offer/climbuplillelesquin`, qui possède un EAP actif sans lien Service, répond 200 et conserve sa section Tarifs.

À livrer pour ce rendu : `izilife` (FO), notamment `app/Libraries/Catalogue/CatalogueResolver.php`, `app/Views/catalogue/service_modal_content.php`, `app/Views/catalogue/product_modal_loader.php` et `app/Views/catalogue/browse.php`. Vérifier le déploiement FO avant de juger le rendu public.

Les sept visuels publiés par Cryotera sur ses pages de prestations ont été autorisés par le responsable iziLife pour cet import. Le drapeau `rights_confirmed=false` du brouillon était une précaution ajoutée lors de la préparation, pas le constat d'un défaut de droits. Le paquet local porte maintenant `rights_confirmed=true`. Le mode `media-only` a rattaché sept médias aux sept Services de `SHOP cryotera-test-local` (IDs média locaux 2616 à 2622). Le visuel du bilan, trop grand pour la limite BO de 2 000 px, est envoyé sous forme d'une copie réduite fidèle de 1 920 × 1 280 px ; le fichier source reste conservé. Les 22 EAP liés ne créent pas de copies supplémentaires de ces visuels. Le catalogue local répond HTTP 200 après cet import.

## Production, contrôle du 30 octobre 2026

`SHOP cryotera-pole-de-cryotherapie-lille` contient exactement 7 Services et 22 EAP déjà créés. La correction ciblée du 30 octobre a mis les 7 Services à `status=2`, `is_active=1` et les cinq prix directs des Services à `NULL` ; le bilan offert reste à `0`. Les 22 EAP restent actifs. Leurs sept images de Service sont présentes : la route BO retourne « image déjà présente » avec les IDs média production 51563 à 51569.

**Liens vérifiés directement dans phpMyAdmin production le 30 octobre 2026** : les 22 EAP de ce Shop avaient chacun une unique ancienne liaison `EapPrice.target_type=ELEMENT_SERVICE` vers le Service attendu (IDs Service 48 à 52). La migration additive a renseigné directement les 22 `ElementAccessPrice.service_id`. Pour assurer la compatibilité avec le code encore déployé, les anciens propriétaires Shop et `EapPrice` restent provisoirement présents ; ils devront être retirés après livraison et contrôle du nouveau FO/BO. Les Services 48 à 54 ont tous `status=2`, `is_active=1` et `media_id` 51563 à 51569 ; leurs prix directs sont `NULL`, sauf le bilan offert à `0`.

Sources détaillées : `scripts/izilife/places/README_site_content_package.md` et `izilife-db/principal/021_Next_Improves.sql`.
