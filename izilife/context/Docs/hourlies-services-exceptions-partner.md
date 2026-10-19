# Horaires iziLife : activités, cuisine et exceptions

## Modèle

`Hourly.service_scope` distingue :

- `GENERAL` : horaires d'ouverture du lieu ou d'une activité/catégorie ;
- `KITCHEN` : horaires réels du service de cuisine, indépendants de la catégorie commerciale.

Un bar servant des tapas peut donc rester un bar et publier des horaires de cuisine sans ajouter artificiellement une catégorie Restaurant. Chaque service possède son propre `Hourly` courant et réutilise les `HourlyContent` hebdomadaires.

Les exceptions concernent uniquement l'ouverture générale. La Cuisine est volontairement un second planning hebdomadaire normal et indépendant ; elle n'expose pas d'exception propre dans le BO.

## Priorité d'affichage FO

Pour une date donnée, un `HourlyContent.exceptional_hourly_day` remplace la ligne hebdomadaire correspondante. Il ne s'ajoute jamais comme un second jour identique. Lorsqu'un `CalendarOccurrence` lié à `CelebrationDay` est férié :

- fermeture d'un jour normalement ouvert : « Fermeture exceptionnelle » ;
- ouverture d'un jour normalement fermé : « Ouverture exceptionnelle » ;
- simple modification des heures : « Horaire exceptionnel » ;
- le nom de la fête est ajouté entre parenthèses lorsqu'il est connu ;
- sans exception : elle conserve l'horaire connu et avertit qu'il peut varier.

Quand plusieurs activités ou services existent, la modale FO les présente sous forme d'accordéon compact. Le résumé de carte donne directement l'état de chaque activité/service, sans la mention technique « horaires selon l'activité ».

## BO interne et espace Partner

Le BO permet de choisir « Ouverture générale » ou « Cuisine » lors de la création/modification d'un horaire. En portée Cuisine, la sélection de catégorie n'est pas utilisée.

Une fermeture antérieure à l'ouverture (`19:00–02:00`) est interprétée comme une fermeture le lendemain. Cette règle vaut pour Place, Shop et Event.

L'espace Partner expose deux semaines séparées : horaires d'ouverture et horaires de cuisine. La cuisine est facultative ; l'absence d'horaire Cuisine ne modifie pas l'horaire général.

La documentation Partner doit toujours expliciter qu'une cuisine fermée ne signifie pas que l'établissement est fermé.

## Contrat multi-catégorie des établissements

La catégorie principale portée directement par `Shop.shopCategory_id` ou `Place.place_type` est une activité à part entière. Elle doit toujours être proposée avec les catégories secondaires de `LocationOtherCategory`.

- aucune activité sélectionnée signifie « Tout l’établissement » ;
- une activité sélectionnée limite l’objet métier à cette activité ;
- les horaires généraux de l’établissement servent de planning hérité ;
- un horaire propre à une activité remplace ce planning uniquement pour cette activité ;
- une configuration de réservation courante est unique par activité, indépendamment de la configuration générale ;
- offres, tarifs d’accès, services et avantages utilisent le même vocabulaire et la même liste d’activités ;
- la rédemption manuelle d’un avantage n’interroge jamais l’utilisateur sur l’activité : son périmètre est affiché avant validation et sur la preuve ;
- une activité secondaire encore référencée ne peut pas être supprimée ;
- lors du changement de catégorie principale, l’ancienne principale est conservée comme catégorie secondaire afin de préserver ses rattachements.

Cette structure permet notamment d’exposer séparément une réservation Bar et une réservation Restaurant sur un établissement unique, avec leurs propres créneaux et contraintes.

## Migration

La migration est ajoutée en fin de `021_Next_Improves.sql` et crée la colonne ainsi que les index courants par propriétaire/service. Elle a été appliquée à la base locale `izilife2`.
# Équipements et scopes BO

- L’entrée BO `Équipements` ouvre un sélecteur de scope obligatoire utilisant l’autocomplétion commune.
- Scopes gérés : ville, lieu, commerce, événement, série d’événements et célébration annuelle.
- Les catégories proposées dépendent du scope (`create_from_city`, `create_from_place`, `create_from_shop`, `create_from_event`). Un équipement ne peut jamais être créé sans propriétaire.
- Les équipements urbains autonomes (préau, zone de pique-nique, cage/parc de street workout) sont localisables et peuvent avoir leur propre fiche. Les objets internes comme une table de restaurant ou un carré VIP ne sont pas proposés depuis une ville.
- Un équipement pérenne d’événement appartient à l’`AnnualCelebration` ou à l’`EventSerie`. Une édition le référence via `EventEquipmentUsage` et peut le masquer, conserver sa position, surcharger adresse/coordonnées ou tarif sans dupliquer l’équipement.

# Catégorie principale d’un lieu multi-catégorie

Le changement est transactionnel : l’ancienne catégorie principale devient secondaire, tandis que la nouvelle catégorie principale est retirée de `LocationOtherCategory` si elle y figurait. Le couple principal/secondaires reste donc cohérent dans les deux sens.

# Périmètre des tarifs d’accès

Pour un Place/Shop multi-catégorie géré comme commerces séparés, le formulaire EAP affiche un simple sélecteur `Activité concernée` dans la ligne principale, juste avant le prix. Il n’apparaît pas pour les autres lieux. Une valeur vide signifie tout l’établissement.
