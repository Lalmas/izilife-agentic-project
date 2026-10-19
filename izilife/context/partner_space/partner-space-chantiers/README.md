# iziLife — Dossier de lancement des chantiers FO / BO / Partner Space

Ce dossier contient les briefs à copier intégralement dans de nouvelles conversations Codex appartenant au même projet iziLife.

## Ordre conseillé

1. `01-foundation-partner-space.md`
2. `05-wallet-credits.md`
3. `02-catalogue-menu-produits-eap-services.md`
4. `03-reservation-privatisation-demandes.md`
5. `04-offers-campagnes-placement-boost.md`

Les chantiers Wallet, Catalogue, Réservation et Campagnes peuvent être analysés en parallèle une fois les contrats du Foundation stabilisés. Leur ouverture publique reste pilotée par les capacités et l'abonnement.

## Autorité documentaire

Les deux textes fournis le 24 août 2026 restent des sources métier :

- « Architecture Catalogue, Menus digitaux, Produits, Accès et Services » ;
- « Décision d'architecture globale du moteur de réservation ».

Les briefs de ce dossier les mettent à jour avec les décisions prises ensuite. En cas de conflit, l'ordre d'autorité est :

1. demande explicite la plus récente d'Alassane ;
2. brief du chantier concerné dans ce dossier ;
3. textes d'architecture sources ;
4. comportement legacy du code.

Le code existant doit toujours être audité avant modification. Un brief décrit la direction voulue, pas la preuve que les tables, modèles ou workflows actuels sont corrects.

## Règles communes aux conversations

- Les projets `izilife`, `izilife-admin` et `izilife-partner-admin` forment un seul système et doivent être analysés ensemble.
- Ne pas copier mécaniquement le BO dans le Partner Space : le BO administre tout ; le Partner ne gère que son périmètre.
- Toute lecture ou mutation est contrôlée côté serveur par Partner, rôle, ownership, scope et capacité.
- Ne jamais considérer un identifiant de route ou de formulaire comme une autorisation.
- Respecter CodeIgniter 4, l'auto-routing et les objets legacy séparés `Place` / `Shop`.
- Réutiliser les helpers, modèles, tables et composants existants après audit ; ne pas créer une deuxième architecture concurrente.
- Préserver les fonctions déjà en production, particulièrement la billetterie Event.
- Toute modification SQL additive du chantier doit être regroupée dans le fichier SQL de continuation prévu par le projet.
- Ne pas activer publiquement une fonction incomplète : préparer le contrat et la placer derrière une capacité désactivée.
- Les termes Catalogue, Offer, Booking, Transaction, Demand/Quote et Payment désignent des concepts différents.
