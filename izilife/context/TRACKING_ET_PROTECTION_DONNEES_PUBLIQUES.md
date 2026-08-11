# Tracking et protection des donnees publiques

## Principes

L'accessibilite d'une page, son indexation, son utilisation par un LLM et son
comptage Analytics sont quatre sujets distincts.

- Une fiche publique reste accessible aux humains.
- Googlebot, Bingbot, DuckDuckBot et OAI-SearchBot peuvent parcourir les fiches
  publiques afin de produire de l'acquisition organique et des citations.
- GPTBot, CCBot et Bytespider sont refuses pour limiter l'entrainement et la
  collecte massive declares.
- Aucun robot, apercu social, client HTTP ou sonde de monitoring ne doit creer
  de UserUuid ou de user_events.
- Un humain arrivant depuis ChatGPT, Claude ou Perplexity reste un vrai
  visiteur et sa source doit etre conservee.

Le fichier robots.txt exprime une consigne aux robots cooperatifs. Il ne
constitue pas une protection de securite contre un scraper qui ment sur son
User-Agent.

## Protection applicative

Le filtre PublicTrafficProtection protege deux profils :

1. les pages de fiches Event, Experience, Place, Shop, Page, Circuit,
   AnnualCelebration et EventSerie ;
2. les surfaces d'extraction plus riches : recherche, WTD, carte,
   geolocalisation et pagination de la Home.

Le score combine IP, User-Agent, cookie anonyme ou cookie de session, nombre de
requetes par minute et nombre de chemins distincts par heure. Les seuils sans
cookie sont plus stricts. Un depassement produit HTTP 429 et une trace warning.
Les robots de collecte explicitement bloques recoivent HTTP 403. Aucun acces a
la session ou a la base n'est necessaire au filtre.

Cette couche augmente le cout d'un scraping simple. Elle ne suffit pas contre
un acteur distribue disposant de nombreuses IP, de navigateurs automatises et
de cookies. Une protection CDN/WAF, des limites par reseau et des challenges
progressifs pourront completer le dispositif.

## Tracking navigateur iziLife

Le collecteur ClientAnalytics utilise l'auto-routing FO historique. Aucune
route explicite n'est ajoutee. Les navigateurs envoient les evenements par lots
de 20 maximum, avec controle same-origin et limite de 60 appels par minute et
par IP.

Evenements pris en charge :

- scroll_depth aux seuils 25, 50, 75 et 90 pour cent ;
- block_impression lorsqu'au moins 50 pour cent du bloc ou du swiper devient
  visible ;
- load_more ;
- swiper_interaction uniquement pour un geste ou un bouton, jamais pour le
  defilement automatique ;
- content_click dans les blocs, cartes et swipers observes.

Les evenements sont agreges par DataTaker_lib::trackOnce() sur 24 heures afin
d'eviter une ligne SQL par mouvement. La fonction globale window.iziTrack()
permettra de raccorder les actions metier futures.

## Politique d'indexation recommandee

Les fiches publiques publiees restent indexables. Les brouillons, contenus
prives, programmes de communaute et fiches sans valeur publique doivent etre
proteges par authentification ou noindex selon leur nature. Bloquer tout le
crawl des fiches publiques ferait perdre l'essentiel du potentiel SEO local et
des arrivees depuis les moteurs de reponse.
