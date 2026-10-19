# Feed ElementNewsPost

Le résumé d’actualités des fiches publiques utilise désormais un rail horizontal de publications et un bouton **Afficher tout** ouvrant le feed détaillé. Le composant est partagé par les Events, AnnualCelebrations, EventSeries, Places, Shops, Pages, Experiences et territoires qui chargent `element_news/scope_sections`.

## Règles de rendu

- `ARTICLE` peut exister sans média et ouvre une page longue dédiée.
- `SINGLE_MEDIA`, `MEDIA_CAROUSEL` et `MEDIA_STORY` sont des formats visuels : le BO doit leur imposer respectivement au moins un média, avec un maximum piloté par le format.
- Le résumé affiche au plus huit cartes et reste tactile grâce au défilement horizontal avec snap ; les flèches sont ajoutées sur les écrans larges.
- Le feed détaillé affiche l’identité de la source, la date, le média, le titre, le résumé et les réactions.
- Les réactions restent visibles hors connexion. Une tentative de réaction ouvre `connexionNeedModal` ; une personne connectée utilise `ContentReaction` avec le scope `element_news`.
- Les alertes sont chargées séparément et ne sont jamais injectées dans le feed News.

## Events récurrents

Une édition Event ne charge que ses propres News. Une News scopée sur une `AnnualCelebration` ou une `EventSerie` reste sur ce parent et ne descend jamais automatiquement dans une édition. Les contenus structurants suivent une autre règle : l’édition remplace le contenu parent lorsqu’elle possède le même type, sinon elle en hérite sans duplication physique.

La navigation Event expose conditionnellement les onglets `Actualités`, `Plan`, `Plus d’infos` et `FAQ`. Le résumé de l’Aperçu conduit à l’onglet Actualités, sans modal de feed. Celui-ci affiche les publications par ordre éditorial et chronologique, dix par dix. `EVENT_MAP` conserve son média ENP, apparaît également dans les actualités récentes et dispose d’une visionneuse avec zoom et déplacement.

Un contenu en mode `ARTICLE` ne propose une lecture dédiée qu’à partir de 600 caractères de contenu utile. En dessous de ce seuil, il reste une publication courte dans le feed et aucun lien « Lire l’article » n’est affiché. Les articles longs restent dans la structure de la fiche Event : en-tête, navigation et onglet Actualités demeurent visibles pendant la lecture.

Les contenus longs restent sur `elementNews/page/{unique_id}`. Les formats visuels s’ouvrent dans leur visionneuse et ne sont pas transformés en articles.
