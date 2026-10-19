# Brief de reprise — Offres, BPR, Brunch et cartes d'avantages

## À lire en premier

La documentation de référence de ce chantier se trouve dans :

`C:\Users\alcamara\Documents\agentic_Workspace\izilife\context`

Le chantier est transverse sur trois dépôts :

- BO : `C:\xampp\htdocs\izilife-admin`
- FO : `C:\xampp\htdocs\izilife`
- Partner Admin : `C:\xampp\htdocs\izilife-partner-admin`

Avant toute modification, relire en priorité `benefit-card-inventory.md`, puis les documents `offers-benefits-*` et ce brief. Le worktree est très chargé : ne pas écraser, réinitialiser ou reformater les changements existants.

## Règles techniques impératives

- Indentation : **4 espaces**.
- Ne jamais utiliser l'auto-routing. Toute route doit être déclarée explicitement.
- Ne créer aucune migration PHP.
- Toute évolution SQL est ajoutée **à la fin**, dans l'ordre d'exécution, de `C:\xampp\htdocs\izilife-admin\statics\izilife_new_version\021_Next_Improves.sql`.
- Le staging et la production sont mis à jour progressivement : les instructions SQL sont séquentielles et on ne revient pas en arrière.
- Lorsqu'une clé métier est renommée, scanner les trois dépôts et prévoir la conversion SQL séquentielle des données existantes. La promo lycéens utilise désormais la clé `promo-lyceens` et l'icône 🎒.
- Vérifier les trois surfaces FO/BO/Partner Admin lorsqu'un contrat, une cible, un scope ou un contenu partagé change.

## Modèle métier retenu

### Brunch

- Brunch est un `application_context` (`special_brunch`), pas une campagne spéciale générique.
- Un brunch possède son propre `BrunchInfo`, son `BookingConfigurationContent`, ses horaires et son `ElementMenu`.
- Le titre public doit venir d'un champ explicite de `BrunchInfo`, jamais d'une déduction fragile faite depuis le nom de la configuration de réservation.
- La page Brunch conserve toujours son véritable menu et ses produits, y compris lorsqu'un avantage « sur facture » s'applique.
- Les contraintes horaires d'une BPR Plan appliquée au brunch viennent du contexte Brunch. Les autres BPR Plan gardent leurs propres contraintes.
- Le bouton **Réserver** existe sur Brunch et Happy Hour mais reste grisé tant que leur condition d'activation dédiée n'est pas implémentée.

### Classement des cartes

- BPR Plan + `special_brunch` : **Avantages iziLife**, carte « Avantage Brunch ».
- Offer Brunch publique, cible `all` : **Offres du lieu**, carte « Offre Brunch ».
- Offer Brunch réservée à `izilife-subscribers` : **Avantages iziLife**, même si sa source technique reste une Offer du lieu.
- Une Offer publique du lieu reste dans **Offres du lieu**.
- Le Brunch est une temporalité visuelle autonome : il ne doit jamais être fusionné dans la carte permanente ni anniversaire.
- Sur la page Brunch, les offres associées apparaissent dans **Offres valables sur ce brunch**.
- Dans les vues générales, le titre de section reste **Autres offres et avantages** ; ne pas fusionner toutes les temporalités dans une seule grande carte.

### Cibles catalogue et mécanique facture

- Une cible produit ou catégorie conserve le comportement historique des produits concernés.
- La page catalogue sait gérer les familles **Produits**, **Services** et **Tickets** via les pills ; toute nouvelle logique doit rester indépendante de la famille.
- `ALL` conserve le catalogue/menu correspondant.
- Pour une mécanique de pourcentage ou montant sur facture appliquée à `ALL`, ne pas fabriquer artificiellement une liste de produits remisés.
- Cette exception ne fait pas disparaître le bloc catalogue : le bloc reste présent avec un libellé et un bouton adaptés à la famille (produits, services, tickets, menu, etc.).
- L'onglet détaillé peut être absent dans cette exception, mais pas le bloc d'accès.
- Sur Brunch, cette exception ne remplace jamais l'`ElementMenu` du brunch.

### CTA et modales

- Les cartes et swipers ouvrent la modale d'action ; un clic ne doit pas seulement recharger la page.
- Une Offer du lieu affiche **Voir l'offre**, jamais **Utiliser**.
- Une BPR Plan peut afficher l'action liée à l'abonnement selon son mode de délivrance.
- Le scope doit être visible dans le header avec le pin vert iziLife et apparaître dans le titre HTML.
- Une carte Brunch doit permettre de retrouver le brunch concerné, y compris depuis son titre ou son lien contextuel.

## Système visuel des cartes

Décision d'architecture : chaque type possède une **couleur canonique unique et connue** et une icône canonique. Mini-carte, grande carte, carte liste et autres rendus doivent consommer la même définition sémantique. Les fonds clairs et badges sont des nuances dérivées de la couleur canonique, pas des palettes indépendantes.

État actuel : les thèmes sont encore dupliqués dans plusieurs vues, ce qui explique les divergences mini/grand format. C'est la dette prioritaire de la prochaine conversation : créer un registre unique des thèmes et faire consommer ce registre par tous les rendus. Un futur modal **En savoir plus** pourra expliquer la temporalité et ses règles, mais ne fait pas partie du correctif actuel.

Identités importantes déjà décidées :

- Brunch : orange canonique `#E67700`, icône 🥞.
- Offre classique du lieu : vert canonique `#2E8B57`, icône 🏷️.
- Promo lycéens : teal canonique `#0F766E`, icône 🎒, clé `promo-lyceens`.
- Happy Hour : vert `#16A66A`, icône 🍹.
- Promo étudiante : bleu `#2563EB` en grand format, icône 🎓.
- Promo senior : violet `#7C3AED`, icône 👵.
- Promo enfant : vert `#059669`, icône 🧒.

Après le dernier correctif, aucune couleur canonique exacte ne se chevauche entre Brunch, offre classique et Promo lycéens. L'inventaire exhaustif et les nuances actuelles sont dans `benefit-card-inventory.md`.

## Changements déjà réalisés dans ce chantier

- Correction de l'erreur FO `Undefined variable $selectedPlanRule` dans les vues d'offre.
- Distinction de Brunch comme `application_context` classique, pas comme special campaign.
- Ajout du titre explicite `BrunchInfo.title` dans le BO/FO et ajout SQL dans `021_Next_Improves.sql`.
- Rattachement du brunch à son `ElementMenu` et maintien du menu réel sur la page Brunch.
- Ajout des swipers/cartes d'offres applicables au brunch et de leurs modales.
- Classement des Offer Brunch abonnées du côté **Avantages iziLife**.
- Séparation des Offer Brunch publiques dans **Offres du lieu**.
- Ajout du scope (pin, nom du lieu) aux pages d'offres et enrichissement des titres.
- Mise en place des variantes de cartes Brunch avec 🥞.
- Renommage complet de Promo ado en **Promo lycéens**, clé `promo-lyceens`, icône 🎒, avec conversion SQL des données existantes.
- Ajout du public cible **Lycéens** dans `PromotionTarget` avec la clé `lyceens`, actif et distinct de la campagne `promo-lyceens`.
- La cible **Étudiants** (`etudiant`) reste active ; seules les anciennes cibles `membre` et `fidele` sont désactivées.
- Correction de la collision exacte entre la mini-carte Brunch et la mini-carte générique d'offre du lieu.

## Points à vérifier ou reprendre en priorité

1. Centraliser réellement le registre type → couleur canonique → nuances → icône et supprimer les tables de styles dupliquées.
2. Tester toutes les variantes sur mini-cartes, grandes cartes, listes, recherche et modales : permanent, cadeau, anniversaire, famille, brunch, happy hour, étudiant, senior, enfant, lycéens, offre classique et opération.
3. Vérifier la recherche de targets BO pour produits, catégories, services et tickets, ainsi que la persistance du scope jusqu'au clic explicite sur **Effacer**.
4. Vérifier le endpoint AJAX de recherche de scope : un screenshot montrait des POST 404 sur `ajaxSearchScopes`.
5. Corriger proprement l'accès BO à `ElementMenu` : un screenshot montrait `RuntimeException: Authentification employé requise` dans `ElementMenu::guard()`. Aligner le comportement de session/redirect sur les autres contrôleurs BO sans ouvrir la route publiquement.
6. Valider les modales depuis tous les swipers : bouton **Voir l'offre** pour les Offers du lieu, actions Plan pour les BPR.
7. Valider l'affichage catalogue multi-famille avec pills quand une même BPR cible Produits, Services et Tickets.
8. Tester Brunch Soultrain et La Luck séparément : titre, horaires, menu, produits, offres applicables, lien de retour et bouton Réserver grisé.
9. Vérifier qu'une mécanique facture `ALL` garde le bloc catalogue adapté sans inventer une remise produit et sans masquer le menu Brunch.
10. Vérifier les contraintes : Brunch utilise les horaires Brunch ; les autres BPR Plan ne doivent pas hériter par erreur de contraintes partagées de scope.

## Fichiers FO au cœur du rendu actuel

- `app/Helpers/live_resume_helper.php`
- `app/Models/CampainsAndOffers/Offer_model.php`
- `app/Views/common_components/advantages/show_search_advantage_swiper.php`
- `app/Views/common_components/advantages/_advantage_card_plan_based.php`
- `app/Views/common_components/advantages/_advantage_card_offer_list.php`
- `app/Views/common_components/advantages/_advantage_card_simple.php`
- `app/Views/offers/offer_overview.php`
- `app/Views/common_components/show_brunch_info_modal.php`

## Méthode de reprise conseillée

1. Lire les docs et inspecter les trois dépôts avant d'éditer.
2. Établir une matrice source × éligibilité × temporalité × famille catalogue × rendu.
3. Centraliser les thèmes avant toute nouvelle retouche visuelle.
4. Tester un cas représentatif de chaque branche métier, sans extrapoler une règle facture au Brunch ou aux targets catégorie.
5. Linter chaque PHP modifié avec `C:\xampp\php\php.exe -l`.
6. Ne déclarer le travail terminé qu'après vérification FO et BO sur les URLs réellement utilisées.
