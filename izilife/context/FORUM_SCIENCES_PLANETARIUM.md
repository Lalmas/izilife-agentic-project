# Forum des Sciences : planétarium et expériences

État au 31 octobre 2026 : le paquet a d'abord été validé et rejoué sans doublon sur la fiche locale inactive `forum-des-sciences-test-local`, puis importé sur `PLACE forum-des-sciences` en production. Les 13 expériences, les 14 EAP et leurs images principales ont été activés et vérifiés. Aucun horaire absent n'a été inventé.

L'agent `agentUpsertExperience` accepte désormais `experience_theme` vide, conformément à la colonne SQL nullable, et exige une valeur numérique lorsqu'elle est fournie. La création reste inactive pour revue. Le paquet exécutable est `scripts/izilife/experiences/forum_sciences_package.json` ; `forum_sciences_draft.json` reste l'inventaire source.

## Rattachement métier

- Le parent est la fiche `PLACE forum-des-sciences` (ID 686 constaté en production). Le site officiel donne l'adresse **1 place François Mitterrand, 59650 Villeneuve-d'Ascq**. Ne pas créer une seconde fiche Place « Planétarium de Lille ».
- Le dôme est un `Equipment` nommé « Planétarium » avec `owner_place_id` et `in_on_place` pointant vers le Forum, `internal_id=planetarium`, catégorie `EquipmentCategory/planetarium`. Capacité publiée : 114 sièges, dont 4 emplacements PMR. La catégorie et le type `ObjectOnPublicPlace/planetarium` figurent dans les inserts de base de `izilife-db/principal/0010_izilife.sql` et ont été rendus disponibles en production avant l'import.
- Les spectacles sont des `Experience` distinctes, liées au Forum par `meet_place` et au dôme par `meet_equipment`. Le champ `Experience.meet_equipment` existe déjà dans le schéma : aucun faux lieu n'est nécessaire.
- Les quatre tarifs du planétarium sont quatre EAP uniques appartenant au Forum. Chacun est diffusé sur l'équipement Planétarium par `LocationEAPUseForEquipment`. Les neuf spectacles héritent de leur applicabilité parce qu'ils ont ce même `meet_equipment`. Il y a donc 4 EAP, 4 liaisons de diffusion vers l'équipement et 9 expériences concernées, jamais 36 EAP dupliqués.
- `LocationEAPUseForService` ne sert pas à cette diffusion : elle concerne uniquement la diffusion d'un EAP supérieur vers des `ElementService`. Ici, les quatre tickets sont diffusés vers l'équipement Planétarium avec `LocationEAPUseForEquipment`. Le prix reste dans `ElementAccessPrice`.
- Les horaires de spectacle sont des `SessionConfiguration` puis `SessionConfigurationContent` propres à chaque expérience, avec `repetition_type=heures-fixes`. Ne pas transformer la grille des vacances en récurrence annuelle : le site ne donne que deux fenêtres explicites.

## Contenus repérés

| Groupe | Expériences |
| --- | --- |
| Planétarium (9) | Le petit ciel étoilé ; À la belle étoile ; Légendes étoilées ; Le ciel ce soir ; Le temps vous est conté ; Un penchant pour les saisons ; L’odyssée solaire ; Biosignature, signal détecté ; Big Bang, l’appel des origines |
| Autres (4) | Tous à plumes! ; Enigma ; Croque Couleurs ; Espace d’Atom |

La grille scolaire publiée associe les six spectacles suivants à des horaires hebdomadaires : mercredi 15 h Le petit ciel étoilé et 16 h 30 L’odyssée solaire ; samedi 15 h À la belle étoile et 16 h 30 Le ciel ce soir ; dimanche 15 h Légendes étoilées et 16 h 30 Biosignature. Le **premier dimanche** publie une grille différente et gratuite ; `day_list` seul ne sait pas exprimer cette exception mensuelle. Ne pas créer de séance régulière sur la base de cette grille sans règle de priorité ou dates explicites.

Les vacances affichées couvrent le 17–31 octobre 2026 et le 19 décembre 2026–2 janvier 2027. Les éventuelles fermetures anticipées des 24 et 31 décembre sont signalées par le site. Une configuration annuelle ou sans borne serait incorrecte.

Tarifs individuels affichés pour le planétarium : adulte 9 €, adolescent 13–18 ans 8 €, enfant jusqu’à 12 ans 4 €, tarif réduit 8 € sous justificatif, Pass tribu 4 personnes 25 € pour une activité et 35 € avec une autre activité. Le premier dimanche du mois est gratuit. Les conditions d’éligibilité doivent accompagner chaque EAP. Les tarifs scolaires et groupes sont hors du périmètre demandé.

Les activités hors planétarium ont leurs propres prix : exposition temporaire / Enigma / Petit Forum 8 € adulte et gratuit jusqu’à 12 ans ; Espace d’Atom 5 € adulte et enfant. Les dates annoncées sont 3 octobre 2026–29 août 2027 pour Tous à plumes!, 14 février 2026–17 janvier 2027 pour Croque Couleurs et Espace d’Atom. Enigma annonce trois thèmes alternés chaque semaine sans calendrier détaillé : ne pas inventer la date de chacun.

La billetterie en ligne est annoncée indisponible sur les pages officielles ; les fiches peuvent indiquer le téléphone **03 59 73 96 00** et « réservation conseillée », sans activer un achat ou une réservation iziLife.

## Intégration contrôlée

1. Vérifier dans la base cible les `string_id` existants, la catégorie et le type d'objet avant tout insert. Les inserts de référentiel dans le SQL source ne modifient pas une base déjà déployée.
2. Créer ou retrouver l'équipement et l'association `PlaceObject`, puis rattacher quelques images vérifiées du planétarium via `EquipmentMedias` et les images de spectacles via `ExperienceMedias`. Utiliser l'import média BO pour créer les objets `Media` dans le bucket de destination ; ne pas recopier les IDs de média ni les URLs externes comme chemins S3.
3. Créer les 13 expériences de façon idempotente, avec un `experience_string_id` stable, une source URL et `meet_place` résolu dans la destination. Elles restent inactives jusqu'à contrôle BO/FO. Le fichier `scripts/izilife/experiences/forum_sciences_draft.json` est un inventaire vérifiable, pas un payload directement accepté par la route `agentUpsertExperience`.
4. Créer les SC/SCC seulement pour les créneaux explicitement publiés et bornés ; vérifier les exceptions premier dimanche et vacances avant d'activer la diffusion des séances.
5. Créer les quatre EAP planétarium une seule fois sur le Forum, puis les lier à l'équipement exact avec `LocationEAPUseForEquipment`. Créer séparément les huit EAP propres aux quatre autres activités et les deux Pass tribu généraux. Tous restent inactifs et à confirmer avant publication.

Le paquet attendu contient donc 13 expériences, 14 EAP distincts au total, 16 médias et aucune séance inventée : 4 EAP planétarium diffusés sur l'équipement, 8 EAP propres aux autres activités et 2 Pass tribu du Forum.

## Validation locale du 30 octobre 2026

- cible : `PLACE forum-des-sciences-test-local`, inactive et non listable ;
- équipement : `Equipment #53`, 3 médias dont un principal ;
- expériences : 13, toutes inactives, toutes reliées au Forum ; les 9 spectacles du dôme ont `meet_equipment=53` ;
- médias : 13 liaisons `ExperienceMedias`, une par expérience ;
- EAP : 4 tarifs du Planétarium diffusés par `LocationEAPUseForEquipment`, 8 EAP possédés par les quatre autres expériences et 2 Pass tribu possédés par le Forum ;
- second passage : tous les objets et médias ont été ignorés comme déjà présents ; aucun doublon n'a été créé ;
- séances : aucune, conformément à la consigne de ne pas inventer d'horaires.

## Sources

- [Planétarium : spectacles, horaires et tarifs](https://forumdepartementaldessciences.fr/activites/le-planetarium/)
- [Ouverture et tarifs du Forum](https://forumdepartementaldessciences.fr/informations-pratiques/ouverture-et-tarifs/)
- [Tous à plumes!](https://forumdepartementaldessciences.fr/activites/tous-a-plumes/)
- [Enigma](https://forumdepartementaldessciences.fr/activites/enigma/)
- [Croque Couleurs](https://forumdepartementaldessciences.fr/activites/croque-couleurs/)
- [Espace d’Atom](https://forumdepartementaldessciences.fr/activites/espace-datom/)
