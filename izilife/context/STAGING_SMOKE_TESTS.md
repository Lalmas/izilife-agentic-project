# Campagne de validation des agents iziLife — staging

Cette procédure est la recette de référence avant toute mise en production et le
parcours d'onboarding de tout développeur ayant terminé l'installation de son
environnement local.

## Ce que valide réellement le test

Le runner cible staging par défaut : `agentic_workspace_staging/.../lille-zone`,
les vraies API et la vraie base staging. Ce n'est pas une simulation locale : le
code est exécuté localement, mais les classeurs, API et écritures sont ceux de
staging.

Les données viennent exclusivement des classeurs du Drive staging. Le dépôt
contient le code, pas les files d'exécution. Avant la recette, le runner compte les
lignes `pending` et indique les données qu'il faut encore fournir :

- liens manuels Shotgun, Facebook et Instagram dans `curate_events.xlsx` ;
- liens de médias dans `medias_igram.xlsx` ;
- villes/divisions dans `territories.xlsx` ;
- nouveaux `string_id` dans `ameliorateur.xlsx` ;
- sources variées dans `enrichisseur_contenus.xlsx` : produits, services,
  tarifs/EAP, équipements et cas mixtes.
- quartiers/divisions de villes, rues connues et opérations de calendrier
  d'événements dans leurs classeurs dédiés.

Le territorial et les quartiers sont deux agents différents :

- `classificateur_territoires.py` qualifie des villes et divisions existantes ;
- `city_subdivisions.py` crée ou met à jour les quartiers d'une ville existante.

Il n'existe pas de script `geography/cities.py` dans le socle actuel. Une entrée
cron qui l'appelle est invalide et ne doit pas être installée.

Une ligne terminée peut servir à valider l'upsert si elle est volontairement
repassée à `pending`. Pour valider une vraie création, il faut fournir une
nouvelle URL ou un nouveau `string_id` staging.

Les entrées doivent être volontairement petites mais représentatives : un lieu
avec produits, un avec services, un avec équipements, un cas mixte, quelques
liens d'événements et médias, une ville à configurer, une rue et un quartier.

## Fixtures métier à préparer dans staging

Avant de remplir les classeurs, créer ou confirmer les objets suivants dans le
BO staging et transmettre leurs vrais `string_id` :

| Fixture | Type attendu | Ce qu'elle valide | Partner | PSP |
| --- | --- | --- | --- | --- |
| Soultrain Café | SHOP | produits/options/prix, tags, liens et rattachement à une rue | oui | non requis pour l'import de contenu |
| Don Vito | SHOP | produits extraits d'images | oui | non requis |
| L'Essenti'Elles | SHOP | services génériques issus d'un site de prestations | oui | non requis |
| Hall U Need | PLACE ou SHOP selon la donnée staging | équipements, caractéristiques, EAP et distinction Animation | oui | non requis pour l'import |
| Follow Park | PLACE ou SHOP selon la donnée staging | EAP, tarifs et équipements | oui | non requis pour l'import |
| La Luck | SHOP | cartes multiples, catégories/sous-catégories et anti-doublon | oui | non requis |
| Disco Volante | SHOP | ElementMenu et catégories ambiguës | oui | non requis |

Le Partner est nécessaire pour valider les scopes et l'espace partenaire. Le
PSP n'est pas un prérequis des agents de contenu : ils créent des catalogues,
services, équipements, EAP ou tarifs, mais n'exécutent aucun paiement. Prévoir
un PSP staging séparément uniquement pour une campagne paiement/réservation
payante ; conserver aussi un Partner sans PSP pour vérifier que l'enrichissement
de contenu n'est pas bloqué.

Pour lancer la campagne, fournir :

- les `string_id` staging exacts des sept fixtures ci-dessus ;
- 1 à 5 nouvelles URL par fixture dans l'Améliorateur++ ;
- une image de menu Don Vito ;
- une URL de prestations beauté/bien-être et une autre d'un secteur différent ;
- une source Equipment/EAP mixte pour Hall U Need ou Follow Park ;
- une ville et une division existantes à qualifier ;
- un quartier à créer dans une ville existante ;
- une rue connue et un membre `SHOP:<string_id>` ou `PLACE:<string_id>` ;
- un Spotlight, une ActivityProposal, une EscapadeProposal, un Link et des Tags ;
- une Offer/BPR/Effect et une récompense de plan BPR/Effect ;
- une EventSerie, une AnnualCelebration et un événement récurrent dans `events/<zone>/event_structures.xlsx` ;
- une opération de calendrier sur EventSerie, AnnualCelebration ou Event ;
- 1 à 5 liens manuels d'événements et, si souhaité, des liens de médias.

## Limite de 1 à 5

`--max` limite les traitements réels, pas seulement la taille d'un fichier :

- Améliorateur : au plus N `string_id`, prioritaires compris ;
- Améliorateur++ : au plus N sources ;
- Chasseur : collecte limitée à 3 minutes et N résultats par catégorie ;
- les agents Excel : au plus N lignes pending.
- recherches automatiques d'événements : une page et au plus N événements par source.

Facebook est exclu : son scraper reste volontairement manuel le lundi.

La commande actuelle du Chasseur ne propose pas de limite pour sa phase
`--insert-only`. Le runner automatise donc la collecte courte, mais ne lance pas
une insertion potentiellement non bornée. Les autres imports sont effectivement
bornés à N.

## Déroulement obligatoire

1. Vérifier les scripts, routes et initialisations sans réseau.
2. Auditer les classeurs staging et fournir les lignes manquantes.
3. Exécuter une campagne bornée à 1–5 objets.
4. Lire le rapport PASS/FAIL puis contrôler les objets créés dans la base et le BO.
5. Corriger et relancer jusqu'à une campagne entièrement verte.
6. Seulement ensuite suivre la recette de production.

## Commandes staging

Le runner ne lit et ne modifie aucun `.env`. Charger les valeurs dans le terminal :

```powershell
$env:AGENTIC_DRIVE_ROOT = 'G:\Mon Drive'
$env:IZILIFE_AGENT_TOKEN = '<jeton-staging>'
```

Préflight sans réseau — compilation et validation de tous les `--init` :

```powershell
python tests/staging_smoke.py
```

Audit des files du Drive staging et liste des entrées manquantes :

```powershell
python tests/staging_smoke.py --prepare --max 5
```

Vraie recette staging, incluant Chasseur, Améliorateur et Améliorateur++ :

```powershell
python tests/staging_smoke.py --prepare --run --online --event-search --media --max 5
```

Les rapports PASS/FAIL sont générés dans `scripts/izilife/tests/reports/`.
`error`, `unmapped`, route cassée, classeur non initialisable ou `string_id`
introuvable sont visibles dans ces rapports.

## Portée actuelle

Le socle couvre Territorial, quartiers/divisions de ville, rues connues,
calendrier d'événements, Equipment, EscapadeProposal, Link, Spotlight, Tags,
ActivityProposal, Brunch, Offer/BPR/Effect, récompenses iziLife,
Améliorateur++, Améliorateur, Chasseur, téléchargement de médias et les
recherches Shotgun, Meetup, HelloAsso, Billetweb et Eventbrite.

Le curateur manuel d'événements traite les liens Shotgun, Facebook, HelloAsso,
Eventbrite, Meetup et Instagram du classeur. Il est lancé séparément après
validation du lot fourni. Instagram utilise son parcours OCR. Facebook n'est
jamais recherché automatiquement.

La campagne staging ne modifie jamais le `crontab -e` du Mac de production.
Voir `PRODUCTION_AGENT_VALIDATION.md` pour la seconde campagne et l'installation
finale du planning.

## Limite actuelle du local partagé

Les classeurs locaux du Drive sont aujourd'hui communs. Deux développeurs qui
lancent simultanément une campagne locale peuvent donc consommer les mêmes
lignes ou intégrer les tests de l'autre. La future isolation devra fournir un
répertoire local par développeur. Cette évolution est volontairement différée ;
staging reste pour l'instant l'environnement commun de validation maîtrisée.
