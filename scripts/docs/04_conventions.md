# 04 — Conventions

## Zones

En CLI, toujours utiliser :

```powershell
--zone=lille
```

Le script transforme automatiquement en :

```text
lille-zone
```

## Environnements

Toujours expliciter pendant les tests :

```powershell
--env=local
```

## Commandes standards

Tous les agents doivent tendre vers :

```text
--init
--dry-run
--collect
--insert
--max
--zone
--env
```

## Statuts Excel

```text
pending / À faire
relancer / Relancer
done / Généré / Validé
error / Erreur
skip / Skip
```

Le script ne doit jamais modifier les lignes `Validé`, `Publié`, `done`, `skip`, sauf demande explicite.
