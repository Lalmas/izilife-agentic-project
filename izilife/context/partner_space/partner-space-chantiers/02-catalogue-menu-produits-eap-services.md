# BRIEF À COPIER — Catalogue, Menu digital, Produits, EAP et Services

Je lance le chantier **iziLife Catalogue / Menu digital / Produits / Accès / Services** sur les projets `izilife`, `izilife-admin` et `izilife-partner-admin`.

Le texte source « IziLife — Architecture Catalogue, Menus digitaux, Produits, Accès et Services » fait partie du contexte métier de cette conversation. Commence par le relire intégralement puis audite le code et le SQL existants avant de proposer ou modifier quoi que ce soit.

## Objectif

Construire le socle commercial générique qui permet à un Place ou Shop de présenter ce qu'il propose : menus/cartes, produits, accès/tickets et services. Le restaurant est un cas d'usage, pas l'architecture du moteur.

Le résultat doit fonctionner dans le FO et être administrable depuis le Partner Space dans le strict périmètre d'ownership du Partner. Le BO conserve l'administration globale et la validation des référentiels.

## Décisions non négociables

- `Catalogue` est le nom d'architecture du regroupement applicatif, pas nécessairement une table SQL.
- Dans l'interface publique, ce regroupement peut être présenté par un onglet **« Offres »** au sens « ce que propose le lieu » : Menus, Produits, Tarifs/Accès et Services.
- Cet onglet « Offres » n'est pas l'objet SQL/métier `Offer` des promotions et bons plans. Le code, les DTO et les routes doivent garder cette distinction explicite même si le wording public emploie « Offres ».
- Place et Shop restent deux objets legacy distincts, mais partagent les composants métier Catalogue lorsque leur comportement est identique.
- Le Catalogue est dynamique et multi-catégorie.
- Les sections vides ne sont pas affichées.
- S'il n'existe qu'un seul menu et rien d'autre, le lien peut ouvrir directement le menu digital.
- S'il n'existe que des services ou que des accès, ne pas imposer une page intermédiaire artificielle.
- `ElementMenu` est le conteneur officiel ; ne pas créer ProductMenu, ShopMenu ou PlaceMenu.
- `ProductCategory.parent_id` gère catégories et sous-catégories ; ne pas créer ProductSubCategory.
- `ElementMenuProductCategory` sélectionne et ordonne les catégories visibles dans un menu.
- Un produit peut exister hors menu.
- Le resolver évite les doublons entre produits déjà couverts par un menu et section Produits générale.
- `Product` reste l'objet produit, y compris pour les produits composés.
- Réutiliser après audit `ProductType`, `ComposedProductSlot`, `ComposedProductSlotItem` et les anciennes modales produit utiles.
- Un service reste un `ElementService`, jamais un Product artificiel.
- Les `PriceModel` et leurs codes existants sont des référentiels protégés et compatibles.
- Tout accès réellement vendable utilise `ElementAccessPrice`. Ne pas recréer `WITHOUT_ACCESS_PRICE` ou vendre depuis `basic_price`.
- La billetterie Event actuelle reste fonctionnelle. Ne pas la migrer brutalement vers le moteur générique pendant cette première phase.

## Partner Space

- Afficher et gérer produits, menus, catégories de menu, EAP et services appartenant au Partner et à ses objets.
- Respecter ownership, rôle, scope du lieu et capacités d'abonnement sur chaque endpoint.
- Supporter plusieurs lieux et la multi-catégorie.
- Reprendre le module média Partner/BO pour les images et couvertures.
- Les limites de nombre, publication ou fonctions avancées sont résolues par entitlements, pas par le nom du plan.
- Le menu digital est inclus dans le gratuit lorsqu'il est activable, mais le Partner décide de son affichage public.
- L'activabilité dépend de la présence d'une configuration exploitable : menus/catégories/produits/prix.

## Génération assistée depuis un fichier

Préparer un parcours permettant au Partner d'importer un PDF, une image ou un fichier de carte puis de générer une proposition structurée :

- `ElementMenu` ;
- catégories et sous-catégories ;
- produits ;
- descriptions ;
- prix ;
- variantes/compositions lorsque détectables ;
- correspondances de médias éventuelles.

La génération ne publie rien automatiquement. Elle produit un brouillon contrôlable, signale les incertitudes et impose une validation humaine avant activation.

## Expérience FO

- Navigation existante de la fiche conservée : header, sticky nav, contenu actif, modales.
- Menu digital léger, mobile first, sans répéter toute la grosse fiche Place/Shop.
- Navigation interne sticky/horizontale par catégories.
- Modal produit pour consultation rapide, variantes et composition.
- Page produit publique pour URL, partage, SEO, analytics et extensions futures.
- Dans la première ouverture, afficher les produits et leurs détails sans activer artificiellement la commande en ligne.
- Générer un lien et un QR code vers le bon contexte : Catalogue, menu précis, section service ou accès.

## EAP et services

- Préserver le moteur Event EAP en production.
- Construire et tester le générique d'abord pour Place, Shop, XP/Experience et Equipment selon les structures réellement présentes.
- Supporter à terme tickets unitaires, packs, cartes de crédits, pass, abonnement, adhésion, prix libre, minimum, stock, quantité, limite utilisateur et validité.
- Ne factoriser Event qu'après tests et stabilisation, sans régression.
- `ElementService` conserve ses modèles de prix : fixe, minute, kilomètre, page, item et autres codes existants.
- Les services doivent pouvoir être ensuite ciblés par le moteur de réservation ou une demande de devis, mais ce chantier ne doit pas dupliquer ces moteurs.

## Promotions `Offer` et tracking

- Une `Offer` promotionnelle peut cibler un menu, une catégorie, un Product, un EAP ou un ElementService sans en devenir le conteneur.
- Préparer le ciblage Happy Hour, étudiant, spécial, Last Minute et autres BPR existantes après audit.
- Tracker au minimum les vues Catalogue, menu, catégorie et produit, en cohérence avec l'analytics Gratuit/Pro.
- Préparer la preuve de présence ou de consommation par ticket validé, sans inventer ici un nouveau workflow de réservation.

## Phasage attendu

1. Audit SQL/code BO/FO/Partner et cartographie des structures existantes.
2. Contrat du `CatalogueResolver` et DTO d'affichage commun.
3. Catalogue Place/Shop en lecture FO.
4. Menu digital et navigation interne.
5. Gestion Partner des `ElementMenu` et catégories.
6. Produits simples/composés et adaptation des modales legacy.
7. EAP génériques hors migration Event.
8. ElementServices et PriceModel.
9. Import assisté de carte en brouillon.
10. QR code, tracking et branchements Offers.

## Hors périmètre initial

- commande et livraison complètes ;
- panier transactionnel final ;
- ProductStory avancée ;
- migration forcée de la billetterie Event ;
- commentaires/avis produit complets ;
- publication automatique d'un import IA/OCR.

## Livrables

- audit et schéma de flux ;
- contrats resolver/DTO ;
- plan SQL compatible ;
- écrans FO/BO/Partner concernés ;
- matrice ownership/capacités ;
- tests multi-lieux, multi-catégories et anti-IDOR ;
- tests de non-régression Event ;
- documentation des fonctions préparées mais désactivées.
