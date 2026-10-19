# Équipements utilisables comme lieu précis

## Règle métier

Un équipement n'est proposé comme lieu précis que si sa catégorie porte
`EquipmentCategory.is_location_candidate = 1`.

Le réglage est volontairement porté par la catégorie : un banc, une poubelle ou
un équipement purement technique ne remonte donc pas, tandis qu'une catégorie
comme un préau, une entrée identifiée ou une zone nommée peut être activée.

## Objets pris en charge

- Event : lieu précis, y compris comme point de rendez-vous d'un Event « à travers la ville ».
- Experience : lieu de rendez-vous ou lieu précis de l'expérience.
- Circuit : départ, arrivée et étape.

Les valeurs enregistrées restent des références typées `EQUIPMENT-{id}` dans les
autocomplétions, puis sont conservées dans les colonnes dédiées de chaque objet.

## Activation d'une catégorie

```sql
UPDATE EquipmentCategory
SET is_location_candidate = 1
WHERE id = :equipment_category_id;
```

La désactivation empêche toute nouvelle sélection. Les contrôleurs refusent
également un POST forgé visant un équipement dont la catégorie est désactivée.
Les liens historiques déjà enregistrés restent en base afin d'éviter une perte
silencieuse de données.

## Compatibilité

L'endpoint commun des lieux n'ajoute les équipements que si le formulaire envoie
explicitement `include_equipment=1`. Les autres autocomplétions historiques
(organisateur, participant, lieu de séance, etc.) conservent donc leur contrat.
