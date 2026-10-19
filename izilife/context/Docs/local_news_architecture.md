# Actualités locales et contenus permanents

## Objectif

Le système ne cherche pas à reproduire Google News. Il sert à présenter des informations locales utiles : alertes opérationnelles, transports, travaux, changements à venir, informations de lieux et publications de médias locaux.

Le flag public reste contrôlé côté front :

```dotenv
PUBLIC_LOCAL_NEWS_ENABLED=false
```

Le flag doit rester à `false` tant que les ALTER placés en fin de `izilife-admin/statics/izilife_new_version/021_Next_Improves.sql` n'ont pas été exécutés.

## Deux volets éditoriaux, un rendu unifié dans le bon bloc

### ElementNewsPost

`ElementNewsPost` est le moteur éditorial central et gère 3 volets métier :

- `NEWS` : actualités classiques
- `ALERT` : alertes opérationnelles (court terme)
- contenus structurants (informations durables pour les fiches)

Le formulaire BO a été pensé pour gérer ces 3 voies sans mélange :

- Actualités : `SINGLE_MEDIA`, `MEDIA_CAROUSEL`, `MEDIA_STORY`, `ARTICLE`
- Alertes : `ALERT` + `alert_type` dédié
- Contenus structurants : `EVENT_MAP`, `FAQ`, `HISTORY`, `PRACTICAL_INFO`, `HOW_TO_COME`, `WHERE_TO_PARK`, `SURVIVAL_KIT`, `PROGRAM_INFO`, `EDITORIAL_SECTION`

`scope_level` indique le propriétaire principal du contenu.
Un lieu a ses contenus propres, une AC/édition conserve ses contenus propres, et la page d’enfant peut récupérer l’héritage depuis le parent.

### ALERT (troisième voix)

Quand `post_type = 'ALERT'`, la colonne `alert_type` doit être renseignée avec :

- `TRAVAUX`
- `SECURITE`
- `METEO_VIGILANCE`
- `TRANSPORT`

Comportement attendu :

- Les alertes restent distinctes visuellement et fonctionnellement des NEWS ;
- Elles sont affichées dans un bloc dédié ;
- Elles peuvent avoir une durée de validité adaptée (ex. `starts_at` / `ends_at` / `feed_until`) ;
- Idéalement elles restent territoriales (City / zone locale), selon le scope utilisé.

### Types structurants

Les types autres que `NEWS`/`ALERT` ne remontent jamais dans « Dernières actualités ».

| Type | Rendu et usage |
|---|---|
| `PRACTICAL_INFO` | Information pratique générique dans l'overview. |
| `FAQ` | Questions/réponses repliables, réservées à EventSerie et AnnualCelebration selon ton usage. |
| `HISTORY` | Histoire durable, réservée à EventSerie et AnnualCelebration. |
| `HOW_TO_COME` | Accès détaillé ou exceptionnel. |
| `WHERE_TO_PARK` | Compatibilité historique ; préférer `HOW_TO_COME` ou `PRACTICAL_INFO` pour les nouveaux contenus. |
| `SURVIVAL_KIT` | « À savoir avant de venir » pour les grands événements. |
| `PROGRAM_INFO` | Explication du programme, jamais le programme structuré lui-même. |
| `EDITORIAL_SECTION` | Bloc libre lorsqu'aucun type précis ne convient. |
| `EVENT_MAP` | Carte dédiée (plan / visualisation). |

Une modification urgente de programme est une `NEWS`. Une explication stable du fonctionnement du programme est un `PROGRAM_INFO`.

## Modes d'une NEWS

### SINGLE_MEDIA

Une image ou vidéo. Aucun faux carousel.

### MEDIA_CAROUSEL

De 2 à 8 médias ordonnés, navigation manuelle, swipe et points. Les textes déjà dessinés dans les images ne reçoivent aucune surimpression iziLife. Le premier média est la couverture du feed.

### MEDIA_STORY

De 2 à 8 médias verticaux présentés en mode story dédié, navigation manuelle possible et progression temporelle cohérente avec le rendu story.

### ARTICLE

Image de couverture, titre, résumé et contenu HTML long. URL publique auto-routée :

```text
elementNews/page/{ElementNewsPost.unique_id}
```

Le BO propose un mode Édition et un mode Aperçu pour le contenu HTML.  
La liste des balises autorisées reste contrôlée côté serveur.

## Cycle de vie et conservation

Une actualité périmée ne doit pas être supprimée immédiatement : ses réactions, sa source, son lien partagé et son historique doivent rester cohérents.

- `feed_until` retire seulement la publication des feeds ;
- `archived_at` retire également des sélections éditoriales courantes ;
- `is_active=0` bloque complètement son accès public ;
- `ends_at` reste une limite absolue de visibilité ;
- `alert_type` doit être renseigné si `post_type='ALERT'` et nul sinon.

Politique recommandée :

- alerte : sortie du feed dès sa date d'expiration ou dès résolution ;
- news courte : 30 à 90 jours dans le feed ;
- article ou carrousel utile : sortie du feed, mais lien direct conservé ;
- contenu permanent : aucune `feed_until` ;
- purge physique : uniquement lors d'un chantier de rétention séparé.

## Emplacements branchés

Le composant `element_news/scope_sections` est branché sur :

- City, AdministrativeDivision et Country ;
- Place et Shop ;
- Event, EventSerie et AnnualCelebration ;
- Experience ;
- Equipment localisable et Partner ;
- Page : les publications dont elle est le scope ou la source (`author_page_id`) apparaissent dans son onglet Feed.

Il affiche d'abord les contenus permanents dans des sections dédiées, puis un bloc « Dernières actualités ».

## Espace de gestion BO

Le menu `Contenus > News` ouvre `elementNews` sans passer forcément par une fiche.  
L'écran global liste toutes les publications et propose un sélecteur polymorphe (`City`, `AdministrativeDivision`, `Country`, `Page`, `Place`, `Shop`, `Equipment`, `Event`, `EventSerie`, `AnnualCelebration`, `Experience`, `Partner`).

Par objet, le BO distingue `ALERT` des `NEWS` classiques pour ne pas casser les formulaires existants.

## Procédure de test

1. Exécuter uniquement le lot SQL préparé en fin de `021_Next_Improves.sql` dans l'environnement de test.
2. Mettre `PUBLIC_LOCAL_NEWS_ENABLED=true` dans `izilife/.env`.
3. Depuis le BO, ouvrir « News et contenus ».
4. Créer une `NEWS`, choisir le mode et définir éventuellement une source de page.
5. Créer une `ALERT` avec `alert_type` et période de validité, vérifier l'affichage dédié.
6. Ajouter les médias depuis le gestionnaire commun.
7. Vérifier une fiche City / Place / Event : sections en place + bloc « Dernières actualités ».
8. Vérifier un `PROGRAM_INFO` ou `FAQ` : pas dans « Dernières actualités ».

## Sécurité de rendu

Les styles ajoutés sont limités aux chaînes `.izilife-local-news-*`, `.izilife-element-content-*` et `.izilife-news-viewer-*`. Aucun sélecteur générique `nav`, `navbar`, `modal`, `card`, `img` ou `carousel` n’est modifié globalement.
