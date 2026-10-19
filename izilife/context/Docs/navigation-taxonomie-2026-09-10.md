# Navigation et taxonomie — état du 10 septembre 2026

## Source et statut

Source de référence analysée : `C:\xampp\htdocs\izilife-admin\statics\izilife_new_version\01_navigation.sql`, modifiée le 10 septembre 2026 (93 142 octets).

La comparaison avec `01_navigation_old.sql` représente 797 ajouts et 536 suppressions. L'import principal a été refondu pour MySQL : transaction explicite, `INSERT IGNORE`, résolution des parents par variables au lieu d'identifiants numériques figés et classement des profils avec `ON DUPLICATE KEY UPDATE`.

## Modèle de données

- `AppEntityType` normalise six types : Shop, Place, Experience, Event, Circuit et Session.
- `UserTourismProfileType` définit six profils : famille, seul, couple, amis, étudiant et touriste.
- `NavigationCategory` porte l'arbre de navigation, les fenêtres temporelles, le ciblage territorial et profil, les liens spéciaux, les icônes et les indicateurs de visibilité/recherche/section applicative.
- `NavigationCategoryEntities` associe une catégorie aux types d'entités qu'elle peut retourner.
- `ProfileNavigationCategories` ordonne les catégories par profil touristique.
- `DirectoryCategoryGroup` et `DirectoryCategory` structurent l'annuaire.
- `NavigationSubCategory` et `NavigationSubCategoryContent` fournissent une taxonomie secondaire réutilisable.

## Nouveaux espaces et catégories notables

- Navigation principale étendue : Sport et Danser sont activés ; Spotlights devient Tendances ; ajout d'Activités nautiques, Plages, Sunset, Se rafraîchir et Pique-niquer. Rooftops et Guinguettes deviennent enfants de Terrasses.
- Manger est approfondi avec Café Croissant, Déjeuner, Dîner, Manger vite, Sandwichs, Manger pas cher et Manger en plein air ; Boire reçoit Apéro plein air et Apéro pique-nique.
- Nouveaux ensembles détaillés pour Beauté/Bien-être, Flâner, Jouer, S'évader, Escapades, Chiner, Shopping, Sessions live, Étudiants, Art et Se détendre.
- Se rafraîchir est saisonnier de mai à septembre avec parcs ombragés, lieux climatisés, baignade, terrasses fraîches, boissons fraîches, fontaines, activités indoor et enfants.
- Deals : Izilife+, codes promos, happy hours et promotions étudiantes.
- Spotlights : bord de l'eau, rooftops, romantique, sunset, nouveaux lieux, tendances, terrasses, lieux secrets, vues panoramiques, pluie et famille.
- Sport : Communautés & Groupes, Clubs & Assos, Événements, Sessions & entraînements et Équipements ; filtres Running & Rando, Fitness & Cross training, Vélo, Raquette, Combat, Escalade & Accrobranche.
- Outdoor : espace racine avec À pied, Running, À vélo, Spots et Circuits.
- Pages transversales : Mis en avant, Events Izilife, Séries Izilife, Coups de cœur et Grands RDV annuels.
- Catégories futures inactives : Petits concerts locaux, Balade nocturne, Vacances, Planning opportunities et ses sous-catégories. Elles ne doivent pas apparaître avant activation fonctionnelle.
- Saisonnalité et profils : Terrasses et Pique-niquer sont actifs d'avril à septembre ; Se rafraîchir de mai à septembre ; plusieurs entrées sont liées au profil étudiant. Le nouveau classement renseigne cinq profils (famille, seul, couple, amis et étudiant) ; aucun bloc Touriste n'apparaît dans cette version.

## Conséquences pour les moteurs et le code

1. Les moteurs ne doivent plus supposer qu'une catégorie ne renvoie qu'un seul objet : le contrat passe par `NavigationCategoryEntities` et inclut désormais les Sessions.
2. `special_management_url` désigne une page ou un traitement spécialisé ; les routes correspondantes doivent exister pour Outdoor, Sport, Deals, Spotlights et les pages transversales.
3. Le filtrage doit appliquer `is_active`, les dates/mois d'activité, le territoire, `linked_profile_type_id` et `not_visible_for_child` avant classement.
4. L'ordre de navigation doit provenir de `ProfileNavigationCategories`, pas d'une liste codée en dur dans les vues.
5. L'annuaire (`DirectoryCategory*`) et la navigation (`NavigationCategory*`) sont deux taxonomies distinctes ; ne pas les fusionner implicitement.
6. Les doublons sémantiques sont intentionnels selon le contexte (par exemple Terrasses, Sport/Outdoor, Événements) : utiliser les `string_id` comme contrats stables.

## Ordre de déploiement recommandé

Local → staging → production. Valider à chaque étape la migration SQL, les clés étrangères, l'unicité des `string_id` et `special_management_url`, les routes spécialisées, les icônes, les résultats multi-entités, les positions sans doublon et les fenêtres saisonnières. Clarifier aussi le sort du profil Touriste avant déploiement.
