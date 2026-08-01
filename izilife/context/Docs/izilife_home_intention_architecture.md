# iziLife V2 - architecture globale Home, intentions et objets

## 1. Promesse produit

La home iziLife doit commencer a repondre sans effort a :

- Que faire ici maintenant, demain, cette semaine ou ce week-end ?
- Que faire seul, en couple, entre amis, avec des enfants ou comme touriste ?

La reponse depend du lieu, de l'heure, du jour, de la meteo, du calendrier, du profil, de la duree disponible, de la distance et du temps de trajet.

La valeur d'iziLife vient de l'assemblage automatique de contenus perennes et perissables : `Event`, `Place`, `Shop`, `Experience`, `Circuit`, `LocalHabit`, `LocalTip`, `EscapadeProposal`, `OutingIdea`, `Selection`, puis Meetz et les collections/guides.

## 2. Roles des objets

### IndependentAction

Une intention generique : se balader, boire un verre, voir un sunset, randonner, passer une journee au lac, prevoir une nuit insolite. Elle ouvre un WTD tant qu'aucun objet precis n'est selectionne.

### Objets concrets

- `Place` / `Shop` : un lieu reel et ses capacites.
- `Event` : une occurrence datee.
- `Experience` : une activite organisee, animee, planifiee ou reservable : visite guidee, atelier, cours, stage, degustation, croisiere, jeu de piste.
- `Circuit` : un parcours trace a suivre.

`Decouverte de lieu` et `Decouverte d'activite` ne doivent plus servir a reformuler artificiellement une fiche existante. Les anciennes donnees doivent etre auditees, pas supprimees aveuglement.

### Objets de composition

- `EscapadeProposal` : destination/proposition contextualisee qui vaut le deplacement.
- `OutingIdea` : composition libre A1 + A2 + A3.
- Collection/Guide : liste editoriale reutilisable.
- `Selection` : produit iziLife vendable : Moment, Pass, Parcours, Sortie cle en main, Nuit, Escapade.

### Connaissance et curation

- Equipment, ObjectOnPublicPlace, AccessType et prix decrivent les faits et modes d'acces.
- `LocalHabit` decrit une pratique locale collective.
- `LocalTip` dit : « moi, ici, je fais cela ainsi ». Un LocalTip iziLife constitue une curation incarnee.
- Les tags decrivent des capacites ou qualites structurelles.
- Spotlight indique une mise en avant editoriale actuelle, saisonniere ou territoriale. Sans date, il est permanent et doit rester exceptionnel.

Les flags `is_izilife_event`, `is_izilife_partnership_event`, `is_izilife_organizer_event` et `is_exclusive_on_izilife` sont des signaux distincts de Spotlight.

## 3. Regle fiche directe ou WTD

Une formulation qui cite un objet deja choisi ouvre toujours sa fiche et utilise son image :

- « Passer une nuit insolite dans les arbres chez Chlorofil » -> fiche Chlorofil ;
- « Passer la journee aux Pres du Hem » -> fiche des Pres du Hem ;
- « Voir le sunset depuis ce rooftop » -> fiche du rooftop ;
- « Faire cette randonnee sur les terrils » -> fiche Circuit.

Une formulation generique ouvre le WTD de l'intention et utilise l'image de l'IA :

- « Nuits insolites » -> WTD ;
- « Une journee dans une base de loisirs » -> WTD ;
- « Ou voir le coucher de soleil ? » -> WTD ;
- « Trouver une randonnee sur les terrils » -> WTD.

Le moteur de presentation peut reformuler un objet selectionne, mais ne cree pas un nouvel objet metier.

## 4. Home

La home a deux fonctions complementaires :

1. aider a decider vite avec les premiers rails contextuels ;
2. donner ensuite le pouls de la ville par un feed de blocs scorés.

Ce feed ne copie pas Instagram : il ne montre pas un post d'un compte a la fois. Il rassemble automatiquement les objets iziLife dans des blocs multi-objets. La serendipite vient des donnees locales et du contexte, sans obliger l'utilisateur a suivre tous les lieux, medias et influenceurs.

### A ne pas manquer

Campagnes/offres iziLife, editions locales d'AnnualCelebration, contenus explicitement structurants, vacances, ponts lorsqu'ils seront actives et roue iziLife lorsqu'elle sera activee.

### Des idees pour maintenant

IA faisables maintenant, plus `EVENT` Spotlight du jour et `EXPERIENCE` Spotlight proches. Les objets directs conservent leur renderer et ouvrent leur fiche.

### Dans les prochains jours

IA a preparer et PlanningOpportunity : plage, lac, parcs, escapades, hotel, nuits insolites, danse, randonnee, etc. Le WTD resout les objets concrets.

`CalendarSignal` est un contexte, jamais une sortie. `PlanningOpportunity` est une idee bientot actionnable. Leur affichage minimal existe dans `home_highlight_helper.php`; il doit encore etre finalise carte par carte.

### WTD Vacances et ponts

Vacances et ponts ouvrent une projection multi-objet, pas un simple agenda. Le WTD assemble : événements strictement compris dans la période, expériences adaptées, lieux de journée (plages, lacs, bases de loisirs, grands parcs, attractions), hébergements, circuits touristiques et destinations qualifiées par `EscapadeProposal`.

Le profil pondère les résultats : bases nautiques, activités enfants, zoos et grands parcs montent pour une famille ; les escapades, expériences, hébergements et événements restent disponibles pour couple, amis et solo. Un pont correspond uniquement à une vraie fenêtre de trois jours et étend davantage le rayon de planification.

La définition WTD expose aussi un contrat `idea_lanes` séparé des objets concrets. Il permettra d'ajouter ultérieurement en tête de page des swipers IndependentAction et PlanningOpportunity/CalendarSignal sans transformer ces idées en faux lieux ou fausses expériences.

### Feed de blocs apres les rails de decision

Objectif cible : disposer d'environ 30 a 40 blocs candidats par profil, scores et diversifies, puis rendre :

- 10 blocs au chargement initial ;
- 10 blocs supplementaires par `Charger plus` ;
- quelques blocs contextuels injectes pour casser la monotonie ;
- au maximum 2 ou 3 blocs lies aux comptes/lieux suivis.

Un bloc affiche plusieurs objets. L'analyse du feed Instagram a simplement permis d'identifier des exemples de blocs ou de contenus que la home iziLife peut faire remonter :

- events aujourd'hui, demain, cette semaine et ce week-end ;
- soirees, concerts, festivals, tournois et petits events locaux ;
- nouvelles ouvertures et nouvelles experiences ;
- lieux/experiences tendances via Spotlight ;
- events iziLife, exclusifs, organises ou partenaires ;
- objets sponsorises ;
- avantages et reductions abonnement iziLife ;
- promotions, concours et bons plans ;
- ElementNews des lieux : fermeture, privatisation, information ponctuelle ;
- produits mis en avant par les commerces lorsque la source sera prete ;
- escapades, hotels et gites particuliers ;
- LocalHabit et LocalTip ;
- Selections vendues par iziLife ;
- Meetz et rencontres ;
- contenus issus des suivis ;
- actions contextuelles injectees entre les blocs.

Le scoring doit combiner pertinence de profil, temps, meteo, territoire, fraicheur, qualite, curation, partenariat/sponsoring et diversite. Il ne doit pas introduire une nouvelle notion de famille : l'unite de planification et de rendu reste le bloc Home.

## 5. Meetz et rencontres

Intention principale : `Rencontrer de nouvelles personnes`.

Ordre de resolution :

1. opportunite immediate reelle -> carte specifique ;
2. prochain creneau qualifie -> carte specifique par activite ;
3. fonctionnalite active dans une ville a moins de 30 km -> carte generique ;
4. sinon aucune carte.

Les events meetzables sont des events capables d'accueillir des groupes Meetz. Les events speciaux Meetz iziLife reserves aux abonnes restent une categorie distincte. Un futur WTD Rencontres pourra melanger Meetz, J'y suis/J'y serai et disponibilite immediate.

La configuration Home est preparee mais desactivee tant que le resolveur territoire/creneau n'est pas branche.

## 6. Selections

Les Selections apparaissent dans les WTD compatibles avec le badge `Vendu par iziLife`. Un bloc Home commercial conditionnel `Les sorties iziLife` est prevu uniquement s'il existe des Selections actives et achetables. Il est configure mais pas encore rendu.

On doit pouvoir les affciher aussi directement en bloc ou dans les à faire maintenant.

## 7. Pipeline de requete cible

```text
question utilisateur
-> intention
-> sources compatibles
-> contexte temps/meteo/profil/territoire
-> eligibilite
-> score automatique + curation
-> deduplication + diversite
-> horizon maintenant/demain/semaine/week-end
-> action generique, objet direct ou composition
```

Pour chaque intention, definir : sources, conditions obligatoires, boosts, exclusions, temporalite, territoire, curation, type de presentation et destination.

Le MDS est prioritairement un moteur post-intention : une fois le champ reduit, il choisit quelques propositions concretes. Search reste la recherche textuelle, categorielle et annuaire.

## 8. Configuration unique des intentions Home

Le point d'entree editorial est :

`app/Helpers/home_discovery_config_helper.php`

Il regroupe :

- etat de toutes les IA Maintenant ;
- cartes Prochains jours ;
- Vacances, Ponts et roue ;
- injection Spotlight ;
- PlanningOpportunity ;
- preparation Meetz ;
- preparation du bloc Selections.

Le futur chargement progressif des blocs n'est pas configure ni implemente dans ce helper. Il sera traite plus tard au niveau du planificateur et du rendu des blocs.

Les definitions techniques historiques restent pour le moment dans `home_layout_helper.php`, mais leurs interrupteurs et surcharges editoriales sont appliques depuis ce registre unique.

## 9. Plan de livraison

### Phase A - cartes des deux rails Home

Pour chaque IA, PlanningOpportunity et futur contenu de rail : titre, description, image, activation, conditions, score, lien, NC/NSC et WTD. Desactiver ce qui ne peut pas encore etre garanti.

### Phase B - blocs Home

Corriger textes et requetes. Tous les nouveaux blocs passent par LocalQuery. Verifier exactement les sources et listes produites.

### Phase C - WTD

Commencer par les nouveaux WTD, puis corriger progressivement les anciens : NC/NSC, sources multi-objets, filtres, classement, pagination et fiches.

### Phase D - Search

Aligner categories et sources avec WTD, puis verifier texte, filtres, distance, tri, pagination et navigations.

### Phase E - coherence et donnees avant lancement

- audit global de coherence ;
- agents manquants ;
- configuration territoriale villes/regions : littoral, balneaire, montagne, frontiere, etc. ;
- fleuves, rivieres, lacs et villes traversees ;
- planning d'installation et d'execution des agents ;
- chasse, creation et amelioration des donnees lieux/events/experiences/circuits.

La qualite des donnees est une condition de lancement aussi importante que l'UX et les requetes.

## 10. Regle de modelisation

1. envie -> IndependentAction ;
2. lieu reel -> Place/Shop ;
3. activite organisee -> Experience ;
4. occurrence datee -> Event ;
5. parcours trace -> Circuit ;
6. destination contextualisee -> EscapadeProposal ;
7. composition libre -> OutingIdea/Collection ;
8. produit vendu -> Selection ;
9. pratique locale -> LocalHabit ;
10. conseil personnel -> LocalTip ;
11. mise en avant actuelle -> Spotlight ;
12. contexte -> CalendarSignal ;
13. idee bientot actionnable -> PlanningOpportunity.

## 11. Taxonomies transversales et contrat d'action

`ActivityPrincipalCategory` regroupe aujourd'hui la nature principale des `Event` et des `Experience`. `EtablishmentType` regroupe les categories de `Shop` et `Place`; LocalQuery accepte maintenant `etablishment_types` dans la configuration de ces deux sources et teste aussi le second type des ShopCategory. `ActivityType` appartient surtout au modele historique et ne doit pas devenir artificiellement le pivot commun.

Une proximite semantique comme `festival de biere` -> `bar a biere` ne se deduit pas de la nature Festival/Bar. Elle vient d'un signal partage : Hobby, Tag, theme, categorie specialisee ou, plus tard, produit MDM. Le contrat canonique est l'`action_string_id`. Chaque action peut declarer ses correspondances vers hobbies, tags, ShopCategory, PlaceType, EventCategory, ExperienceCategory, equipements et objets. Home, MDS post-intention et WTD doivent lire ce meme contrat au lieu d'entretenir des listes divergentes.

Le contrat peut aussi decrire sans l'activer immediatement :

- actions compatibles avant/apres ;
- variantes par profil ;
- duree, distance et temps de trajet ;
- contraintes meteo/calendrier ;
- destination generique WTD ou objet concret.

Cette base servira aux enchainements et aux futures soirees preparees. Elle ne remplace ni les objets reels ni les Selections vendues.

Le registre des enchainements est independant des ecrans : `app/Helpers/action_sequence_helper.php`. Il expose `action_sequence_for()` et `action_sequence_candidates()` ; il n'est pas encore injecte automatiquement dans le score ou l'affichage.

## 12. Contenus editoriaux et feed de ville

La Home et, eventuellement, Search peuvent recevoir des rails dedies pour : Collections, Votes, `Que faire` editorial, vraies Escapades/voyages, guides et contenus d'influenceurs. Un influenceur pourra composer son propre `Que faire a Lille/Seclin ce week-end` avec les objets iziLife.

`ElementNews` doit aussi pouvoir porter une actualite territoriale rattachee directement a une ville ou une division administrative, sans exiger un Place/Shop/Event parent. Ces contenus enrichissent le pouls de la ville mais ne doivent pas etre melanges arbitrairement aux resultats objets d'un WTD.

## 13. Produits et MDM (orientation, non branchee)

Les produits equivalents entre commerces doivent converger vers un produit et une categorie MDM canoniques, avec GS1 lorsque pertinent. Les produits generiques (canette, bouteille, espresso, verre de soda) pourront etre reutilises puis relies a l'offre propre du commerce. Ce sujet reste distinct du chantier Home/WTD actuel.

## 14. Rails transversaux des WTD

Un WTD conserve sa grille principale d'objets correspondant a l'intention. Des rails separes peuvent la completer sans polluer ses resultats :

- Sponsorises, uniquement s'il existe des cibles actives ;
- Partenaires, uniquement s'il existe des objets partenaires compatibles ;
- suggestions MDS post-intention, resolues apres reduction du champ ;
- pour Evenements : Aujourd'hui, Demain, Cette semaine, Ce week-end ;
- offres ponctuelles actives, avec leur vraie destination.

Les rails Home savent deja melanger actions generiques et objets concrets avec une formulation contextualisee. En revanche, une vraie `Offer` ne doit etre declaree supportee par un swiper que si son renderer est branche ; `PROMO` et `EXTERNAL_PROMO` sont deja rendus dans la grille WTD, ce qui n'equivaut pas encore a un support universel de `Offer` dans chaque rail.
