# Recette V2 avant lancement

## Périmètre

- Tester les fonctionnalités existantes de bout en bout avant lancement.
- Pour chaque anomalie : reproduire, documenter, corriger, rejouer le scénario et les scénarios voisins.
- Contrôler le résultat dans l'interface, en base de données et dans les logs.
- La partie Vécu est exclue : elle a déjà été testée et validée en re7.
- Les documents de contexte peuvent être anciens. Le comportement réel doit être vérifié, puis la documentation correspondante mise à jour après validation.

## Méthode de travail actuelle

Pour chaque scénario : état initial connu, action réelle, contrôle de l'interface, contrôle BDD, contrôle des logs, résultat, puis remise en état si nécessaire.

- Le Product Owner réalise les parcours humains, notamment la souscription initiale et le paiement, puis valide l'UX, le rendu, la compréhension et la cohérence métier.
- Codex identifie les données techniques, modifie temporairement les dates et horaires en local, lance les commandes, appelle les routes pertinentes, vérifie les contraintes serveur, contrôle la BDD et les logs, puis remet les données dans l'état convenu.
- Une correction n'est jamais validée sans rejeu du scénario défaillant et des scénarios voisins.
- Les données de recette existantes sont réutilisées avant toute création de fixture.

## Inventaire QA local

- [x] Base locale `izilife2` accessible.
- [x] Un User existe dans la table `User`.
- [x] Des Partners et PartnerEmployees existent.
- [ ] Identifier et documenter précisément les deux Partners de recette.
- [ ] Identifier le User de recette existant.
- [ ] Créer par le parcours métier les Users supplémentaires destinés aux abonnements User mensuel et annuel.
- [ ] Documenter le rôle de chaque User, Partner, Place et Shop de recette.

## Partner Foundation et abonnement Pro

Actions réalisées par le Product Owner :

- [ ] Faire passer le Partner de recette mensuel en Pro par le parcours réel jusqu'au paiement.
- [ ] Faire passer le Partner de recette annuel en Pro par le parcours réel jusqu'au paiement.
- [ ] Valider humainement l'affichage des plans, du paiement et du retour dans Partner Admin.

Contrôles réalisés par Codex après création des abonnements :

- [ ] Capturer l'état initial des abonnements, transactions, périodes et droits.
- [ ] Modifier uniquement les dates de recette locales pour provoquer l'échéance mensuelle.
- [ ] Lancer la commande de renouvellement Partner et vérifier transaction, statut, nouvelle période, événements, droits et logs.
- [ ] Refaire le scénario pour l'abonnement annuel.
- [ ] Provoquer un échec de paiement avec le mécanisme Stripe de test prévu.
- [ ] Vérifier `past_due`, délai de grâce, droits conservés ou coupés et récupération.
- [ ] Remettre les dates et données temporaires dans l'état convenu.
- [ ] Vérifier passage Pro, désactivation, réactivation et changement de plan.
- [ ] Vérifier que les fonctionnalités affichées correspondent réellement au plan et aux FeaturePlan.
- [ ] Confirmer l'emplacement et l'exploitation de la commande `subscriptions:renew-partners` dans le BO central.

## Abonnements User

- [ ] Créer un User de recette avec abonnement mensuel par le parcours réel.
- [ ] Créer un User de recette avec abonnement annuel par le parcours réel.
- [ ] Capturer l'état initial des abonnements, moyens de paiement, transactions et droits.
- [ ] Changer les dates en local et rejouer `subscriptions:renew` pour le mensuel puis l'annuel.
- [ ] Vérifier succès, échec, absence de carte, reprise, nouvelle période et logs.
- [ ] Vérifier que les droits restent cohérents après chaque transition.

## Catalogue, Products, menus, EAP et Services

- [ ] Tester l'ajout de Products au Partner de recette.
- [ ] Tester les Products actifs et inactifs, prix et options.
- [ ] Ajouter et vérifier les EAP.
- [ ] Ajouter et vérifier les Services, notamment un cas coiffure ou autre service représentatif.
- [ ] Tester un objet mono-catégorie.
- [ ] Tester un objet multi-catégories sans menu existant.
- [ ] Créer plusieurs menus et y glisser Products et ProductCategories.
- [ ] Vérifier une ProductCategory présente dans plusieurs menus.
- [ ] Vérifier le rendu final du menu digital dans le FO.
- [ ] Contrôler chaque création et relation en BDD et dans les logs.

## Booking, BCC et réservations

- [ ] Configurer une BCC depuis un compte Partner.
- [ ] Vérifier en BDD la configuration, les contenus, jours, horaires, capacités, statuts et rattachements.
- [ ] Tester une réservation nominale User vers Partner puis acceptation et confirmation User.
- [ ] Tester groupes et communautés.
- [ ] Tester le cas multi-catégories identifié dans la checklist produit.
- [ ] Tester pause et reprise des réservations.
- [ ] Tester auto-acceptation et validation manuelle lorsqu'elles sont configurées.
- [ ] Tester capacité, conflit de créneau et permissions entre Partners.
- [ ] Modifier temporairement jours, horaires et capacités pour tester les frontières, puis restaurer les valeurs.
- [ ] Tester privatisation et demandes si les parcours sont exposés.

## Offers, opérations, Grant et Redemption

- [ ] Vérifier Happy Hour, brunch et promotion étudiante.
- [ ] Créer une Offer d'opération avec un seul Product.
- [ ] Créer une Offer avec une liste de Products.
- [ ] Créer une Offer couvrant une ou deux ProductCategories.
- [ ] Tester prix normal, prix réduit, quantité, période et limites d'achat.
- [ ] Réaliser le paiement sandbox par le parcours humain.
- [ ] Vérifier la création du Payment ou de la Transaction et du Grant.
- [ ] Réaliser un Redemption nominal.
- [ ] Tenter un Redemption avant la période, après la période, le mauvais jour et hors horaires.
- [ ] Modifier temporairement les contraintes horaires pour provoquer acceptation et refus, puis restaurer les horaires.
- [ ] Tester mauvais Target et double Redemption.
- [ ] Vérifier que chaque refus est appliqué côté serveur et tracé.
- [ ] Vérifier la règle de non-cumul entre l'Operation et le Benefit Pass sur le Target couvert.

## Match, Team et diffusion

- [ ] Vérifier Team, Page associée et Partner associé via la Page.
- [ ] Vérifier Competition, Edition/Season et Match.
- [ ] Ajouter et vérifier un stade ou Place de rencontre.
- [ ] Brancher un lieu sur une diffusion de Match.
- [ ] Vérifier la liste FO des lieux diffusant le Match.
- [ ] Ajouter et vérifier une BPR ou Offer promotionnelle liée au Match et au Partner.
- [ ] Vérifier les liens de codes promotionnels.
- [ ] Vérifier les liens de réservation, billetterie et Services.

## Autres contrôles de la checklist actuelle

- [ ] Tester les boutons IA réellement exposés, sans juger la qualité éditoriale humaine.
- [ ] Tester les différentes familles d'Offers exposées.
- [ ] Tester les écrans Partner Products déjà développés.
- [ ] Vérifier les éléments Agents déjà indiqués comme réalisés dans la checklist source sans les redévelopper.
- [ ] Mettre à jour les documents de contexte après validation de chaque domaine.

## Sécurité CSRF

État constaté le 10 septembre 2026 : plusieurs formulaires transmettent déjà un jeton CSRF, mais le filtre global est désactivé dans `izilife`, `izilife-admin` et `izilife-partner-admin`. La route front `payment/pay` n'est actuellement pas protégée par le filtre CSRF global.

- [ ] Recenser toutes les routes et méthodes POST des trois applications.
- [ ] Recenser les formulaires classiques et les appels AJAX associés.
- [ ] Identifier les exceptions légitimes, notamment les webhooks Stripe protégés par vérification de signature.
- [ ] Activer le filtre CSRF global en local dans les trois applications.
- [ ] Vérifier qu'une requête mutante sans jeton est refusée côté serveur.
- [ ] Vérifier qu'une requête avec un jeton valide est acceptée.
- [ ] Corriger tous les formulaires et appels AJAX qui reçoivent une erreur 403 après activation.
- [ ] Vérifier le renouvellement du jeton dans les réponses AJAX lorsque sa régénération est active.
- [ ] Rejouer les parcours de connexion, compte, paiement, abonnement User, abonnement Partner, Booking, Offer, Grant et Redemption.
- [ ] Vérifier les logs PHP, applicatifs et HTTP pendant les rejouements.
- [ ] Réaliser les mêmes contrôles nominaux en staging avant lancement.
- [ ] Mettre à jour la documentation sécurité et la checklist de lancement après validation.

Critère de clôture : toutes les mutations applicatives sont protégées par CSRF ou couvertes par une exception explicitement justifiée et protégée par un mécanisme serveur adapté. Les parcours nominaux fonctionnent sans erreur 403 inattendue.

## Accès staging

- [ ] Au moment du passage en staging, créer un accès SSH temporaire par clé publique dédiée.
- [ ] Limiter cet accès au staging, sans accès production ni privilèges inutiles.
- [ ] Révoquer la clé à la fin de la recette staging.

La préparation de cet accès est volontairement différée jusqu'au début des tests staging.

## Après la V2 — industrialisation QA

Cette section décrit la cible ultérieure. Elle ne doit pas retarder la recette actuelle.

- [ ] Définir une petite hiérarchie commune de scénarios Markdown par domaine.
- [ ] Décrire chaque workflow sous forme d'étapes reproductibles, avec état initial, actions, assertions BDD et logs attendus.
- [ ] Maintenir des fixtures permanentes et clairement identifiables pour chaque développeur.
- [ ] Rendre les fixtures réinitialisables et indépendantes des données réelles.
- [ ] Ajouter progressivement une commande `qa:prepare` ou équivalente.
- [ ] Transformer chaque bug métier important en test de non-régression versionné.
- [ ] Séparer tests unitaires, tests d'intégration avec vraie BDD de test et tests navigateur ciblés.
- [ ] Utiliser un navigateur automatisé uniquement pour les parcours graphiques essentiels.
- [ ] Utiliser Stripe sandbox et les services externes de test sans transactions ni messages coûteux inutiles.
- [ ] Produire des rapports d'exécution et fichiers de logs exploitables par domaine.
- [ ] Permettre à terme des commandes comme `qa:test partner`, `qa:test booking` et `qa:test offer` si leur utilité est confirmée.
- [ ] Définir le workflow développeur : développement, tests unitaires, recette automatisée du domaine, scénarios voisins, staging, puis validation humaine ciblée.
- [ ] Conserver la séparation : les tests automatisés prouvent la mécanique ; les tests humains prouvent l'expérience.
