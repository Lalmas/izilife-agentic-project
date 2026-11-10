# Mission Event / Experience — récurrence et taxonomie

## Règles actives

- `activite-collective` n'est jamais une valeur de secours. Elle reste limitée à
  une véritable pratique collective réservable tant que cette ancienne notion
  existe.
- Une visite régulière est une `Experience`. Une mission VR nommée est un
  `Equipment`. Une soirée, un cocktail-spectacle ou un dîner-spectacle est un
  objet événementiel, éventuellement rattaché à une `EventSerie`.
- Un atelier, workshop, cours ou visite ne peut pas être matérialisé comme un
  `LocalEvent` continu entre deux dates éloignées. La source doit produire des
  occurrences distinctes, une récurrence à valider ou un reclassement
  `Experience`.
- `fête-et-musique` n'est pas une catégorie par défaut. Une catégorie précise
  est obligatoire lorsqu'elle est démontrée; sinon la fiche reste à valider.
- Stage, cours, atelier, workshop, salon et festival exigent une activité
  principale. Le sport, la danse et le style musical sont renseignés lorsqu'ils
  sont prouvés par la source.

## Référentiels transmis au premier appel

Les catalogues `Sport`, `Dance` et `MusicStyle` ont été étendus par migrations
idempotentes. Un sport doit toujours être rattaché à une `SportCategory`
existante ; une migration doit échouer explicitement si une contrainte ou une
catégorie manque, jamais être considérée comme réussie après un insert refusé.

La détection d'un mot dans le titre, la description ou le snapshot source ne
constitue qu'un candidat de réanalyse. Elle ne doit jamais affecter une
référence automatiquement : le contexte peut être trompeur (par exemple
« échecs » dans une phrase sans rapport avec le jeu). La valeur finale doit être
prouvée par la source et appartenir au catalogue BDD.

## Ville autoritaire d'un endpoint officiel

Un endpoint municipal officiel doit transmettre sa ville à EventTmp et à tout
ingesteur, même lorsque la fiche source omet ce champ. La ville est résolue dans
l'ordre suivant : ville du Place/Shop lié, `official_city_id`, puis correspondance
univoque du nom ou de l'URL de l'endpoint avec les villes autorisées du Hub.
La ville centrale du Hub n'est jamais appliquée aveuglément à un endpoint
ambigu. Une fois résolue, cette ville est autoritaire : ni le LLM, ni OpenAgenda,
ni le résolveur de lieu ne peuvent la remplacer par une ville ou un lieu hors
territoire.

## Heure de fin sans information publiée

Une fin explicite reste toujours prioritaire. À défaut de durée et de fin :

- début avant 16:00 : 18:00 ;
- début de 16:00 à 18:59 : 19:00 ;
- début à partir de 19:00 : 23:59 ;
- vraie soirée/bar/afterwork/karaoké/blind test/club : 02:00 le lendemain.

## Reprise ponctuelle du stock futur

Le rattrapage est un traitement ponctuel, audit-only par défaut, et non un agent
permanent. Il parcourt les `LocalEvent` actifs dont la fin est future et cible :

1. les catégories qui déclarent `need_principal_activity_category` ;
2. les titres/catégories contenant stage, cours, atelier, workshop, salon ou
   festival et dont l'APC est absente ;
3. les événements de musique/danse/sport sans sous-référence alors que le texte
   source permet de la déterminer ;
4. les ateliers/workshops/visites/cours ayant un intervalle de plusieurs jours ;
5. les catégories génériques `fête-et-musique`.

Le traitement ponctuel existe dans `backfill_active_event_taxonomy.py`. Il doit
être étendu en un audit consolidé des événements futurs actifs, sans devenir un
daemon permanent. En plus de la taxonomie ci-dessus, il doit couvrir :

6. les doublons sémantiques (même jour et même lieu, titre normalisé/fuzzy,
   même si les horaires ou le suffixe du titre divergent) ;
7. les événements payants sans `access_link`, conservés en EventTmp avec le
   blocage `lien_billetterie_payant_manquant` ;
8. les événements déclarés gratuits sans preuve textuelle explicite, et les
   contradictions entre prix/fourchette/lien de réservation et gratuité ;
9. les liens d'accès sans tarif ni preuve de gratuité, conservés en EventTmp
   avec `tarification_a_verifier` ;
10. les `Representation` sans média : réutiliser d'abord l'image et les faits
    déjà conservés dans EventTmp/`raw_json`, sans nouvel appel LLM. Le script
    historique `transfer_representation_media.py` ne couvre que le transfert
    entre environnements et n'est donc pas ce rattrapage ;
11. la résolution des lieux qualifiés (`Nom de base - ville` ou `Nom de base -
    lieu parent`) lorsque le nom de base est exact et le résultat univoque.

Le même exécutable expose ces chantiers comme agents ponctuels nommés, sans
dupliquer leurs règles : `--quality-only --quality-focus duplicates`,
`representation-media`, `paid-without-link` ou `false-free`. Le focus `pricing`
reste un raccourci compatible qui exécute ensemble les deux audits tarifaires
et les tarifications inconnues. Sans `--quality-only`, le script couvre aussi
la taxonomie des événements futurs actifs. Aucun de ces parcours n'est un
daemon.

### Doublons : ponctuel contre pérenne

- Le parcours rétroactif de tous les événements futurs déjà publiés est un
  **agent ponctuel non pérenne**. Il produit des paires, leurs preuves et une
  décision de fusion/archivage ; il n'est pas exécuté en continu.
- Le validateur d'ingestion est le **verrou pérenne** : tout nouveau doublon
  probable reste dans EventTmp en validation manuelle et ne peut pas être
  validé automatiquement.
- Une paire certaine, sans conflit de prix, d'horaire, de gratuité ni de lien,
  peut être archivée logiquement par l'agent ponctuel avec l'option explicite
  d'application. La fiche conservée doit être la plus complète.
- En présence d'un conflit métier, l'agent ne choisit pas silencieusement : il
  fournit les deux liens BO nommés et exige une fusion/décision manuelle.
- Le lieu commun est établi par Equipment, Place ou Shop ; à défaut de liaison,
  la combinaison ville + adresse normalisée est utilisée. Cela couvre les
  doublons provenant d'un lieu textuel non encore résolu.

Les liens et prix ne dépendent jamais d'une liste de billetteries en dur. Une
preuve monétaire rend l'événement payant quel que soit le domaine. Un
`access_link` sans prix n'autorise pas à conclure « gratuit » ; inversement, la
gratuité exige une preuve source explicite (`gratuit`, `entrée libre`, etc.).
Toutes les preuves doivent rester dans EventTmp afin de pouvoir créer plus tard
les offres/prix sans rappeler le LLM.

Ordre de résolution : réutiliser d'abord le `scrapping_json`/snapshot EventTmp,
puis le texte source déjà conservé, et ne rappeler le LLM que si ces données ne
suffisent pas. Toute proposition est limitée aux catalogues BDD. Un résultat
ambigu reste en validation manuelle. Le mode d'application doit journaliser
avant/après et refuser toute modification de date, horaire, lieu ou contenu.

## Architecture ultérieure des sessions récurrentes

Le chantier n'est pas implémenté maintenant. Il introduira une configuration de
sessions et ses contenus pour les événements réellement récurrents (par exemple
deux cours par semaine), sans créer d'avance 104 `LocalEvent`. Les occurrences
matérialisées resteront réservées aux interactions/inscriptions nécessaires.
Les `EventSerie`, célébrations annuelles et représentations conservent leurs
`LocalEvent` liés : leur sémantique éditoriale n'est pas remplacée par cette
récurrence virtuelle.

