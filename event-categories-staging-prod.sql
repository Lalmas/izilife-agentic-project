START TRANSACTION;

INSERT INTO ActivityPrincipalCategory
    (name, string_id, usable, use_for_course, use_for_visit, use_for_festival)
SELECT 'Citoyenneté', 'citoyennete', 1, 1, 1, 1
WHERE NOT EXISTS (SELECT 1 FROM ActivityPrincipalCategory WHERE string_id = 'citoyennete');

INSERT INTO EventCategory
    (name, event_category_string_id, is_principal, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT 'Animation', 'animation', 1, 1, 1, 0, NULL
WHERE NOT EXISTS (SELECT 1 FROM EventCategory WHERE event_category_string_id = 'animation')
UNION ALL
SELECT 'Commémoration', 'commemoration', 0, 1, 1, 0,
       (SELECT id FROM ActivityPrincipalCategory WHERE string_id = 'citoyennete')
WHERE NOT EXISTS (SELECT 1 FROM EventCategory WHERE event_category_string_id = 'commemoration');

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT 'Rencontre amicale', 'rencontre',
       COALESCE((SELECT id FROM EventCategory WHERE event_category_string_id = 'art-et-culture'), 0),
       1, 1, 0,
       COALESCE((SELECT id FROM ActivityPrincipalCategory WHERE string_id = 'art'), 0)
WHERE NOT EXISTS (SELECT 1 FROM EventCategory WHERE event_category_string_id = 'rencontre');

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Boum' AS name, 'boum-enfant' AS slug, 'animation-enfant' AS parent_slug, NULL AS second_slug, 1 AS needs_activity, NULL AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Lecture publique' AS name, 'lecture-publique' AS slug, 'litterature' AS parent_slug, 'conte' AS second_slug, 0 AS needs_activity, 'litterature' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Chasse aux œufs' AS name, 'chasse-aux-oeufs' AS slug, 'chasse-au-tresor' AS parent_slug, 'animation-enfant' AS second_slug, 0 AS needs_activity, 'jeux' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Geocaching' AS name, 'geocaching' AS slug, 'jeu-de-piste' AS parent_slug, 'jeux-en-plein-air' AS second_slug, 0 AS needs_activity, 'jeux' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Feu d''artifice' AS name, 'feu-d-artifice' AS slug, 'spectacle' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'spectacle' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Spectacle de drones' AS name, 'spectacle-de-drones' AS slug, 'spectacle-de-lumiere' AS parent_slug, 'spectacle-numerique' AS second_slug, 0 AS needs_activity, 'spectacle' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Mapping vidéo' AS name, 'mapping-video' AS slug, 'spectacle-de-lumiere' AS parent_slug, 'spectacle-numerique' AS second_slug, 0 AS needs_activity, 'spectacle' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Parcours lumineux' AS name, 'parcours-lumineux' AS slug, 'visite' AS parent_slug, 'spectacle-de-lumiere' AS second_slug, 0 AS needs_activity, 'art' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Parcours immersif' AS name, 'parcours-immersif' AS slug, 'visite' AS parent_slug, 'spectacle' AS second_slug, 0 AS needs_activity, 'art' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Parcours horreur' AS name, 'parcours-horreur' AS slug, 'visite' AS parent_slug, 'spectacle' AS second_slug, 0 AS needs_activity, 'art' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Drag show' AS name, 'drag-show' AS slug, 'cabaret' AS parent_slug, 'spectacle' AS second_slug, 0 AS needs_activity, 'cabaret' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Spectacle burlesque' AS name, 'burlesque' AS slug, 'cabaret' AS parent_slug, 'spectacle' AS second_slug, 0 AS needs_activity, 'cabaret' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Concert acoustique' AS name, 'concert-acoustique' AS slug, 'concert' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'musique' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Concert classique' AS name, 'concert-classique' AS slug, 'concert' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'musique' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Pièce de théâtre' AS name, 'piece-de-theatre' AS slug, 'theatre' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'theatre' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Théâtre de boulevard' AS name, 'theatre-de-boulevard' AS slug, 'theatre-comedie' AS parent_slug, 'theatre' AS second_slug, 0 AS needs_activity, 'theatre' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Réveillon' AS name, 'reveillon' AS slug, 'soiree' AS parent_slug, 'diner' AS second_slug, 0 AS needs_activity, 'musique' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Goûter' AS name, 'gouter' AS slug, 'alimentation' AS parent_slug, 'animation-enfant' AS second_slug, 0 AS needs_activity, 'a-manger' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Pique-nique' AS name, 'pique-nique' AS slug, 'alimentation' AS parent_slug, 'rencontre' AS second_slug, 0 AS needs_activity, 'a-manger' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Rassemblement food trucks' AS name, 'rassemblement-food-trucks' AS slug, 'festival-culinaire' AS parent_slug, 'alimentation' AS second_slug, 0 AS needs_activity, 'a-manger' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Guinguette' AS name, 'guinguette' AS slug, 'fete-et-musique' AS parent_slug, 'bal' AS second_slug, 0 AS needs_activity, 'musique' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Bal des pompiers' AS name, 'bal-des-pompiers' AS slug, 'bal' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'musique' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Soirée à thème' AS name, 'soiree-a-theme' AS slug, 'soiree' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'musique' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Soirée étudiante' AS name, 'soiree-etudiante' AS slug, 'soiree' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'musique' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Speed dating' AS name, 'speed-dating' AS slug, 'rencontre' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'art' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Atelier créatif DIY' AS name, 'atelier-creatif' AS slug, 'atelier' AS parent_slug, 'art-et-culture' AS second_slug, 1 AS needs_activity, NULL AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Atelier peinture' AS name, 'atelier-peinture' AS slug, 'atelier' AS parent_slug, 'art-et-culture' AS second_slug, 1 AS needs_activity, NULL AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Atelier céramique' AS name, 'atelier-ceramique' AS slug, 'atelier' AS parent_slug, 'art-et-culture' AS second_slug, 1 AS needs_activity, NULL AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Atelier poterie' AS name, 'atelier-poterie' AS slug, 'atelier' AS parent_slug, 'art-et-culture' AS second_slug, 1 AS needs_activity, NULL AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Atelier couture' AS name, 'atelier-couture' AS slug, 'atelier' AS parent_slug, 'mode' AS second_slug, 1 AS needs_activity, NULL AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Atelier tricot' AS name, 'atelier-tricot' AS slug, 'atelier' AS parent_slug, 'mode' AS second_slug, 1 AS needs_activity, NULL AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Atelier floral' AS name, 'atelier-floral' AS slug, 'atelier' AS parent_slug, 'jardinage' AS second_slug, 1 AS needs_activity, NULL AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Atelier écriture' AS name, 'atelier-ecriture' AS slug, 'atelier' AS parent_slug, 'litterature' AS second_slug, 1 AS needs_activity, NULL AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Atelier théâtre' AS name, 'atelier-theatre' AS slug, 'atelier' AS parent_slug, 'theatre' AS second_slug, 1 AS needs_activity, NULL AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Atelier musique' AS name, 'atelier-musique' AS slug, 'atelier' AS parent_slug, 'fete-et-musique' AS second_slug, 1 AS needs_activity, NULL AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Atelier photo' AS name, 'atelier-photo' AS slug, 'atelier' AS parent_slug, 'art-et-culture' AS second_slug, 1 AS needs_activity, NULL AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Atelier numérique' AS name, 'atelier-numerique' AS slug, 'atelier' AS parent_slug, NULL AS second_slug, 1 AS needs_activity, NULL AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Repair Café' AS name, 'repair-cafe' AS slug, 'atelier' AS parent_slug, 'maison' AS second_slug, 1 AS needs_activity, NULL AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Atelier enfant' AS name, 'atelier-enfant' AS slug, 'atelier' AS parent_slug, 'animation-enfant' AS second_slug, 1 AS needs_activity, NULL AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Marché nocturne' AS name, 'marche-nocturne' AS slug, 'marche' AS parent_slug, 'marches-braderie-et-brocante' AS second_slug, 0 AS needs_activity, 'marches-et-brocantes' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Marché gourmand' AS name, 'marche-gourmand' AS slug, 'marche' AS parent_slug, 'alimentation' AS second_slug, 0 AS needs_activity, 'marches-et-brocantes' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Marché aux fleurs' AS name, 'marche-aux-fleurs' AS slug, 'marche' AS parent_slug, 'jardinage' AS second_slug, 0 AS needs_activity, 'marches-et-brocantes' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Troc aux plantes' AS name, 'troc-aux-plantes' AS slug, 'troc' AS parent_slug, 'jardinage' AS second_slug, 0 AS needs_activity, 'event-business' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Bourse aux vélos' AS name, 'bourse-aux-velos' AS slug, 'marches-braderie-et-brocante' AS parent_slug, 'sport' AS second_slug, 0 AS needs_activity, 'marches-et-brocantes' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Bourse de collectionneurs' AS name, 'bourse-collectionneurs' AS slug, 'marches-braderie-et-brocante' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'marches-et-brocantes' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Dédicace' AS name, 'dedicace' AS slug, 'art-et-culture' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'art' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Murder party' AS name, 'murder-party' AS slug, 'escape-game' AS parent_slug, 'jeux' AS second_slug, 0 AS needs_activity, 'jeux' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Jeu de rôle' AS name, 'jeu-de-role' AS slug, 'jeux-de-societe' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'jeux-de-societe' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Randonnée pédestre' AS name, 'randonnee' AS slug, 'sortie-sportive' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'sport' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Marche gourmande' AS name, 'marche-gourmande' AS slug, 'sortie-sportive' AS parent_slug, 'alimentation' AS second_slug, 0 AS needs_activity, 'sport' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Sortie vélo' AS name, 'sortie-velo' AS slug, 'sortie-sportive' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'sport' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Bain givré' AS name, 'bain-en-mer' AS slug, 'sortie-sportive' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'sport' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Sortie nature' AS name, 'sortie-nature' AS slug, 'visite' AS parent_slug, 'jardinage' AS second_slug, 0 AS needs_activity, 'art' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Observation des étoiles' AS name, 'observation-etoiles' AS slug, 'art-et-culture' AS parent_slug, 'animation' AS second_slug, 0 AS needs_activity, 'art' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Gala sportif' AS name, 'gala-sportif' AS slug, 'sport' AS parent_slug, 'spectacle' AS second_slug, 0 AS needs_activity, 'sport' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Compétition sportive' AS name, 'competition-sportive' AS slug, 'sport' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'sport' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Initiation sportive' AS name, 'initiation-sportive' AS slug, 'seance-de-sport' AS parent_slug, 'sport' AS second_slug, 0 AS needs_activity, 'sport' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Emballage cadeaux solidaire' AS name, 'emballage-cadeaux-solidaire' AS slug, 'benevolat' AS parent_slug, 'collecte' AS second_slug, 1 AS needs_activity, NULL AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Vœux de la municipalité' AS name, 'voeux-municipalite' AS slug, 'commemoration' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'citoyennete' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Cérémonie officielle' AS name, 'ceremonie-officielle' AS slug, 'commemoration' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'citoyennete' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Célébration religieuse' AS name, 'celebration-religieuse' AS slug, 'commemoration' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'citoyennete' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Réunion publique' AS name, 'reunion-publique' AS slug, 'conference' AS parent_slug, NULL AS second_slug, 1 AS needs_activity, NULL AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Forum des associations' AS name, 'forum-des-associations' AS slug, 'salon' AS parent_slug, NULL AS second_slug, 1 AS needs_activity, NULL AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Ducasse' AS name, 'ducasse' AS slug, 'fete-foraine' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'jeux' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Animation municipale' AS name, 'animation-municipale' AS slug, 'animation' AS parent_slug, NULL AS second_slug, 1 AS needs_activity, NULL AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Déambulation' AS name, 'deambulation' AS slug, 'parade' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'musique' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Rencontre fraternelle' AS name, 'rencontre-fraternelle' AS slug, 'rencontre' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'art' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

INSERT INTO EventCategory
    (name, event_category_string_id, parent_id, second_parent_id, free_use_by_user,
     is_usable_for_programmation, need_principal_activity_category, principal_activity_category)
SELECT source.name, source.slug, COALESCE(parent.id, 0) AS parent_id,
       CASE WHEN source.second_slug IS NULL THEN NULL ELSE COALESCE(second_parent.id, 0) END AS second_parent_id,
       1 AS free_use_by_user, 1 AS is_usable_for_programmation, source.needs_activity,
       CASE WHEN source.activity_slug IS NULL THEN NULL ELSE COALESCE(activity.id, 0) END AS principal_activity_category
FROM (
    SELECT 'Déambulation de Noël' AS name, 'deambulation-de-noel' AS slug, 'deambulation' AS parent_slug, NULL AS second_slug, 0 AS needs_activity, 'musique' AS activity_slug
) AS source
LEFT JOIN EventCategory AS parent ON parent.event_category_string_id = source.parent_slug
LEFT JOIN EventCategory AS second_parent ON second_parent.event_category_string_id = source.second_slug
LEFT JOIN ActivityPrincipalCategory AS activity ON activity.string_id = source.activity_slug
WHERE NOT EXISTS (
    SELECT 1 FROM EventCategory WHERE event_category_string_id = source.slug
);

COMMIT;
