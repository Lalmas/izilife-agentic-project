# Texte de reprise — agents de curation iziLife

Je travaille sur iziLife, une plateforme locale qui doit répondre automatiquement à « Que faire ici, maintenant, demain, cette semaine ou ce week-end ? », selon la ville, la météo, le calendrier, le profil (seul, couple, amis, famille, touriste) et la capacité à se déplacer.

Avant toute modification, lis entièrement :

- `C:\Users\alcamara\Documents\agentic_Workspace\izilife\context\izilife-context-long.md`
- `C:\xampp\htdocs\izilife\docs\izilife_home_intention_architecture.md`
- `C:\xampp\htdocs\izilife\docs\home_hb_mds_opportunites_v2.md`
- `C:\xampp\htdocs\izilife\docs\home_discovery_mode_emploi.md`
- `C:\xampp\htdocs\izilife\docs\home_ia_wtd_references_audit.md`
- les SQL de référence dans `C:\xampp\htdocs\izilife-admin\statics\izilife_new_version`, surtout `020_New_Entities`, `021_Next_Improves` et le SQL Navigation.

## Objectif de ce chantier

Les agents iziLife servent à réduire au maximum la curation manuelle sans inventer de données. Ils doivent chercher, créer, compléter, contrôler et maintenir les objets qui alimentent réellement Home, Home Blocks, LocalQuery, WTD et Search :

- Place et Shop ;
- Event, EventSerie et AnnualCelebration/éditions ;
- Experience ;
- Circuit ;
- Page/Community ;
- LocalHabit et LocalTip ;
- EscapadeProposal ;
- équipements, objets présents, accès, prix et services ;
- tags, hobbies, ambiances, sports, danses, musiques et catégories.

Le but n’est pas de produire des articles génériques. iziLife possède des objets pérennes et périssables qui doivent être assemblés et contextualisés. Les agents doivent enrichir ces objets structurés afin que les moteurs puissent les retrouver.

## Règles métier essentielles

1. Ne crée pas une fausse Experience lorsqu’un lieu suffit.
   - « Passer une nuit insolite chez Chlorofil » est une formulation de présentation produite à partir de la fiche du lieu ; le clic ouvre Chlorofil.
   - « Nuits insolites » est une intention générique et ouvre un WTD.
2. Experience est réservée aux prestations/activités véritables : visite guidée, atelier, cours, stage, dégustation, jeu de piste, croisière, etc.
3. LocalTip porte un conseil personnel et éditorial (« Moi, je fais ceci ici »), pas une donnée opérationnelle qui pourrait être structurée.
4. Equipment, ObjectOnPublicPlace, AccessType, prix, réservation, prêt/location et horaires doivent être structurés lorsque les tables le permettent. Un tag ne doit pas remplacer une information opérationnelle.
5. Spotlight est une curation éditoriale datée ou permanente : tendance, lieu réputé, nouveauté à tester, objet qui vaut le coup. Il ne signifie pas automatiquement « À ne pas manquer ».
6. Pour les événements :
   - un enfant d’un récurrent remonte avis et médias au récurrent ;
   - une édition d’EventSerie ou AnnualCelebration remonte avis et médias à la série/célébration ;
   - une édition peut conserver au maximum deux images propres pour sa couverture ;
   - les booléens `is_izilife_event`, `is_izilife_partnership_event`, `is_izilife_organizer_event`, `is_exclusive_on_izilife` ont chacun un sens distinct et ne remplacent pas les tags.
7. EscapadeProposal n’est pas un contenu avec titre : c’est une configuration qui qualifie une ville, division, Place, Shop, EventSerie ou AnnualCelebration comme destination pertinente (demi-journée, journée, week-end, city-trip), avec profils, météo, saison, priorité et raisons.
8. Les Selections sont des produits commerciaux iziLife (Moment, Pass, Parcours, Sortie clé en main, Nuit, Escapade). Elles peuvent compléter les résultats d’une intention, avec une mention « Vendu par iziLife », sans remplacer l’intention.

## Couche territoire indispensable

Les agents doivent progressivement qualifier les régions, départements, villes et divisions : littoral, balnéaire, montagne, frontière, village, capitale/principale, plage/lac/forêt proches, fleuve et quais, patrimoine, romantique, famille journée, hub city-trip, etc.

Ils doivent également relier les fleuves, rivières, lacs et canaux aux territoires traversés et identifier les quais, plages, bases nautiques et spots utilisables. Ne parcours pas toutes les villes si une division parente rend le trait impossible.

Distance provisoire :

- 0–10 km : immédiat/local ;
- 10–35 km : sortie locale/demi-journée ;
- 35–90 km : demi-journée/journée ;
- 90–180 km : journée/soirée/week-end court ;
- au-delà : week-end/mini-vacances.

La distance doit ensuite être pondérée par un vrai temps de trajet voiture/transports (OSRM, GraphHopper ou Valhalla). La décision dépend toujours de distance + trajet + météo + calendrier + profil + durée disponible.

## Agents attendus et chaîne d’installation

Audite les agents/scripts existants avant d’en créer. Propose ensuite une architecture cohérente couvrant au minimum :

1. chasseur de lieux manquants ;
2. améliorateur/contrôleur de fiches Place et Shop ;
3. chasseur d’événements et rattachement aux séries/célébrations ;
4. améliorateur d’événements ;
5. constructeur/contrôleur de Pages et organisateurs ;
6. qualification territoire (côte, montagne, frontière, patrimoine, escapade) ;
7. eau et géographie (fleuves, rivières, lacs, quais, plages, villes traversées) ;
8. équipements/services/accès/prix ;
9. détection de doublons et cohérence multi-objet ;
10. scoring de complétude et file de validation humaine.

Pour chaque agent, documente : source, fréquence, objets lus/écrits, règles de confiance, déduplication, statut brouillon/validation, journalisation, reprise après erreur, coût API, dépendances et ordre d’exécution. Les agents ne doivent jamais publier silencieusement une information incertaine.

## Résultat demandé

Commence par cartographier ce qui existe réellement dans le code, les Commands, Models, Services, SQL et docs. Donne ensuite :

- les agents existants et leurs recouvrements ;
- les agents réellement manquants (un ou deux si cela suffit, pas une explosion de micro-agents) ;
- les corrections d’architecture ;
- un planning d’installation/exécution ;
- les tables et statuts utilisés ;
- les contrôles qualité et la validation humaine résiduelle ;
- les fichiers précis à modifier.

Ne modifie rien avant d’avoir compris l’ensemble et proposé ce plan. N’invente ni table ni objet si une structure générique existante convient.
