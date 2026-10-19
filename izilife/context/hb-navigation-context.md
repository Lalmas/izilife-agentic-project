# HB — contexte de navigation préparé

## Décision de modèle

Le profil principal reste exclusif : `seul`, `en-couple`, `en-famille`, `entre-amis` ou `etudiant`.

`touriste` n'est plus un profil. Il est remplacé par le signal transversal `navigation_context.is_visitor`, présenté comme « Je suis en visite dans cette ville ». Ce signal affine les bonus/malus sans imposer un parcours touristique.

## Données préparées

Le contexte est conservé dans `search_filters.navigation_context` et dans le cookie `izilife_navigation_context` :

- `is_visitor` : actif et exploitable dès maintenant ;
- `is_15_17` : préparé, mais contrôle visuel masqué ;
- `child_age_bands` : liste parmi `0-3`, `4-7`, `8-11`, `12-14`, `15-17`, préparée mais masquée.

L'endpoint auto-routé `POST home/navigationContext` normalise ces valeurs avant de les écrire. Les événements de suivi recopient aussi ce contexte. Une ancienne sélection `touriste` est migrée vers `seul + is_visitor`.

## Contrat pour le futur chantier HB

Les signaux ne sont pas des exclusions rigides. Ils doivent modifier le scoring selon l'heure, le jour, la météo, le territoire et le profil.

- `is_visitor` favorise incontournables, découverte, patrimoine, Local Habits, Spotlights locaux et propositions caractéristiques du territoire.
- `is_15_17` favorise les contenus de jeune quasi-adulte tout en pénalisant ou excluant les offres réservées aux majeurs.
- `child_age_bands` recherche un compromis familial ; les poids des tranches ne doivent pas être simplement additionnés.

Les fenêtres horaires de référence sont : 6h–9h, 9h–11h30, 11h30–14h30, 14h30–17h30, 17h30–20h, 20h–22h, 22h–00h, 00h–2h et 2h–5h.

## État volontaire au terme de cette préparation

Seul `is_visitor` influence actuellement l'interface. Les contrôles 15–17 ans et tranches d'enfants sont conservés derrière un bloc PHP désactivé jusqu'au chantier qui raccordera ces signaux aux requêtes centralisées HB, IA et WTD.
