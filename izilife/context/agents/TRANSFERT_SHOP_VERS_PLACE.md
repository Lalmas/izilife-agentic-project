# Transfert contrôlé Place / Shop

## Objectif

Fusionner ou convertir une fiche `Place`/`Shop` sans copier aveuglément les identifiants, sans perdre ses contenus et sans laisser deux fiches publiques concurrentes. Aushopping V2 (`Shop` vers `Place`) est le premier pilote appliqué et vérifié en production le 31 octobre 2026.

Le moteur couvre :

- `Place` vers une nouvelle `Shop` ;
- `Place` vers une `Place` existante ;
- `Shop` vers une `Place` existante ;
- `Place` vers une `Shop` existante ;
- `Shop` vers une `Shop` existante ;
- les créations symétriques restent possibles si la catégorie cible est fournie explicitement.

`EXISTING` signifie fusion vers une fiche explicitement nommée. `CREATE` crée
d'abord une cible inactive et non listable, avec une catégorie résolue par sa
référence stable, puis lui applique le même transfert contrôlé.

Le transfert n'est pas une suppression de la source. La fiche Shop devient une trace désactivée et non listable qui indique vers quelle Place elle a été purgée. Le journal conserve le couple source/destination et permet de rejouer l'opération sans duplication.

## Séquence

1. Résoudre la source et la destination par type et référence publique (`string_id`, `unique_id` ou Google Place ID selon le cas), jamais par un ID provenant d'un autre environnement.
2. Produire un plan en lecture seule : champs de base, relations, médias, objets dépendants, conflits et exclusions.
3. Bloquer l'écriture si la destination n'est pas certaine, si plusieurs cibles sont possibles ou si une relation ne peut pas être reconstruite sans perte.
4. Créer la Place cible ou utiliser une Place cible explicitement validée.
5. Copier ou rattacher seulement les familles autorisées, dans une transaction lorsque la base le permet.
6. Vérifier les compteurs et les pages BO/FO.
7. Désactiver et rendre non listable la source, ajouter une mention de purge vers la référence cible et conserver son identifiant interne pour l'audit.

## Familles à traiter

- fiche, localisation, ville et catégorie principale Place ;
- médias et albums, sans déplacer ni supprimer les fichiers source ;
- liens, médias externes et sources ;
- `PrincipalCharacteristics`, tags et caractéristiques éditoriales ;
- horaires et `HourlyContent` ;
- équipements, Services et EAP ;
- produits, catégories, options et menus lorsque le modèle destination les accepte ;
- événements, expériences, circuits et endpoints Hub associés ;
- enfants `Shop.in_on_place` lorsque la Place cible devient leur vrai conteneur.

Chaque famille possède une stratégie explicite : `COPY_MISSING`, `REPOINT`, `MERGE`, `REPORT_ONLY` ou `EXCLUDE`. Une table inconnue ou non déclarée est bloquante, pas ignorée silencieusement.

Le cas nominal est une fiche mal typée encore pauvre. Si elle ne possède ni produits, ni Services, ni EAP, ni autres contenus dépendants, le rapport l'indique et n'exécute aucune opération inutile sur ces familles. La couverture complète reste nécessaire pour les exceptions.

## Références polymorphes

L'audit ne se limite pas aux colonnes physiques `shop_id` et `place_id`. Il recherche également les références de la forme :

- `scope_type` / `scope_id` ;
- `target_type` / `target_id` ;
- `object_type` / `object_id` ;
- `owner_type` / `owner_id` ;
- leurs variantes réellement présentes dans le schéma déployé.

Une référence polymorphe n'est repointée que si sa valeur de type désigne explicitement le Shop source et si le type Place est autorisé par le consommateur. Les historiques d'audit et références de source peuvent conserver la source désactivée au lieu d'être réécrits. Les tables transactionnelles, utilisateur ou commerciales restent exclues même si elles utilisent un couple polymorphe.

## Exclusions obligatoires

Les réservations, transactions, paiements, tickets consommés, données utilisateur, avis et historiques personnels ne sont jamais déplacés automatiquement. Ils sont signalés dans le plan pour décision métier. Les offres temporaires et campagnes ne sont pas transférées par défaut.

## Médias

Un fichier déjà présent dans le bucket de destination n'est pas recopié. Les relations `ShopMedias` sont reconstruites comme relations `PlaceMedias` vers la Place cible lorsque le même objet `Media` est valable. Si un chemin dépend réellement du type de propriétaire, le fichier est copié, jamais déplacé, puis un nouveau média est rattaché. Le dry-run indique le cas retenu.

## Implantation disponible localement

- modèle BO transactionnel `LocationTypeTransfer_model` dédié au plan et à l'application ;
- routes agent génériques `agentLocationTransferPlan` et `agentLocationTransferApply` ;
- anciens alias `agentShopToPlacePlan` et `agentShopToPlaceApply` conservés pour compatibilité ;
- script opérateur `scripts/izilife/commercial_centers/location_transfer.py` ;
- ancien opérateur `shop_to_place.py` conservé pour les plans historiques ;
- plan figé par hash, clé d'idempotence et journal `CurationSyncJournal` dans la même transaction ;
- option explicite `--activate-destination`, jamais implicite ;
- repointage des relations éditoriales vers la Place, sans dupliquer leurs `unique_id` ;
- copie des pivots médias et des seuls champs simples manquants inscrits dans une liste blanche.

Le code doit être livré dans `izilife-admin` avant utilisation distante. Le plan
reste toujours en lecture seule. Exemple :

```powershell
python scripts/izilife/commercial_centers/location_transfer.py plan `
  --env staging --source-type PLACE --source-ref ancienne-fiche `
  --destination-type SHOP --destination-ref nouvelle-fiche `
  --destination-mode CREATE --destination-category-ref restaurant

python scripts/izilife/commercial_centers/location_transfer.py apply `
  --env staging --source-type PLACE --source-ref ancienne-fiche `
  --destination-type SHOP --destination-ref nouvelle-fiche `
  --destination-mode CREATE --destination-category-ref restaurant `
  --plan-file <rapport.json> `
  --activate-destination
```

En production, `apply` exige en plus `--confirm-production`. Une référence
transactionnelle ou utilisateur est signalée et exclue ; une référence métier
inconnue bloque le plan. Un conflit de contrainte pendant le repointage annule
toute la transaction.

Le code PHP et le script Python passent leurs contrôles syntaxiques. Le
1er novembre 2026, la version générique a été rejouée contre la base locale sur
les six cas : `Place→nouvelle Shop`, `Place→Place existante`,
`Shop→Place existante`, `Place→Shop existante`, `Shop→Shop existante` et
`Shop→nouvelle Place`. Les liens et médias ont été contrôlés, le second passage
n'a créé aucun doublon et toutes les fixtures `TEST-CODEX` ont été supprimées.
Ces essais locaux ne remplacent pas le smoke test staging après livraison.

L'inventaire `information_schema` est comparé sans tenir compte de la casse afin
de fonctionner avec MySQL Windows. Les requêtes d'exécution conservent en
revanche les noms physiques canoniques (`Place`, `Shop`, `PlaceMedias`,
`ShopMedias`, `Link`) : aucune table n'est mise en minuscules à l'exécution, ce
qui préserve la compatibilité des serveurs Linux staging et production. Un test
de contrat source verrouille cette règle.

Le plan est généré à partir du schéma réellement déployé. L'inventaire SQL local montre de nombreuses familles portant `shop_id`, `place_id`, `in_on_shop`, `in_on_place` ou un couple polymorphe ; une liste codée à la main et incomplète serait dangereuse.

## Suite du pilote centre commercial

Après la conversion d'Aushopping V2 en Place, l'inventaire commercial déjà extrait est réconcilié avec la production. Les commerces existants sont rattachés avec `Shop.in_on_place` ; seuls les commerces confirmés absents deviennent des candidats à créer. Les services, hobbies, équipements et objets sur place sont traités dans un second passage contrôlé.

Lillenium suit le même pipeline d'inventaire et de rattachement, mais sans conversion Shop vers Place : sa fiche production est déjà une Place.

## Résultat du pilote Aushopping V2

La conversion production a été exécutée dans une transaction avec préconditions strictes : même Google Place ID entre la source et la cible, cible de type `centre-commercial`, onze médias source et aucun média cible avant bascule.

- la Place `aushopping-v2` est active et listable ;
- ses onze relations média ont été reconstruites dans `PlaceMedias` ;
- ses pointeurs principal et couverture utilisent le média `3254` déjà présent ;
- l'ancien Shop est inactif, non listable et nommé `Lieu purgé vers Place : Aushopping V2` ;
- vingt Shops de Villeneuve-d'Ascq confirmés par leur identité et leur adresse ont été rattachés à la Place avec `in_on_place` ;
- un Shop confirmé a été rattaché à Lillenium ;
- `new-yorker` n'a pas été rattaché à Lillenium : sa fiche production correspond à Euralille.

Les essais local et staging ont été réalisés avec `ROLLBACK`. Ils n'ont laissé aucune conversion de test persistante. Les commerces absents, probables ou ambigus ne sont pas créés automatiquement : ils restent dans l'inventaire pour validation.

État de clôture : la conversion structurelle d'Aushopping V2 est terminée et Lillenium était déjà correctement modélisé comme `Place`. En revanche, l'inventaire commercial complet des deux centres n'est pas clôturé : seuls les rattachements confirmés ci-dessus sont appliqués. Les commerces absents, probables ou ambigus doivent encore être réconciliés, créés si nécessaire, puis rattachés.

Le script d'inventaire résout désormais la ville par `City.string_id`. Un homonyme situé dans une autre ville ne peut plus être classé `EXISTANT_A_RATTACHER`, même si son nom est exact.

## Règle globale des homonymes Place/Shop

Cette règle ne concerne pas seulement les centres commerciaux. Toute création automatisée de `Place` ou `Shop` passe par le même espace logique de `string_id` :

- si le `string_id` de base est libre, il est conservé ;
- s'il appartient déjà à une fiche d'une autre ville, la nouvelle référence devient `<base>-<City.string_id>` ;
- si le contenant `in_on_place` est connu, le backend essaie ensuite des suffixes déterministes issus de sa `Place.string_id` : par exemple `<base>-v2`, `<base>-<ville>-v2`, puis les variantes avec la référence complète du centre ;
- la création n'est bloquée pour validation qu'après épuisement de ces références déterministes ;
- une fiche existante n'est jamais renommée automatiquement par cette règle ;
- le `google_place_id` reste le critère décisif pour reconnaître une fiche déjà importée.

La résolution est centralisée dans `public_identifier_helper.php` et appliquée dans `Place_model::createPlace()` et `Shop_model::createShop()`. Les précontrôles Scraper, Hub et Maps ne doivent donc plus rejeter un homonyme uniquement parce que son slug existe dans une autre ville. La route agent accepte `in_on_place_ref`, toujours sous forme de `Place.string_id` et jamais d'ID copié entre environnements.
