# Agent compétitions iziLife

L'agent tourne depuis ce poste. Il ne demande ni connexion SSH, ni commande Spark, ni ID numérique.

## Initialiser le fichier Excel

```powershell
python .\scripts\izilife\competitions\fetch_competition_schedule.py --init --env prod
```

Si le fichier existe déjà, il n'est pas écrasé.

## Lancement standard (prod, staging ou local)

```powershell
python .\scripts\izilife\competitions\fetch_competition_schedule.py --env prod
```

Cette commande lit `competition-planning.xlsx`. C'est le fichier de pilotage à copier avec l'agent sur chaque environnement. Il contient uniquement les compétitions à préparer/importer, jamais les matchs.

## Lancer exceptionnellement la configuration du BO

```powershell
python .\scripts\izilife\competitions\fetch_competition_schedule.py --all --env prod
```

Avec `--all`, le fichier Excel est volontairement ignoré et la liste vient du BO. Ne pas utiliser cette option pour la tâche planifiée si Excel doit rester la configuration de référence.

## Lancer une seule compétition

```powershell
python .\scripts\izilife\competitions\fetch_competition_schedule.py --competition ligue-1 --env prod
```

`AUTO` ne fait rien si l'édition et son calendrier sont déjà à jour. `FORCE` relit le calendrier. `SKIP` prépare l'édition sans importer les matchs.

Les cellules `starts_at` et `ends_at` décrivent l'édition. Lorsqu'elles sont vides, l'agent conserve les dates déjà enregistrées dans le BO.
