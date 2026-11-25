# Tags et caractéristiques : saisie manuelle

`tags_and_characts.py` complète le script historique `tags.py`. Il ne collecte aucune donnée sur Google et n'appelle aucune IA. Il lit un classeur de l'environnement choisi et appelle le BO uniquement lors d'un lancement réel.

## Classeur

`<racine Drive de l'environnement>/izilife/tags/<zone>-zone/tags_and_characts.xlsx`

Une ligne cible une fiche par `scope_type` et `scope_ref` (`string_id`). Les tags et chaque famille éditoriale se saisissent avec des `string_id` séparés par `|`. `principal_characteristics` accepte une liste de champs : `wifi|have_terrace` active les deux, `-wifi` le désactive ; `wifi=1|have_terrace=0` est également accepté. Une cellule vide n'entraîne aucun changement. `ADD` ajoute les associations manquantes, `REMOVE` retire les associations indiquées ; les valeurs explicites 0/1 de `principal_characteristics` sont appliquées dans les deux cas. Une référence inconnue, un tag hors portée ou une association indisponible bloque toute la ligne avant écriture.

Le classeur contient des onglets de référence : tags avec leurs portées, champs 0/1 et familles éditoriales avec leurs portées Place, Shop, Event, EventSerie, Experience ou AnnualCelebration. `Hobby` utilise `hobby_string_id`, `ObjectOnPublicPlace` utilise `object_string_id`, `Occasion` utilise `occasion_string_id`, et `DishOrigin` lit le référentiel `PlaceOrigin`. `AgeCategory` n'a pas de `string_id` : sa liste affiche son ID numérique propre à l'environnement. Excel ne gère pas proprement les listes déroulantes à sélections multiples ; ces onglets servent de catalogue de références. Le BO revalide chaque valeur.

## Commandes

Depuis `C:\Users\alcamara\Documents\agentic_Workspace\scripts\izilife` :

```powershell
& 'C:\Users\alcamara\AppData\Local\Python\bin\python.exe' tags\tags_and_characts.py --env local --zone lille --init
& 'C:\Users\alcamara\AppData\Local\Python\bin\python.exe' tags\tags_and_characts.py --env local --zone lille --refresh-references
& 'C:\Users\alcamara\AppData\Local\Python\bin\python.exe' tags\tags_and_characts.py --env local --zone lille --dry-run
& 'C:\Users\alcamara\AppData\Local\Python\bin\python.exe' tags\tags_and_characts.py --env local --zone lille --max 20
```

`--init` copie les lignes de l'ancien `tags.xlsx` si celui-ci existe ; il ne le modifie pas. `--refresh-references` lit les référentiels du BO correspondant à `--env`, inscrit la date de lecture dans `tags/references.json` et recrée les onglets de référence du classeur, sans toucher aux lignes de saisie. À refaire manuellement environ toutes les deux semaines ou après modification d'un référentiel. Cette commande exige que les nouvelles routes BO soient livrées dans l'environnement choisi. Pour staging et production, choisir explicitement `--env staging` ou `--env prod` ; le lancement réel écrit sur cet environnement.

Avant la livraison des routes BO, `--init` utilise le catalogue local sauvegardé dans `references.json` pour garnir les onglets staging et production. L'onglet `Références` le signale explicitement comme **à actualiser après livraison BO**. Il ne faut pas considérer ces valeurs locales comme validées pour staging ou production avant le rafraîchissement ciblé.

Ajouter `--refresh-all-zones` à `--refresh-references` pour actualiser les onglets de tous les classeurs `tags_and_characts.xlsx` déjà présents dans les zones de l'environnement choisi. Les autres environnements restent inchangés.

Le `--dry-run` n'appelle pas le BO. Il vérifie la conversion des cellules en payload et affiche ce qui serait envoyé ; il ne garantit pas que les références existent encore sur l'environnement cible. Le lancement réel journalise le résultat dans `status` et `last_result`.
