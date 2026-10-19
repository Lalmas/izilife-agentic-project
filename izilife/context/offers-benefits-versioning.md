# Versionnement des Offers et des récompenses

## Décision métier

Une version d'Offer, de BPR ou d'Effect reste modifiable tant qu'aucune trace métier ne la référence.

Dès la première utilisation, cette version devient immuable. Une utilisation est établie par au moins une ligne liée dans l'une des sources suivantes :

- `BenefitLedger` ;
- `BenefitGrant` ;
- `OfferPurchase` ;
- `Booking`.

La publication seule ne verrouille pas la version. Une version publiée mais jamais utilisée peut donc encore être corrigée.

## Éléments figés

Le verrou porte sur l'ensemble de la définition qui a déterminé l'avantage présenté ou appliqué :

- l'Offer et sa nature ;
- la BPR ;
- les Effects, leur titre court, leur mécanique et leur valeur ;
- les targets ;
- les contraintes d'utilisation ;
- la temporalité, le scope et les périodes de validité.

Une désactivation reste possible pour empêcher de nouvelles utilisations, mais elle ne réécrit jamais l'ancienne définition.

## Faire évoluer une offre

Exemple : une offre à 25 % a été utilisée pendant vingt mois et doit passer à 20 %.

1. Conserver la version V1 à 25 % et arrêter son éligibilité à la date de bascule.
2. Dupliquer V1 en V2.
3. Modifier V2 à 20 %, avec une date de début égale à la date de bascule.
4. Publier V2.
5. Le Front résout uniquement la version éligible à la date courante. Les historiques continuent à référencer V1.

Deux versions ne doivent pas être actives simultanément pour la même identité métier, le même scope et la même période, sauf règle de priorité explicitement prévue.

## Historique et snapshots

Les références vers les anciennes lignes sont conservées. Les événements transactionnels conservent également un snapshot de ce que l'utilisateur a réellement vu ou obtenu : titre, Effect, valeur, cible, contraintes et prix le cas échéant.

Le snapshot garantit la lecture historique même si des données périphériques évoluent. Il ne remplace pas l'immutabilité de la version métier : les deux protections sont complémentaires.

## Règle BO et PS

Avant toute mutation d'une Offer ou d'une récompense, le BO et le PS recherchent une trace dans les quatre sources d'historique. Si une trace existe, l'édition de la version est refusée et l'utilisateur doit créer une nouvelle version par duplication.

