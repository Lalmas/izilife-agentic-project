# Home contextuelle V2 - schema produit de reference

Configuration et mode d'emploi : `docs/home_discovery_mode_emploi.md`.

Architecture produit globale et plan de livraison : `docs/izilife_home_intention_architecture.md`.

## Objectif

La home doit produire, pour chaque ville et chaque contexte, une selection comparable a une curation locale : profil, heure, meteo, calendrier, territoire, distance, temps de trajet et importance editoriale.

Les stories sont mises de cote. La home repose sur trois rails stables :

1. `A ne pas manquer` ;
2. `Des idees pour maintenant` ;
3. `Dans les prochains jours`.

## 1. A ne pas manquer

Ce rail porte uniquement les contenus structurants :

- carte fixe `Que faire cette semaine` ;
- campagnes, offres et promotions iziLife ;
- editions locales liees a une `AnnualCelebration` : ce sont les gros events du territoire ;
- objets explicitement marques `a-ne-pas-manquer` ;
- vacances scolaires actives ;
- ponts lorsqu'ils seront reactives ;
- roue iziLife lorsqu'elle sera activee.

Une `AnnualCelebration` n'a pas besoin de Spotlight. Les editions sont reconnues par la relation existante `Event.annual_celebration_id`.

Les vacances et les ponts restent dans ce rail. Ils ne sont pas injectes dans les rails d'idees. Les vacances sont activees ; les ponts restent masques par configuration tant que leur WTD n'est pas pret.

## 2. Des idees pour maintenant

Ce rail contient ce qui est reellement faisable aujourd'hui :

- `IndependentAction` contextuelle ;
- `Place`, `Experience` ou autre objet concret correspondant a l'action ;
- `Event` en cours ou commencant assez tot ;
- edition locale d'une `AnnualCelebration` actionnable aujourd'hui ;
- `EscapadeProposal` encore realisable dans la journee.

Le candidat doit respecter l'heure, la meteo, les horaires, le profil, la duree utile, le trajet et le temps restant dans la journee.

Un evenement annule, termine ou explicitement complet est exclu. L'absence de billetterie ou de stock ne signifie jamais `complet` pour une braderie, une exposition ou un evenement ouvert.

## 3. Dans les prochains jours

Ce rail contient ce qui demande de l'anticipation ou dont la meilleure fenetre arrive bientot :

- `PlanningOpportunity` ;
- idee produite par un `CalendarSignal` ;
- `EscapadeProposal` ;
- action liee a une future fenetre meteo ;
- event Spotlight futur ;
- grand parc, parc d'attractions ou parc aquatique eloigne ;
- journee plage ou lac ;
- journee hotel ou week-end hotel.

Une action generique ouvrant un WTD n'a pas a resoudre les objets sur la home. Par exemple, `Week-end hotel` est affiche selon le contexte ; la vue WTD cherche ensuite les hotels, les dates, les offres et les disponibilites.

## Spotlight

Spotlight est un signal de curation, pas une affectation au rail `A ne pas manquer`.

Types deja acceptes par `SpotlightTarget` :

- `PLACE` ;
- `SHOP` ;
- `EXPERIENCE` ;
- `EVENT` ;
- `EVENT_SERIE`.

Regles :

- Spotlight sur un `EVENT` : curation de cet event ;
- Spotlight local sur une `EVENT_SERIE` : ses events enfants doivent heriter du signal via `Event.event_serie_id` ;
- Spotlight sur `PLACE`, `SHOP` ou `EXPERIENCE` : l'objet est favorise dans les idees compatibles ;
- pas de Spotlight necessaire sur `ANNUAL_CELEBRATION`.

Apres curation, date, heure, trajet et faisabilite placent le candidat dans `Maintenant` ou `Prochains jours`.

## Arbitre Maintenant / Prochains jours

Le temps de trajet est prioritaire lorsqu'il existe. La distance sert de repli.

Un candidat va dans `Maintenant` lorsque :

```text
trajet aller + duree utile + retour eventuel + marge
<= temps reellement disponible aujourd'hui
```

Sinon, s'il reste pertinent et preparable, il va dans `Prochains jours`.

Reperes indicatifs :

- 0-10 km : action locale immediate ;
- 10-35 km : sortie locale / demi-journee ;
- 35-90 km : demi-journee / journee ;
- 90-120 km : possible le jour meme si l'heure et le trajet le permettent ;
- 120-180 km : generalement a preparer ;
- 180 km+ : week-end, mini-sejour ou masque selon le contexte.

La distance ne decide jamais seule. L'arbitre est implemente dans `app/Libraries/Home/HomeHorizonResolver.php`.

## Catalogue d'actions territoriales

Les fiches et actions existantes ne doivent pas etre remplacees. Une action exprime l'envie ; le WTD ou le moteur resout les objets concrets.

| Idee | Maintenant | Prochains jours | Regle principale |
|---|---:|---:|---|
| Escapade | oui si proche | oui | destination et duree compatibles |
| Balade, glace et sunset | oui | eventuellement | cote/spot adapte et beau temps |
| Sunset | oui | oui | environ 1-2 h avant le coucher du soleil jusqu'a la limite configuree |
| Journee plage | oui si encore faisable | oui | meteo, trajet et temps restant |
| Apres-midi plage | oui | oui | avant l'heure limite depuis une ville interieure ; plus souple pres de la cote |
| Journee au lac | oui | oui | lac/base de loisirs reelle et meteo compatible |
| Grand parc | oui | oui | parc adapte a une demi-journee ou journee |
| Parc d'attractions | rarement immediate | oui | temps restant, trajet et horaires |
| Parc aquatique | oui si proche | oui | trajet, horaires, meteo si exterieur |
| Sortie velo | oui | oui | meteo, duree et terrain |
| Journee hotel | oui si contextuelle | oui | le WTD resout l'offre concrete |
| Week-end hotel | non | oui | le WTD resout hotels et disponibilites |
| Apres-midi a la Citadelle | oui | oui | conserve sa fiche/action propre |
| Journee aux Pres du Hem | oui | oui | le lieu concret repond a l'idee lac/base de loisirs |

## Objets et responsabilites

- `IndependentAction` : envie generique.
- `Place`, `Experience`, `Event` : objet concret.
- `EscapadeProposal` : destination/proposition qui vaut le deplacement.
- `CalendarSignal` : contexte, jamais une action.
- `PlanningOpportunity` : idee bientot actionnable.
- `Spotlight` : curation manuelle locale.
- `WTD` : surface qui resout et affiche les objets concrets d'une action generique.

## Tags structurels

- `a-ne-pas-manquer`
- `parfait-week-end`
- `parfait-famille-journee`
- `parfait-couple`
- `parfait-sunset`
- `parfait-pluie`
- `parfait-forte-chaleur`
- `parfait-vacances`
- `vaut-le-deplacement`
- `habitude-locale`
- `transport-bon-plan`
- `bord-de-mer`
- `lac`
- `fleuve`
- `quais`
- `foret`
- `montagne`
- `plage`
- `escapade-journee`
- `demi-journee`
- `soiree-romantique`

## Regle de synthese

```text
curation + contexte + territoire + faisabilite
                    |
                    +-- contenu structurant -> A ne pas manquer
                    +-- faisable aujourd'hui -> Maintenant
                    +-- a preparer -> Prochains jours
```
