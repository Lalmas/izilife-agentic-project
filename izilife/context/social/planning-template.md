# Planning éditorial izilife — V4 simplifié

## Principe
Le planning sert à préparer les posts. Il ne sert plus à répéter la configuration visuelle.

La configuration durable est dans l'onglet `Post Types`.

## Onglet Planning

| Colonne | Rôle |
|---|---|
| DATE | Date de publication souhaitée |
| RÉSEAU | Instagram / Facebook / Les deux |
| TYPE | Code du post |
| VILLE | Ville concernée |
| LIEU | Lieu précis si utile |
| SUJET | Sujet court du post |
| DATA / INFOS | Toutes les infos à injecter : liste, artistes, comptes, tarifs, distance, programme, ton, contraintes |
| DATE EVENT | Date d'événement si besoin |
| HEURE / DURÉE | Heure, durée ou créneau |
| INPUT_ID | Dossier dans `inputs/` |
| IMAGE_PROMPT | Prompt image ponctuel, optionnel |
| POST OUTPUT | Sortie texte générée |
| IMAGE_OUTPUT | Fichiers générés |
| IMAGE_STATUS | non demandé / généré / erreur / template utilisé / canva à faire |
| STATUT | À faire / Généré / Relancer / Validé / Publié / Skip |

## Onglet Post Types

| Colonne | Rôle |
|---|---|
| POST_TYPE | Code du type de post |
| CONTENT_TYPE | post / carrousel / story / reel / video |
| TEMPLATE_LOCAL | Dossier template local |
| TEMPLATE_SOURCE | owned / inspiration / none |
| TEMPLATE_REF | Canva ID, URL, chemin ou note |
| IMAGE_PROVIDER | canva / gpt / pillow / none |
| IMAGE_MODE | auto / template / input / generate / none |
| NOTES | Règles du type |

## Règle importante
`TEMPLATE_SOURCE`, `TEMPLATE_REF` et `IMAGE_PROVIDER` ne doivent pas être dans le planning. Ils se règlent une seule fois par type de post.

## Série / concept
Il n'y a plus de colonne `SERIE`. Pour un `EVENT_SERIE`, écrire le nom de la série dans `SUJET` ou `DATA / INFOS`.
