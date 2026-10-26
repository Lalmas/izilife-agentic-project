# TODO — Restitution des contextes Spotlight et ActivityProposal

## État actuel

Les contextes sémantiques sont enregistrés en base. Ils ne doivent pas filtrer les candidats dans les parcours ordinaires : ils servent d'abord à expliquer quand une proposition est particulièrement adaptée.

Comportement attendu :

- Navigation Contextuelle « Spotlight » : tous les Spotlights classiques actifs restent candidats, sans filtrage par contexte sémantique ;
- « Idées date » : tous les `GOOD_FOR date` restent candidats, sans filtrage par jour, moment, météo ou saison ;
- `ActivityProposal` : la proposition reste candidate et son contexte est restitué par des indications visuelles, par exemple « parfait le week-end » ;
- le contexte pourra aussi servir à pondérer ou ordonner les résultats, sans les exclure.

## Filtrage strict réservé à un futur mode « maintenant »

Les `ActivityProposal` ne possèdent aucun interrupteur de filtrage contextuel : leur `context_json` est uniquement une information de présentation et, plus tard, éventuellement de classement.

Dans `C:\xampp\htdocs\izilife\app\Libraries\LocalQuery\ActivityEngineResolver.php`, l'option suivante concerne uniquement les raisons Spotlight `GOOD_FOR` et reste réservée à un futur appel explicitement instantané/contextuel :

```php
'good_for_context_filtering_enabled' => true,
```

Lorsqu'elle est explicitement activée, elle filtre seulement les raisons Spotlight `GOOD_FOR` utilisées par le moteur selon leur propre `context_json`.

Elle doit rester absente ou à `false` par défaut.

Ce n'est ni une variable globale ni un paramètre `.env`. C'est une option transmise au moteur par un parcours précis, dans le tableau `activity_engine` de la définition WTD concernée.

Exemple pour un futur mode « pertinent maintenant » sur « Idées date », dans `C:\xampp\htdocs\izilife\app\Controllers\Whattodo.php` :

```php
'activity_engine' => [
    'enabled' => true,
    'occasion' => 'date',
    'good_for_context_filtering_enabled' => true,
    // ...
],
```

La valeur est ensuite lue par `ActivityEngineResolver.php`. L'activation se ferait donc intention par intention dans `Whattodo.php`, jamais globalement. Actuellement, aucune définition ne transmet cette option.

Cette option ne filtre jamais les `ActivityProposal`. Elle concerne exclusivement les `GOOD_FOR`.

## Affichage des « Parfait pour » sur les fiches

Dans `C:\xampp\htdocs\izilife\app\Views\common_components\spotlights\show_spotlight_context.php`, conserver :

```php
$enableTargetContextFiltering = false;
```

Ne passer cette variable à `true` que dans un futur affichage explicitement intitulé « pertinent maintenant ». Sur une fiche ordinaire, tous les `GOOD_FOR` doivent rester visibles et leur contexte doit être présenté sous forme de libellés ou d'icônes.

Cet interrupteur local de vue est distinct de `good_for_context_filtering_enabled` : il agit seulement sur les libellés affichés dans une fiche, pas sur la liste des candidats renvoyée par le moteur WTD.

## Distinction des destinations du Spotlight manuel

- `spotlight` : Spotlight classique. Sa configuration globale (titre, description, thème, dates et mois) lui appartient.
- `perfect_for` : rend les raisons `GOOD_FOR` éligibles au WTD/LocalQuery. Chaque `GOOD_FOR` utilise son propre `context_json`.
- `home_today`, `home_future`, `home_both` : rails Home.

La destination `spotlight` classique n'active pas automatiquement `perfect_for`. Si un même Spotlight doit être à la fois classique et exploitable comme « Parfait pour », les deux destinations doivent être cochées.

## TODO de restitution FO

1. Créer un composant commun transformant `context_json` en badges/icônes compréhensibles : week-end, soirée, beau temps, novembre → février, etc.
2. L'utiliser sur les `GOOD_FOR` et les `ActivityProposal` sans retirer les candidats.
3. Prévoir ultérieurement un bonus de classement lorsque le contexte courant correspond.
4. Réserver le filtrage strict à une intention explicite de type « maintenant ».
5. Vérifier qu'un Spotlight uniquement classique ne devient pas éligible comme « Parfait pour ».
6. Vérifier le comportement sans `context_json` : l'élément reste compatible avec tous les contextes et n'affiche aucun badge contextuel.
