# Offers / BPR — suivi des corrections

## Terminé

- [x] Une BPR Plan utilise `PLAN_MAPPING`; le choix Pass / Prime est porté par les Effects.
- [x] Le titre court public appartient à l'Effect et est obligatoire, limité à 50 caractères.
- [x] Le titre de l'Offer et le titre interne de la BPR restent des repères métier et ne remplacent pas le titre public de l'Effect.
- [x] La création d'une Offer crée une BPR vide; les mécaniques sont ajoutées ensuite.
- [x] Les mécaniques sur facture n'affichent pas et n'ouvrent pas la page Produits et cibles.
- [x] En Front, une mécanique facture reste consultable comme avantage global mais n'affiche ni onglet ni bloc Produits.
- [x] Une cible `ALL` conserve le menu Front et applique la mécanique à tous les produits concernés. Seules les mécaniques sur facture n'affichent aucun catalogue.
- [x] Le PS peut consulter une BPR Plan mais ne peut pas la modifier.
- [x] Une Offer classique et une BPR Plan peuvent cibler le brunch via `application_context=special_brunch`; elles sont permanentes et n'ont pas de dates.
- [x] Chaque BPR Plan normale porte ses propres contraintes. Une BPR `special_brunch` ne saisit pas de contraintes concurrentes et suit les horaires du BCC spécial brunch.
- [x] Brunch n'est pas une `SpecialCampain` et n'est jamais proposé dans le sélecteur « Spéciale ».
- [x] Le Front charge les BPR et les Offers classiques dont le contexte est `special_brunch`.
- [x] Le bloc À propos de l'offre rassemble description, horaires/contraintes, information Brunch et un swiper unique de mini-cartes.
- [x] Le swiper réutilise les mini-cartes de `place_live_resume` et agrège les autres avantages iziLife et les offres du lieu, Brunch compris.
- [x] Les mini-cartes des pages Offer ouvrent le même modal d’action (`Voir l’offre`, connexion/abonnement, utilisation) que `place_live_resume`.
- [x] L'offre ou la BPR actuellement consultée est exclue du swiper.
- [x] Le bandeau des pages Offer/Plan/Brunch affiche le scope avec 📍 et le nom du scope complète aussi le titre HTML.
- [x] Le scope du bandeau utilise l'icône et la couleur verte iziLife; l'aperçu d'une mécanique ciblée propose un CTA `Voir le menu` au lieu de dupliquer les cartes produits.
- [x] Les libellés brunch distinguent `Avantage Brunch` (BPR Plan) et `Offre Brunch` (Offer classique avec contexte brunch).
- [x] Le libellé du sélecteur est `Abonnement iziLife`; sa largeur est limitée et il reste sur la même ligne que la catégorie dans Produits.
- [x] Le plan actif de l'utilisateur connecté est sélectionné par défaut; le paramètre `plan` garde la priorité pour la prévisualisation.
- [x] Les retours depuis Produits et cibles conservent `return_to`; la BPR du breadcrumb est un lien.
- [x] Les Offers/BPR utilisées sont immuables dans le BO et le PS; une évolution passe par une nouvelle version.
- [x] La politique d'historisation et de snapshot est documentée dans `offers-benefits-versioning.md`.
- [x] Les sous-titres Étudiant / Senior / Enfant / Lycéens indiquent `Proposé par le lieu`.
- [x] Les listes et pages publiques refusent une Offer en brouillon même si un ancien enregistrement porte encore `is_active=1`.
- [x] L'autocomplete Produit du BO possède une route POST explicite et transmet le scope au moteur de recherche.

## Vérification

- [x] Analyse syntaxique PHP de tous les fichiers modifiés.
- [ ] Recette visuelle manuelle sur le localhost HTTPS (le navigateur automatisé refuse le certificat local auto-signé).
