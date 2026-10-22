# Audit complet des Home Blocks

Audit du 14 octobre 2026 portant sur les 104 entrées de
`get_home_blocks_catalog()`, leur builder réel et leur rôle métier.

## Légende

- **OK** : définition exploitable et cohérente avec le nom du rail.
- **CORRIGÉ** : écart trouvé et corrigé pendant l'audit.
- **À CHALLENGER** : techniquement branché, mais la promesse éditoriale doit être précisée.
- **VIDE** : le catalogue appelle volontairement `HB_build_empty_home_block_definition`.
- **SPÉCIAL** : alimenté par un parcours différent du moteur multi-objets classique.

## 1. Système, compte et actions

| HB | Définition réelle | État |
|---|---|---|
| `sponsored_partners` | Partenaires sponsorisés, builder dédié. | OK |
| `user_agenda` | Agenda du compte connecté. | OK |
| `user_liked_all` | Tous les favoris utilisateur. | OK |
| `user_liked_places` | Favoris de type lieu. | OK |
| `user_liked_events` | Favoris de type événement. | OK |
| `user_liked_experiences` | Favoris de type expérience. | OK |
| `ideas_to_do` | Rail d'IndependentActions, pas une requête d'objets. | SPÉCIAL |
| `good_deals` | Agrégation des offres/deals achetables dans leur fenêtre de validité, avec injection de l'abonnement iziLife offert lorsqu'il est actif. | OK ; une opération simplement marquée `active` mais expirée n'est pas affichée. |
| `subscriber_promos` | Avantages d'abonnement ; affinité profil puis distance. | CORRIGÉ |
| `student_promos` | Promos réellement marquées étudiantes. | OK |

## 2. Maintenant, aujourd'hui et événements

| HB | Définition réelle | État |
|---|---|---|
| `what_now_events` | Événements pertinents maintenant. | OK |
| `what_now_experiences` | Expériences disponibles maintenant. | OK |
| `tonight_ideas` | Idées du soir ; même builder que `tonight_around`. | OK |
| `tonight_around` | Idées du soir autour de la position. | OK |
| `events_today` | Événements du jour. | OK |
| `weekend_events` | Événements du prochain week-end. | OK |
| `local_events` | Événements de proximité. | OK |
| `around_you` | Aucun builder métier et absent des cinq listes de profils. | DÉBRANCHÉ |
| `new_places` | Objets récents, classement par nouveauté. | OK |

## 3. Manger, boire et cafés

| HB | Définition réelle | État |
|---|---|---|
| `breakfast_spots` | Commerces servant un petit déjeuner. | OK |
| `cafes_open_morning` | Cafés ouverts le matin. | OK |
| `brunch_spots` | Brunch déclaré, avec ses horaires/offres spécifiques. | OK |
| `lunch_spots` | Restauration adaptée au déjeuner. | OK |
| `snack_spots` | Goûter/snacking. | OK |
| `sweet_spots` | Pâtisseries, glaciers, chocolatiers, confiseries et salons de thé. | OK |
| `dinner_spots` | Restauration du soir. | OK |
| `where_to_eat_tonight` | Alias éditorial de `dinner_spots`. | OK |
| `local_food` | Adresses liées aux spécialités/local food. | OK |
| `street_food` | Catégories street-food et restauration rapide dédiée. | OK |
| `cheap_eats` | Prix bas ou signaux petit budget/étudiant. | OK |
| `drinks_tonight` | Bars et lieux pour boire ce soir. | OK |
| `happy_hour` | Happy hours actifs ; conserve le parcours modal intermédiaire. | OK |
| `student_happy_hour` | Happy hours adaptés au profil étudiant. | OK |
| `afterwork_spots` | Tags/atmosphères afterwork, groupe ou ambiance adaptée. | OK |
| `bars_terraces` | Bars possédant une vraie terrasse. | OK |
| `best_terraces` | Terrasses avec signaux qualitatifs/vue. | OK |
| `wine_bars` | Bars à vin. | OK |
| `cozy_cafes` | Café/salon de thé + atmosphère `cosy`, ou tags `ambiance-posee`/`intimiste`. | CORRIGÉ |
| `trendy_restaurants` | Utilise `importance_in_city` comme note éditoriale stable de connaissance/importance locale, indépendante du trafic iziLife. | DÉCIDÉ : champ conservé ; libellé public « Restaurants connus dans la ville ». |
| `trendy_bars` | Utilise `importance_in_city` comme note éditoriale stable de connaissance/importance locale, indépendante du trafic iziLife. | DÉCIDÉ : champ conservé ; libellé public « Bars connus dans la ville ». |
| `student_bars` | Bars explicitement étudiants/petit budget. | OK |
| `first_part_bar` | Bar adapté à un début de soirée. | OK |
| `bar_ambiance` | Bars avec ambiance déclarée. | OK |
| `trendy_discotheques` | Fiches commerces de catégorie réelle `discotheque` ; `club` et `bar-dansant` n'existent pas dans `ShopCategory`, les bars lounge sont exclus et aucun événement n'est agrégé actuellement. | CONSERVÉ ; recherche directe à 100 km pour le bassin régional/transfrontalier. |
| `ou_drink_and_play` | Lieux combinant boisson et jeu. | OK |
| `late_night_kebabs` | Kebabs/tacos ouverts tard. | OK |
| `lunch_terrace_spots` | Déjeuner avec terrasse. | OK |
| `drinks_terrace` | Boire avec terrasse. | OK |

## 4. Sorties, musique, culture et jeu

| HB | Définition réelle | État |
|---|---|---|
| `local_concerts` | Petites scènes et concerts locaux. | OK |
| `party_events` | Événements festifs/nocturnes. | OK |
| `student_parties` | Soirées portant les signaux ou catégories étudiantes. | OK |
| `sortir-nuit` | Bars nocturnes, clubs et sorties tardives. | OK |
| `standup_shows` | Stand-up, humour et comedy clubs via les vraies catégories. | OK |
| `markets` | Marchés permanents et événements de marché. | OK |
| `museums_now` | Lieux de type réel `musee`, ouverts au moment de la requête ; visible pour les cinq profils et relié au WTD Musées & Galeries. | CORRIGÉ |
| `places_to_play` | Lieux de jeu réels. | OK |
| `playgrounds` | Aires de jeux. | OK |
| `highlights` | Spotlights éditoriaux multi-objets. | OK |
| `highlighted_events` | Événements mis en avant. | OK |
| `partners` | Partenaires mis en avant. | OK |
| `izilife_partner_events` | Événements opérés par des partenaires iziLife. | OK |

## 5. Famille, enfants, sport et groupes

| HB | Définition réelle | État |
|---|---|---|
| `kids_activities` | Moteur multi-objets strict enfants/famille. | CORRIGÉ |
| `kids_activities_mixed` | Variante mixte reposant sur la même exigence enfant. | CORRIGÉ |
| `kids_events` | Événements explicitement enfants. | OK |
| `family_walks` | Balades adaptées aux familles. | OK |
| `kids_snack` | Goûters adaptés aux enfants. | OK |
| `kids_restaurants` | Restaurants réellement adaptés aux enfants/familles. | OK |
| `creative_workshops` | Ateliers créatifs adaptés au profil famille. | OK |
| `kids_sports` | Sports/activités sportives enfants. | OK |
| `family_weekend` | Propositions de week-end familial. | OK |
| `sport_activities` | Lieux où pratiquer un sport. | OK |
| `sport_groups` | XP sportives `activite-collective` rattachées à une communauté/un groupe, plus événements de séance, sortie ou cours sportif collectif même indépendants. Les soirées et compétitions génériques sont exclues. | CORRIGÉ ; aucune carte Community/CommunityActivity. MeetZ pourra devenir une source ultérieure. |
| `dance_groups` | Activités et communautés de danse. | OK |

## 6. Profils solo et couple

| HB | Définition réelle | État |
|---|---|---|
| `solo_experiences` | Tous types d'objets, mais uniquement avec `bien-en-solo`. | CORRIGÉ |
| `romantic_restaurants` | Restaurant + signal romantique/date/couple. | OK |
| `romantic_bars` | Bar + signal romantique/date/couple. | OK |
| `romantic_places` | Lieu public + signal romantique/date/intimiste. | OK, volontairement étroit. |
| `romantic_walks` | Balade + signal romantique/date. | OK |
| `date_ideas` | Objets reliés à l'occasion Date/GOOD_FOR. | OK |
| `couple_experiences` | Expériences adaptées au couple/date. | OK |
| `couple_late_night_experiences` | Variante couple disponible tard. | OK |
| `detente_couple` | Bien-être/détente adaptés au couple. | OK |
| `weekend_for_two` | Escapades adaptées au couple. | OK |

## 7. Découverte locale, météo et curation

| HB | Définition réelle | État |
|---|---|---|
| `life_areas` | Types collectifs ou tag explicite `lieu-de-vie-local`; la notoriété seule ne suffit plus. | CORRIGÉ |
| `trendy_places` | Spotlights actifs multi-objets ; renommé **Tendances**. | CORRIGÉ |
| `must_see` | Incontournables via signaux dédiés. | OK |
| `city_districts` | Quartiers/zones urbaines à découvrir. | OK |
| `local_experiences` | Expériences locales. | OK |
| `unusual_activities` | `is_insolite` ou tag insolite explicite. | OK |
| `rainy_day_ideas` | Objets reliés à `VisitWeather=pluvieux`, tags pluie/intérieur, atmosphère cosy ou XP explicitement intérieure. | CORRIGÉ multi-objets |
| `sunny_day_ideas` | Objets reliés à `VisitWeather=ensoleille`, tags extérieurs/soleil ou commerces avec terrasse. | CORRIGÉ multi-objets |
| `study_places` | Alias de cafés/lieux pour travailler. | OK |
| `work_friendly_cafes` | Café + signaux travail, calme ou wifi. | OK |

Les anciens placeholders `hot_weather_spots`, `cold_weather_spots`,
`indoor_when_raining` et `outdoor_when_sunny` ont été retirés du catalogue.
La Home conserve uniquement les deux intentions météo actives ci-dessus ; la
forte chaleur reste couverte par le WTD spécialisé `se-rafraichir`.
Le schéma Spotlight accepte une condition et une raison météo, mais aucune
donnée locale ne les utilise actuellement. Surtout, LocalQuery ne confronte pas
encore `SpotlightRule.weather_condition_id` à la météo courante : ces règles ne
doivent pas être activées avant ce raccordement.

## 8. Escapades et géographie

| HB | Définition réelle | État |
|---|---|---|
| `cities_to_discover_nearby` | `EscapadeProposal` proches et actives. | OK |
| `international_city_trips` | Aucun builder métier. | DIFFÉRÉ volontairement |
| `major_cities_1h_2h` | Aucun builder métier. | DIFFÉRÉ volontairement |
| `geographic_areas_to_explore` | Aucun builder métier. | DIFFÉRÉ volontairement |
| `country_international_cities` | Aucun builder métier. | DIFFÉRÉ volontairement |

Les quatre blocs vides sont actuellement placés dans tous les profils. Ils ne
produisent pas de cartes, mais encombrent la configuration et doivent être soit
définis, soit retirés des listes de profils.

## 9. Features iziLife

| HB | Définition réelle | État |
|---|---|---|
| `selection_boxes` | Builder classique vide ; contenu attendu par le parcours Sélections. | DIFFÉRÉ volontairement |
| `meetz_categories` | Builder classique vide ; contenu attendu par Meetz. | DIFFÉRÉ volontairement |
| `izilife_signature_events` | Builder classique vide ; contenu signature attendu ailleurs. | DIFFÉRÉ volontairement |
| `meetz_feature` | Feature sans builder d'objets. | DIFFÉRÉ volontairement |
| `selection_feature` | Feature sans builder d'objets. | DIFFÉRÉ volontairement |
| `subscription_feature` | Feature sans builder d'objets. | DIFFÉRÉ volontairement |

Ces six blocs ne doivent pas être déclarés « fonctionnels » par l'audit du
moteur classique. Leur rendu doit être vérifié dans leur parcours spécialisé.

## Décisions et anomalies restantes

1. Décider comment distinguer connaissance locale, importance structurelle et
   tendance avant de modifier les blocs `trendy_*`.
2. Étendre ultérieurement `sport_groups` à certains MeetZ sportifs sans y
   afficher directement les communautés.
3. Les quatre blocs géographiques présents dans les profils sont différés
   volontairement et ne sont plus signalés comme erreurs par l'audit.
4. Enrichir `rainy_day_ideas` et `sunny_day_ideas` avec les raisons météo
   Spotlight ; aucun rail Home séparé grand froid/forte chaleur n'est retenu.
5. Les six blocs iziLife/Meetz/Sélections sont différés volontairement et
   devront être testés lors de leur activation dédiée.
