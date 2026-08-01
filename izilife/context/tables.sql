
#region Partenaire
CREATE TABLE `PartnerCategory` (
  `id` smallint NOT NULL primary key auto_increment,
  `name` varchar(50) NOT NULL,
  `string_id` varchar(50) NOT NULL,

  `is_active` tinyint(1) NOT NULL default 1,
  `is_usable_for_network` tinyint(1) NOT NULL default 1,
  `is_usable_for_partner` tinyint(1) NOT NULL default 1,

  is_for_place boolean default 0,

  need_shop_category boolean default 0,
  need_place_type boolean default 0,

  parent_id smallint default null,

  foreign key(parent_id) references PartnerCategory(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `PartnerCategory` (id, `name`, `string_id`, parent_id, is_usable_for_partner, is_usable_for_network, need_shop_category, is_for_place, need_place_type) values
  (1, 'Distributeurs', 'distributeur', NULL, 1, 0, 0, 0, 0),
  (2, 'Marque', 'marque', NULL, 1, 0, 0, 0, 0),
  (3, 'Bien-être & Beauté', 'bien-etre-et-beaute', NULL, 1, 0, 0, 0, 0),
  (4, 'Restauration', 'restauration', NULL, 1, 0, 0, 0, 0),
  (5, 'Bars, Discotheques & autres', 'bars-discotheques-et-autres', NULL, 1, 0, 0, 0, 0),
  (6, 'Transport', 'transport', NULL, 0, 0, 0, 0, 0),

  (7, 'Parcs & Loisirs', 'parcs-et-loisirs', NULL, 0, 0, 0, 1, 0),
  (8, 'Centres commerciaux', 'centres-commeriaux', NULL, 0, 0, 0, 1, 0),
  (9, 'Hotellerie', 'hotellerie', NULL, 0, 0, 0, 1, 0),
  
  (10, 'Place multi-activités', 'place-multi-activites', NULL, 0, 0, 0, 1, 0),
  (11, 'Autres places', 'autres-places', NULL, 0, 0, 0, 1, 0),
  (12, 'Autres commerces', 'autres-commerces', NULL, 0, 0, 1, 0, 0);

INSERT INTO `PartnerCategory` (id, `name`, `string_id`, parent_id, is_usable_for_partner, is_usable_for_network, need_shop_category, is_for_place, need_place_type) values
-- Distributeurs 
  (13, 'Généraliste', 'distributeur-generaliste', 1, 1, 1, 0, 0, 0),
  (14, 'Alimentation', 'distributeur-alimentation', 1, 1, 1, 0, 0, 0),
  (15, 'Hygiène & Beauté', 'distributeur-hygiene-et-beaute', 1, 1, 1, 1, 0, 0),
  (16, 'Articles de Sport', 'distributeur-articles-de-sport', 1, 1, 1, 1, 0, 0),
  (17, 'Prêt à porter', 'distributeur-pret-a-porter', 1, 1, 1, 1, 0, 0),
  (18, 'Electronique & Electroménager', 'distributeur-electronique-et-electromenager', 1, 1, 1, 1, 0, 0),
  (19, 'Ameublement, Décoration & Travaux', 'distributeur-ameublement-decoration-et-travaux', 1, 1, 1, 1, 0, 0),
  (20, 'Jardins & Fleurs', 'distributeur-jardins-et-fleurs', 1, 1, 1, 1, 0, 0),
  (21, 'Jouet', 'distributeur-jouet', 1, 1, 1, 0, 0, 0),
  (22, 'Loisirs Culturels', 'distributeur-loisirs-culturels', 1, 1, 1, 0, 0, 0),
  (23, 'Pièces Voiture & Moto', 'distributeur-pieces-voiture-et-moto', 1, 1, 1, 0, 0, 0),
  (24, 'Articles de vélo', 'distributeur-articles-de-velo', 1, 1, 1, 0, 0, 0),

-- Marques 
  (25, 'Alimentation', 'marque-alimentation', 2, 1, 0, 0, 0, 0),
  (26, 'Boissons', 'marque-boissons', 2, 1, 0, 0, 0, 0),
  (27, 'Hygiène & Beauté', 'marque-hygiene-et-beaute', 2, 1, 0, 0, 0, 0),
  (28, 'Articles de Sport', 'marque-articles-de-sport', 2, 1, 0, 0, 0, 0),
  (29, 'Prêt à porter', 'marque-pret-a-porter', 2, 1, 0, 0, 0, 0),
  (30, 'Produits électroniques', 'marque-produits-electroniques', 2, 1, 0, 0, 0, 0),
  (31, 'Produits électroménager', 'marque-produits-electromenager', 2, 1, 0, 0, 0, 0),
  (32, 'Ameublement, Décoration & Travaux', 'marque-ameublement-decoration-et-travaux', 2, 1, 0, 0, 0, 0),
  (33, 'Jouet', 'marque-jouet', 2, 1, 0, 0, 0, 0),
  (34, 'Loisirs Culturels', 'marque-loisirs-culturels', 2, 1, 0, 0, 0, 0),
  (35, 'Pièces Voiture & Moto', 'marque-pieces-voiture-et-moto', 2, 1, 0, 0, 0, 0),
  (36, 'Articles de vélo', 'marque-articles-de-velo', 2, 1, 0, 0, 0, 0),
  (37, 'Articles de trotinette & autres', 'marque-articles-de-trotinette-et-autres', 2, 1, 0, 0, 0, 0),
  (38, 'Constructeur de voiture', 'constructeur-de-voiture', 2, 1, 0, 0, 0, 0),
-- Bien-être & Beauté 
  (39, 'Salon de coiffure & babier', 'salon-de-coiffure-et-barbier', 3, 1, 1, 1, 0, 0),
  (40, 'Institut de beauté', 'institut-de-beaute', 3, 1, 1, 1, 0, 0),
  (41, 'Spa & Hammam', 'spa-et-hamam', 3, 1, 1, 1, 0, 0),

-- Restauration 
  (42, 'Restaurant', 'restaurant', 4, 1, 1, 0, 0, 0),
  (43, 'Fast-food', 'fast-food', 4, 1, 1, 0, 0, 0),
  (44, 'Street food', 'street-food', 4, 1, 1, 0, 0, 0),
  (45, 'Brasseries & Bistros', 'brasseries-et-bistros', 4, 1, 1, 0, 0, 0),
  (46, 'Café, Boulangerie & Patisserie', 'cafe-boulangerie-et-patisserie', 4, 1, 1, 0, 0, 0),

-- Transport 
  (47, 'Transport en commun', 'transport-en-commun', 5, 1, 0, 0, 0, 0),
  (48, 'Taxi', 'taxi', 5, 1, 0, 0, 0, 0),
  (49, 'Vtc', 'vtc', 5, 1, 0, 0, 0, 0),
  (50, 'Vélo libre-service', 'velo-libre-service', 5, 1, 0, 0, 0, 0),
  (51, 'Trotinette libre-service', 'trotinette-libre-service', 5, 1, 0, 0, 0, 0),

-- Services 
  (52, 'Assurance', 'assurance', 6, 1, 0, 0, 0, 0),
  (53, 'Garage, Pièces détachées', 'garage-pieces-detachees', 6, 1, 1, 1, 0, 0),
  (54, 'Agence Immo', 'agence-immobiliere', 6, 1, 1, 0, 0, 0),
  (55, 'Notaire', 'notaire', 6, 1, 0, 0, 0, 0),
  (56, 'Opticien', 'opticien', 6, 1, 1, 0, 0, 0);

INSERT INTO `PartnerCategory` (id, `name`, `string_id`, parent_id, is_usable_for_partner, is_usable_for_network, need_shop_category, is_for_place, need_place_type) values
  (57, 'Association', 'association', NULL, 1, 0, 0, 0, 0),
  (58, 'ONG', 'ong', NULL, 1, 0, 0, 0, 0)

;


CREATE TABLE `Network` (
  `id` bigint NOT NULL primary key auto_increment,
  `name` varchar(200) NOT NULL,
  `network_string_id` varchar(200) NOT NULL,

  partner_category smallint default null, 
  `shopCatagory` int(11) default NULL,
  `place_type` smallint unsigned default NULL,

  `is_with_franchise` tinyint(1) NOT NULL DEFAULT 0,
  `partner_id` bigint DEFAULT NULL,
  `created` datetime NOT NULL DEFAULT current_timestamp(),
  `is_active` tinyint(1) NOT NULL DEFAULT 1,

  parent_id bigint default null, 
  network_activity_level tinyint unsigned not null, -- 1 - International, 2  National, 3 - Régional

  foreign key(parent_id) references Network(id),
  foreign key(partner_category) references PartnerCategory(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `Network`
--

INSERT INTO `Network` (`name`, `network_string_id`, `shopCatagory`, `is_with_franchise`, `partner_id`, `is_active`, partner_category, network_activity_level) VALUES
('Auchan', 'auchan', NULL, 1, NULL, 1, 8, 1),
('Carrefour', 'carrefour', NULL, 1, NULL, 1, 8, 1),
('Leclerc', 'leclerc', NULL, 1, NULL, 1, 8, 1),
('Lidl', 'lidl', NULL, 1, NULL, 1, 8, 1),
('Aldi', 'aldi', NULL, 1, NULL, 1, 8, 1),
('Grand Frais', 'grand-frais', NULL, 1, NULL, 1, 8, 1),

("McDonald’s", 'mcdonalds', NULL, 1, NULL, 1, 43, 1),
('KFC', 'kfc', NULL, 1, NULL, 1, 43, 1),
('Burger King', 'burger-king', NULL, 1, NULL, 1, 43, 1)

;
-- --------------------------------------------------------


CREATE TABLE `Place` (
  `id` bigint NOT NULL,
  `name` varchar(200) NOT NULL,
  `place_string_id` varchar(200) NOT NULL,
  unique_id varchar(32) default NULL unique,  

  `cover_picture` bigint unsigned default NULL,
  `principal_picture` bigint unsigned default NULL,

  `place_type` int NOT NULL,
  `is_shop_place` tinyint(1) NOT NULL DEFAULT 0,
  `phone_number` varchar(20) DEFAULT NULL,
  mail varchar(50) default null,

  is_transport_object_place boolean default 0,

  train_station_id bigint unsigned default NULL,
  subway_station_id bigint unsigned default NULL,
  tramway_stop_id bigint unsigned default NULL,

  `is_multi_category_place` tinyint(1) NOT NULL DEFAULT 0,
  `is_office` tinyint(1) NOT NULL DEFAULT 0,
  `listable` tinyint(1) NOT NULL DEFAULT 1,
  is_place_for_association boolean not null default 0,
  is_privatizable boolean default 0,
  use_seperated_menu boolean default 0, 
  closed_state_id tinyint unsigned default 1,
  multi_category_management_type tinyint unsigned default null, 

  is_new_in_city boolean default 0,
  opening_date date default null,
  is_unusual_activity boolean default 0,

  `is_for_eat` tinyint(1) NOT NULL DEFAULT 0,
  `is_for_sleep` tinyint(1) NOT NULL DEFAULT 0,
  `is_local_service_place` tinyint(1) NOT NULL DEFAULT 0,

  `address` varchar(100) NOT NULL,
  `address_complement` varchar(100) DEFAULT NULL,
  `longitude` float(10,5) DEFAULT NULL,
  `latitude` float(10,5) DEFAULT NULL,
  `zip_code` int(11) NOT NULL,
  `city` varchar(100) DEFAULT NULL,
  `city_id` bigint NOT NULL,
  administrative_division_id bigint unsigned default null, 

  osm_node_id bigint default NULL, 
  road_id bigint default NULL, 
  address_id bigint default NULL, 
  google_place_id varchar(50) default null,
  is_verified boolean default 0,
  is_claimed boolean default 0,

  `google_maps_iframe` varchar(500) default NULL,

  `is_country_principal_place` tinyint(1) NOT NULL DEFAULT 0,
  `is_region_principal_place` tinyint(1) NOT NULL DEFAULT 0,
  `is_department_principal_place` tinyint(1) NOT NULL DEFAULT 0,
  `is_city_principal_place` tinyint(1) NOT NULL DEFAULT 0,

  is_tourist_attraction boolean default 0,
  accessible_for_visit boolean default 0,
  is_building_to_see_from_outside tinyint(1) NOT NULL DEFAULT 0,
  place_location_frame tinyint unsigned default NULL, 

  is_owned_by_in_on_place boolean default 0, 
  is_multi_category_principale_place boolean default 0, 
  
  is_free_access_place boolean default 0,
  `basic_price` float DEFAULT 0,
  basic_price_currency smallint unsigned default 1,

  place_access_type tinyint unsigned default NULL, 
  place_booking_needed_for_access tinyint unsigned default NULL,

  `have_toilets` tinyint(1) NOT NULL DEFAULT 0,
  `toilets_accessibility` tinyint unsigned  NOT NULL DEFAULT 0,
  toilet_accessibility_minimum_buy decimal(10,2) unsigned  default NULL,
  toilet_accessibility_minimum_buy_currency smallint unsigned default 2,

  `place_of_life` tinyint(1) NOT NULL,
  `importance_in_city` tinyint unsigned NOT NULL DEFAULT 1,
  
  `price_text` text DEFAULT NULL,
  `hourly_text` text DEFAULT NULL,
  `access_text` tinytext DEFAULT NULL,
  `all_time_opened` tinyint(1) NOT NULL DEFAULT 0,
  `hourly_of_in_on_place` tinyint(1) NOT NULL DEFAULT 0,
  
  `created` datetime NOT NULL DEFAULT current_timestamp(),
  `is_active` tinyint(1) NOT NULL,
  is_degraded_mode BOOLEAN DEFAULT FALSE,

  `in_on_place` bigint DEFAULT NULL,
  `shop_id` bigint DEFAULT NULL,
  `is_part_of` bigint DEFAULT NULL,
  `partner_id` bigint DEFAULT NULL,

  `is_building` tinyint(1) NOT NULL DEFAULT 0,
  `number_of_floors` int(11) NOT NULL DEFAULT 0,
  `more_than_one_bloc` tinyint(1) NOT NULL DEFAULT 0,
  `number_of_levels` int(11) NOT NULL DEFAULT 1,
  `number_of_under_floors` int(11) DEFAULT NULL,

  `short_description` varchar(500) DEFAULT NULL,
  `description` text DEFAULT NULL,
  ai_description text default null,
  health_pass boolean default 0,

  overtourism_indicator tinyint unsigned default NULL,

  saving_default_language int default 1,

  creation_date Datetime default CURRENT_TIMESTAMP,
  google_place_details json default null, 

  
  foreign key(toilet_accessibility_minimum_buy_currency) references Currency(id),
  foreign key(basic_price_currency) references Currency(id),
  foreign key(place_access_type) references AccessType(id),
  foreign key(place_booking_needed_for_access) references AccessBookingNeeded(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `Shop` (
  `id` bigint NOT NULL,
  `name` varchar(100) NOT NULL,
  `shop_string_id` varchar(100) NOT NULL,

  unique_id varchar(32) default NULL unique,
  osm_node_id bigint default NULL, 
  google_place_id varchar(50) default null,

  is_verified boolean default 0,
  is_claimed boolean default 0,

  road_id bigint default NULL, 
  address_id bigint default NULL,
  
  `is_active` tinyint(1) DEFAULT 1,
  is_degraded_mode BOOLEAN DEFAULT FALSE,
  `online_shop` tinyint(1) NOT NULL DEFAULT 0,
  `physical_shop` tinyint(1) DEFAULT 1,
  `shop_type` int(1) NOT NULL,

  `is_itinerant` tinyint(1) NOT NULL DEFAULT 0,
  `itinerant_organisation_type` tinyint unsigned DEFAULT NULL,
  itinerant_vehicule_type tinyint unsigned default NULL,

  `importance_in_city` tinyint unsigned DEFAULT NULL,

  is_owned_by_in_on_place boolean default 0, 
  is_multi_category_shop boolean default 0,
  use_seperated_menu boolean default 0,
  is_multi_category_principale_shop boolean default 0, 

  multi_category_management_type tinyint unsigned default null, 

  is_popup_store boolean default 0,
  popup_store_start_date date default null, 
  popup_store_end_date date default null,

  closed_state_id tinyint unsigned default 1,

  is_privatizable boolean default 0,
  is_new_in_city boolean default 0,
  opening_date date default null,
  is_unusual_activity boolean default 0,

  `shopCategory_id` smallint NOT NULL,
  `secondShopCategory_id` smallint DEFAULT NULL,
  `thirdShopCategory_id` smallint DEFAULT NULL,
  `short_description` text DEFAULT NULL,
  ai_description text default null,

  `principal_picture` bigint unsigned DEFAULT NULL,
  `principal_cover` bigint unsigned DEFAULT NULL,

  `qr_code` varchar(200) DEFAULT NULL,
  
  `phone_number` varchar(20) DEFAULT NULL,
  `url_website` varchar(100) DEFAULT NULL,
  `url_facebook` varchar(255) DEFAULT NULL,
  `url_instagram` varchar(255) DEFAULT NULL,
  `partner_id` bigint default NULL,

  `listable` tinyint(1) NOT NULL DEFAULT 1,
  `network_id` bigint DEFAULT NULL,
  
  `self_delivery` tinyint(1) NOT NULL,
  `click_delivery_active` tinyint(1) NOT NULL default 0,
  `click_collect_active` tinyint(1) NOT NULL default 0,
  `click_collect_promo` tinyint(1) DEFAULT 0 default 0,
  `click_collect_promo_amount` int(11) DEFAULT 0 default 0,

  `have_fidelity_program` tinyint(1) NOT NULL DEFAULT 1,
  `is_cold_relay_point` tinyint(1) NOT NULL DEFAULT 0,
  `is_dry_relay` tinyint(1) NOT NULL DEFAULT 1,
  `is_clothes_relay` tinyint(1) NOT NULL DEFAULT 0,

  `cold_food_for_delivery_tour` tinyint(1) DEFAULT 0,
  `tour_minimum_order` float DEFAULT 0,
  `self_delivery_minimum_order` float DEFAULT 0,
  `now_delivery_minimum_order` float DEFAULT 0,
  `click_collect_minimum_order` float DEFAULT 0,
  `is_food_shop` tinyint(1) DEFAULT 1,
  `is_in_food_planning_program` tinyint(1) DEFAULT 0,
  `is_in_scooter_delivery_program` tinyint(1) DEFAULT 1,
  `is_in_collaborative_delivery_program` tinyint(1) DEFAULT 0,

  `sms_notification_number` varchar(10) DEFAULT NULL,
  `mail` varchar(100) default NULL,
  `haveTab` tinyint(1) DEFAULT 0,
  `user_principal_admin` bigint DEFAULT NULL,
  `connexion_password` varchar(512) default NULL,

  `receive_peoples` tinyint(1) NOT NULL DEFAULT 0,
  `have_toilets` tinyint(1) NOT NULL DEFAULT 0,
  `toilets_accessibility` tinyint unsigned NOT NULL DEFAULT 0,
  toilet_accessibility_minimum_buy decimal(10, 2) default NULL,
  toilet_accessibility_minimum_buy_currency smallint unsigned default 1,

  `basic_price` float DEFAULT 0,
  basic_price_currency smallint unsigned default 1,
  shop_access_type tinyint unsigned default NULL, 
  shop_booking_needed_for_access tinyint unsigned default NULL,

  `access_text` tinytext DEFAULT NULL,
  access_link tinytext default null,

  `address` varchar(100) DEFAULT NULL,
  `additional_address` varchar(100) DEFAULT NULL,
  `zip_code` varchar(5) Default NULL,
  `city_id` bigint NOT NULL,
  administrative_division_id bigint unsigned default null,
  `in_on_place` bigint DEFAULT NULL,
  `hourly_of_in_on_place` tinyint(1) NOT NULL DEFAULT 0,
  `google_maps_iframe` tinytext DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  shop_location_frame tinyint unsigned default NULL, 

  shop_country_code varchar(2) default 'FR',

  `created` datetime NOT NULL DEFAULT current_timestamp(),
  `updated` datetime DEFAULT NULL,
  `history` longtext DEFAULT NULL,

  `shop_hourly_text` varchar(200) DEFAULT NULL,
  
  `shop_building_type` int(11) DEFAULT NULL,
  `number_of_levels` int(11) DEFAULT 1,

  saving_default_language int default 1,
  creation_date Datetime default CURRENT_TIMESTAMP,

  is_speciality_business boolean default 0,
  shop_origin_id smallint unsigned default NULL,

  health_pass boolean default 0,
  google_place_details json default null,

  foreign key(basic_price_currency) references Currency(id),
  foreign key(toilet_accessibility_minimum_buy_currency) references Currency(id),
  foreign key(itinerant_organisation_type) references ItinerantOrganisationType(id),
  foreign key(itinerant_vehicule_type) references ItinerantVehiculeType(id),

  foreign key(shop_access_type) references AccessType(id),
  foreign key(shop_booking_needed_for_access) references AccessBookingNeeded(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `LocalEvent` (
  `id` bigint NOT NULL,
  `title` varchar(100) NOT NULL,

  local_event_official_name varchar(100) default null, 
  local_event_official_string_id varchar(100) unique default null, 
  event_string_id varchar(100) unique default null, 

  unique_id varchar(32) default NULL unique,

  principal_activity_category smallint unsigned default NULL,

  `event_category` smallint unsigned NOT NULL,
  `cover_picture` bigint unsigned default NULL,
  `is_online_event` tinyint(1) DEFAULT 0,
  `listable` tinyint(1) NOT NULL DEFAULT 1,
  `multiple_places` tinyint(1) NOT NULL DEFAULT 0,
  
  `event_in_all_city` tinyint(1) NOT NULL DEFAULT 0,

  `is_active` tinyint(1) NOT NULL DEFAULT 0,
  is_degraded_mode BOOLEAN DEFAULT FALSE,
  `is_tour` tinyint(1) NOT NULL DEFAULT 0,

  `event_start_date` date NOT NULL,
  `event_start_hour` varchar(5) NOT NULL,
  `event_end_date` date NOT NULL,
  `event_end_hour` varchar(5) NOT NULL,
  `is_nocturnal` tinyint unsigned DEFAULT NULL,
  `time_on_place` smallint unsigned DEFAULT NULL,
  time_on_place_measurement_unity_id tinyint unsigned default 2,

  timezone_id SMALLINT DEFAULT 296,

  number_of_tickets smallint unsigned default NULL,
  use_izilife_paiement boolean default 0,

  `is_recurrent_event` tinyint(1) DEFAULT 0,
  recurrence_type tinyint unsigned default null,
  `recurrent_day` int(11) DEFAULT NULL,
  `recurrent_until` date DEFAULT NULL,
  `is_another_date_of` bigint DEFAULT NULL,
  kill_recurrency boolean default 0,

  is_local_annual_celebration boolean default 0,
  is_alive_representation boolean default 0,
  local_celebration_level tinyint unsigned default NULL,
  can_be_linked_by_others boolean default 0,

  event_serie_id bigint default NULL,
  annual_celebration_id bigint default null, 

  representation_id bigint default null,

  celebration_campain_id bigint unsigned default null, -- Campagne de fête 
  link_to_local_celebration bigint default null, -- Lié à un gros event local (Plus tard CelebrationLocale)
  `parent_id` bigint DEFAULT NULL, -- Programmation et évènement du même proprio
  `on_parent_event` tinyint(1) NOT NULL DEFAULT 0,
  on_local_celebration_event boolean null,

  is_exclusive_on_izilife boolean default 0,
  is_izilife_event boolean default 0,
  is_izilife_partnership_event boolean default 0, 
  is_izilife_organizer_event boolean default 0,

  `created` datetime DEFAULT current_timestamp(),
  `minimal_age` tinyint unsigned DEFAULT NULL,
  `student_event` tinyint(1) NOT NULL DEFAULT 0,
  `only_for_students` tinyint(1) NOT NULL DEFAULT 0,
  `is_for_kids` tinyint(1) NOT NULL DEFAULT 0,
  `accessible_for_kids` tinyint(1) NOT NULL DEFAULT 0,
  `event_cancelled` tinyint(1) NOT NULL DEFAULT 0,
  `event_reported` tinyint(1) NOT NULL DEFAULT 0,
  `event_reported_sens` tinyint(1) DEFAULT NULL,  
  
  `is_free_event` tinyint(1) DEFAULT 0,
  `health_pass` tinyint(1) DEFAULT 0,
  `event_booking_needed_for_access` tinyint unsigned DEFAULT NULL,
  `event_access_type` tinyint unsigned DEFAULT NULL,
  `access_on_booking` tinyint(1) NOT NULL DEFAULT 1,

  `access_text` tinytext DEFAULT NULL,
  access_link tinytext default null,

  `basic_price` float DEFAULT 0,
  basic_price_currency smallint unsigned default 1,
  `registration_state` tinyint unsigned DEFAULT NULL,

  `there_is_toilets_on_event` tinyint(1) NOT NULL DEFAULT 0,
  `toilets_accessibility` tinyint(1) NOT NULL DEFAULT 0,
  toilet_accessibility_minimum_buy decimal(10,2) default NULL,
  toilet_accessibility_minimum_buy_currency smallint unsigned default 1,
  
  `confidentiality` int(11) DEFAULT NULL,

  `event_place` bigint DEFAULT NULL,
  `event_shop` bigint DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `address_complement` varchar(100) DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `zip_code` int(11) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `city_id` bigint DEFAULT NULL,
  administrative_division_id bigint unsigned default null,
  
  `number_of_levels` int(11) DEFAULT NULL,
  maximum_tickets_per_user tinyint unsigned  default NULL,
  
  -- Organizer
  `partner_id` bigint DEFAULT NULL,
  page_id bigint default null,
  group_id bigint default null,
  `place_id` bigint DEFAULT NULL,
  `shop_id` bigint DEFAULT NULL,

  `event_brand_text` varchar(100) DEFAULT NULL,

  `phone_number` varchar(20) DEFAULT NULL,
  `description` text DEFAULT NULL,

  created_by_user bigint default null, 
  created_by_page bigint default null,

  saving_default_language int default 1,
  creation_date Datetime default CURRENT_TIMESTAMP,

  sport_id int unsigned default NULL,
  dance_id smallint unsigned default null, 
  music_style_id smallint unsigned default null,
  artisan_technique_id tinyint unsigned default null,

  is_mts_event boolean default 0,
  is_mts_friendly_event boolean default 0,

  scrapped_from tinytext default null, 
  scrapping_json TEXT default null,

  foreign key(sport_id) references Sport(id),
  foreign key(dance_id) references Dance(id),
  foreign key(music_style_id) references MusicStyle(id),
  foreign key (principal_activity_category) references ActivityPrincipalCategory(id),
  foreign key (artisan_technique_id) references ArtisanTechnique(id),
  
  foreign key(basic_price_currency) references Currency(id),
  foreign key(toilet_accessibility_minimum_buy_currency) references Currency(id),
  foreign key(time_on_place_measurement_unity_id) references TimeMeasurementUnity(id),
  foreign key(recurrence_type) references RecurrenceType(id),
  foreign key(representation_id) references Representation(id),
  foreign key(event_access_type) references AccessType(id),
  foreign key(event_booking_needed_for_access) references AccessBookingNeeded(id),
  foreign key (local_celebration_level) references ActivityAreaLevel(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `Experience` (
  `id` bigint NOT NULL,
  unique_id varchar(32) default NULL unique,

  `title` varchar(255) DEFAULT NULL,
  `experience_string_id` varchar(255) DEFAULT NULL,

  is_multi_local_habit boolean default 0, 

  `is_insolite` tinyint(1) NOT NULL DEFAULT 0,
  `is_for_kids` tinyint(1) NOT NULL DEFAULT 0,
  `accessible_for_kids` tinyint(1) NOT NULL DEFAULT 0,
  
  `experience_type` tinyint unsigned DEFAULT NULL,
  `experience_nature` TINYINT UNSIGNED NOT NULL DEFAULT 1 COMMENT '1=INVENTORY, 2=DISCOVERY_ACTIVITY, 3=DISCOVERY_PLACE, 4=LOCAL_HABIT',

  principal_activity_category smallint unsigned default NULL,
  with_equipment_rent boolean default 0,

  -- `experience_category` int(11) DEFAULT NULL,
   `is_active` tinyint(1) DEFAULT 0,

  `experience_picture` bigint unsigned DEFAULT NULL,
  `duration` smallint unsigned DEFAULT NULL,
  duration_measurement_unity_id tinyint unsigned default 2,

  `minimal_age` tinyint unsigned DEFAULT NULL,


  `exterior` tinyint(1) NOT NULL DEFAULT 0,
  `with_equipment` tinyint(1) DEFAULT 0,
  `equipment_gived` tinyint(1) DEFAULT 0,
  `equipment_text` varchar(500) DEFAULT NULL,
  `minimal_number_of_people` int(11) DEFAULT NULL,
  `maximal_number_of_people` int(11) DEFAULT NULL,
  `is_nocturnal` int(1) DEFAULT 0,

  `experience_theme` tinyint unsigned DEFAULT NULL,
  `experience_theme2` tinyint unsigned DEFAULT NULL,
  `experience_theme3` tinyint unsigned DEFAULT NULL,

  `basic_price` float NOT NULL DEFAULT 0,
  basic_price_currency smallint unsigned default 1,

  `partner_id` bigint DEFAULT NULL,
  page_id bigint default null,
  `brand_text` varchar(100) DEFAULT NULL,
  
  is_exclusive_on_izilife boolean default 0,
  is_izilife_experience boolean default 0,

  `phone_number` varchar(20) DEFAULT NULL,

  `meet_place` bigint DEFAULT NULL,
  `meet_shop` bigint DEFAULT NULL,
  `experience_on_event` bigint DEFAULT NULL,
  `experience_in_all_city` tinyint(1) NOT NULL DEFAULT 0,

  `address` varchar(100) DEFAULT NULL,
  `address_complement` varchar(100) DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `zip_code` int(11) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `city_id` bigint NOT NULL,
  administrative_division_id bigint unsigned default null,
  `map_image` varchar(255) DEFAULT NULL,

  `vehicule_type` tinyint unsigned DEFAULT NULL,
  `place_visit` tinyint(1) DEFAULT 0,
  `specialExperience_id` bigint DEFAULT NULL,
  
  `experience_access_type` tinyint unsigned DEFAULT NULL,
  `access_on_booking` tinyint(1) DEFAULT 0,
  experience_booking_needed_for_access tinyint unsigned default NULL,

  `access_text` tinytext DEFAULT NULL,
  access_link tinytext default null,
  
  `health_pass` tinyint(1) DEFAULT null,
  `special_experience` tinyint(1) NOT NULL DEFAULT 0,
  
  `noise_level` int(11) DEFAULT 2,
  `registration_state` tinyint unsigned DEFAULT NULL,
  
  `price_text` text DEFAULT NULL,
  `description` text DEFAULT NULL,
  `short_description` text DEFAULT NULL,

  saving_default_language int default 1,

  sport_id int unsigned default NULL,
  dance_id smallint unsigned default null, 
  music_style_id smallint unsigned default null,
  artisan_technique_id tinyint unsigned default null,

  creation_date Datetime default CURRENT_TIMESTAMP,

  scrapped_from tinytext default null, 
  scrapping_json TEXT default null,
  
  foreign key(basic_price_currency) references Currency(id),
  foreign key(principal_activity_category) references ActivityPrincipalCategory(id),
  foreign key(experience_booking_needed_for_access) references AccessBookingNeeded(id),
  foreign key(duration_measurement_unity_id) references TimeMeasurementUnity(id),

  foreign key(sport_id) references Sport(id),
  foreign key(dance_id) references Dance(id),
  foreign key(music_style_id) references MusicStyle(id),
  foreign key(artisan_technique_id) references ArtisanTechnique(id),

  foreign key(experience_access_type) references AccessType(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `EquipmentCategory` (
  `id` int(11) NOT NULL primary key auto_increment,
  `name` varchar(50) NOT NULL,
  `string_id` varchar(50) NOT NULL,

  equipment_category_type_id tinyint unsigned not null, 
  is_mobility_equipment boolean default 0,
  is_lodging_equipment boolean default 0, 

  can_be_several_on_interest boolean default 0,

  with_page boolean default 0,
  with_pop_up boolean default 0,

  create_from_place boolean default 0,
  create_from_shop boolean default 0,  
  create_from_event boolean default 0,
  create_from_city boolean default 0, 

  name_is_mandatory boolean default 0,
  is_free_access_equipment boolean default 1,

  with_picture boolean default 1,
  need_localization boolean default 0,

  bookable_equipment boolean default 0,
  rentable_equipment boolean default 0,
  privatizable_equipment boolean default 0,
  unique_object_creation boolean default 0

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `EquipmentCategory` (`name`, `string_id`, equipment_category_type_id, is_mobility_equipment,  with_page, with_pop_up, create_from_place, 
  create_from_shop, create_from_event, create_from_city, can_be_several_on_interest, is_lodging_equipment, name_is_mandatory, is_free_access_equipment,
  with_picture, need_localization
) VALUES
-- Objets spécifiques : Bar & Restaurant : ils auront leur qr code pour déclenché une commande
  ('Table', 'table', 2, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0),  
  ('Carré VIP', 'carre-vip', 2, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0),
  ('Espace', 'espace', 2, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0), 
  ('Terrasse', 'terresse', 2, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0),    

  ('Cabine Photo', 'cabine-photo', 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1), -- Vivant
  ('Toilettes publiques', 'toilettes-publiques', 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1),

  ('Bac de compostage', 'bac-de-compostage', 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1),
  ("Point d'apport volontaire", 'point-d-apport-volontaire', 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1),

  ('Terrain de pétanque', 'terrain-de-petanque', 3, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1),
  ('Parc Street-workout', 'parc-street-workout', 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1),

  ('Point d\'eau potable', 'point-d-eau-potable', 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1),
  ('Distributeur de billet', 'distributeur-de-billet', 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1),

  ('Boîte à livres', 'boire-a-livres', 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1),
  ('Boîte à dons', 'boite-a-don', 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1),
  ('Collecte de textile', 'collecte-de-textile', 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1),
  ('Distributeur de préservatif', 'distributeur-de-preservatif',  1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1),
  ('Défibrilateur', 'defibrilateur', 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1), 

  ('Banc', 'banc-public', 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1),
  ('Poubelle publique', 'poubelle-publique', 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1),
  ('Poubelle interne', 'poubelle-interne', 2, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1),
  ('Table de pique-nique', 'table-de-pique-nique', 3, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1),
  -- Autres équipements ? Feux tricolore, Bennes à ordure, ...
-- Rayons, 

-- Hebergements 
  ("Chambre d'hôtel", 'chambre-d-hotel', 2, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1),
  ("Suite", 'suite', 2, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0),
  ("Chambre d'hôte", 'chambre-d-hote', 2, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0),
  -- Place caravane, Place Camping, Appartement entier à louer, ....

-- Equipements de Mobilité 
  ('Abris de vélos', 'abri-velos', 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1),
  ('Horodateur', 'horodateur', 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1),
  ('Arceau Vélo', 'arceau-velo', 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1),
  ('Box à Vélo', 'box-a-velo', 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1),

  ('Station Vélo libre service', 'station-velo-libre-service', 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1),
  ('Trotinette libre service', 'trotinette-libre-service', 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1),

  ('Stationnement', 'stationnement', 1,  1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1), -- Places de Stationnement dans la rue, on va noter les zones géolocalisable avec leurs nombres de plaes

-- Terrains Piste réservables
  ('Piste de bowling', 'piste-de-bowling', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Piste de karting', 'piste-de-karting', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Mission escape game', 'mission-escape-game', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ("Mur d'escalade", 'mur-d-escalade', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),

  ('Terrain de paintball', 'terrain-de-paintball', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ("Terrain d'airsoft", 'terrain-d-airsoft', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Salle karaoké', 'salle-de-karaoké', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Arène VR', 'arene-vr', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Salle de quizz', 'salle-de-quizz', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),

  ('Terrain de Basketball', 'terrain-de-basket', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Terrain de Football', 'terrain-de-football', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Terrain de Futsal', 'terrain-de-futsal', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Court de tennis', 'court-de-tennis', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Gymnase', 'gymnase', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Salle de sport', 'salle-de-sport', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Salle de danse', 'salle-de-danse', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Autre terrain', 'autre-terrain', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Autre salle de sport', 'autre-salle-de-sport', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
-- Salles 
  ('Auditorium', 'auditorium', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Amphitheatre', 'amphitheatre', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Bibliothèque', 'bibliotheque', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Salle de projection', 'salle-de-projection', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Salle de cinéma', 'salle-de-cinema', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Salle de réunion', 'salle-de-reunion', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Salle de conférence', 'salle-de-conférence', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
-- 
  ('Cabine d\'essayage', 'fitting-room', 2,  0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0),
  ('Pression air', 'pression-air', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1),
  ('Borne électrique', 'borne-electrique', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1),

-- Jeux physiques 
  ('Jeu de fléchettes', 'jeu-de-flechettes', 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1), -- Vivant
  ('Billard', 'billard', 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1),
  ('Babyfoot', 'baby-foot', 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1),
  ('Tennis de table', 'ping-pong', 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1),
  
  ('Studio de danse', 'studio-de-danse', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ("Studio d'enregistrement", 'studio-d-enregistrement', 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
  ('Cave', 'cave', 2, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0)
;

CREATE TABLE `EquipmentShape` (
  `id` tinyint unsigned NOT NULL,
  `name` varchar(50) NOT NULL,
  string_id varchar(50) not null
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `NoiseLevel`
--

INSERT INTO `EquipmentShape` (`id`, `name`, string_id) VALUES
(1, 'Rond', 'rond'),
(2, 'Carré', 'carre'),
(3, 'Rectangulaire', 'rectangulaire');

--
-- Structure de la table `Equipment`
--

CREATE TABLE `Equipment` (
  `id` bigint NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `internal_id` varchar(100) not NULL,
  `equipment_category_id` int(11) NOT NULL,

  unique_id varchar(32) default NULL unique,
  osm_node_id bigint default NULL, 
  google_place_id varchar(50) default null, 

  road_id bigint default NULL, 
  address_id bigint default NULL,

  `exterior` tinyint(1) DEFAULT 0,
  `picture` bigint unsigned DEFAULT NULL,
  `description` text DEFAULT NULL,

  `localization_node_id` varchar(30) DEFAULT NULL,

  `address` varchar(100) NOT NULL,
  `longitude` float DEFAULT NULL,
  `latitude` float DEFAULT NULL,  

  `city_id` bigint DEFAULT NULL,
  administrative_division_id bigint unsigned default null,
  `in_on_place` bigint DEFAULT NULL,
  `in_on_shop` bigint DEFAULT NULL,

  is_active boolean default 0,
  is_privatisable boolean default 0, 
  is_degraded_mode BOOLEAN DEFAULT FALSE,

  bookable_per_team boolean default 0,
  number_of_people_by_team tinyint default NULL, 
  privative_use_or_adding_one_by_one tinyint default NULL, -- 1 : Usage privatif, 2 - Ouvert au public on rajoute jusqu'à la limite 

  `duration_time_measurement` TINYINT UNSIGNED DEFAULT NULL, -- minutes / heures
  `duration` SMALLINT UNSIGNED DEFAULT NULL, 

  owner_page_id bigint default null,
  owner_partner_id bigint default null, 
  owner_place_id bigint default null, 
  owner_shop_id bigint default null,
  owner_event_id bigint default null,
  owner_city_id bigint default null,
  owner_administrative_division_id bigint unsigned default null,

  place_type_id  INT default NULL,
  shop_category_id smallint default null, 

  shape tinyint unsigned default null, 
  capacity int unsigned default null,

  localization_text varchar(50) default NULL,

  FOREIGN KEY (`duration_time_measurement`) REFERENCES `TimeMeasurementUnity`(`id`),
  foreign key(equipment_category_id) references EquipmentCategory(id)
  -- foreign key(shape) references EquipmentShape(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `ObjectOnPublicPlace`
--

CREATE TABLE `ObjectOnPublicPlace` (
  `id` int(11) NOT NULL primary key auto_increment,
  `name` varchar(50) NOT NULL,
  `object_string_id` varchar(50) NOT NULL,

  is_service_object boolean default 0,
  is_animation_object boolean default 0,

  is_usable_for_service_resume boolean not null,
  `localizable_on_local_plan` boolean NOT NULL,
  is_living_equipment boolean default 0

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Déchargement des données de la table `ObjectOnPublicPlace`
--

INSERT INTO `ObjectOnPublicPlace` (`name`, `object_string_id`, is_service_object, `localizable_on_local_plan`, is_living_equipment, is_usable_for_service_resume) VALUES
--  Tables, toilettes
  ('Toilettes payantes', 'toilettes-payantes', 0, 1, 1, 1),
  ('Toilettes gratuites', 'toilettes-gratuites', 0, 1, 1, 1),
  ('Table', 'table', 0, 0, 1, 1),
  ('Banc', 'banc', 0, 0, 1, 1),
  ('Poubelle', 'poubelle', 0, 0, 1, 1),
  ('Table de pique-nique', 'table-de-pique-nique', 0, 0, 1, 1),
  ('Distributeur de billet', 'distributeur-de-billet', 0, 0, 1, 1),

-- Terrains, Salles & Piste réservables
  ('Terrain de Basketball', 'terrain-de-basket', 0, 0, 1, 1),
  ('Terrain de Football', 'terrain-de-football', 0, 0, 1, 1),
  ('Terrain de Futsal', 'terrain-de-futsal', 0, 0, 1, 1),
  ('Court de tennis', 'court-de-tennis', 0, 0, 1, 1),
  ('Gymnase', 'gymnase', 0, 0, 1, 1),
  ('Salle de sport', 'salle-de-sport', 0, 0, 1, 1),
  ('Salle de danse', 'salle-de-danse', 0, 0, 1, 1),
  ("Mur d'escalade", 'mur-d-escalade',  0, 0, 1, 1),

-- Salles 
  ('Auditorium', 'auditorium', 0, 0, 1, 1),
  ('Amphitheatre', 'amphitheatre', 0, 0, 1, 1),
  ('Bibliothèque', 'bibliotheque', 0, 1, 1, 1),
  ('Salle de projection', 'salle-de-projection', 0, 0, 1, 1),
  ('Salle de cinéma', 'salle-de-cinema', 0, 0, 1, 1),
  ('Salle de réunion', 'salle-de-reunion', 0, 0, 1, 1),

-- Equipements, Espaces : Santé  & Sécurité 
  ('Défibrilateur', 'defibrilateur', 0, 0, 1, 1),

-- Outils & Objets: Non Visible sur maps 
  ('Vestiaire', 'vestiaire', 0, 1, 0, 1),
  ('Douche', 'douche', 0, 1, 0, 1),
  ('Casier', 'casier', 0, 1, 0, 1),

  ('Terrasse', 'terrasse', 0, 0, 1, 1),
  ('Rooftop', 'rooftop', 0, 0, 1, 1),
  ('Transat', 'transat', 0, 0, 0, 1),

  ('Cendrier', 'cendrier', 0, 0, 0, 1),
  ('Ascenseur', 'ascenseur', 0, 1, 0, 1),
  ('Escalator', 'escalator', 0, 1, 0, 1),

  ('Garde Casque', 'garde-casque', 0, 1, 0, 1),
  ('Recharge téléphones', 'borne-de-recharge-pour-telephone', 0, 1, 0, 1),
  ('Cabine d\'essayage', 'cabine-essayage', 0, 0, 1, 1),
  ('Longue-vue', 'longue-vue', 0, 0, 0, 1),
  ('Jumelles', 'jumelles', 0, 0, 0, 1),

-- Service de Restauration, Boissons 
  ('Restaurant', 'restaurant', 0, 0, 0, 1),
  ('Hebergement', 'hebergement', 1, 0, 0, 0),
  ('Se garer la nuit', 'se-garer-la-nuit', 1, 0, 0, 0),
  ('Bar', 'bar', 0, 0, 0, 1),
  ('Café', 'coffee-shop', 0, 0, 0, 1),
  ('Food Truck', 'food-truck', 0, 0, 0, 1),
  ('Stands Street Food', 'street-food', 0, 0, 0, 1),
  ('Boutique', 'boutique', 0, 0, 0, 1),

-- Services 
  ('Espace détente', 'espace-detente', 0, 1, 0, 1),
  ('Nurserie', 'nurserie', 1, 1, 0, 1),
  ('Prêt de poussette', 'pret-de-poussette', 1, 0, 0, 1),
  ('Doudou perdu', 'doudou-perdu', 1, 0, 0, 1),
  ('Bibliothèque partagée', 'bibliotheque-partagee', 1, 1, 0, 1),
  ('Vinted Go', 'vinted-go', 1, 0, 0, 1),
  ('Point relais', 'point-relais', 1, 0, 0, 1),
  ('Espace fumeur', 'espace-fumeur', 0, 1, 0, 1),
  ('Change bébé', 'change-bebe', 0, 0, 0, 1),
  ('Consigne', 'consigne', 1, 0, 0, 1),

  ('Wifi', 'wifi', 1, 0, 0, 1),
  ('TV', 'tv', 1, 0, 0, 1),
  ('Diffusions sportives', 'diffusion-sportives', 1, 0, 0, 1),
  ('Recyclage piles', 'recyclage-piles', 0, 1, 0, 1),
  
  ('Amazon Locker', 'amazon-locker', 0, 0, 0, 1),

-- Services : Se garer 
  ('Parking gratuit', 'parking-gratuit', 1, 0, 0, 1),
  ('Parking payant', 'parking-payant', 1, 0, 0, 1),
  ('Parking 2 roues', 'parking-2-roues', 1, 0, 0, 1),
  ('Parking vélo', 'parking-velo', 1, 0, 0, 1),
  ('Borne électrique', 'borne-electrique', 1, 0, 0, 1),
  ('Voiturier', 'voturier', 1, 0, 0, 0),

-- Espace: Réception, 
  ('Entrée', 'entrée', 0, 1, 0, 0),
  ('Reception', 'reception', 0, 1, 0, 0),
  ('Poste de Sécurité', 'pc-securite', 0, 1, 1, 0),

-- Equipements Amusement pour enfants
  ('Aire de jeux', 'aire-de-jeux', 0, 0, 0, 1),
  ('Balançoire', 'balancoire', 0, 0, 0, 1),
  ('Manège', 'manege', 0, 0, 0, 1),
  ('Montagne russe', 'montagnes-russes', 0, 0, 0, 1),
  ('Trampoline', 'trampoline', 0, 0, 0, 1),
  ('Toboggan', 'toboggan', 0, 0, 0, 1),
  ('Grande roue', 'grande-roue', 0, 0, 0, 1),

  ('Chateau gonflable', 'chateau-gonflable', 0, 0, 0, 1),
  ('Piscine gonflable', 'piscine-gonflable', 0, 0, 0, 1),

  ('Baby Foot', 'baby-foot', 0, 0, 1, 1),
  ('Jeux d\'Arcade', 'arcade', 0, 0, 1, 1),
  ('Fléchettes', 'flechettes', 0, 0, 1, 1),
  ('Billard', 'billard', 0, 0, 1, 1),
  ('Flippers', 'flipper', 0, 0, 1, 1),
  ('Ping pong', 'ping-pong', 0, 0, 1, 1),

  ('Parc aquatique', 'parc-aquatique', 0, 0, 0, 1),

-- Matériels de bien-être 
  ('Spa', 'spa', 0, 0, 0, 1),
  ('Jacuzzi', 'jacuzzi', 0, 0, 1, 1),
  ('sauna', 'sauna', 1, 0, 1, 1),
  ('Hammam', 'hammam', 1, 0, 1, 1),
  ('Piscine intérieur', 'piscine-interieur', 1, 1, 1, 1),
  ('Piscine extérieur', 'piscine-exterieur', 1, 1, 1, 1),

-- Stations Services & Autres 
  ('Station service', 'station-service', 1, 0, 0, 1),
  ('Pression air', 'pression-air', 1, 0, 0, 1),
  ('Station de lavage auto', 'station-de-lavage-auto', 1, 0, 0, 1),

-- Monuments & cours d'eau : Juste pour dire ce qui est présent 
  ('Grotte', 'grotte', 0, 0, 0, 1),
  ('Cours d\'eau', 'cours-d-eau', 0, 1, 0, 1),
  ('Phare', 'phare', 0, 0, 0, 1),
  ('Fontaine ', 'fontaine', 0, 1, 0, 1),

-- Ferme, Animaux & 
  ('Ferme', 'ferme', 0, 0, 0, 1),
  ('Serre', 'serre', 0, 0, 0, 1),

-- 
  ('Parc Street-workout', 'parc-street-workout', 0, 0, 1, 1),
  ('Point d\'eau potable', 'point-d-eau-potable', 0, 0, 1, 1), 
  
  ('Scène', 'scene', 0, 1, 0, 1),
  ('Musée', 'musee', 0, 0, 0, 1),
  ('Cave', 'cave', 0, 1, 0, 1),
  ('Marché', 'marche', 0, 0, 0, 1),
  ('Studio danse', 'studio-de-danse', 0, 0, 0, 1),
  ("Studio d'enregistrement", 'studio-d-enregistrement', 0, 0, 0, 1);

INSERT INTO `ObjectOnPublicPlace` (`name`, `object_string_id`, is_service_object, `localizable_on_local_plan`, is_living_equipment, is_usable_for_service_resume) VALUES

  ('Chaise haute', 'chaise-haute', 0, 0, 0, 1),
  ('Micro-ondes', 'micro-ondes', 0, 0, 0, 1),
  ('Chauffe biberon', 'chauffe-biberon', 0, 0, 0, 1),
  ('Chauffe Terrasse', 'chauffe-terrasse', 0, 0, 0, 1),
  ('Skatepark', 'Skatepark', 0, 1, 1, 1),
  ('Skateboard', 'skateboard', 0, 0, 0, 1),
  ('Location de salle', 'location-de-salle', 1, 0, 0, 1)
;


CREATE TABLE `Hobby` (
  `id` int(11) NOT NULL primary key,
  `name` varchar(100) NOT NULL,
  `hobby_string_id` varchar(100) NOT NULL,
  `hobby_principal_category` int(11) NOT NULL,
  `hobby_category_2` int(11) DEFAULT NULL,
  `hobby_category_3` int(11) DEFAULT NULL,

  is_shop_service_hobby boolean default 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `Hobby`
--

INSERT INTO `Hobby` (`id`, `name`, `hobby_string_id`, `hobby_principal_category`, `hobby_category_2`, `hobby_category_3`) VALUES
  (1, 'Campagne', 'campagne', 1, NULL, NULL),
  (2, 'Ville', 'ville', 1, NULL, NULL),
  (3, 'Montagne', 'montagne', 1, NULL, NULL),
  (4, 'Champs', 'champs', 1, NULL, NULL),
  (5, 'Mer', 'mer', 1, NULL, NULL),
  (6, 'Animaux', 'animaux', 1, NULL, NULL),
  (7, 'Nature', 'nature', 1, NULL, NULL),
  (8, 'Monuments', 'monument', 1, NULL, NULL),
  (9, 'Couché de soleil', 'couche-de-soleil', 1, NULL, NULL),
  (10, 'Levé de soleil', 'leve-de-soleil', 1, NULL, NULL),
  (11, 'Regarder les étoiles', 'etoiles', 3, NULL, NULL),
  (12, 'Voir des Cascades', 'cascade', 3, NULL, NULL),
  (13, 'Voir un volcan', 'volcan', 1, NULL, NULL),
  (14, 'Voir la forêt', 'foret', 1, NULL, NULL),
  (15, 'Plage', 'plage', 1, NULL, NULL),
  (16, 'Grottes', 'grotte', 1, NULL, NULL),
  (17, 'Vue panoramique', 'vue-panoramique', 1, NULL, NULL),
  (18, 'Fontaine', 'fontaine-eau', 1, NULL, NULL),
  (19, 'Eau', 'eau', 1, NULL, NULL),

  (20, 'Petit-déjeûner', 'petit-dejeuner', 2, NULL, NULL),
  (21, 'Brunch', 'brunch', 2, NULL, NULL),
  (22, 'Déjeûner/Dîner', 'dejeuner', 2, NULL, NULL),
  (23, 'Goûter', 'gouter', 2, NULL, NULL),
  (24, 'Apéro', 'apero', 2, NULL, NULL),
  (26, 'Pique-nique', 'pique-nique', 3, NULL, NULL),
  (27, 'Café', 'cafe', 5, NULL, NULL),
  (28, 'Thé', 'the', 5, NULL, NULL),
  (29, 'Glace', 'glace', 2, NULL, NULL),
  (30, 'Gaufre', 'gaufre', 2, NULL, NULL),
  (31, 'Crêpe', 'crepe', 2, NULL, NULL),

  (32, 'Se balader', 'balade', 3, NULL, NULL),
  (33, 'Jardiner', 'jardiner', 3, NULL, NULL),
  (34, 'Cuisiner', 'cuisiner', 3, NULL, NULL),
  (35, 'Boire un verre', 'boire', 3, NULL, NULL),
  (36, 'Danser', 'danser', 3, NULL, NULL),
  (37, 'Rencontre', 'rencontrer', 3, NULL, NULL),
  (38, 'Shopping', 'shopping', 3, NULL, NULL),
  (39, 'Travailler', 'travailler', 3, NULL, NULL),
  (40, 'Camper', 'camper', 3, NULL, NULL),
  (41, 'Se détendre', 'se-detendre', 3, NULL, NULL),
  (42, 'Karaoké', 'karaoke', 3, NULL, NULL),
  (43, 'Ceuillette', 'ceuillette', 3, NULL, NULL),
  (44, 'Bain de soleil', 'bain-de-soleil', 3, NULL, NULL),
  (45, 'Massage', 'massage', 4, NULL, NULL),
  (46, 'Spa', 'spa  ', 3, NULL, NULL),
  (47, 'Promenade de chien', 'promenade-de-chien', 3, NULL, NULL),

  (48, 'Running', 'running', 4, 6, 3),
  (49, 'Vélo', 'velo', 4, 6, 3),
  (50, 'Marche', 'marche', 4, 6, 3),
  (51, 'Kayak', 'kayak', 4, 6, 3),
  (52, 'Nager', 'nager', 4, 6, 3),

  (53, 'Paintball', 'paintball', 6, 3, NULL),
  (54, 'Laser Game', 'laser-game', 6, 3, NULL),
  (55, 'Karting', 'karting', 6, 3, NULL),
  (56, 'Fitness', 'fitness', 6, 3, NULL),

  (57, 'Marche nordique', 'marche-nordique', 4, 6, 3),
  (58, 'Boxe', 'boxe', 4, 6, 3),
  (59, 'Aviron', 'aviron', 4, 6, 3),
  (60, 'Badminton', 'badminton', 4, 6, 3),

  (61, 'Billard', 'billard', 6, 3, NULL),
  (62, 'Bowling', 'bowling', 6, 3, NULL),

  (63, 'Equitation', 'equitation', 4, 6, 3),
  (64, 'Football', 'football', 4, 6, 3),
  (65, 'Frisbee', 'frisbee', 4, 6, 3),
  (66, 'Skateboard', 'skateboard', 4, 6, 3),
  (67, 'Golf', 'golf', 4, 6, 3),

  (68, 'Montgolfière', 'montgolfiere', 6, NULL, NULL),
  (69, 'Paddle', 'paddle', 4, 6, 3),
  (70, 'Parachute', 'parachute', 4, 6, 3),
  (71, 'Ping pong', 'ping-pong',4, 6, 3),
  (72, 'Roller', 'roller', 4, 6, 3),
  (73, 'Ski', 'ski', 4, 6, 3),
  (74, 'Tennis', 'tennis', 4, 6, 3),
  (75, 'Trampoline', 'trampoline', 4, 6, 3),

  (77, 'Pause Dej', 'pause-dejeuner', 2, 3, NULL),
  (78, 'Chute libre', 'chute-libre', 3, NULL, NULL),
  (79, 'Base Jump', 'base-jumping', 3, NULL, NULL),

  (80, 'Feu d\'artifice', 'feu-artifice', 3, NULL, NULL),

  (81, 'Parapente', 'parapente', 3, 6, NULL),
  (82, 'Fléchettes', 'flechettes', 6, 3, NULL),
  (83, 'Tir à l\'arc', 'tir-a-larc',  6, 3, NULL),
  (84, 'Surf', 'surf',  6, 3, NULL),
  (85, 'Ski nautique', 'ski-nautique', 6, 3, NULL),

  (86, 'Courses', 'courses', 3, NULL, NULL),

  (88, 'Escalade', 'escalade',  4, 6, 3),
  (89, 'Escape Game', 'escape-game', 4, 6, 3),
  (90, 'Réalité virtuelle', 'realite-virtuelle',  4, 6, 3),

  (91, 'Vente directe', 'vente-directe', 3, NULL, NULL),

  (92, 'Balade en bateau', 'bateau', 3, 6, NULL),
  (93, 'Lancer de hache', 'lancer-de-hache', 6, 3, NULL),
  (94, 'Accrobranche', 'accrobranche', 6, 3, NULL),

  (95, 'Jeux d\'Arcade', 'arcade', 6, NULL, NULL),
  (96, 'Flipper', 'flipper', 6, NULL, NULL),
  (97, 'Planche à voile', 'planche-a-voile', 4, 6, 3),

  (98, 'Bière', 'biere', 5, NULL, NULL),

  (99, 'Pétanque', 'petanque', 6, NULL, NULL),

  (100, 'Voir un film', 'voir-un-film', 3, NULL, NULL),
  (101, 'Blind Test', 'blind-test', 3, NULL, NULL),
  (102, 'Concerts', 'concert', 3, NULL, NULL),
  (103, 'Fêter un anniversaire', 'anniversaire', 3, NULL, NULL),
  (104, 'Fabrication de beurre', 'beurre', 3, NULL, NULL),
  (105, 'Ecouter de la musique', 'ecouter-musique', 3, NULL, NULL),
  (106, 'Jeux de société', 'jeux-de-societe', 4, NULL, NULL),
  (107, 'Atelier cuisine', 'atelier-cuisine.png', 3, NULL, NULL),
  (108, 'Moment en famille', 'moment-familial', 3, NULL, NULL),
  (109, 'Pâtisserie', 'patisserie', 3, NULL, NULL),
  (110, 'Atelier pâtisserie', 'atelier-patisserie', 3, NULL, NULL),
  (111, 'Marché aux livres', 'marche-aux-livres.png', 3, NULL, NULL),
  (112, 'Patinage', 'patinage', 3, NULL, NULL),
  (113, 'Moment en couple', 'moment-en-couple', 3, NULL, NULL),
  (114, 'Snack', 'snack', 3, NULL, NULL),

  (115, 'Dj Set', 'dj-set', 3, NULL, NULL),
  (117, 'Conférence', 'conference', 3, NULL, NULL),
  (118, 'Comedy club', 'comedy-club', 3, NULL, NULL),
  (119, 'Exposition', 'exposition', 3, NULL, NULL),

  (120, 'Dormir', 'dormir', 3, NULL, NULL),
  (121, 'Poker', 'poker', 6, 3, NULL),
  (122, 'Bingo', 'bingo', 6, 3, NULL),
  (123, 'Visiter', 'visiter', 3, NULL, NULL),

  (124, 'Bricoler', 'bricoler', 3, 6, NULL),
  (125, 'Poterie', 'poterie', 6, 3, NULL),
  (126, 'Activité manuelle', 'activite-manuelle', 3, 6, NULL),
  (127, 'Marché', 'courses-marche', 3, 6, NULL),
  (128, 'Bmx', 'bmx', 4, 6, 3),
  (129, 'Dessiner', 'dessiner', 3, 6, NULL),
  (130, 'Peinture', 'peinture', 3, 6, NULL),

  (131, 'Quiz', 'quiz', 3, 6, NULL),
  (132, 'Yoga', 'yoga', 3, 6, NULL),
  (133, 'Pilate', 'pilate', 3, 6, NULL),
  (134, 'Raclette', 'raclette', 3, 6, NULL)
;
-- --------------------------------------------------------

--
-- Structure de la table `HobbyCategory`
--

CREATE TABLE `HobbyCategory` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `category_string_id` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `HobbyCategory`
--

INSERT INTO `HobbyCategory` (`id`, `name`, `category_string_id`) VALUES
(1, 'Voir', 'voir'),
(2, 'Manger', 'manger'),
(3, 'Faire', 'faire'),
(4, 'Sports', 'sports'),
(5, 'Boire', 'boire'),
(6, 'Loisirs', 'loisirs');

--

#region EventCategory
  CREATE TABLE `EventCategory` (
    `id` smallint unsigned NOT NULL primary key auto_increment,
    `name` varchar(100) NOT NULL,
    `event_category_string_id` varchar(100) NOT NULL,
    `is_principal` tinyint(1) DEFAULT 0,

    free_use_by_user boolean default 0,
    can_be_a_tour boolean default 0, -- Peut-être une tournée (Concert, Spectacle, Opéra, ...)
    is_representation_type boolean default 0, -- Est-ce une Représentation (Les spectacles, les théâtres, les opéra, ...)
    is_special_category boolean default 0, -- Catégories spéciale qui ne sont pas des catégory (mais des types), il faut donc obligatoirement choisir un activité principale. P ex: Un salon, peut avoir pour catégorie principale Restauration 
    is_usable_for_programmation boolean default 0,

    with_hourly boolean default 0,

    is_professional_event_category boolean default 0, -- Un évent de professionnel comme Salon, Convention, Conférence

    need_principal_activity_category boolean default 1, -- On a absolument besoin de fournir un secteur principal lors de la création de l'évent/expérience
    principal_activity_category smallint unsigned default NULL, -- Catégorie principale par défaut  

    second_parent_id smallint unsigned default NULL,
    parent_id smallint unsigned default NULL,

    is_charitable_event boolean default 0,

    foreign key (principal_activity_category) references ActivityPrincipalCategory(id),
    foreign key (parent_id) references EventCategory(id),
    foreign key (second_parent_id) references EventCategory(id)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

  --
  -- Déchargement des données de la table `EventCategory`
  --

  INSERT INTO `EventCategory` (`id`, `name`, `event_category_string_id`, `is_principal`, `parent_id`, free_use_by_user, can_be_a_tour, is_representation_type, is_special_category,
    is_professional_event_category,  need_principal_activity_category, principal_activity_category, is_usable_for_programmation
  ) VALUES
  (1, 'Fête & Musique', 'fete-et-musique', 1, NULL, 1, 0, 0, 0, 0, 1, 4, 0),
  (2, 'Art & Culture', 'art-et-culture', 1, NULL, 1, 0, 0, 0, 0, 1, 1, 0),
  (3, 'Litterature', 'litterature', 1, NULL, 1, 0, 0, 0, 0, 1, 8, 0),
  (4, 'Sport', 'sport', 1, NULL, 1, 0, 0, 0, 0, 1, 6, 0),
  (5, 'Cinéma', 'cinema', 1, NULL, 1, 0, 0, 0, 0, 1, 5, 0),
  (6, 'Théâtre', 'theatre', 1, NULL, 1, 0, 1, 0, 0, 1, 10, 1),
  (7, 'Spectacle', 'spectacle', 1, NULL, 1, 0, 1, 0, 0, 1, 9, 1),
  (8, 'Danse', 'danse', 1, NULL, 1, 0, 0, 0, 0, 0, 7, 0),

  (9, 'Alimentation', 'alimentation', 1, NULL, 1,  0, 0, 0, 0, 0, 16, 0),
  (10, 'Marchés, Braderies & Brocantes', 'marches-braderie-et-brocante', 1, NULL, 1, 0, 0, 0, 0, 0, 19, 0),
  (11, 'Mode', 'mode', 1, NULL, 1, 0, 0, 0, 0, 0, 12, 0),

  (12, 'Jeux ', 'jeux', 1, NULL, 1, 0, 0, 0, 0, 0, 14, 0),

  (13, 'Bien-être', 'bien-etre', 1, NULL, 1, 0, 0, 0, 0, 0, 13, 0),
  (14, 'Boissons', 'boissons', 1, NULL, 1, 0, 0, 0, 0, 0, 17, 0),

  (15, 'Jardinage', 'jardinage', 1, NULL, 1, 0, 0, 0, 0, 1, 157, 0),
  (16, 'Maison', 'maison', 1, NULL, 1, 0, 0, 0, 0, 0, 156, 0),
  (17, 'Commerce & Business', 'commerce-et-business', 1, NULL, 1, 0, 0, 0, 0, 0, 158, 0),

  (18, 'Retraite', 'retraite', 1, NULL, 1, 0, 0, 0, 1, 1, NULL, 0),
  (19, 'Séjour', 'sejour', 1, NULL, 1, 0, 0, 0, 1, 1, NULL, 0),
  (20, 'Salon', 'salon', 1,  NULL, 1, 0, 0, 0, 1, 1, NULL, 0),
  (21, 'Convention', 'convention', 1, NULL, 1, 0, 0, 0, 1, 1, NULL, 0),
  (22, 'Congrès', 'congrès', 1, NULL, 1, 0, 0, 0, 1, 1, NULL, 0),
  (23, 'Autre Festival', 'autre-festival', 1, NULL, 1, 0, 0, 0, 0, 1, NULL, 0),
  (24, 'Séminaire', 'seminaire', 1, NULL, 1, 0, 0, 0, 1, 1, NULL, 0)
  ;


  INSERT INTO `EventCategory` (`id`, `name`, `event_category_string_id`, `is_principal`, `parent_id`, second_parent_id, free_use_by_user, can_be_a_tour, 
    is_representation_type, is_special_category, is_professional_event_category, need_principal_activity_category, principal_activity_category,
    is_usable_for_programmation
  ) VALUES

  -- Fête & Musique
    (25, 'Festival', 'festival', 0, 1, NULL, 0, 0, 0, 0, 0, 0, 4, 0),
    (26, 'Concert', 'concert', 0, 1, NULL, 0, 0, 1, 0, 0, 0, 4, 1),
    (27, 'Afterwork', 'afterwork', 0, 1, NULL, 1, 0, 0, 0, 0, 0, 4, 0),
    (28, 'Karaoké', 'karaoké', 0, 1, NULL, 1, 0, 0, 0, 0, 0, 4, 1),
    (29, 'Block party', 'block-party', 0, 1, NULL, 1, 0, 0, 0, 0, 0, 4, 0),
    (30, 'Blind test', 'blind-test', 0, 1, NULL, 1, 0, 0, 0, 0, 0, 4, 1),
    (31, 'Soirée', 'soiree', 0, 1, NULL, 1, 0, 0, 0, 0, 0, 4, 1), 
    (32, 'Carnaval', 'carnaval', 0, 1, NULL, 1, 0, 0, 0, 0, 0, 4, 0),
    (33, 'Bal', 'bal', 0, 1, NULL, 1, 0, 0, 0, 0, 0, 4, 1),

    (34, 'Parade', 'parade', 0, 1, NULL, 1, 0, 0, 0, 0, 0, 4, 1),
    (35, 'Dj Set', 'dj-set', 0, 1, NULL, 1, 0, 0, 0, 0, 0, 4, 1),

  -- Art & Culture
    (36, 'Exposition', 'exposition', 0, 2, NULL, 0, 0, 1, 0, 0, 0, 2, 1),

  -- Litterature
    (37, 'Dédicace', 'dedicace-litteraire', 0, 3, 2, 0, 1, 0, 0, 0, 0, 8, 1),
    (38, 'Groupe de lecture', 'groupe-de-lecture', 0, 3, 2, 0, 0, 0, 0, 0, 0, 8, 0),

  -- Sport
    (39, 'Séance', 'seance-de-sport', 0, 4, NULL, 1, 0, 0, 0, 0, 0, 6, 1),
    (40, 'Challenge', 'challenge-sportif', 0, 4, NULL, 1, 0, 0, 0, 0, 0, 6, 1),
    (41, 'Course', 'course', 0, 4, NULL, 1, 0, 0, 0, 0, 0, 6, 1),
    (42, "Course d'obstacle", 'course-d-obstacle', 0, 4, NULL, 1, 0, 0, 0, 0, 0, 6, 1),
    (43, 'Marathon', 'marathon', 0, 4, NULL, 1, 0, 0, 0, 0, 0, 6, 0),
    (44, 'Trail', 'trail', 0, 4, NULL, 1, 0, 0, 0, 0, 0, 6, 0),
    (45, 'Tri-athlon', 'tri-athlon', 0, 4, NULL, 1, 0, 0, 0, 0, 0, 6, 1),
    
    (46, 'Retraite sportive', 'retraite-sportive', 0, 4, NULL, 1, 0, 0, 0, 0, 0, 6, 0),
    (47, 'Séjour sportif', 'sejour-sportif', 0, 4, NULL, 1, 0, 0, 0, 0, 0, 6, 0),
    (48, 'Diffusion de match', 'diffusion-de-match', 0, 4, NULL, 1, 0, 0, 0, 0, 0, 6, 1),

    (49, 'Sortie sportive', 'sortie-sportive', 0, 4, NULL, 1, 0, 0, 0, 0, 0, 6, 1),
    (50, 'Tournoi', 'tournoi', 0, 4, NULL, 1, 0, 0, 0, 0, 0, 6, 1),

  -- Cinéma
    (51, 'Avant première', 'avant-premiere', 0, 5, NULL, 0, 0, 0, 0, 0, 0, 5, 1),
    (52, 'Projection en plein air', 'projection-en-plein-air', 0, 5, NULL, 1, 0, 0, 0, 0, 0, 5, 1),
    (53, 'Soirée cinéma', 'soiree-cinema', 0, 5, NULL, 1, 0, 0, 0, 0, 0, 5, 1),

    (54, 'Ciné rencontre', 'cine-rencontre', 0, 5, 2, 1, 0, 0, 0, 0, 0, 5, 1),
    (55, 'Ciné concert', 'cine-concert', 0, 5, 2, 0, 0, 1, 0, 0, 0, 5, 1),

  -- Théâtre
    (56, 'Opéra', 'opera', 0, 6, 2, 0, 1, 1, 0, 0, 0, 10, 0),
    (57, 'Improvisation', 'improvisation', 0, 6, 2, 1, 1, 1, 0, 0, 0, 10, 0),

    (58, 'Théâtre contemporain', 'theatre-contemporain', 0, 6, 2, 1, 1, 1, 0, 0, 0, 10, 0),
    (59, 'Théâtre jeune public', 'theatre-jeune-public', 0, 6, 2, 1, 1, 1, 0, 0, 0, 10, 0),
    (60, 'Comédie', 'theatre-comedie', 0, 6, 2, 1, 1, 1, 0, 0, 0, 10, 0),

    (61, 'Autres théâtres', 'autres-theatres', 0, 6, NULL, 1, 1, 1, 0, 0, 0, 10, 0),

  -- Spectacle
    (62, 'Ballet', 'ballet', 0, 7, 2, 1, 1, 1, 0, 0, 0, 34, 1),
    (63, 'Cabaret', 'cabaret', 0, 7, 2, 1, 1, 1, 0, 0, 0, 35, 1),
    (64, 'Cirque', 'cirque', 0, 7, 2, 1, 1, 1, 0, 0, 0, 36, 1),
    (65, 'Conte', 'conte', 0, 7, 2, 1, 1, 1, 0, 0, 0, 40, 1),
    (66, 'Chorale', 'chorale', 0, 7, 2, 1, 1, 1, 0, 0, 0, 40, 1),

    (67, 'One man show', 'one-man-show', 0, 7, 2, 1, 1, 1, 0, 0, 0, 42, 1),
    (68, 'Stand Up', 'stand-up', 0, 7, 2, 1, 1, 1, 0, 0, 0, 42, 1),
    (69, 'Diner spectacle', 'diner-spectacle', 0, 7, 2, 1, 1, 1, 0, 0, 0, 9, 1),

    (70, 'Comédie', 'spectacle-comedie', 0, 7, 2, 1, 1, 1, 0, 0, 0, 38, 1),
    (71, 'Comédie musicale', 'comedie-musicale', 0, 7, 2, 1, 1, 1, 0, 0, 0, 38, 1),
    (72, 'Spectacle de marionnettes', 'spectacles-de-marionnettes', 0, 7, 2, 1, 1, 1, 0, 0, 0, 40, 1),

    (73, 'Music Live', 'music-live', 0, 7, 2, 1, 1, 1, 0, 0, 0, 9, 1),
    (74, 'Spectacle numérique', 'spectacle-numerique', 0, 7, NULL, 1, 1, 1, 0, 0, 0, 9, 1),
    (75, 'Spectacle Lumière', 'spectacle-de-lumière', 0, 7, NULL, 1, 1, 1, 0, 0, 0, 9, 1),
    (76, 'Spectacle d\'illusion', 'spectacle-d-illusion', 0, 7, NULL, 1, 1, 1, 0, 0, 0, 37, 1),
    (77, 'Spectacle d\'Hypnose', 'spectacle-d-hypnose', 0, 7, NULL, 1, 1, 1, 0, 0, 0, 39, 1),
    (78, 'Spectacle de magie', 'spectacle-de-magie', 0, 7, NULL, 1, 1, 1, 0, 0, 0, 41, 1),

    (79, 'Spectacles sur glaces', 'spectacles-sur-glaces', 0, 7, 2, 1, 1, 1, 0, 0, 0, 9, 1),

  -- Danse
    (80, 'Cours de danse', 'cours-de-danse', 0, 8, 1, 1, 1, 1, 0, 0, 0, 7, 1),  -- 
    (81, 'Spectacle de danse', 'spectacle-de-danse', 0, 8, 1, 1, 1, 1, 0, 0, 0, 7, 1),
    (82, 'Battle', 'battle', 0, 8, 1, 1, 0, 0, 0, 0, 0, 7, 1),
    (83, 'Freestyle', 'freestyle',  0, 8, 1, 1, 0, 0, 0, 0, 0, 7, 1),
    (84, 'Gala de danse', 'gala-de-danse', 0, 8, 1,  1, 0, 0, 0, 0, 0, 7, 1),
    
  -- Alimentation
    (85, 'Dégustation', 'degustation', 0, 9, NULL, 1, 0, 0, 0, 0, 0, NULL, 1),
    (86, 'Brunch', 'brunch', 0, 9, NULL, 1, 0, 0, 0, 0, 0, NULL, 1),
    (87, 'Barbecue', 'barbecue', 0, 9, NULL, 1, 0, 0, 0, 0, 0, NULL, 1),

    -- Il se déplace vers Fête & Musique 
    (88, 'Festival culinaire', 'festival-culinaire', 0, 1, 9, 0, 0, 0, 0, 0, 0, 16, 1),

  -- Marchés, Braderies & Brocantes
    (89, 'Foire', 'foire', 0, 10, NULL, 0, 0, 0, 0, 0, 0, 19, 0),
    (90, 'Braderie', 'braderie', 0, 10, NULL, 0, 0, 0, 0, 0, 0, 19, 0),
    (91, 'Brocante', 'brocante', 0, 10, NULL, 0, 0, 0, 0, 0, 0, 19, 0),
    (92, 'Vide grenier', 'vide-grenier', 0, 10, NULL, 1, 0, 0, 0, 0, 0, 19, 1),
    (93, 'Marché', 'marche', 0, 10, NULL, 0, 0, 0, 0, 0, 0, 19, 1),
    (94, 'Marché de noël', 'marche-de-noel', 0, 10, NULL, 0, 0, 0, 0, 0, 0, 19, 0),
    (95, 'Bourse aux livres', 'bourse-aux-livres', 0, 10, 3, 0, 0, 0, 0, 0, 0, 19, 1),

  -- Mode
    (96, 'Défilé', 'défile', 0, 11, NULL, 1, 0, 1, 0, 0, 0, 12, 1),
    (97, 'Gala', 'gala-de-mode', 0, 11, NULL, 1, 0, 1, 0, 0, 0, 12, 1),
    (98, 'Pop up apéro', 'pop-up-apero', 0, 11, NULL, 1, 0, 0, 0, 0, 0, 12, 1),

  -- Jeux
    (99, 'Jeux vidéo', 'jeux-video', 0, 12, NULL, 1, 0, 0, 0, 0, 0, 63, 0),
    (100, 'Jeux en plein air', 'jeux-en-plein-air', 0, 12, NULL, 1, 0, 0, 0, 0, 0, 14, 0),
    (101, 'Fête foraine', 'fete-foraine', 0, 12, NULL, 0, 0, 0, 0, 0, 0, 14, 0),
    (102, 'Jeux de société', 'jeux-de-societe', 0, 12, NULL, 1, 0, 0, 0, 0, 0, 64, 0),
    (103, 'Autres Jeux', 'autres-jeux', 0, 12, NULL, 1, 0, 0, 0, 0, 0, 14, 0),

  -- Bien-être
  -- Boissons
    (104, 'Dégustation de vins', 'degustation-de-vins', 0, 14, NULL, 1, 0, 0, 0, 0, 0, 90, 1),
    (105, 'Dégustation de bières', 'degustation-de-bieres', 0, 14, NULL, 1, 0, 0, 0, 0, 0, 89, 1),
    (106, 'Dégustation boissons', 'degustation-boissons', 0, 14, NULL, 1, 0, 0, 0, 0, 0, 88, 0),

  -- Affaires
    (107, 'Inauguration', 'inauguration', 0, 17, NULL, 1, 0, 0, 0, 0, 0, 158, 1),
    (108, 'Lancement de produit', 'lancement-de-produit', 0, 17, NULL, 0, 0, 1, 0, 0, 0, 158, 0),
    (109, 'Portes ouvertes', 'portes-ouvertes', 0, 17, NULL, 1, 0, 0, 0, 0, 0, 158, 0),
    (110, 'Réseautage', 'reseautage', 0, 17, NULL, 1, 0, 0, 0, 0, 0, 158, 0),

  (111, 'Rentrée', 'rentree', 1, NULL, NULL, 1, 0, 0, 0, 0, 1, NULL, 0),
  (112, 'Journée recrutement', 'journee-recrutement', 1, NULL, NULL,  1, 0, 0, 0, 0, 1, NULL, 0),

  (113, 'Fête locale', 'fete-locale', 1, NULL, NULL, 0, 0, 0, 1, 0, 0, NULL, 0),

  (114, 'Autre Festival', 'autres-festivals', 1, NULL, NULL, 0, 0, 0, 0, 0, 1, NULL, 0),

  (115, 'Autres', 'autres', 1, NULL, NULL, 1, 0, 0, 0, 0, 1, NULL, 0),
  (116, 'Conférence', 'conference', 1, NULL, NULL, 1, 0, 0, 0, 1, 1, NULL, 1),

  (117, 'Marché aux puces', 'marche-aux-puces', 0, 10, NULL, 0, 0, 0, 0, 0, 0, 19, 0),
  (118, 'Assemblée générale', 'assemblee-generale', 0, 17, NULL, 1, 0, 0, 0, 0, 0, 158, 0),

  (119, 'Fan Zone', 'fan-zone', 0, 4, NULL, 1, 0, 0, 0, 0, 0, 6, 1),
  (120, 'Village Sportif', 'village-sportif', 0, 4, NULL, 1, 0, 0, 0, 0, 0, 6, 1),
  (121, 'Festival de cinéma', 'festival-de-cinema', 0, 5, 2, 0, 0, 1, 0, 0, 0, 5, 1);

  INSERT INTO `EventCategory` (`id`, `name`, `event_category_string_id`, `is_principal`, `parent_id`, free_use_by_user, can_be_a_tour, is_representation_type, is_special_category,
    is_professional_event_category,  need_principal_activity_category, principal_activity_category, is_usable_for_programmation
  ) VALUES

  (122, 'Atelier', 'atelier', 1, NULL, 1, 0, 0, 0, 1, 1, NULL, 0),
  (123, 'Cours', 'cours', 1, NULL, 1, 0, 0, 0, 1, 1, NULL, 0),
  (124, 'Stage', 'stage', 1,  NULL, 1, 0, 0, 0, 1, 1, NULL, 0)
  ;

  INSERT INTO `EventCategory` (`id`, `name`, `event_category_string_id`, `is_principal`, `parent_id`, free_use_by_user, can_be_a_tour, is_representation_type, is_special_category,
    is_professional_event_category,  need_principal_activity_category, principal_activity_category, is_usable_for_programmation, is_charitable_event
  ) VALUES

  (125, 'Maraude', 'maraude', 1, NULL, 1, 0, 0, 0, NULL, NULL, NULL, 1, 1),
  (126, 'Don de sang', 'don-de-sang', 1, NULL, 1, 0, 0, 0, 1, 1, NULL, 1, 1),
  (127, 'Release party', 'release-party', 0, 1, 0, 0, 1, 0, 0, 0, 4, 1, 0),
  (128, 'Viste guidée', 'visite-guidee',  1, NULL, 0, 0, 1, 0, 0, 0, NULL, 1, 0),
  (129, 'Viste', 'visite',  1, NULL, 0, 0, 1, 0, 0, 0, NULL, 1, 0),
  (130, 'Boutique éphémère', 'boutique-ephemere',  1, NULL, 0, 0, 1, 0, 0, 0, NULL, 1, 0),
  (131, 'Collecte', 'collecte',  1, NULL, 0, 0, 1, 0, 0, 0, NULL, 1, 0);

  INSERT INTO `EventCategory` (`id`, `name`, `event_category_string_id`, `is_principal`, `parent_id`, second_parent_id, free_use_by_user, can_be_a_tour, 
    is_representation_type, is_special_category, is_professional_event_category, need_principal_activity_category, principal_activity_category,
    is_usable_for_programmation
  ) VALUES
  (132, 'Projection', 'projection', 0, 5, NULL, 1, 0, 0, 0, 0, 0, 5, 1);

  INSERT INTO `EventCategory` (`id`, `name`, `event_category_string_id`, `is_principal`, `parent_id`, free_use_by_user, can_be_a_tour, is_representation_type, is_special_category,
    is_professional_event_category,  need_principal_activity_category, principal_activity_category, is_usable_for_programmation, is_charitable_event
  ) VALUES

  (133, 'Kermesse', 'kermesse', 1, NULL, 1, 0, 0, 0, 1, 1, NULL, 1, 0);


  INSERT INTO `EventCategory` (
    `id`, `name`, `event_category_string_id`, `is_principal`,
    `free_use_by_user`, `can_be_a_tour`, `is_representation_type`,
    `is_special_category`, `is_usable_for_programmation`, `with_hourly`,
    `is_professional_event_category`, `need_principal_activity_category`,
    `principal_activity_category`, `second_parent_id`, `parent_id`, `is_charitable_event`
  ) VALUES
  (134, 'Agenda', 'agenda', 1, 0, 0, 0, 1, 0, 0, 0, 0, NULL, NULL, NULL, 0),
  (135, 'Vente spéciale', 'vente-speciale', 1, 0, 0, 0, 1, 0, 0, 0, 1, 158, NULL, NULL, 0),

  -- Vente spéciale / commerce
  (136, 'Liquidation', 'liquidation', 0, 1, 0, 0, 0, 1, 0, 0, 0, 158, 17, 135, 0),
  (137, 'Déstockage', 'destockage', 0, 1, 0, 0, 0, 1, 0, 0, 0, 158, 17, 135, 0),
  (138, 'Vente avant fermeture', 'vente-avant-fermeture', 0, 1, 0, 0, 0, 1, 0, 0, 0, 158, 17, 135, 0),
  (139, 'Vente privée', 'vente-privee', 0, 1, 0, 0, 0, 1, 0, 0, 0, 158, 17, 135, 0),
  (140, 'Vente flash', 'vente-flash', 0, 1, 0, 0, 0, 1, 0, 0, 0, 158, 17, 135, 0),
  (141, 'Grande vente', 'grande-vente', 0, 1, 0, 0, 0, 1, 0, 0, 0, 158, 17, 135, 0),
  (142, 'Vente de créateurs', 'vente-de-createurs', 0, 1, 0, 0, 0, 1, 0, 0, 0, 158, 11, 135, 0),
  (143, 'Vide-dressing', 'vide-dressing', 0, 1, 0, 0, 0, 1, 0, 0, 0, 12, 11, 135, 0),
  (144, 'Bourse aux vêtements', 'bourse-aux-vetements', 0, 1, 0, 0, 0, 1, 0, 0, 0, 12, 11, 135, 0),
  (145, 'Troc', 'troc', 0, 1, 0, 0, 0, 1, 0, 0, 0, 158, 10, 135, 0),
  (146, 'Vente aux enchères', 'vente-aux-encheres', 0, 1, 0, 0, 0, 1, 0, 0, 0, 158, 17, 135, 0),

  -- Vie des lieux
  (147, 'Ouverture de lieu', 'ouverture-de-lieu', 0, 1, 0, 0, 0, 1, 0, 0, 0, 158, NULL, 17, 0),
  (148, 'Réouverture de lieu', 'reouverture-de-lieu', 0, 1, 0, 0, 0, 1, 0, 0, 0, 158, NULL, 17, 0),
  (149, 'Anniversaire de lieu', 'anniversaire-de-lieu', 0, 1, 0, 0, 0, 1, 0, 0, 0, 158, NULL, 17, 0),

  -- Formats récurrents utiles
  (150, 'Quiz', 'quiz', 0, 1, 0, 0, 0, 1, 0, 0, 0, 14, NULL, 12, 0),
  (151, 'Soirée jeux', 'soiree-jeux', 0, 1, 0, 0, 0, 1, 0, 0, 0, 14, NULL, 12, 0),
  (152, 'Escape game', 'escape-game', 0, 1, 0, 0, 0, 1, 0, 0, 0, 14, NULL, 12, 0),
  (153, 'Jeu de piste', 'jeu-de-piste', 0, 1, 0, 0, 0, 1, 0, 0, 0, 14, NULL, 12, 0),
  (154, 'Chasse au trésor', 'chasse-au-tresor', 0, 1, 0, 0, 0, 1, 0, 0, 0, 14, NULL, 12, 0),

  -- Musique / scène participative
  (155, 'Open mic', 'open-mic', 0, 1, 0, 1, 0, 1, 0, 0, 0, 4, NULL, 1, 0),
  (156, 'Scène ouverte', 'scene-ouverte', 0, 1, 0, 1, 0, 1, 0, 0, 0, 4, NULL, 1, 0),
  (157, 'Jam session', 'jam-session', 0, 1, 0, 1, 0, 1, 0, 0, 0, 4, NULL, 1, 0),
  (158, 'Bœuf musical', 'boeuf-musical', 0, 1, 0, 1, 0, 1, 0, 0, 0, 4, NULL, 1, 0),

  -- Pro / emploi
  (159, 'Job dating', 'job-dating', 0, 1, 0, 0, 0, 1, 0, 1, 1, NULL, NULL, 17, 0),
  (160, 'Forum emploi', 'forum-emploi', 0, 1, 0, 0, 0, 1, 0, 1, 1, NULL, NULL, 17, 0),
  (161, 'Meetup', 'meetup', 0, 1, 0, 0, 0, 1, 0, 1, 1, NULL, NULL, 17, 0),
  (162, 'Hackathon', 'hackathon', 0, 1, 0, 0, 0, 1, 0, 1, 1, NULL, NULL, 17, 0),
  (163, 'Table ronde', 'table-ronde', 0, 1, 0, 0, 0, 1, 0, 1, 1, NULL, NULL, 116, 0),
  (164, 'Conférence-débat', 'conference-debat', 0, 1, 0, 0, 0, 1, 0, 1, 1, NULL, NULL, 116, 0),
  (165, 'Masterclass', 'masterclass', 0, 1, 0, 0, 0, 1, 0, 1, 1, NULL, NULL, 122, 0),

  -- Solidarité / santé / citoyen
  (166, 'Collecte alimentaire', 'collecte-alimentaire', 0, 1, 0, 0, 0, 1, 0, 0, 0, 16, NULL, 131, 1),
  (167, 'Collecte de vêtements', 'collecte-de-vetements', 0, 1, 0, 0, 0, 1, 0, 0, 0, 12, NULL, 131, 1),
  (168, 'Collecte de jouets', 'collecte-de-jouets', 0, 1, 0, 0, 0, 1, 0, 0, 0, 14, NULL, 131, 1),
  (169, 'Distribution alimentaire', 'distribution-alimentaire', 1, 1, 0, 0, 0, 1, 0, 0, 0, 16, NULL, NULL, 1),
  (170, 'Repas solidaire', 'repas-solidaire', 1, 1, 0, 0, 0, 1, 0, 0, 0, 16, NULL, NULL, 1),
  (171, 'Dépistage', 'depistage', 1, 1, 0, 0, 0, 1, 0, 0, 0, NULL, NULL, NULL, 0),
  (172, 'Journée de sensibilisation', 'journee-de-sensibilisation', 1, 1, 0, 0, 1, 1, 0, 0, 1, NULL, NULL, NULL, 0),
  (173, 'Opération nettoyage', 'operation-nettoyage', 1, 1, 0, 0, 0, 1, 0, 0, 0, NULL, NULL, NULL, 1),
  (174, 'Bénévolat', 'benevolat', 1, 1, 0, 0, 1, 1, 0, 0, 1, NULL, NULL, NULL, 1),

  -- Famille / local
  (175, 'Animation enfant', 'animation-enfant', 1, 1, 0, 0, 0, 1, 0, 0, 1, NULL, NULL, NULL, 0),
  (176, 'Fête d’école', 'fete-ecole', 1, 1, 0, 0, 0, 1, 0, 0, 1, NULL, NULL, NULL, 0),

  -- Bien-être : raccourcis populaires
  (177, 'Cours de yoga', 'cours-de-yoga', 0, 1, 0, 0, 0, 1, 0, 0, 0, 13, 13, 123, 0),
  (178, 'Cours de méditation', 'cours-de-meditation', 0, 1, 0, 0, 0, 1, 0, 0, 0, 13, 13, 123, 0),
  (179, 'Cours de pilates', 'cours-de-pilates', 0, 1, 0, 0, 0, 1, 0, 0, 0, 13, 13, 123, 0),
  (180, 'Cours de sophrologie', 'cours-de-sophrologie', 0, 1, 0, 0, 0, 1, 0, 0, 0, 13, 13, 123, 0),
  (181, 'Atelier bien-être', 'atelier-bien-etre', 0, 1, 0, 0, 0, 1, 0, 0, 0, 13, 13, 122, 0),
  (182, 'Massage découverte', 'massage-decouverte', 0, 1, 0, 0, 0, 1, 0, 0, 0, 13, 13, NULL, 0),
  (183, 'Bain sonore', 'bain-sonore', 0, 1, 0, 0, 0, 1, 0, 0, 0, 13, 13, NULL, 0),
  (184, 'Cercle de parole', 'cercle-de-parole', 0, 1, 0, 0, 0, 1, 0, 0, 0, 13, 13, NULL, 0),

  -- Food : raccourcis populaires
  (185, 'Atelier cuisine', 'atelier-cuisine', 0, 1, 0, 0, 0, 1, 0, 0, 0, 16, 9, 122, 0),
  (186, 'Cours de cuisine', 'cours-de-cuisine', 0, 1, 0, 0, 0, 1, 0, 0, 0, 16, 9, 123, 0),
  (187, 'Repas thématique', 'repas-thematique', 0, 1, 0, 0, 0, 1, 0, 0, 0, 16, NULL, 9, 0),
  (188, 'Dîner', 'diner', 0, 1, 0, 0, 0, 1, 0, 0, 0, 16, NULL, 9, 0),
  (189, 'Banquet', 'banquet', 0, 1, 0, 0, 0, 1, 0, 0, 0, 16, NULL, 9, 0),
  (190, 'Apéro', 'apero', 0, 1, 0, 0, 0, 1, 0, 0, 0, 17, NULL, 14, 0),
  (191, 'Brunch musical', 'brunch-musical', 0, 1, 0, 0, 0, 1, 0, 0, 0, 16, 1, 9, 0),
  (192, 'Dégustation produits locaux', 'degustation-produits-locaux', 0, 1, 0, 0, 0, 1, 0, 0, 0, 16, NULL, 9, 0),
  (193, 'Accord mets et vins', 'accord-mets-et-vins', 0, 1, 0, 0, 0, 1, 0, 0, 0, 90, 9, 14, 0),

  -- Pro / rencontres pro
  (194, 'Rencontre professionnelle', 'rencontre-professionnelle', 0, 1, 0, 0, 0, 1, 0, 1, 1, NULL, NULL, 17, 0),
  (195, 'Petit-déjeuner business', 'petit-dejeuner-business', 0, 1, 0, 0, 0, 1, 0, 1, 1, NULL, NULL, 17, 0),
  (196, 'Déjeuner business', 'dejeuner-business', 0, 1, 0, 0, 0, 1, 0, 1, 1, NULL, NULL, 17, 0),
  (197, 'Workshop', 'workshop', 0, 1, 0, 0, 0, 1, 0, 1, 1, NULL, NULL, 122, 0),
  (198, 'Pitch', 'pitch', 0, 1, 0, 0, 0, 1, 0, 1, 1, NULL, NULL, 17, 0),
  (199, 'Remise de prix', 'remise-de-prix', 0, 1, 0, 0, 0, 1, 0, 1, 1, NULL, NULL, 17, 0),

  -- Concours
  (200, 'Concours', 'concours', 1, 1, 0, 0, 1, 0, 0, 0, 1, NULL, NULL, NULL, 0),
  (201, 'Concours d’éloquence', 'concours-eloquence', 0, 1, 0, 1, 0, 1, 0, 0, 1, NULL, 3, 200, 0),
  (202, 'Concours artistique', 'concours-artistique', 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 2, 200, 0),
  (203, 'Concours culinaire', 'concours-culinaire', 0, 1, 0, 0, 0, 1, 0, 0, 1, 16, 9, 200, 0),
  (204, 'Concours photo', 'concours-photo', 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 2, 200, 0),
  (205, 'Concours de danse', 'concours-de-danse', 0, 1, 0, 1, 0, 1, 0, 0, 1, 7, 8, 200, 0),
  (206, 'Concours de chant', 'concours-de-chant', 0, 1, 0, 1, 0, 1, 0, 0, 1, 4, 1, 200, 0);


  INSERT INTO `EventCategory` (
    `id`, `name`, `event_category_string_id`, `is_principal`,
    `free_use_by_user`, `can_be_a_tour`, `is_representation_type`,
    `is_special_category`, `is_usable_for_programmation`, `with_hourly`,
    `is_professional_event_category`, `need_principal_activity_category`,
    `principal_activity_category`, `second_parent_id`, `parent_id`, `is_charitable_event`
  ) VALUES

  -- Battles / compétitions artistiques urbaines
  (207, 'Battle de danse', 'battle-de-danse', 0, 1, 0, 1, 0, 1, 0, 0, 0, 7, 8, 82, 0),
  (208, 'Battle hip-hop', 'battle-hip-hop', 0, 1, 0, 1, 0, 1, 0, 0, 0, 7, 8, 82, 0),
  (209, 'Battle rap', 'battle-rap', 0, 1, 0, 1, 0, 1, 0, 0, 0, 4, 1, 82, 0),
  (210, 'Freestyle rap', 'freestyle-rap', 0, 1, 0, 1, 0, 1, 0, 0, 0, 4, 1, 83, 0),

  -- Tournois de jeux / bar / loisirs
  (211, 'Tournoi de jeux', 'tournoi-de-jeux', 0, 1, 0, 0, 0, 1, 0, 0, 0, 14, 12, 50, 0),
  (212, 'Tournoi de jeux de société', 'tournoi-de-jeux-de-societe', 0, 1, 0, 0, 0, 1, 0, 0, 0, 64, 12, 211, 0),
  (213, 'Tournoi de jeux vidéo', 'tournoi-de-jeux-video', 0, 1, 0, 0, 0, 1, 0, 0, 0, 63, 12, 211, 0),
  (214, 'Tournoi e-sport', 'tournoi-e-sport', 0, 1, 0, 0, 0, 1, 0, 0, 0, 63, 12, 211, 0),
  (215, 'Tournoi de fléchettes', 'tournoi-de-flechettes', 0, 1, 0, 0, 0, 1, 0, 0, 0, 14, 12, 211, 0),
  (216, 'Tournoi de billard', 'tournoi-de-billard', 0, 1, 0, 0, 0, 1, 0, 0, 0, 14, 12, 211, 0),
  (217, 'Tournoi de baby-foot', 'tournoi-de-baby-foot', 0, 1, 0, 0, 0, 1, 0, 0, 0, 14, 12, 211, 0),
  (218, 'Tournoi Beer pong', 'tournoi-de-beer-pong', 0, 1, 0, 0, 0, 1, 0, 0, 0, 14, 14, 211, 0),
  (219, 'Loto', 'loto', 0, 1, 0, 0, 0, 1, 0, 0, 0, 14, 12, 12, 0),
  (220, 'Bingo', 'bingo', 0, 1, 0, 0, 0, 1, 0, 0, 0, 14, 12, 12, 0),
  (221, 'Dîner-concert', 'diner-concert', 0, 1, 0, 1, 0, 1, 0, 0, 0, 4, 9, 1, 0);


  -- Corrections conseillées
  UPDATE EventCategory SET name = 'Littérature', event_category_string_id = 'litterature' WHERE id = 3;
  UPDATE EventCategory SET name = 'Jeux', event_category_string_id = 'jeux' WHERE id = 12;
  UPDATE EventCategory SET event_category_string_id = 'congres' WHERE id = 22;
  UPDATE EventCategory SET name = 'Karaoké', event_category_string_id = 'karaoke' WHERE id = 28;
  UPDATE EventCategory SET name = 'DJ set' WHERE id = 35;
  UPDATE EventCategory SET name = 'Triathlon', event_category_string_id = 'triathlon' WHERE id = 45;
  UPDATE EventCategory SET name = 'Avant-première' WHERE id = 51;
  UPDATE EventCategory SET name = 'Dîner-spectacle' WHERE id = 69;
  UPDATE EventCategory SET name = 'Spectacle de lumière', event_category_string_id = 'spectacle-de-lumiere' WHERE id = 75;
  UPDATE EventCategory SET name = 'Spectacle sur glace', event_category_string_id = 'spectacle-sur-glace' WHERE id = 79;
  UPDATE EventCategory SET event_category_string_id = 'defile' WHERE id = 96;
  UPDATE EventCategory SET name = 'Visite guidée' WHERE id = 128;
  UPDATE EventCategory SET name = 'Visite' WHERE id = 129;
#endregion


CREATE TABLE `Atmosphere` (
  `id` tinyint unsigned NOT NULL primary key auto_increment,
  `name` varchar(30) NOT NULL,
  `string_id` varchar(30) NOT NULL unique,
  icone_url varchar(50) default null
);

INSERT INTO `Atmosphere` (`name`, `string_id`) values('Chic', 'chic');
INSERT INTO `Atmosphere` (`name`, `string_id`) values('Cosy', 'cosy');
INSERT INTO `Atmosphere` (`name`, `string_id`) values('Luxe', 'luxe');
INSERT INTO `Atmosphere` (`name`, `string_id`) values('Chaleureux', 'chaleureux');
INSERT INTO `Atmosphere` (`name`, `string_id`) values('Romantique', 'romantique');
INSERT INTO `Atmosphere` (`name`, `string_id`) values('Rustique', 'rustique');
INSERT INTO `Atmosphere` (`name`, `string_id`) values('Cheap', 'cheap');
INSERT INTO `Atmosphere` (`name`, `string_id`) values('Champêtre', 'champetre');
INSERT INTO `Atmosphere` (`name`, `string_id`) values('Moderne', 'moderne');
INSERT INTO `Atmosphere` (`name`, `string_id`) values('Vintage', 'vintage');
INSERT INTO `Atmosphere` (`name`, `string_id`) values('Chill', 'chill');
INSERT INTO `Atmosphere` (`name`, `string_id`) values('Décontracté', 'decontracte');
INSERT INTO `Atmosphere` (`name`, `string_id`) values('Haut de gamme', 'haut-de-gamme');
INSERT INTO `Atmosphere` (`name`, `string_id`) values('Calme', 'calme');

-- Tags sur les lieux & commerces
CREATE TABLE `ShopAndPlaceCharactTag` (
  `id` int unsigned NOT NULL primary key auto_increment,
  `name` varchar(50) NOT NULL,
  `string_id` varchar(50) NOT NULL unique,
  icone_url varchar(50) default null
);

-- Enfants
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values('Kids friendly', 'kids-friendly');

-- Terrasses
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values('Extérieur agréable', 'exterieur-agreable');

-- Produits Locaux, Ecologie
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values('Produits locaux', 'produits-locaux');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values('Eco responsable', 'eco-responsable');

-- Coins cachés, secrets 
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values('Coin secret', 'coin-secret');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values('Coin caché', 'coin-cache');


-- Vue 
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values('Super vue', 'super-vue');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values("Au bord de l'eau", 'au-bord-de-leau');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values("Vue sur mer", 'vue-sur-mer');

INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values('Cosmopolite', 'cosmopolite');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values('Populaire', 'populaire');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values('Insolite', 'insolite');


INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values('Terasse agréable', 'terasse-agreable');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values('Terasse avec vue', 'terasse-avec-vue');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values('Terasse en bord de route', 'terasse-en-bord-de-route');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values('Terasse en bord de mer', 'terasse-en-bord-de-mer');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values("Terasse en bord de d'eau", 'terasse-en-bord-d-eau');

INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values("Stationnement facile", 'stationnement-facile');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values("Parking gratuit", 'parking-gratuit');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values("Parking gratuit dans la rue", 'parking-gratuit-dans-la-rue');

INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values("Excellents cocktails", 'excellents-cocktails');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values("Bien pour danser", 'bien-pour-danser');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values("Bien pour concerts", 'bien-pour-concerts');

INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values("Grand choix de bières", 'grand-choix-de-bieres');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values("Grand choix de vins", 'grand-choix-de-vins');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values("Service rapide", 'service-rapide');

INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values("Roof top", 'roof-top');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values("Excellents desserts", 'excellents-desserts');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values("Excellentes pâtisseries", 'excellents-patisseries');

INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values("Diffusion sport", 'diffusion-sport');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values("Produits sains", 'produits-sains');
INSERT INTO `ShopAndPlaceCharactTag` (`name`, `string_id`) values("Healthy", 'healthy');

INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Incontournable', 'incontournable');
INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Très populaire', 'tres-populaire');
INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Lieu iconique', 'lieu-iconique');
INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Adresse signature', 'adresse-signature');

INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Parfait pour un date', 'parfait-pour-un-date');
INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Cadre romantique', 'cadre-romantique');
INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Intimiste', 'intimiste');

INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Adapté aux familles', 'adapte-aux-familles');
INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Poussette friendly', 'poussette-friendly');
INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Bien avec enfants', 'bien-avec-enfants');

INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Bien pour travailler', 'bien-pour-travailler');
INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Calme pour travailler', 'calme-pour-travailler');
INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Bon wifi', 'bon-wifi');
INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Bien en solo', 'bien-en-solo');

INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Bien par beau temps', 'bien-par-beau-temps');
INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ("A l'ombre", 'a-l-ombre');
INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Lieu couvert', 'lieu-couvert');
INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Bien quand il pleut', 'bien-quand-il-pleut');

INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Ambiance festive', 'ambiance-festive');
INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Ambiance posée', 'ambiance-posee');
INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Bien pour afterwork', 'bien-pour-afterwork');
INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Bien pour groupe', 'bien-pour-groupe');

INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('A voir absolument', 'a-voir-absolument');
INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Parfait pour une balade', 'parfait-pour-une-balade');
INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Spot photo', 'spot-photo');
INSERT INTO ShopAndPlaceCharactTag (name, string_id) VALUES ('Vue panoramique', 'vue-panoramique');

ALTER TABLE ShopAndPlaceCharactTag
    ADD COLUMN tag_types SET('PLACE', 'EVENT', 'EXPERIENCE', 'CAMPAIN', 'PARTNERS') NOT NULL DEFAULT 'PLACE',
    ADD COLUMN logo_media varchar(100) DEFAULT NULL,
    ADD COLUMN is_public_page BOOLEAN DEFAULT 0,
    ADD COLUMN description TEXT DEFAULT NULL;

/* ============================================================
   UPDATES DES TAGS EXISTANTS
   ============================================================ */

/* PLACE uniquement */
UPDATE ShopAndPlaceCharactTag
SET tag_types = 'PLACE'
WHERE string_id IN (    
    'exterieur-agreable',
    'produits-locaux',
    'eco-responsable',
    'coin-secret',
    'coin-cache',
    'super-vue',
    'au-bord-de-leau',
    'vue-sur-mer',
    'cosmopolite',    
    'terasse-agreable',
    'terasse-avec-vue',
    'terasse-en-bord-de-route',
    'terasse-en-bord-de-mer',
    'terasse-en-bord-d-eau',
    'stationnement-facile',
    'parking-gratuit',
    'parking-gratuit-dans-la-rue',
    'grand-choix-de-bieres',
    'grand-choix-de-vins',
    'service-rapide',
    'roof-top',
    'excellents-desserts',
    'excellents-patisseries',
    'produits-sains',
    'healthy',
    'spot-photo',
    'vue-panoramique',
    'a-l-ombre',
    'lieu-couvert'
);


/* PLACE + EVENT */
UPDATE ShopAndPlaceCharactTag
SET tag_types = 'PLACE,EVENT'
WHERE string_id IN (
    'excellents-cocktails',
    'bien-pour-concerts',
    'diffusion-sport',
    'ambiance-festive',
    'populaire',
    'insolite'
);


/* PLACE + EVENT + EXPERIENCE */
UPDATE ShopAndPlaceCharactTag
SET tag_types = 'PLACE,EVENT,EXPERIENCE'
WHERE string_id IN (
    'bien-pour-danser',
    'bien-pour-groupe',
    'parfait-pour-un-date',
    'intimiste',
    'bien-en-solo',
    'bien-pour-afterwork',
    'parfait-pour-une-balade',
    'kids-friendly'
);


/* PLACE + EXPERIENCE */
UPDATE ShopAndPlaceCharactTag
SET tag_types = 'PLACE,EXPERIENCE'
WHERE string_id IN (
    'cadre-romantique',
    'adapte-aux-familles',
    'poussette-friendly',
    'bien-avec-enfants',
    'bien-pour-travailler',
    'calme-pour-travailler',
    'bon-wifi',
    'bien-par-beau-temps',
    'bien-quand-il-pleut',
    'ambiance-posee'
);


/* PLACE + CAMPAIGN */
UPDATE ShopAndPlaceCharactTag
SET tag_types = 'PLACE,CAMPAIN'
WHERE string_id IN (
    'incontournable',
    'tres-populaire',
    'lieu-iconique',
    'adresse-signature',
    'a-voir-absolument'
);


/* Pages publiques (sans doublons) */
UPDATE ShopAndPlaceCharactTag
SET is_public_page = 1
WHERE string_id IN (
    'kids-friendly',
    'exterieur-agreable',
    'produits-locaux',
    'eco-responsable',
    'coin-secret',
    'coin-cache',
    'super-vue',
    'au-bord-de-leau',
    'vue-sur-mer',
    'cosmopolite',
    'populaire',
    'insolite',
    'terasse-agreable',
    'terasse-avec-vue',
    'terasse-en-bord-de-route',
    'terasse-en-bord-de-mer',
    'terasse-en-bord-d-eau',
    'stationnement-facile',
    'parking-gratuit',
    'parking-gratuit-dans-la-rue',
    'grand-choix-de-bieres',
    'grand-choix-de-vins',
    'service-rapide',
    'roof-top',
    'excellents-desserts',
    'excellents-patisseries',
    'produits-sains',
    'healthy',
    'spot-photo',
    'vue-panoramique',
    'a-l-ombre',
    'lieu-couvert',
    'incontournable',
    'tres-populaire',
    'lieu-iconique',
    'adresse-signature',
    'a-voir-absolument',
    'cadre-romantique',
    'adapte-aux-familles',
    'poussette-friendly',
    'bien-avec-enfants',
    'bien-pour-travailler',
    'calme-pour-travailler',
    'bon-wifi',
    'bien-par-beau-temps',
    'bien-quand-il-pleut',
    'ambiance-posee',
    'excellents-cocktails',
    'bien-pour-concerts',
    'diffusion-sport',
    'ambiance-festive',
    'bien-pour-danser',
    'bien-pour-groupe',
    'parfait-pour-un-date',
    'intimiste',
    'bien-en-solo',
    'bien-pour-afterwork',
    'parfait-pour-une-balade'
);

/* Inserts corrigés avec tag_types + non publics */

INSERT INTO ShopAndPlaceCharactTag
(name, string_id, tag_types, is_public_page)
VALUES
('Scènes izilife', 'scenes-izilife', 'EVENT', 0);

INSERT INTO ShopAndPlaceCharactTag
(name, string_id, tag_types, is_public_page)
VALUES
('Events izilife', 'events-izilife', 'EVENT', 0);

INSERT INTO ShopAndPlaceCharactTag
(name, string_id, tag_types, is_public_page)
VALUES
('Partenaires izilife', 'partners-izilife', 'PARTNERS', 0);

INSERT INTO ShopAndPlaceCharactTag
(name, string_id, tag_types, is_public_page)
VALUES
('Coups de coeur', 'coups-de-coeur', 'PLACE,EVENT,CAMPAIN', 0);



('Spots touristes', 'spots-touristes', 'PLACE,LOCALITY', 0, 1, 65, 1, 1),
('Spots locaux', 'spots-locaux', 'PLACE,LOCALITY', 0, 1, 70, 1, 1),;


--  Scènes Izilife 


ALTER TABLE ShopAndPlaceCharactTag
    ADD COLUMN is_signal BOOLEAN DEFAULT 0,
    ADD COLUMN signal_weight SMALLINT DEFAULT 0,
    ADD COLUMN usable_for_suggestion BOOLEAN DEFAULT 0,
    ADD COLUMN usable_for_filter BOOLEAN DEFAULT 0;

UPDATE ShopAndPlaceCharactTag
SET is_signal = 1,
    usable_for_suggestion = 1,
    usable_for_filter = 1,
    signal_weight = 80
WHERE string_id IN (
    'lieu-iconique',
    'incontournable',
    'adresse-signature',
    'a-voir-absolument'
);

UPDATE ShopAndPlaceCharactTag
SET is_signal = 1,
    usable_for_suggestion = 1,
    usable_for_filter = 1,
    signal_weight = 75
WHERE string_id IN (
    'coups-de-coeur',
    'super-vue',
    'vue-panoramique',
    'spot-photo',
    'au-bord-de-leau',
    'vue-sur-mer'
);

UPDATE ShopAndPlaceCharactTag
SET is_signal = 1,
    usable_for_suggestion = 1,
    usable_for_filter = 1,
    signal_weight = 70
WHERE string_id IN (
    'roof-top',
    'terasse-avec-vue',
    'terasse-agreable',
    'terasse-en-bord-de-mer',
    'terasse-en-bord-d-eau',
    'exterieur-agreable'
);

UPDATE ShopAndPlaceCharactTag
SET is_signal = 1,
    usable_for_suggestion = 1,
    usable_for_filter = 1,
    signal_weight = 65
WHERE string_id IN (
    'coin-secret',
    'coin-cache',
    'insolite',
    'tres-populaire',
    'populaire'
);

UPDATE ShopAndPlaceCharactTag
SET is_signal = 1,
    usable_for_suggestion = 1,
    usable_for_filter = 1,
    signal_weight = 60
WHERE string_id IN (
    'parfait-pour-un-date',
    'cadre-romantique',
    'intimiste',
    'parfait-pour-une-balade',
    'bien-par-beau-temps',
    'bien-quand-il-pleut',
    'lieu-couvert'
);

UPDATE ShopAndPlaceCharactTag
SET is_signal = 1,
    usable_for_suggestion = 1,
    usable_for_filter = 1,
    signal_weight = 55
WHERE string_id IN (
    'ambiance-festive',
    'ambiance-posee',
    'bien-pour-afterwork',
    'bien-pour-groupe',
    'bien-pour-travailler',
    'calme-pour-travailler',
    'bon-wifi',
    'bien-en-solo',
    'kids-friendly',
    'adapte-aux-familles',
    'bien-avec-enfants'
);


INSERT IGNORE INTO ShopAndPlaceCharactTag
(name, string_id, tag_types, is_public_page, is_signal, signal_weight, usable_for_suggestion, usable_for_filter)
VALUES
('Lieu de rendez-vous', 'lieu-de-rdv', 'PLACE', 0, 1, 65, 1, 1),
('Lieu central', 'lieu-central', 'PLACE', 0, 1, 55, 1, 1),
('Lieu de passage', 'lieu-de-passage', 'PLACE', 0, 1, 45, 1, 1),
('Lieu de vie local', 'lieu-de-vie-local', 'PLACE', 0, 1, 70, 1, 1),
('Haut lieu local', 'haut-lieu-local', 'PLACE', 0, 1, 75, 1, 1),
('Spot coucher de soleil', 'spot-coucher-de-soleil', 'PLACE', 0, 1, 80, 1, 1),
('Spot calme', 'spot-calme', 'PLACE', 0, 1, 55, 1, 1),
('Spot pour se poser', 'spot-pour-se-poser', 'PLACE', 0, 1, 60, 1, 1),
('Lieu animé', 'lieu-anime', 'PLACE', 0, 1, 55, 1, 1),
('Lieu très fréquenté', 'lieu-tres-frequente', 'PLACE', 0, 1, 45, 1, 1),

('Event partenaire', 'event-partenaire', 'EVENT', 0, 1, 80, 1, 1),
('Event original', 'event-original', 'EVENT', 0, 1, 75, 1, 1),
('Grand event', 'grand-event', 'EVENT', 0, 1, 85, 1, 1),

('Expérience forte', 'experience-forte', 'EXPERIENCE', 0, 1, 80, 1, 1),
('Expérience signature', 'experience-signature', 'EXPERIENCE', 0, 1, 85, 1, 1),
('Expérience insolite', 'experience-insolite', 'EXPERIENCE', 0, 1, 80, 1, 1),
('Expérience originale', 'experience-originale', 'EXPERIENCE', 0, 1, 80, 1, 1),
('Expérience immersive', 'experience-immersive', 'EXPERIENCE', 0, 1, 80, 1, 1);



CREATE TABLE `LocalHabit` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,

  `name` varchar(150) NOT NULL,
  `string_id` varchar(150) DEFAULT NULL UNIQUE,
  `unique_id` varchar(32) DEFAULT NULL UNIQUE,

    scope_level ENUM(
            'PLACE',
            'SHOP',
            'ANNUAL_CELEBRATION',
            'EVENT_SERIE',
            'EVENT',
            'EXPERIENCE'
    ) NOT NULL,
    scope_id BIGINT UNSIGNED NOT NULL,

  `hobby_id` int DEFAULT NULL,

  `description` text DEFAULT NULL,
  `media_id` bigint unsigned DEFAULT NULL,

  `is_active` tinyint(1) NOT NULL DEFAULT 0,
  `priority` int NOT NULL DEFAULT 0,

  -- période d’affichage simple
  `start_month` tinyint unsigned DEFAULT NULL,
  `end_month` tinyint unsigned DEFAULT NULL,

  -- météo simple
  `weather_contexts` json DEFAULT NULL,
  -- ex: ["ensoleille","pluvieux","froid","chaud","neigeux"]

  -- moments simples
  `moment_contexts` json DEFAULT NULL,
  -- ex: ["matin","aprèsmidi","soir","nuit","weekday","weekend"]

  `creation_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  CONSTRAINT `chk_localhabit_months_range`
    CHECK (
      (start_month IS NULL OR (start_month BETWEEN 1 AND 12)) AND
      (end_month IS NULL OR (end_month BETWEEN 1 AND 12))
    ),
    
  INDEX `idx_localhabit_active_priority` (`is_active`, `priority`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `PrincipalCharacteristics` (
  `place_id` bigint default NULL,
  shop_id bigint default null, 
  event_id bigint default null,
  experience_id bigint default null,

  event_serie_id bigint default null, 
  annual_celebration_id bigint default null,

  `is_for_children` tinyint(1) DEFAULT 1,
  `adapted_to_children` tinyint(1) DEFAULT 1,
  `adapted_to_groups` tinyint(1) DEFAULT 1,
  `adapted_to_family` tinyint(1) NOT NULL DEFAULT 0,
  `adapted_to_family_with_children` tinyint(1) NOT NULL DEFAULT 0,
  `adapted_for_alone` tinyint(1) NOT NULL DEFAULT 0,
  `adapted_to_couple` tinyint(1) DEFAULT 1,
  `adapted_to_handicap` tinyint(1) NOT NULL DEFAULT 0,
  `adapted_to_strollers` tinyint(1) NOT NULL DEFAULT 0,

  is_lgbtq_place boolean default 0, 
  is_lgbtq_friendly_place boolean default 0,

  minimal_age tinyint unsigned default null, 

  range_price_start smallint default null, 
  range_price_end smallint default null, 
  range_level_id tinyint unsigned default null, 

  age_start tinyint unsigned not null, 
  age_end tinyint unsigned not null, 

  interior boolean default 0, 

  `can_eat_here` tinyint(1) DEFAULT 0,
  `can_drink_coffee` tinyint(1) DEFAULT 0,
  can_have_tea_time tinyint(1) DEFAULT 0,
  sell_tapas tinyint(1) DEFAULT 0,

  `can_work` tinyint(1) DEFAULT 0,
  `can_drink_alcool` tinyint(1) DEFAULT 0,
  `sell_alcool` tinyint(1) DEFAULT 0,
  
  `can_stay_for_sleep` tinyint(1) DEFAULT 0,

  `play_music` tinyint(1) DEFAULT 0,
  `can_danse` tinyint(1) DEFAULT 0,


  `have_terrace` tinyint(1) DEFAULT 0,
  `have_tv` tinyint(1) DEFAULT 0,
  `park` int(1) DEFAULT 1,
  wifi boolean default 0, 

  `noise_level` int(11) NOT NULL DEFAULT 0,
  is_active boolean default 1,
  is_adapted_for_date boolean default NULL,

  foreign key (range_level_id) references RangeLevel(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS CircuitImportLog;
DROP TABLE IF EXISTS CircuitTrackPoint;
DROP TABLE IF EXISTS CircuitRouteFile;
DROP TABLE IF EXISTS CircuitStep;
DROP TABLE IF EXISTS CircuitPlace;
DROP TABLE IF EXISTS Circuit;

CREATE TABLE Circuit (
  id bigint unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT,

  title varchar(255) NOT NULL,
  circuit_string_id varchar(255) NOT NULL UNIQUE,
  unique_id varchar(32) DEFAULT NULL UNIQUE,

  is_active tinyint(1) NOT NULL DEFAULT 0,
  publication_status enum('draft','review','published','archived') NOT NULL DEFAULT 'draft',

  circuit_picture bigint unsigned DEFAULT NULL,
  map_image varchar(255) DEFAULT NULL,

  circuit_type_id tinyint unsigned NOT NULL,
  circuit_theme_id tinyint unsigned DEFAULT NULL,
  sport_circuit_type_id tinyint unsigned DEFAULT NULL,
  vehicule_type tinyint unsigned DEFAULT NULL,
  difficulty_level_id tinyint unsigned DEFAULT NULL,

  scope_level enum('administrative_division','city') NOT NULL DEFAULT 'city',
  city_id bigint DEFAULT NULL,
  administrative_division_id bigint unsigned DEFAULT NULL,
  country_id bigint DEFAULT NULL,

  distance_measurement_unity_id tinyint unsigned DEFAULT 1,
  distance decimal(10,2) unsigned DEFAULT NULL,

  duration_measurement_unity_id tinyint unsigned DEFAULT 2,
  duration int unsigned DEFAULT NULL,

  height_difference_direction tinyint unsigned DEFAULT NULL,
  height_difference decimal(10,2) unsigned DEFAULT NULL,

  elevation_gain decimal(10,2) unsigned DEFAULT NULL,
  elevation_loss decimal(10,2) unsigned DEFAULT NULL,
  min_altitude decimal(10,2) DEFAULT NULL,
  max_altitude decimal(10,2) DEFAULT NULL,

  route_shape_type enum('steps_only','gpx','geojson','kml','tcx','fit','manual_track','encoded_polyline') NOT NULL DEFAULT 'steps_only',
  route_geometry longtext DEFAULT NULL,
  route_point_count int unsigned DEFAULT NULL,
  is_loop tinyint(1) NOT NULL DEFAULT 0,

  start_place_id bigint DEFAULT NULL,
  start_shop_id bigint DEFAULT NULL,
  start_address varchar(255) DEFAULT NULL,
  start_longitude decimal(20,17) DEFAULT NULL,
  start_latitude decimal(20,17) DEFAULT NULL,

  end_place_id bigint DEFAULT NULL,
  end_shop_id bigint DEFAULT NULL,
  end_address varchar(255) DEFAULT NULL,
  end_longitude decimal(20,17) DEFAULT NULL,
  end_latitude decimal(20,17) DEFAULT NULL,

  longitude decimal(20,17) DEFAULT NULL,
  latitude decimal(20,17) DEFAULT NULL,

  is_accessible_for_kids tinyint(1) NOT NULL DEFAULT 0,
  minimal_age tinyint unsigned DEFAULT NULL,
  place_visit tinyint(1) NOT NULL DEFAULT 0,

  description text DEFAULT NULL,
  circuit_good_point text DEFAULT NULL,
  practical_infos text DEFAULT NULL,
  safety_infos text DEFAULT NULL,
  parking_infos text DEFAULT NULL,
  public_transport_infos text DEFAULT NULL,

  owner_type enum('izilife','user','page','partner') NOT NULL DEFAULT 'izilife',
  source_user_id bigint DEFAULT NULL,
  source_page_id bigint DEFAULT NULL,
  source_partner_id bigint DEFAULT NULL,
  source_name varchar(120) DEFAULT NULL,

  url_scrapped_from varchar(1024) DEFAULT NULL,
  external_id varchar(255) DEFAULT NULL,
  scraped_at datetime DEFAULT NULL,
  imported_at datetime DEFAULT NULL,
  import_status enum('raw','normalized','validated','rejected') DEFAULT NULL,

  watch_provider varchar(40) DEFAULT NULL,
  watch_activity_id varchar(255) DEFAULT NULL,
  watch_activity_type varchar(80) DEFAULT NULL,
  watch_synced_at datetime DEFAULT NULL,

  saving_default_language int DEFAULT 1,
  created_at datetime DEFAULT CURRENT_TIMESTAMP,
  updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  FOREIGN KEY(circuit_type_id) REFERENCES CircuitType(id),
  FOREIGN KEY(sport_circuit_type_id) REFERENCES SportCircuitType(id),
  FOREIGN KEY(difficulty_level_id) REFERENCES DifficultyLevel(id),
  FOREIGN KEY(distance_measurement_unity_id) REFERENCES DistanceMeasurementUnity(id),
  FOREIGN KEY(duration_measurement_unity_id) REFERENCES TimeMeasurementUnity(id),
  FOREIGN KEY(circuit_theme_id) REFERENCES CircuitTheme(id),

  INDEX idx_circuit_scope (scope_level, city_id, administrative_division_id),
  INDEX idx_circuit_type (circuit_type_id, sport_circuit_type_id, circuit_theme_id),
  INDEX idx_circuit_owner (owner_type, source_user_id, source_page_id, source_partner_id),
  INDEX idx_circuit_status (is_active, publication_status),
  INDEX idx_circuit_scrap (url_scrapped_from(255), external_id),
  FULLTEXT INDEX ft_circuit_text (title, circuit_string_id, description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE CircuitStep (
  id bigint unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT,
  circuit_id bigint unsigned NOT NULL,
  position smallint unsigned NOT NULL,

  object_type enum('place','shop','equipment','event','experience','art_piece','manual_point') NOT NULL DEFAULT 'place',

  place_id bigint DEFAULT NULL,
  shop_id bigint DEFAULT NULL,
  equipment_id bigint DEFAULT NULL,
  event_id bigint DEFAULT NULL,
  experience_id bigint DEFAULT NULL,
  art_piece_id bigint DEFAULT NULL,

  title varchar(255) DEFAULT NULL,
  short_description tinytext DEFAULT NULL,
  instruction text DEFAULT NULL,
  address varchar(255) DEFAULT NULL,

  longitude decimal(20,17) DEFAULT NULL,
  latitude decimal(20,17) DEFAULT NULL,

  distance_from_previous decimal(10,2) unsigned DEFAULT NULL,
  duration_from_previous int unsigned DEFAULT NULL,

  is_required tinyint(1) NOT NULL DEFAULT 1,

  created_at datetime DEFAULT CURRENT_TIMESTAMP,
  updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  FOREIGN KEY(circuit_id) REFERENCES Circuit(id) ON DELETE CASCADE,

  UNIQUE KEY uk_circuit_step_position (circuit_id, position),
  INDEX idx_step_place (place_id),
  INDEX idx_step_shop (shop_id),
  INDEX idx_step_object (object_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE CircuitRouteFile (
  id bigint unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT,
  circuit_id bigint unsigned NOT NULL,

  file_type enum('gpx','kml','geojson','fit','tcx') NOT NULL,
  original_filename varchar(255) DEFAULT NULL,
  storage_path varchar(512) NOT NULL,
  sha1_hash char(40) DEFAULT NULL,

  provider varchar(80) DEFAULT NULL,
  url_source varchar(1024) DEFAULT NULL,
  is_active tinyint(1) NOT NULL DEFAULT 1,

  created_at datetime DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY(circuit_id) REFERENCES Circuit(id) ON DELETE CASCADE,
  INDEX idx_route_file_circuit (circuit_id, file_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE CircuitTrackPoint (
  id bigint unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT,
  circuit_id bigint unsigned NOT NULL,
  route_file_id bigint unsigned DEFAULT NULL,

  position int unsigned NOT NULL,
  latitude decimal(20,17) NOT NULL,
  longitude decimal(20,17) NOT NULL,
  altitude decimal(10,2) DEFAULT NULL,
  recorded_at datetime DEFAULT NULL,
  distance_from_start decimal(10,2) unsigned DEFAULT NULL,

  FOREIGN KEY(circuit_id) REFERENCES Circuit(id) ON DELETE CASCADE,
  FOREIGN KEY(route_file_id) REFERENCES CircuitRouteFile(id) ON DELETE SET NULL,

  UNIQUE KEY uk_track_position (circuit_id, position),
  INDEX idx_track_file (route_file_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE CircuitImportLog (
  id bigint unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT,
  circuit_id bigint unsigned DEFAULT NULL,

  provider varchar(80) NOT NULL,
  source_url varchar(1024) NOT NULL,
  external_id varchar(255) DEFAULT NULL,

  status enum('pending','success','failed','ignored') NOT NULL DEFAULT 'pending',
  message text DEFAULT NULL,
  raw_payload mediumtext DEFAULT NULL,

  created_at datetime DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY(circuit_id) REFERENCES Circuit(id) ON DELETE SET NULL,
  INDEX idx_import_provider (provider, external_id),
  INDEX idx_import_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

#region Meetz
    DROP TABLE IF EXISTS
      MeetzCalendarOverride,
      MeetzDispatchLog,
      MeetzDispatchRun,
      MeetzCategoryCancellation,
      UserMeetzProfile,
      MeetzPlaceParticipationCategory,
      MeetzEventCategoryCommercial,
      MeetzPlaceParticipation,
      MeetzGroupMember,
      MeetzCategorySchedule,
      MeetzGroup,
      Meetzable,
      MeetzGroupStatus,
      MeetzOccurrenceStateCode,
      MeetzOccurrenceState,
      MeetzUserCredit,
      MeetzBooking,
      MeetzBookingStatus,
      MeetzParticipationPrice,
      MeetzZoneCity,
      MeetzCategoryVariantConf,
      MeetzZone,
      MeetzEventCategoryAllowedVariant,
      MeetzCategoryVariant,
      MeetzEventCategoryConf,
      MeetzEventCategory,
      MeetzCountry,
      WorkSector,
      MeetCoupleSituation,
      MeetPublicHobby,
      MeetzOverrideReasonCode,
      MeetzCountryOneShotPrice,
      UserPreferences,
      MeetzZoneCategoryActive,
      IzilifeMeetzProduct,
      MeetzMedias;

    CREATE TABLE MeetzEventCategory (
      id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(100) NOT NULL,
      string_id VARCHAR(100) NOT NULL UNIQUE,
      unique_id VARCHAR(32) NOT NULL UNIQUE,

      category_picture bigint unsigned default null,

      is_active BOOLEAN DEFAULT 0,

      media_id BIGINT UNSIGNED DEFAULT NULL,

      mvg_number tinyint unsigned default 3,
      perfect_number tinyint unsigned default NULL,
      min_per_unit tinyint UNSIGNED DEFAULT NULL,
      max_per_unit TINYINT UNSIGNED NOT NULL,
      max_unit_per_place INT DEFAULT 1, 

      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

      -- is_new boolean default 0,
      CONSTRAINT fk_category_picture
        FOREIGN KEY (category_picture) REFERENCES Media(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    CREATE TABLE MeetzEventCategoryCommercial (
        category_id SMALLINT UNSIGNED PRIMARY KEY,

        commercial_title VARCHAR(120) NOT NULL,
        commercial_subtitle VARCHAR(180) DEFAULT NULL,
        description TEXT NOT NULL,

        highlights JSON DEFAULT NULL,
        duration_minutes INT DEFAULT NULL,
        average_price DECIMAL(6,2) DEFAULT NULL,

        is_active BOOLEAN DEFAULT 1,

        FOREIGN KEY (category_id) REFERENCES MeetzEventCategory(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


    CREATE TABLE MeetzEventCategoryConf (
        id SMALLINT unsigned AUTO_INCREMENT PRIMARY KEY,
        category_id SMALLINT UNSIGNED NOT NULL,

        country_id INT NOT NULL,
        zone_id BIGINT UNSIGNED DEFAULT NULL,

        currency SMALLINT UNSIGNED NOT NULL,
        amount decimal(10,2) NOT NULL DEFAULT 0,

        is_automatically_frequent BOOLEAN DEFAULT 0,

      FOREIGN KEY (category_id) REFERENCES MeetzEventCategory(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    ALTER TABLE MeetzEventCategoryConf
        ADD UNIQUE KEY uq_conf_scope (category_id, country_id, zone_id);

    INSERT INTO MeetzEventCategory
        (id, name, string_id, is_active, media_id,
         perfect_number, min_per_unit, max_per_unit, mvg_number,
         max_unit_per_place, unique_id)
    VALUES
        (1,  'Dîner',               'diner',             1, NULL, 6, 5, 7, 4, 3, 'cat_1'),
        (2,  'Verre',               'verre',             1, NULL, 6, 4, 8, 4, 3, 'cat_2'),
        (3,  'Fléchettes',          'flechettes',        1, NULL, 5, 4, 6, 3, 2, 'cat_3'),
        (4,  'Billard',             'billard',           1, NULL, 4, 3, 6, 3, 2, 'cat_4'),
        (5,  'Café',                'cafe',              0, NULL, 4, 3, 5, 3, 2, 'cat_5'),
        (6,  'Jeux de société',     'jeux-de-societe',   0, NULL, 6, 4, 8, 4, 2, 'cat_6'),
        (7,  'Brunch',              'brunch',            0, NULL, 5, 4, 6, 4, 2, 'cat_7'),
        (8,  'Goûter',              'gouter',            0, NULL, 4, 3, 6, 3, 2, 'cat_8'),
        (9,  'Bowling',             'bowling',           0, NULL, 5, 4, 6, 4, 2, 'cat_9'),
        (10, 'Padel',               'padel',             0, NULL, 4, 4, 4, 4, 2, 'cat_10'),
        (11, 'Badminton',           'badminton',         0, NULL, 4, 4, 4, 4, 2, 'cat_11'),
        (12, 'Marche & Discussion', 'marche-discussion', 0, NULL, 6, 4,10, 4, 5, 'cat_12');    

    -- Conf (pricing + scope)
    INSERT INTO MeetzEventCategoryConf (category_id, country_id, zone_id, currency, amount, is_automatically_frequent)
    VALUES
      (1,  1, NULL, 1, 0.00, TRUE),
      (2,  1, NULL, 1, 0.00, TRUE),
      (3,  1, NULL, 1, 0.00, TRUE),
      (4,  1, NULL, 1, 0.00, TRUE),
      (5,  1, NULL, 1, 0.00, TRUE),
      (6,  1, NULL, 1, 0.00, TRUE),
      (7,  1, NULL, 1, 0.00, TRUE),
      (8,  1, NULL, 1, 0.00, TRUE),
      (9,  1, NULL, 1, 0.00, TRUE),
      (10, 1, NULL, 1, 0.00, TRUE),
      (11, 1, NULL, 1, 0.00, TRUE);


    -- Les differentes variantes existantes 
    CREATE TABLE MeetzCategoryVariant (
      id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(80) NOT NULL,
      string_id VARCHAR(80) NOT NULL UNIQUE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    INSERT INTO MeetzCategoryVariant(name, string_id) VALUES
      ('Entre Femmes','women-only'),
      ('LGBTQ+','lgbtq'),
      ('55 +','seniors'),
      ('Parents - Enfants','parents-enfants'),
      ('Enfants','enfants');


    -- On Alloue l'existance possible d'une variante à une catégorie 
    CREATE TABLE MeetzEventCategoryAllowedVariant (
        category_id SMALLINT UNSIGNED NOT NULL,
        variant_id SMALLINT UNSIGNED NOT NULL,
        is_active BOOLEAN DEFAULT 1,
        CONSTRAINT fk_allowedvariant_category
            FOREIGN KEY (category_id)
            REFERENCES MeetzEventCategory(id),

        CONSTRAINT fk_allowedvariant_variant
            FOREIGN KEY (variant_id)
            REFERENCES MeetzCategoryVariant(id),


        UNIQUE KEY uq_cat_variant (category_id, variant_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    INSERT INTO MeetzEventCategoryAllowedVariant (category_id, variant_id, is_active) VALUES
        -- Dîner
        (1, 1, 1),
        (1, 2, 0),
        (1, 3, 0),

        -- Apéro & Verre
        (2, 1, 1),
        (2, 2, 0),
        (2, 3, 0),

        -- Fléchettes & Verre
        (3, 1, 1),
        (3, 2, 0),
        (3, 3, 0),

        -- Billard & Verre
        (4, 1, 1),
        (4, 2, 0),
        (4, 3, 0)
        ON DUPLICATE KEY UPDATE is_active = VALUES(is_active);

    -- Configure les heures et les jours de répétition pour une conf plus haut. Donc ici on peut dire 
    -- Le Diner sans Variante (conf plus haut) a lieu les mercredis à 19:00
    -- Le Diner en mode 100% femme a lieu : Mardi à 20h (Si variante configuré), Sinon c'est le même jour et aux mêmes horaire que l'event normal
    CREATE TABLE MeetzCategorySchedule (
      id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,

      conf_id smallint UNSIGNED NOT NULL,
      variant_id SMALLINT UNSIGNED NULL,

      weekday TINYINT UNSIGNED NOT NULL, -- 1..7 (Mon..Sun)
      meeting_hour TIME NOT NULL,

      is_active BOOLEAN NOT NULL DEFAULT 1,

      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

      FOREIGN KEY (conf_id) REFERENCES MeetzEventCategoryConf(id),

      INDEX idx_conf_active (conf_id, is_active),
      INDEX idx_weekday (weekday)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    ALTER TABLE MeetzCategorySchedule    
      ADD KEY idx_variant (variant_id),
      ADD CONSTRAINT fk_sched_variant FOREIGN KEY (variant_id) REFERENCES MeetzCategoryVariant(id);



    INSERT INTO MeetzCategorySchedule (conf_id, weekday, meeting_hour, is_active)
        SELECT c.id, s.weekday, s.meeting_hour, 1
        FROM MeetzEventCategoryConf c
        JOIN (
          SELECT  1 AS category_id, 3 AS weekday, '19:00' AS meeting_hour UNION ALL
          SELECT  2, 4, '19:00' UNION ALL
          SELECT  2, 5, '19:00' UNION ALL
          SELECT  3, 3, '19:00' UNION ALL
          SELECT  3, 5, '19:00' UNION ALL
          SELECT  4, 3, '19:00' UNION ALL
          SELECT  4, 5, '19:00' UNION ALL
          SELECT  5, 6, '10:00' UNION ALL
          SELECT  5, 7, '10:00' UNION ALL
          SELECT  6, 7, '11:30' UNION ALL
          SELECT  7, 6, '16:00' UNION ALL
          SELECT  7, 7, '16:00' UNION ALL
          SELECT  8, 6, '15:00' UNION ALL
          SELECT  9, 6, '10:00' UNION ALL
          SELECT  9, 7, '10:00' UNION ALL
          SELECT 10, 6, '15:00' UNION ALL
          SELECT 11, 7, '08:00'
        ) s ON s.category_id = c.category_id
        WHERE c.country_id = 1
          AND c.zone_id IS NULL;

    CREATE TABLE MeetzZone (
      id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
      unique_id varchar(32) NOT NULL unique,

      country_id INT NOT NULL,
      name VARCHAR(120) NOT NULL,
      string_id VARCHAR(140) NOT NULL UNIQUE,

      central_city_id BIGINT NOT NULL,

      parent_zone_id BIGINT UNSIGNED DEFAULT NULL,
      weight INT DEFAULT 0,
      is_active BOOLEAN DEFAULT 1,

      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

      constraint meetz_zone_country_id_fk FOREIGN KEY (country_id) REFERENCES Country(id),
      constraint meetz_zone_city_id_fk FOREIGN KEY (central_city_id) REFERENCES City(id),
      constraint meetz_parent_zone_id_fk FOREIGN KEY (parent_zone_id) REFERENCES MeetzZone(id),

      INDEX idx_zone_country (country_id, is_active),
      INDEX idx_zone_city (central_city_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


     -- On configure une Variante sur une catégorie dans un pays/une zone. Et on l'active ou nos 
    CREATE TABLE MeetzCategoryVariantConf (
        id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

        -- Catégorie concernée (ex: diner, apero-et-verre...)
        category_id SMALLINT UNSIGNED NOT NULL,

        -- Variante concernée (classic, women-only, lgbtq, seniors...)
        variant_id SMALLINT UNSIGNED NOT NULL,

        -- Scope pays obligatoire
        country_id INT NOT NULL,

        -- Scope zone optionnel (NULL = conf pays / non NULL = override zone)
        zone_id BIGINT UNSIGNED DEFAULT NULL,

        -- Activation de la variante dans ce scope (1=active, 0=inactive)
        is_active BOOLEAN DEFAULT 1,

        -- Unicité sur le scope
        UNIQUE KEY uq_variant_scope (category_id, variant_id, country_id, zone_id),

        FOREIGN KEY (category_id) REFERENCES MeetzEventCategory(id),
        FOREIGN KEY (variant_id) REFERENCES MeetzCategoryVariant(id),
        FOREIGN KEY (zone_id) REFERENCES MeetzZone(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



    CREATE TABLE MeetzZoneCity (

      zone_id BIGINT UNSIGNED NOT NULL,
      city_id BIGINT NOT NULL,
      is_active BOOLEAN DEFAULT 1,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

      CONSTRAINT MZC_zone_id FOREIGN KEY (zone_id) REFERENCES MeetzZone(id),
      CONSTRAINT MZC_city_id FOREIGN KEY (city_id) REFERENCES City(id),

      UNIQUE KEY uq_zone_city (zone_id, city_id),
      INDEX idx_city_zone (city_id, zone_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



    CREATE TABLE MeetzBookingStatus (
      id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(50) NOT NULL,
      string_id VARCHAR(50) NOT NULL UNIQUE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    INSERT INTO MeetzBookingStatus(name, string_id) VALUES
      ('Brouillon','brouillon'),
      ('En attente paiement','en-attente-de-paiement'),
      ('Payé','paye'),
      ('Assigné','assigne'),
      ("En liste d'attente",'en-liste-d-attente'),
      ('Place offerte','place-offerte'), -- Il n'a pas été repeché de la file d'attente donc au procain il ne paie rien même s'il n'est pas abonné
      ('Expiré','expiré'), -- Expiré de la liste d'attente, nous n'avons pas pu placé
      ('Confirmé','confirme'),
      ('Suspendu','suspendu'),
      ('Annulé','annule'),
      ('Remboursé','rembourse');


    CREATE TABLE MeetzBooking (
      id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
      unique_id varchar(32) NOT NULL unique,

      user_id BIGINT NOT NULL,

      zone_id BIGINT UNSIGNED NOT NULL,
      category_id SMALLINT UNSIGNED NOT NULL,
      variant_id SMALLINT UNSIGNED DEFAULT NULL,
      date DATE NOT NULL,

      selected_date DATE NOT NULL,
      transaction_id BIGINT DEFAULT NULL,
      subscription_id BIGINT DEFAULT NULL,

      status_id TINYINT UNSIGNED NOT NULL,

      snapshot_meeting_hour TIME DEFAULT NULL,
      snapshot_spoken_languages_json JSON DEFAULT NULL,
      snapshot_diet_type_ids_json JSON DEFAULT NULL,
      snapshot_meetz_budget_band TINYINT UNSIGNED DEFAULT NULL,

      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

      accept_meetzable_event TINYINT(1) DEFAULT 0,
      source_type ENUM('classic','local_event','experience') NOT NULL DEFAULT 'classic',
      event_id bigint default NULL,
      experience_id bigint default NULL, 
      session_conf_id bigint unsigned default NULL, 

      waitlist_reason ENUM('late_join','replacement','group_full') NULL,
      waitlist_until DATETIME NULL,
      waitlist_priority SMALLINT UNSIGNED DEFAULT 0,


      constraint MB_1 FOREIGN KEY (event_id) REFERENCES LocalEvent(id),
      constraint MB_2 FOREIGN KEY (experience_id) REFERENCES Experience(id),
      constraint MB_3 FOREIGN KEY (session_conf_id) REFERENCES SessionConfigurationContent(id),

      constraint MB_4 FOREIGN KEY (user_id) REFERENCES User(id),
      constraint MB_5 FOREIGN KEY (zone_id) REFERENCES MeetzZone(id),
      constraint MB_6 FOREIGN KEY (category_id) REFERENCES MeetzEventCategory(id),
      constraint MB_7 FOREIGN KEY (variant_id) REFERENCES MeetzCategoryVariant(id),
      constraint MB_8 FOREIGN KEY (transaction_id) REFERENCES Transaction(id),
      constraint MB_9 FOREIGN KEY (subscription_id) REFERENCES Subscription(id),
      constraint MB_10 FOREIGN KEY (status_id) REFERENCES MeetzBookingStatus(id),

      INDEX idx_booking_dispatch (zone_id, selected_date, category_id, variant_id, status_id),
      INDEX idx_booking_user (user_id, selected_date)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    CREATE TABLE MeetzUserCredit (
      id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
      unique_id VARCHAR(32) NOT NULL UNIQUE,

      user_id BIGINT NOT NULL,
      source_booking_id BIGINT UNSIGNED NULL,

      credit_type ENUM('waitlist_compensation') NOT NULL,
      scope_country_id INT NULL,
      scope_category_id SMALLINT UNSIGNED NULL,

      remaining_uses SMALLINT UNSIGNED NOT NULL DEFAULT 1,
      expires_at DATETIME NULL,

      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      used_at DATETIME NULL,
      used_booking_id BIGINT UNSIGNED NULL,

      transaction_id bigint not null,

      INDEX idx_credit_user (user_id, remaining_uses, expires_at),
      constraint MBC_1 FOREIGN KEY (user_id) REFERENCES User(id),
      constraint MBC_2 FOREIGN KEY (source_booking_id) REFERENCES MeetzBooking(id),
      constraint MBC_3 FOREIGN KEY (used_booking_id) REFERENCES MeetzBooking(id)
    );


    CREATE TABLE Meetzable (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,

        event_id bigint default NULL,
        experience_id bigint default NULL, 
        circuit_id bigint default null, 
        equipment_id bigint default null, 
        zone_id BIGINT UNSIGNED not null, 

        is_active TINYINT(1) NOT NULL DEFAULT 1,

        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,


        FOREIGN KEY (event_id) REFERENCES LocalEvent(id),
        FOREIGN KEY (experience_id) REFERENCES Experience(id),
        FOREIGN KEY (circuit_id) REFERENCES Circuit(id),
        FOREIGN KEY (equipment_id) REFERENCES Equipment(id),
        FOREIGN KEY (zone_id) REFERENCES MeetzZone(id)

    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    CREATE TABLE MeetzGroupStatus (
      id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(50) NOT NULL,
      string_id VARCHAR(50) NOT NULL UNIQUE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    INSERT INTO MeetzGroupStatus(name, string_id) VALUES
      ('En création','pending'),
      ('Confirmé','confirmed'),
      ('Complet','full'),
      ('Annulé','cancelled');


    CREATE TABLE MeetzGroup (
      id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
      unique_id varchar(32) NOT NULL unique,

      zone_id BIGINT UNSIGNED NOT NULL,
      category_id SMALLINT UNSIGNED NOT NULL,
      variant_id SMALLINT UNSIGNED DEFAULT 1,
      scheduled_date DATE NOT NULL,

      place_id BIGINT DEFAULT NULL,
      shop_id BIGINT DEFAULT NULL,

      local_event_id BIGINT DEFAULT NULL,

      unit_index INT DEFAULT 1,
      max_capacity INT NOT NULL,

      meeting_hour TIME DEFAULT NULL,
      status_id TINYINT UNSIGNED NOT NULL DEFAULT 1,

      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

      destination_type ENUM('classic_place','local_event','experience') DEFAULT NULL,
      destination_id BIGINT UNSIGNED DEFAULT NULL,
      destination_label VARCHAR(120) DEFAULT NULL,
      destination_starts_at DATETIME DEFAULT NULL,

      CONSTRAINT MG_1 FOREIGN KEY (zone_id) REFERENCES MeetzZone(id),
      CONSTRAINT MG_2 FOREIGN KEY (category_id) REFERENCES MeetzEventCategory(id),
      CONSTRAINT MG_3 FOREIGN KEY (variant_id) REFERENCES MeetzCategoryVariant(id),
      CONSTRAINT MG_4 FOREIGN KEY (place_id) REFERENCES Place(id),
      CONSTRAINT MG_5 FOREIGN KEY (shop_id) REFERENCES Shop(id),
      CONSTRAINT MG_6 FOREIGN KEY (local_event_id) REFERENCES LocalEvent(id),
      CONSTRAINT MG_7 FOREIGN KEY (status_id) REFERENCES MeetzGroupStatus(id),

      INDEX idx_group_lookup (zone_id, scheduled_date, category_id, variant_id, status_id),
      INDEX idx_group_place (place_id, scheduled_date),
      INDEX idx_group_shop (shop_id, scheduled_date)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    CREATE TABLE MeetzGroupMember (
      group_id BIGINT UNSIGNED NOT NULL,
      user_id BIGINT NOT NULL,
      booking_id BIGINT UNSIGNED DEFAULT NULL,

      joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,

      CONSTRAINT MGM_1 FOREIGN KEY (group_id) REFERENCES MeetzGroup(id),
      CONSTRAINT MGM_2 FOREIGN KEY (user_id) REFERENCES User(id),
      CONSTRAINT MGM_3 FOREIGN KEY (booking_id) REFERENCES MeetzBooking(id),

      UNIQUE KEY uq_group_user (group_id, user_id),
      UNIQUE KEY uq_booking_once (booking_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    CREATE TABLE MeetzPlaceParticipation (
      id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
      unique_id varchar(32) NOT NULL unique,

      zone_id BIGINT UNSIGNED NOT NULL,

      place_id BIGINT DEFAULT NULL,
      shop_id  BIGINT DEFAULT NULL,


      priority TINYINT UNSIGNED NOT NULL DEFAULT 5,

      budget_band_id TINYINT UNSIGNED not null default 1, 

      is_active BOOLEAN DEFAULT 1,

      max_groups_per_day INT DEFAULT 2,
      max_groups_per_week INT DEFAULT NULL,

      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

      CONSTRAINT MPP_1 FOREIGN KEY (zone_id) REFERENCES MeetzZone(id),
      CONSTRAINT MPP_2 FOREIGN KEY (place_id) REFERENCES Place(id),
      CONSTRAINT MPP_3 FOREIGN KEY (shop_id) REFERENCES Shop(id),
      CONSTRAINT MPP_4  FOREIGN KEY (budget_band_id) REFERENCES SelectionBudgetBand(id),


      INDEX idx_part_zone (zone_id, is_active),
      INDEX idx_part_place (place_id),
      INDEX idx_part_shop (shop_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    CREATE TABLE MeetzPlaceParticipationCategory (
      participation_id BIGINT UNSIGNED NOT NULL,
      category_id SMALLINT UNSIGNED NOT NULL,

      priority TINYINT UNSIGNED NOT NULL DEFAULT 5,
      max_groups_per_day INT DEFAULT NULL,
      is_active BOOLEAN DEFAULT 1,

      Constraint MPPC_1 FOREIGN KEY (participation_id) REFERENCES MeetzPlaceParticipation(id),
      Constraint MPPC_2 FOREIGN KEY (category_id) REFERENCES MeetzEventCategory(id),

      UNIQUE KEY uq_part_cat (participation_id, category_id),
      INDEX idx_cat_priority (category_id, priority)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    CREATE TABLE MeetzOccurrenceStateCode (
        id tinyint UNSIGNED NOT NULL AUTO_INCREMENT primary key,
        name VARCHAR(50) NOT NULL,
        string_id VARCHAR(50) not null unique,
        step_order TINYINT UNSIGNED NOT NULL,
        is_terminal BOOLEAN NOT NULL DEFAULT 0,
        is_active BOOLEAN NOT NULL DEFAULT 1
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    INSERT INTO MeetzOccurrenceStateCode (string_id, name, step_order, is_terminal, is_active) VALUES
        ('collecting',          'En cours (inscriptions)',                 10, 0, 1),
        ('groups_created',      'Groupes créés (cron J-1)',                20, 0, 1),
        ('place_booking',       'Booking lieu',                            30, 0, 1),
        ('place_emailed',       'Email lieu',                              40, 0, 1),
        ('participants_emailed','Email participant',                       50, 0, 1),
        ('ok_final',            'OK final',                                60, 1, 1),
        ('cancelled',           'Annulé',                                  90, 1, 1);


    CREATE TABLE MeetzOccurrenceState (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,

        zone_id BIGINT UNSIGNED NOT NULL,
        category_id SMALLINT UNSIGNED NOT NULL,
        variant_id SMALLINT UNSIGNED NOT NULL DEFAULT 1,
        scheduled_date DATE NOT NULL,

        state_id tinyint unsigned NOT NULL DEFAULT 1,

        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

        note VARCHAR(255) DEFAULT NULL,
        updated_by BIGINT DEFAULT NULL,

        FOREIGN KEY (zone_id) REFERENCES MeetzZone(id),
        FOREIGN KEY (category_id) REFERENCES MeetzEventCategory(id),
        FOREIGN KEY (variant_id) REFERENCES MeetzCategoryVariant(id),
        FOREIGN KEY (state_id) REFERENCES MeetzOccurrenceStateCode(id),

        UNIQUE KEY uq_occurrence (zone_id, category_id, variant_id, scheduled_date),
        INDEX idx_state_lookup (zone_id, scheduled_date, category_id, variant_id),
        INDEX idx_state_code (state_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    CREATE TABLE WorkSector (
        id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(120) NOT NULL,
        string_id VARCHAR(120) NOT NULL UNIQUE,
        is_active BOOLEAN NOT NULL DEFAULT 1
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    INSERT INTO WorkSector (name, string_id, is_active) VALUES
        ('Tech / IT', 'tech-it', 1),
        ('Finance / Assurance', 'finance-assurance', 1),
        ('Santé', 'sante', 1),
        ('Éducation', 'education', 1),
        ('Commerce / Vente', 'commerce-vente', 1),
        ('Marketing / Communication', 'marketing-communication', 1),
        ('Hôtellerie / Restauration', 'hotellerie-restauration', 1),
        ('Industrie', 'industrie', 1),
        ('BTP / Immobilier', 'btp-immobilier', 1),
        ('Transport / Logistique', 'transport-logistique', 1),
        ('Droit / Juridique', 'droit-juridique', 1),
        ('Secteur public', 'secteur-public', 1),
        ('Arts / Culture', 'arts-culture', 1),
        ('Média', 'media', 1),
        ('ONG / Social', 'ong-social', 1),
        ('Entrepreneuriat', 'entrepreneuriat', 1),
        ('Étudiant', 'etudiant', 1),
        ('En recherche', 'en-recherche', 1),
        ('Autre', 'autre', 1);

    CREATE TABLE MeetPublicHobby (
        id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(120) NOT NULL,
        string_id VARCHAR(120) NOT NULL UNIQUE,
        is_active BOOLEAN NOT NULL DEFAULT 1
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    INSERT INTO MeetPublicHobby (name, string_id, is_active) VALUES
        ('Sport', 'sport', 1),
        ('Cinéma / Séries', 'cinema-series', 1),
        ('Musique', 'musique', 1),
        ('Concerts', 'concerts', 1),
        ('Lecture', 'lecture', 1),
        ('Jeux de société', 'jeux-de-societe', 1),
        ('Jeux vidéos', 'jeux-videos', 1),
        ('Cuisine', 'cuisine', 1),
        ('Voyage', 'voyage', 1),
        ('Photo', 'photo', 1),
        ('Nature / Rando', 'nature-rando', 1),
        ('Art / Musées', 'art-musees', 1),
        ('Bien-être', 'bien-etre', 1),
        ('Technologie', 'technologie', 1), 
        ('Business', 'business', 1);

    CREATE TABLE MeetCoupleSituation (
      id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(80) NOT NULL,
      string_id VARCHAR(80) NOT NULL UNIQUE,
      is_active BOOLEAN NOT NULL DEFAULT 1
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    INSERT INTO MeetCoupleSituation (name, string_id, is_active) VALUES
    ('Célibataire', 'single', 1),
    ('En couple', 'couple', 1),
    ('C’est compliqué', 'complicated', 1),
    ('Je préfère ne pas répondre', 'prefer-not', 1);


    CREATE TABLE UserMeetzProfile (
      user_id BIGINT NOT NULL PRIMARY KEY,

      birth_year SMALLINT UNSIGNED DEFAULT NULL,
      gender_identity TINYINT UNSIGNED DEFAULT NULL,

      activity_sector_id SMALLINT UNSIGNED DEFAULT NULL,
      nationality_id INT DEFAULT NULL,

      have_children TINYINT(1) NOT NULL DEFAULT 0,
      couple_situation_id TINYINT UNSIGNED DEFAULT NULL,

      spontaneity_level TINYINT UNSIGNED DEFAULT NULL,  -- 1..10

      i_think_im_introvert_person TINYINT UNSIGNED DEFAULT NULL, -- 1..10
      talkativeness TINYINT UNSIGNED DEFAULT NULL,      -- 1..10

      im_motivated_person TINYINT UNSIGNED DEFAULT NULL, 
      im_creative_person TINYINT UNSIGNED DEFAULT NULL,
      im_stressed_person TINYINT UNSIGNED DEFAULT NULL,
      i_love_my_job TINYINT UNSIGNED DEFAULT NULL,
      i_think_im_funny_person TINYINT UNSIGNED DEFAULT NULL, 
      i_think_im_smart_person TINYINT UNSIGNED DEFAULT NULL,
      i_think_im_non_conformist TINYINT UNSIGNED DEFAULT NULL,

      family_importance_for_me TINYINT UNSIGNED DEFAULT NULL,
      spirituality_importance_for_me TINYINT UNSIGNED DEFAULT NULL,
      humor_importance_for_me TINYINT UNSIGNED DEFAULT NULL,

      felling_alone_frequence TINYINT UNSIGNED DEFAULT NULL,

      i_love_party_with_friend TINYINT UNSIGNED DEFAULT NULL,
      i_love_sport TINYINT UNSIGNED DEFAULT NULL,
      nature_or_city_lover TINYINT UNSIGNED DEFAULT NULL,

      politically_incorrect_humor TINYINT UNSIGNED DEFAULT NULL,
      love_talk_about_polics_and_actuality TINYINT UNSIGNED DEFAULT NULL,
      political_scale TINYINT UNSIGNED DEFAULT NULL, -- 1..10

      topics_interest JSON DEFAULT NULL,
      hobbies JSON DEFAULT NULL,

      meetz_budget_band TINYINT UNSIGNED DEFAULT NULL, -- 1..10 (optionnel)
      preferred_currency_id SMALLINT UNSIGNED DEFAULT NULL,
      default_country_id INT DEFAULT NULL,
      default_city_id INT DEFAULT NULL,
      default_language_id INT DEFAULT NULL,

      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

      CONSTRAINT MUP_1 FOREIGN KEY (user_id) REFERENCES User(id),
      CONSTRAINT MUP_2 FOREIGN KEY (activity_sector_id) REFERENCES WorkSector(id),
      CONSTRAINT MUP_3 FOREIGN KEY (nationality_id) REFERENCES Country(id),
      CONSTRAINT MUP_4 FOREIGN KEY (couple_situation_id) REFERENCES MeetCoupleSituation(id),

      INDEX idx_profile_politics (political_scale),
      INDEX idx_profile_sector (activity_sector_id),
      INDEX idx_profile_nat (nationality_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    -- Meetz BO additions (activation par zone + pays "activé")
    CREATE TABLE IF NOT EXISTS MeetzCountry (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
        country_id INT NOT NULL UNIQUE,
        is_active BOOLEAN NOT NULL DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        constraint mc_1 FOREIGN KEY (country_id) REFERENCES Country(id),
        INDEX idx_country_active (is_active)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    INSERT INTO MeetzCountry (country_id, is_active)
    VALUES
      (1,  1);


    -- Meetz BO additions (activation par zone + pays "activé")
    CREATE TABLE IF NOT EXISTS MeetzCountryOneShotPrice (
        country_id INT NOT NULL UNIQUE,
        amount decimal(10, 2) not null,
        is_active boolean default 1,

        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        constraint mcocp_1 FOREIGN KEY (country_id) REFERENCES Country(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    INSERT INTO MeetzCountryOneShotPrice (country_id, amount) VALUES
      (1, 10)
      ;


    CREATE TABLE IF NOT EXISTS MeetzZoneCategoryActive (
        zone_id BIGINT UNSIGNED NOT NULL,
        category_id SMALLINT UNSIGNED NOT NULL,
        is_active BOOLEAN NOT NULL DEFAULT 1,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        constraint mzca_1 FOREIGN KEY (zone_id) REFERENCES MeetzZone(id),
        constraint mzca_2 FOREIGN KEY (category_id) REFERENCES MeetzEventCategory(id),
        UNIQUE KEY uq_zone_category (zone_id, category_id),
        INDEX idx_zone_active (zone_id, is_active)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    CREATE TABLE MeetzDispatchRun (
      id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,

      zone_id BIGINT UNSIGNED NOT NULL,
      scheduled_date DATE NOT NULL,

      started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      ended_at DATETIME DEFAULT NULL,

      created_groups INT NOT NULL DEFAULT 0,
      assigned_bookings INT NOT NULL DEFAULT 0,

      status VARCHAR(20) NOT NULL DEFAULT 'ok',
      message VARCHAR(255) DEFAULT NULL,

      constraint mdr_1 FOREIGN KEY (zone_id) REFERENCES MeetzZone(id),
      INDEX idx_dispatch (zone_id, scheduled_date)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    CREATE TABLE MeetzDispatchLog (
      id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,

      run_id BIGINT UNSIGNED NOT NULL,
      booking_id BIGINT UNSIGNED DEFAULT NULL,
      group_id BIGINT UNSIGNED DEFAULT NULL,

      action VARCHAR(40) NOT NULL,
      message VARCHAR(255) DEFAULT NULL,

      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

      constraint mdl_1 FOREIGN KEY (run_id) REFERENCES MeetzDispatchRun(id),
      constraint mdl_2 FOREIGN KEY (booking_id) REFERENCES MeetzBooking(id),
      constraint mdl_3 FOREIGN KEY (group_id) REFERENCES MeetzGroup(id),

      INDEX idx_run_action (run_id, action),
      INDEX idx_run_booking (run_id, booking_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    CREATE TABLE MeetzOverrideReasonCode (
      code VARCHAR(40) NOT NULL PRIMARY KEY,
      label VARCHAR(120) NOT NULL,
      is_active BOOLEAN NOT NULL DEFAULT 1
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    INSERT INTO MeetzOverrideReasonCode (code, label, is_active) VALUES
      ('holiday',            'Jour férié',                               1),
      ('weather',            'Conditions météorologiques défavorables',  1),
      ('partner_closed',     'Lieu ou partenaire fermé',                 1),
      ('low_demand',         'Demande insuffisante',                     1),
      ('staffing',           'Indisponibilité des équipes opérationnelles', 1),
      ('security',           'Incident ou contrainte de sécurité',       1),
      ('exceptional_event',  'Événement exceptionnel en ville',          1),
      ('maintenance',        'Maintenance produit ou infrastructure',    1),
      ('regulatory',         'Contrainte légale ou administrative',       1);

    CREATE TABLE MeetzCalendarOverride (
      id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
      unique_id varchar(32) NOT NULL unique,

      country_id INT NOT NULL,
      zone_id BIGINT UNSIGNED DEFAULT NULL,

      override_date DATE NOT NULL,
      reason_code VARCHAR(40) DEFAULT NULL,

      is_for_all_activities BOOLEAN NOT NULL DEFAULT 0,
      category_id SMALLINT UNSIGNED DEFAULT NULL,
      variant_id SMALLINT UNSIGNED DEFAULT NULL,

      override_kind ENUM('cancel','special') NOT NULL,

      override_meeting_hour TIME DEFAULT NULL,
      override_max_capacity INT DEFAULT NULL,

      note VARCHAR(255) DEFAULT NULL,

      is_active BOOLEAN DEFAULT 1,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

      constraint mco_1 FOREIGN KEY (country_id) REFERENCES Country(id),
      constraint mco_2 FOREIGN KEY (zone_id) REFERENCES MeetzZone(id),
      constraint mco_3 FOREIGN KEY (category_id) REFERENCES MeetzEventCategory(id),
      constraint mco_4 FOREIGN KEY (variant_id) REFERENCES MeetzCategoryVariant(id),

      INDEX idx_override_lookup (country_id, zone_id, override_date, is_active),
      INDEX idx_override_scope (override_date, is_for_all_activities, category_id, variant_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    CREATE TABLE UserPreferences (
      user_id BIGINT NOT NULL PRIMARY KEY,

      -- Identité "soft" / defaults
      origin_country_id INT DEFAULT NULL,
      default_city_id BIGINT DEFAULT NULL,
      default_zone_id BIGINT UNSIGNED DEFAULT NULL,
      default_language_id INT DEFAULT NULL,
      default_currency_id SMALLINT UNSIGNED DEFAULT NULL,

      -- Notifications
      notif_email_enabled TINYINT(1) NOT NULL DEFAULT 1,
      notif_sms_enabled TINYINT(1) NOT NULL DEFAULT 1,
      notif_push_enabled TINYINT(1) NOT NULL DEFAULT 0,

      -- JSON: langues parlées (ex: ["fr","en"])
      spoken_languages_json JSON DEFAULT NULL,

      -- JSON: restrictions alimentaires (ex: [1,4,6] => ids DietType)
      diet_type_ids_json JSON DEFAULT NULL,

      -- Meetz
      meetz_budget_band TINYINT UNSIGNED DEFAULT NULL,

      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

      CONSTRAINT fk_userpref_user FOREIGN KEY (user_id) REFERENCES User(id),
      CONSTRAINT fk_userpref_origin_country FOREIGN KEY (origin_country_id) REFERENCES Country(id),
      CONSTRAINT fk_userpref_city FOREIGN KEY (default_city_id) REFERENCES City(id),
      CONSTRAINT fk_userpref_zone FOREIGN KEY (default_zone_id) REFERENCES MeetzZone(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    CREATE TABLE IzilifeMeetzProduct (
      product_id BIGINT default null,

      requires_validation BOOLEAN NOT NULL DEFAULT 1,
      meetz_rules_json JSON DEFAULT NULL,

      created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated DATETIME NULL,

      cancel_booking_pay boolean default 0,

      CONSTRAINT fk_meetz_product FOREIGN KEY (product_id) REFERENCES Product(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    CREATE TABLE MeetzMedias (
        `meetz_event_category_id` SMALLINT UNSIGNED  NOT NULL ,
        `media_id` bigint unsigned NOT NULL ,

        is_principal boolean not null default 0,
        foreign key (meetz_event_category_id) references MeetzEventCategory(id),
        foreign key (media_id) references Media(id)
    );
#endregion


CREATE TABLE `UserFollowing` (
  `start_user_id` bigint NOT NULL,
  following_scope_level ENUM('user', 'page', 'place', 'shop', 'partner') not null, 
  following_scope_id bigint not null,
  `following_date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Les likes
CREATE TABLE `UserFavorite` (
  `user_id` bigint default NULL,
  page_id bigint default null, 

  `user_destination_id` bigint DEFAULT NULL,
  `page_destination_id` bigint DEFAULT NULL,
  `shop_destination_id` bigint DEFAULT NULL,
  `place_destination_id` bigint DEFAULT NULL,
  `event_destination_id` bigint DEFAULT NULL,
  `experience_destination_id` bigint DEFAULT NULL,
  `animation_destination_id` bigint DEFAULT NULL,
  `product_destination_id` bigint DEFAULT NULL,
  circuit_destination_id bigint DEFAULT NULL,

  `adding_date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci


#region Terrace & User Content
    CREATE TABLE `TerraceType` (
      `id` tinyint unsigned NOT NULL primary key auto_increment,
      `name` varchar(50) NOT NULL,
      `string_id` varchar(50) NOT NULL unique
    );

    INSERT INTO `TerraceType` (`name`, `string_id`) values('Privé', 'prive');
    INSERT INTO `TerraceType` (`name`, `string_id`) values('Espace public', 'espace-public');
    INSERT INTO `TerraceType` (`name`, `string_id`) values('Sur une rue connue', 'sur-une-rue-connue');
    INSERT INTO `TerraceType` (`name`, `string_id`) values('Sur une place connue', 'sur-une-place-connue');

    CREATE TABLE `Orientation` (
      `id` tinyint unsigned NOT NULL primary key auto_increment,
      `name` varchar(50) NOT NULL,
      `string_id` varchar(50) NOT NULL unique
    );
    INSERT INTO `Orientation` (`name`, `string_id`) values('Nord', 'nord');
    INSERT INTO `Orientation` (`name`, `string_id`) values('Sud', 'sud');
    INSERT INTO `Orientation` (`name`, `string_id`) values('Est', 'est');
    INSERT INTO `Orientation` (`name`, `string_id`) values('Ouest', 'ouest');

    INSERT INTO `Orientation` (`name`, `string_id`) values('Nord-est', 'nord-est');
    INSERT INTO `Orientation` (`name`, `string_id`) values('Nord-ouest', 'nord-ouest');
    INSERT INTO `Orientation` (`name`, `string_id`) values('Sud-ouest', 'sud-ouest');
    INSERT INTO `Orientation` (`name`, `string_id`) values('Sud-est', 'sud-est');


    CREATE TABLE Terrace (
        id BIGINT unsigned AUTO_INCREMENT PRIMARY KEY,
        unique_id varchar(32) not NULL unique,

        shop_id BIGINT default NULL,
        place_id BIGINT default null, 


        on_place_id BIGINT NULL, -- ex. Place Rihour
        on_known_street_id BIGINT NULL, -- futur FK vers une table Street
        on_known_street_name VARCHAR(255) NULL, -- ex. Rue de la Monnaie

        type tinyint unsigned NOT NULL,

        hidden BOOLEAN DEFAULT FALSE,
        waterfront BOOLEAN DEFAULT FALSE,
        roadside BOOLEAN DEFAULT FALSE,

        orientation tinyint unsigned default NULL,
        sun_periods JSON NULL,

        sun_from TIME NULL,
        sun_to TIME NULL,

        capacity SMALLINT NULL,
        has_parasol BOOLEAN DEFAULT FALSE,
        has_heater BOOLEAN DEFAULT FALSE,
        is_rooftop BOOLEAN DEFAULT FALSE,
        is_secret boolean default 0,
        is_privatizable boolean default 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

        FOREIGN KEY (shop_id) REFERENCES Shop(id),
        FOREIGN KEY (place_id) REFERENCES Place(id),
        FOREIGN KEY (on_place_id) REFERENCES Place(id)

        -- FOREIGN KEY (on_known_street_id) REFERENCES Street(id) -- à activer plus tard
    );
#endregion

#region Spotlights - Reference Tables
    CREATE TABLE LittleActivityOccasion (
        id TINYINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(200) NOT NULL,
        occasion_string_id VARCHAR(200) NOT NULL UNIQUE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    INSERT INTO LittleActivityOccasion (name, occasion_string_id) VALUES
        ('Soirée en amoureux', 'date-romantique'),
        ('Date', 'date'),
        ('Pause solo', 'pause-solo'),
        ('Sortie culturelle', 'sortie-culturelle'),
        ('Sortie sportive', 'sortie-sportive'),
        ('Sortie en famille', 'sortie-famille'),
        ('Sortie insolite', 'sortie-insolite'),
        ('Balade romantique', 'balade-romantique'),
        ('Activité créative', 'activite-creative'),
        ('Détente & bien-être', 'detente-bien-etre'),
        ('Journée pluvieuse', 'jour-de-pluie'),
        ('Journée ensoleillée', 'jour-en-soleil'),
        ('Activité entre seniors', 'entre-seniors'),
        ('Sortie avec animaux', 'avec-animaux'),
        ('Rencontre entre inconnus', 'rencontre-inconnus');
#endregion

#region Spotlights - Targets (Polymorphism Pivot)
    CREATE TABLE SpotlightTarget (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        target_type ENUM('PLACE','SHOP','EXPERIENCE','EVENT','EVENT_SERIE') NOT NULL,
        target_id BIGINT UNSIGNED NOT NULL,
        UNIQUE KEY uq_target (target_type, target_id),
        INDEX idx_target_type_id (target_type, target_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
#endregion

#region Spotlights - Manual Spotlights (Editorial Only)
    CREATE TABLE Spotlight (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,

        target_id BIGINT UNSIGNED NOT NULL,

        country_id BIGINT UNSIGNED NULL,
        region_id BIGINT UNSIGNED NULL,
        city_id BIGINT UNSIGNED NULL,

        start_month TINYINT UNSIGNED NULL,
        end_month TINYINT UNSIGNED NULL,

        start_date DATE NULL,
        end_date DATE NULL,

        status ENUM('DRAFT','PUBLISHED','ARCHIVED') NOT NULL DEFAULT 'DRAFT',

        priority INT NOT NULL DEFAULT 0,
        base_weight INT NOT NULL DEFAULT 1,

        mapped_spotlight_theme VARCHAR(100) NULL,

        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

        FOREIGN KEY (target_id) REFERENCES SpotlightTarget(id),

        INDEX idx_spotlight_scope_status (status, country_id, region_id, city_id),
        INDEX idx_spotlight_target (target_id),
        INDEX idx_spotlight_season (start_month, end_month),
        INDEX idx_spotlight_dates (start_date, end_date),
        INDEX idx_spotlight_priority (priority),

        CONSTRAINT chk_spotlight_months_range CHECK (
            (start_month IS NULL OR (start_month BETWEEN 1 AND 12)) AND
            (end_month IS NULL OR (end_month BETWEEN 1 AND 12))
        ),

        CONSTRAINT chk_spotlight_dates_range CHECK (
            (start_date IS NULL OR end_date IS NULL OR start_date <= end_date)
        ),

        CONSTRAINT chk_spotlight_time_window_consistency CHECK (
            NOT (start_month IS NULL AND end_month IS NOT NULL) AND
            NOT (start_month IS NOT NULL AND end_month IS NULL)
        )
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    -- De-dupe editorial: avoid multiple manual spotlights for the same target and same window+scope.
    -- If you want to allow several editorial spotlights per target, remove/relax this unique key.
    ALTER TABLE Spotlight
        ADD UNIQUE KEY uq_spotlight_manual_dedupe (
            target_id,
            country_id,
            region_id,
            city_id,
            start_month,
            end_month,
            start_date,
            end_date
        );
#endregion

#region Spotlights - Reasons & Profiles (Attached to Target, not Spotlight)
    CREATE TABLE TargetReason (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        target_id BIGINT UNSIGNED NOT NULL,

        reason_type ENUM(
            'HOBBY',
            'OBJECT',
            'ATMOSPHERE',
            'OCCASION',
            'EQUIPMENT_CATEGORY',
            'TAG',
            'LITTLE_ACTIVITY_OCCASION',
            'WEATHER'
        ) NOT NULL,

        reason_ref_id BIGINT UNSIGNED NOT NULL,
        weight INT NOT NULL DEFAULT 1,

        source ENUM('MANUAL','RULE','MODEL') NOT NULL DEFAULT 'MANUAL',

        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

        UNIQUE KEY uq_target_reason (target_id, reason_type, reason_ref_id),
        INDEX idx_target_reason_lookup (reason_type, reason_ref_id),
        INDEX idx_target_reason_target (target_id),

        FOREIGN KEY (target_id) REFERENCES SpotlightTarget(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    CREATE TABLE TargetTourismProfile (
        target_id BIGINT UNSIGNED NOT NULL,
        tourism_profile_id BIGINT UNSIGNED NOT NULL,

        PRIMARY KEY (target_id, tourism_profile_id),

        FOREIGN KEY (target_id) REFERENCES SpotlightTarget(id) ON DELETE CASCADE
        -- Add FK to TourismProfile(id) if/when that table exists in your schema
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
#endregion

#region Spotlights - Rules (Query Builder Only: No Spotlight Generation)
    CREATE TABLE SpotlightRule (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(200) NOT NULL,

        country_id BIGINT UNSIGNED NULL,
        region_id BIGINT UNSIGNED NULL,
        city_id BIGINT UNSIGNED NULL,

        start_month TINYINT UNSIGNED NULL,
        end_month TINYINT UNSIGNED NULL,

        start_date DATE NULL,
        end_date DATE NULL,

        weather_condition_id BIGINT UNSIGNED NULL,

        is_enabled BOOLEAN NOT NULL DEFAULT TRUE,

        base_weight INT NOT NULL DEFAULT 1,
        priority_delta INT NOT NULL DEFAULT 0,
        mapped_spotlight_theme VARCHAR(100) NULL,

        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

        INDEX idx_rule_scope (is_enabled, country_id, region_id, city_id),
        INDEX idx_rule_season (start_month, end_month),
        INDEX idx_rule_dates (start_date, end_date),
        INDEX idx_rule_weather (weather_condition_id),

        CONSTRAINT chk_rule_months_range CHECK (
            (start_month IS NULL OR (start_month BETWEEN 1 AND 12)) AND
            (end_month IS NULL OR (end_month BETWEEN 1 AND 12))
        ),

        CONSTRAINT chk_rule_dates_range CHECK (
            (start_date IS NULL OR end_date IS NULL OR start_date <= end_date)
        ),

        CONSTRAINT chk_rule_time_window_consistency CHECK (
            NOT (start_month IS NULL AND end_month IS NOT NULL) AND
            NOT (start_month IS NOT NULL AND end_month IS NULL)
        )
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    CREATE TABLE SpotlightRuleCondition (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        rule_id BIGINT UNSIGNED NOT NULL,

        condition_type ENUM(
            'TARGET_TYPE_IN',

            'HAS_TAG',
            'HAS_EQUIPMENT_CATEGORY',
            'HAS_ATTRIBUTE',
            'HAS_ATMOSPHERE',
            'HAS_OBJECT',
            'HAS_HOBBY',

            'IS_EVENT_LOCAL_FEAST',
            'IS_EVENT_BIG_RECURRENT',

            -- Used when the rule is attached to EVENT_SERIE target:
            -- include events whose parent_id matches the serie's "anchor event",
            -- or whose event_serie_id matches the serie target.
            'INCLUDE_EVENTS_BY_PARENT_OF_SERIE_TARGET',
            'INCLUDE_EVENTS_BY_SERIE_ID_OF_SERIE_TARGET'
        ) NOT NULL,

        ref_id BIGINT UNSIGNED NULL,
        value_string VARCHAR(200) NULL,

        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (rule_id) REFERENCES SpotlightRule(id) ON DELETE CASCADE,
        INDEX idx_rule_condition (rule_id, condition_type),
        INDEX idx_rule_condition_ref (condition_type, ref_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    CREATE TABLE SpotlightRuleEffect (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        rule_id BIGINT UNSIGNED NOT NULL,

        effect_type ENUM(
            'ADD_REASON',
            'SET_THEME',
            'ADD_PRIORITY',
            'ADD_BASE_WEIGHT'
        ) NOT NULL,

        reason_type ENUM(
            'HOBBY',
            'OBJECT',
            'ATMOSPHERE',
            'OCCASION',
            'EQUIPMENT_CATEGORY',
            'TAG',
            'LITTLE_ACTIVITY_OCCASION',
            'WEATHER'
        ) NULL,

        reason_ref_id BIGINT UNSIGNED NULL,
        weight INT NOT NULL DEFAULT 1,

        mapped_spotlight_theme VARCHAR(100) NULL,
        priority_delta INT NULL,
        base_weight_delta INT NULL,

        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (rule_id) REFERENCES SpotlightRule(id) ON DELETE CASCADE,
        INDEX idx_effect_rule (rule_id, effect_type),
        INDEX idx_effect_reason (reason_type, reason_ref_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
#endregion


CREATE TABLE `EventParticipant` (
  `event_id` bigint NOT NULL,
  `shop_id` bigint DEFAULT NULL,
  `place_id` bigint DEFAULT NULL,
  `partner_id` bigint DEFAULT NULL,
  `page_id` bigint DEFAULT NULL,
  `user_id` bigint DEFAULT NULL,

  is_new boolean default null,
  fist_addin_date  Datetime default CURRENT_TIMESTAMP,

  FOREIGN KEY (`user_id`) REFERENCES `User` (`id`),
  FOREIGN KEY (`event_id`) REFERENCES `LocalEvent` (`id`),
  FOREIGN KEY (`shop_id`) REFERENCES `Shop` (`id`),
  FOREIGN KEY (`place_id`) REFERENCES `Place` (`id`),
  FOREIGN KEY (`partner_id`) REFERENCES `Partner` (`id`),
 FOREIGN KEY (`page_id`) REFERENCES `Page` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `EventOrganizers` (
  `event_id` bigint NOT NULL ,
  `page_id` bigint  default NULL,
  partner_id bigint default null, 
  place_id bigint default null, 
  shop_id bigint default null,

  foreign key (event_id) references LocalEvent(id),
  foreign key (place_id) references Place(id),
  foreign key (partner_id) references Partner(id),
  foreign key (shop_id) references Shop(id),
  foreign key (page_id) references Page(id)
);

CREATE TABLE `ExperienceOrganizers` (
    `experience_id` bigint NOT NULL ,
    `page_id` bigint  default NULL,
    partner_id bigint default null, 
    place_id bigint default null, 
    shop_id bigint default null,

  foreign key (experience_id) references Experience(id),
  foreign key (place_id) references Place(id),
  foreign key (partner_id) references Partner(id),
  foreign key (shop_id) references Shop(id),
  foreign key (page_id) references Page(id)
);


CREATE TABLE `EventProgrammation` (
  `id` bigint unsigned NOT NULL primary key auto_increment,
  `title` varchar(150) NOT NULL,
  event_id bigint default null, 

  programmation_event_category_id smallint unsigned default null,
  programmation_day date default null,

    `page_id` bigint  default NULL,
    line_up_name varchar(50) default null,
    is_event_line_up boolean default null,  -- pour les events qui rentrent dedans, et uniquement pour les pages Artistes, Dj, ....

  `programmation_start_date` date NOT NULL,
  `programmation_start_hour` varchar(5) NOT NULL,
  `programmation_end_date` date NOT NULL,
  `programmation_end_hour` varchar(5) NOT NULL,

  `description` tinytext DEFAULT NULL,
  picture varchar(255) default null,

  `minimal_age` tinyint unsigned DEFAULT NULL,  

  `is_for_children` tinyint DEFAULT 0,
  `adapted_to_children` tinyint DEFAULT 0,
  `adapted_to_groups` tinyint DEFAULT 0,
  `adapted_to_family` tinyint NOT NULL DEFAULT 0,
  `adapted_to_family_with_children` tinyint NOT NULL DEFAULT 0,
  `adapted_for_alone` tinyint NOT NULL DEFAULT 0,
  `adapted_to_couple` tinyint DEFAULT 0,
  `adapted_to_handicap` tinyint NOT NULL DEFAULT 0,
  `adapted_to_strollers` tinyint NOT NULL DEFAULT 0,

  `programmation_booking_needed_for_access` tinyint unsigned DEFAULT NULL,
  `programmation_access_type` tinyint unsigned DEFAULT NULL,

  foreign key (page_id) references Page(id),
  foreign key(programmation_access_type) references AccessType(id),
  foreign key(programmation_booking_needed_for_access) references AccessBookingNeeded(id),
  foreign key (programmation_event_category_id) references EventCategory(id),
  foreign key (event_id) references LocalEvent(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;;

CREATE TABLE `HourlyContent` (
  `id` bigint NOT NULL primary key auto_increment,
  `day_id` int(1) NOT NULL,
  `closing_day` tinyint(1) NOT NULL,
  `opening_hour` varchar(5) DEFAULT NULL,
  `closure_hour` varchar(5) DEFAULT NULL,
  `with_break` tinyint(1) NOT NULL,
  `reopening_hour` varchar(5) DEFAULT NULL,
  `reclosure_hour` varchar(5) DEFAULT NULL, 

  exceptional_hourly_day date default null,

  shop_id bigint default null, 

  place_id bigint default null, -- emplacement

  hourly_id bigint unsigned default null
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `EventHourly` (
  `id` bigint NOT NULL,
  `event_id` bigint DEFAULT NULL,
  `day_id` int(1) DEFAULT NULL,
  `event_date` date DEFAULT NULL,
  `closing_day` tinyint(1) NOT NULL,
  `opening_hour` varchar(5) DEFAULT NULL,
  `closure_hour` varchar(5) DEFAULT NULL,
  `with_break` tinyint(1) NOT NULL,
  `reopening_hour` varchar(5) DEFAULT NULL,
  `reclosure_hour` varchar(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Types d'accès : Shop, Place, Experience, Event 
CREATE TABLE `AccessType` (
  `id` tinyint unsigned NOT NULL primary key auto_increment,
  `name` varchar(50) NOT NULL,
  `string_id` varchar(50) NOT NULL unique,

  can_be_use_as_default boolean default 0, -- Est-ce qu'on peut l'utiliser comme type d'accès principal ?
  can_be_use_as_others boolean default 0, -- Est-ce utilisable en sécondaire. p.ex : Libre & Gratuit en principal, mais gratuit pour les enfants non (Faut d'abord un principal pay, et gratuit pour les autres)
  is_free_access boolean default 0, -- Accès libre 
  is_free_services boolean default 0, -- ??
  is_free_by_situation boolean default 0, -- Ce sont les accès qui sont libres par lma situation de la personne
  is_booking_needed boolean default 0 -- est-ce que c'est un type qui a absolument besoin d'une réservation 

);

INSERT INTO `AccessType` (`name`, `string_id`, is_free_access, is_free_services, is_booking_needed, is_free_by_situation, can_be_use_as_default, can_be_use_as_others) values 
  ('Libre & Gratuit', 'libre-et-gratuit', 1, 1, 0, 0, 1, 0),
  ('Gratuit, sur réservation', 'gratuit-sur-reservation', 1, 1, 1, 0, 1, 0),
  ('Gratuit pour les enfants', 'gratuit-pour-les-enfants', 1, 0, 0, 1, 0, 1),
  ('Gratuit pour les écoliers', 'gratuit-pour-les-ecoliers', 1, 0, 0, 1, 0, 1),
  ('Gratuit pour les sans emplois', 'gratuit-pour-les-sans-emplois', 1, 0, 0, 1, 0, 1),
  ('Gratuit pour les séniors', 'gratuit-pour-les-seniors', 1, 0, 0, 1, 0, 1),

  ('Tarif libre', 'tarif-libre', 0, 0, 1, 0, 1, 0),
  ('Payant', 'acces-payant', 0, 1, 0, 0, 1, 0),
  ('Payant par attraction', 'payant-par-attraction', 1, 0, 0, 0, 1, 0),

  ('Accès sur adhésion', 'accessible-sur-adhesion', 1, 1, 0, 0, 1, 1),
  ('Accès sur abonnement', 'accessible-sur-abonnement', 1, 1, 0, 0, 1, 1),
 
  ('Libre à partir de', 'tarif-libre-a-partir-de', 0, 0, 1, 0, 1, 0),
  ('Gratuit avec conso', 'gratuit-avec-conso', 1, 1, 1, 0, 1, 0),
  -- ('Accès réservé', 'access-reserve', 0, 0, 0, 0, 1, 0),
  -- ('Gratuit selon horaire', 'gratuit-selon-horaire', 1, 1, 1, 0, 1, 0),
  ('Tarif groupe ou famille', 'tarif-groupe-famille', 0, 1, 0, 0, 1, 0)
  ;


-- Si la réservation préalable est obligatoire ou pas 
CREATE TABLE `AccessBookingNeeded` (
  `id` tinyint unsigned NOT NULL primary key auto_increment,
  `name` varchar(50) NOT NULL,
  `string_id` varchar(50) NOT NULL unique
);

INSERT INTO `AccessBookingNeeded` (`name`, `string_id`) values ('Sur réservation', 'uniquement-sur-reservation');
INSERT INTO `AccessBookingNeeded` (`name`, `string_id`) values ('Réservation conseillée', 'reservation-conseillee');
INSERT INTO `AccessBookingNeeded` (`name`, `string_id`) values ('Possible sans réservation', 'sans-reservation-possible');
INSERT INTO `AccessBookingNeeded` (`name`, `string_id`) values ('Uniquement sur place', 'reservation-sur-place-seulement');

-- Contenu, coeur de la configuration 
CREATE TABLE `SessionConfigurationContent` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    `session_conf_id` BIGINT UNSIGNED not NULL,

    configuration_source_type varchar(20) default null, -- EXPERIENCE, MOVIE, CONF, ...
  
    `repetition_type` TINYINT UNSIGNED NOT NULL, -- Heures fixes ou répétition
    `repetition_time_measurement` TINYINT UNSIGNED DEFAULT NULL, -- Si EVERY_X
    `repetition_time` SMALLINT UNSIGNED DEFAULT NULL, -- Valeur numérique (ex: toutes les 15 minutes)

    repetition_time_hour_from TIME default null,
    repetition_time_hour_to TIME default null,

    `hour_list` JSON DEFAULT NULL, -- Liste d'heures fixes si conf_type = FIXED_HOURS
    `day_list` JSON DEFAULT NULL, -- Liste des jours concernés [1,2,3,4,5]

    movie_id bigint unsigned default null,
    place_id bigint  default null,
    experience_id bigint  default null,

    is_active boolean default 1,
    `is_for_all_days` BOOLEAN DEFAULT 0,

    `max_capacity` SMALLINT UNSIGNED DEFAULT NULL, -- Capacité maximale de cette session

    FOREIGN KEY (`session_conf_id`) REFERENCES `SessionConfiguration`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`repetition_type`) REFERENCES `SessionRepetitionType`(`id`),
    FOREIGN KEY (`repetition_time_measurement`) REFERENCES `TimeMeasurementUnity`(`id`),

    FOREIGN KEY (`experience_id`) REFERENCES `Experience`(`id`),
    -- FOREIGN KEY (`movie_id`) REFERENCES `Movie`(`id`),
    FOREIGN KEY (`place_id`) REFERENCES `Place`(`id`),

    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Objet regroupant la configuration des sessions : Pour les cours, les expériences, certains équipements (Salle d'escape, ..)...
CREATE TABLE `SessionConfiguration` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `is_current` BOOLEAN DEFAULT 0, -- Est-elle active actuellement

    `temporary_type` TINYINT UNSIGNED DEFAULT NULL,
    `with_annual_recurrence` BOOLEAN DEFAULT 0,

    `start_date` DATE DEFAULT NULL, -- Si applicable à une période spécifique
    `end_date` DATE DEFAULT NULL,

    `start_month` TINYINT UNSIGNED DEFAULT NULL, -- Si applicable à un intervalle de mois (ex: été)
    `end_month` TINYINT UNSIGNED DEFAULT NULL,

    `description` TINYTEXT DEFAULT NULL,

    `experience_id` BIGINT DEFAULT NULL,

    is_active boolean default 0,    

    FOREIGN KEY (`experience_id`) REFERENCES `Experience`(`id`),
    -- FOREIGN KEY (`movie_id`) REFERENCES `Movie`(`id`),
    FOREIGN KEY (`temporary_type`) REFERENCES `TemporaryHourlyType`(`id`),
    FOREIGN KEY (`start_month`) REFERENCES `Month`(`id`),
    FOREIGN KEY (`end_month`) REFERENCES `Month`(`id`),
  
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

Et session manuelle
-- Session physique crée à la mano ou automatiquement
CREATE TABLE `Session` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    unique_id varchar(32) not NULL unique,

    experience_id bigint default null,
    equipment_id bigint default null, 
    animation_id bigint default null, 

    session_conf_content_id bigint unsigned default null,
    booking_conf_content_id bigint unsigned default null,


    `date` DATE NOT NULL, -- date de la session
    `time_start` TIME NOT NULL, -- heure de début
    `time_end` TIME NOT NULL, -- heure de fin

    `capacity` SMALLINT UNSIGNED DEFAULT NULL, -- capacité maximale de la session
    `booked_count` SMALLINT UNSIGNED DEFAULT 0, -- nombre de réservations déjà effectuées

    `status` TINYINT UNSIGNED DEFAULT 1, -- statut : 1=active, 0=annulée, etc.

    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    shop_category_id smallint default null, 
    place_type_id int default null, 

    FOREIGN KEY (`shop_category_id`) REFERENCES `ShopCategory`(`id`),
    FOREIGN KEY (`place_type_id`) REFERENCES `PlaceType`(`id`),

    FOREIGN KEY (`session_conf_content_id`) REFERENCES `SessionConfigurationContent`(`id`),
    FOREIGN KEY (`booking_conf_content_id`) REFERENCES `BookingConfigurationContent`(`id`),


    FOREIGN KEY (`experience_id`) REFERENCES `Experience`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`animation_id`) REFERENCES `Animation`(`id`),
    FOREIGN KEY (`equipment_id`) REFERENCES `Equipment`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
-- je te rajoute ça dans la conf des Session d'expérience pour leur accessibilité. 


CREATE TABLE `ElementAccessPrice` (
  `id` BIGINT unsigned AUTO_INCREMENT PRIMARY KEY,
  unique_id varchar(32) default NULL unique,
  `element_access_type_id` tinyint unsigned NOT NULL, 
  element_price_model_id tinyint unsigned not null default 9,
  
  `name` VARCHAR(100) NOT NULL, -- Nom du tarif (ex: "Entrée Parc Standard", "Accès VIP")
  `price` DECIMAL(10,2) NOT NULL, -- Prix  
  `currency` smallint unsigned DEFAULT 1, -- Devise

  media_id bigint unsigned default NULL, 

  -- Ici c'est la quantité maximale de ticket ouverts. Uniquement sur Event 
  quantity smallint unsigned default NULL,
  minimum_quantity_to_choose tinyint unsigned default NULL,
  maximum_quantity_per_user tinyint default NULL,

  -- Ici ce sont les Abonnements, les accès spécial izilife pour nos projets. traitements très spécique
  is_pack_access boolean default 0,
  is_izilife_eap boolean default 0, 
  is_izilife_mts_eap boolean default 0,

  is_active boolean default 0, 

  is_with_consumption boolean default 0,
  is_reducted_price boolean default 0,
  is_user_segment_restricted_price boolean default 0,
  
  is_all_event_access_price boolean default 0,

  -- On va garder les champs pour ne pas casser mais ça permet de dire si c'est un PASS ou pas & nombre de jours
  is_event_one_day_accees boolean default 0,
  is_event_more_than_one_day_accees boolean default 0,
  number_of_pass_days tinyint unsigned default NULL,

  need_to_be_confirmed_manually boolean default 0,
  -- need_to_call_for_validate_date boolean 

  `duration_minutes` smallint unsigned DEFAULT NULL, -- Durée si applicable (ex: 30 min)
  duration_period_measurement tinyint unsigned default NULL,

  validation_period_measurement tinyint unsigned default NULL,
  validity_period smallint unsigned DEFAULT NULL, -- Validité (ex: "1 jour", "1 mois")

  `description` TEXT DEFAULT NULL, -- Description optionnelle
  `conditions_description` tinytext DEFAULT NULL, -- Conditions particulières

  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  is_template boolean default 0,
  is_variant_of bigint unsigned default NULL,   

  place_id bigint default NULL, 
  shop_id bigint default NULL,
  event_id bigint default NULL, 
  event_serie_id bigint default NULL, 
  experience_id bigint default NULL,

  animation_id bigint default NULL, 
  equipment_id bigint default NULL,
  programmation_id bigint default NULL,
  partner_id bigint default null,
  annual_celebration_id bigint unsigned default NUll, 
  -- element_session_id bigint default null, 


  foreign key(element_access_type_id) references ElementAccessType(id),
  foreign key(currency) references Currency(id),
  foreign key(validation_period_measurement) references ValidationPeriodMeasurement(id),  
  -- foreign key(element_session_id) references ElementSession(id),
  foreign key(is_variant_of) references ElementAccessPrice(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE ElementAccessGroupedPrice (
    id BIGINT unsigned PRIMARY KEY AUTO_INCREMENT,
    access_price_id BIGINT unsigned NOT NULL,
    group_size tinyint unsigned NOT NULL,
    currency smallint unsigned default null,
    total_price DECIMAL(10,2) NOT NULL,

    foreign key(access_price_id) references ElementAccessPrice(id),
    foreign key(currency) references Currency(id)
);

CREATE TABLE ElementAccessPricePackComposition (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    pack_access_price_id BIGINT unsigned NOT NULL,
    included_access_price_id BIGINT unsigned NOT NULL,
    quantity tinyint NOT NULL, 

    foreign key(pack_access_price_id) references ElementAccessPrice(id),
    foreign key(included_access_price_id) references ElementAccessPrice(id)
);


create table if not exists AppEntityType (
    id smallint not null primary key AUTO_INCREMENT,
    name varchar(50) not null, 
    string_id varchar(50) not null unique
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


INSERT INTO `AppEntityType` (`id`, `string_id`, `name`) VALUES
    (1, 'shop', 'Shop'),
    (2, 'place', 'Place'),
    (3, 'experience', 'Expérience'),
    (4, 'event', 'Evènement'),
    (5, 'circuit', 'Circuit'),
    (6, 'session', 'Session') -- Cinéma - Théâtre - Cours (sport/yoga/salle de sport - cuisine) - Bar (Happy Hour, Ladies Night, Soirée étudiantes) 
    ;


create table if not exists UserTourismProfileType (
    id tinyint not null primary key AUTO_INCREMENT,
    name varchar(50) not null, 
    string_id varchar(50) not null unique, 
    parent_id tinyint default null, 

    icon varchar(20) not null, 
    `position` TINYINT NOT NULL DEFAULT '1',

    foreign key(parent_id) references UserTourismProfileType(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


INSERT INTO `UserTourismProfileType` (`id`, `string_id`, `name`, parent_id, icon, position) VALUES
    (1, 'en-famille', 'En famille', NULL, "fas fa-child", 1),
    (2, 'seul', 'Seul(e)', NULL, "fas fa-user", 2),
    (3, 'en-couple', 'En couple', NULL, "fas fa-user-friends", 4),
    (4, 'entre-amis', 'Entre amis', NULL, "fas fa-users", 5),
    (5, 'etudiant', 'Etudiant', NULL, "fas fa-user-graduate", 3), 
    (6, 'touriste', 'Touriste', NULL, "fas fa-user", 6);

CREATE TABLE IF NOT EXISTS NavigationCategory (
  id SMALLINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  string_id VARCHAR(50) NOT NULL UNIQUE,

  show_text VARCHAR(100) DEFAULT NULL,
  parent_id SMALLINT DEFAULT NULL,

  is_temporary BOOLEAN DEFAULT 0,
  active_from DATETIME NULL,
  active_to   DATETIME NULL,

  active_month_from TINYINT UNSIGNED NULL,  -- 1..12
  active_month_to   TINYINT UNSIGNED NULL,  -- 1..12

  country_id INT DEFAULT NULL,
  area_id BIGINT UNSIGNED DEFAULT NULL,

  not_visible_for_child BOOLEAN DEFAULT 0,
  linked_profile_type_id TINYINT DEFAULT NULL,

  special_management_url VARCHAR(100) DEFAULT NULL UNIQUE,

  icon_file_name VARCHAR(50) DEFAULT NULL,
  is_active BOOLEAN DEFAULT 1,
  is_search_result BOOLEAN DEFAULT 0,
  is_app_section BOOLEAN DEFAULT 0,
  icon VARCHAR(50) DEFAULT NULL,

  FOREIGN KEY (parent_id) REFERENCES NavigationCategory(id),
  FOREIGN KEY (linked_profile_type_id) REFERENCES UserTourismProfileType(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS NavigationCategoryEntities (
  navigation_category_id SMALLINT NOT NULL,
  entity_type_id SMALLINT NOT NULL,
  FOREIGN KEY(navigation_category_id) REFERENCES NavigationCategory(id),
  FOREIGN KEY(entity_type_id) REFERENCES AppEntityType(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


/* ============================================================
   1) CATEGORIES PRINCIPALES
   ============================================================ */

INSERT INTO `NavigationCategory`
(`id`, `string_id`, `name`, `parent_id`, `linked_profile_type_id`, `special_management_url`, `show_text`, `icon_file_name`,
 `is_active`, `is_search_result`, `is_app_section`, `not_visible_for_child`, `is_temporary`, `active_month_from`, `active_month_to`)
VALUES
    (1,  'manger',        'Manger',        NULL, NULL, NULL, NULL, 'restaurant.png', 1, 0, 0, 0, 0, NULL, NULL),
    (2,  'bruncher',      'Bruncher',      NULL, NULL, NULL, NULL, 'brunch.png',     1, 0, 0, 0, 0, NULL, NULL),
    (3,  'gouter',        'Goûter',        NULL, NULL, NULL, NULL, 'gouter.png',     1, 0, 0, 0, 0, NULL, NULL),
    (4,  'boire',         'Boire',         NULL, NULL, NULL, NULL, 'boire.png',      1, 0, 0, 0, 0, NULL, NULL),
    (5,  'cafe-the',      'Café, Thé',     NULL, NULL, NULL, 'Cafés, Thés, Bubble-teas & autres boissons', 'cafe.png', 1, 0, 0, 0, 0, NULL, NULL),
    (6,  'balades',       'Balades',       NULL, NULL, NULL, 'Balades & Circuits crées par la communauté.', 'balades.png', 1, 0, 0, 0, 0, NULL, NULL),
    (7,  'sortir',        'Sortir',        NULL, NULL, NULL, NULL, 'bowling.png',    1, 0, 0, 0, 0, NULL, NULL),
    (8,  'jouer',         'Jouer',         NULL, NULL, NULL, NULL, 'jeux-et-loisirs.png', 1, 0, 0, 0, 0, NULL, NULL),
    (9,  's-evader',      "S'évader",     NULL, NULL, NULL, NULL, 's-evader.png',   0, 0, 0, 0, 0, NULL, NULL),

    (10, 'travailler',    'Travailler',    NULL, NULL, 'travailler', NULL, 'travailler.png', 0, 0, 0, 0, 0, NULL, NULL),
    (11, 'sport',         'Sport',         NULL, NULL, 'sport',      NULL, 'fitness.png',    0, 0, 0, 0, 0, NULL, NULL),
    (12, 'danser',        'Danser',        NULL, NULL, 'danse',      NULL, 'danser.png',     0, 0, 0, 0, 0, NULL, NULL),

    (13, 'se-detendre',   'Se détendre',   NULL, NULL, NULL, 'Se détendre', 'se-detendre.png', 1, 0, 0, 0, 0, NULL, NULL),
    (14, 'prendre-soin-de-soi', 'Soins & Beauté', NULL, NULL, NULL, NULL, 'prendre-soin-de-soi.png', 1, 0, 0, 0, 0, NULL, NULL),
    (15, 'dormir',        'Dormir',        NULL, NULL, NULL, NULL, 'hebergement.png', 1, 0, 0, 0, 0, NULL, NULL),
    (16, 'experiences',   'Expériences',   NULL, NULL, NULL, NULL, 'experiences.png', 1, 0, 0, 0, 0, NULL, NULL),
    (17, 'evenements',    'Événements',    NULL, NULL, NULL, NULL, 'evenements.png',  1, 0, 0, 0, 0, NULL, NULL),
    (18, 'marches',       'Marchés',       NULL, NULL, NULL, NULL, 'marche.png',      1, 0, 0, 0, 0, NULL, NULL),

    (19, 'spotlights',    'Spotlights',    NULL, NULL, 'spotlights', NULL, 'spotlights.png', 1, 0, 0, 0, 0, NULL, NULL),
    (20, 'nouveaux-lieux', 'Nouveaux',     NULL, NULL, 'nouveaux-lieux', NULL, 'nouveaux.png', 1, 0, 0, 0, 0, NULL, NULL),

    (21, 'sorties',       'Sorties',       NULL, NULL, 'sorties', NULL, 'sorties.png', 1, 0, 1, 0, 0, NULL, NULL),

    /* ✅ Art remplace Circuits (id 22) */
    (22, 'art',           'Art',           NULL, NULL, 'art', NULL, 'art.png', 1, 0, 0, 0, 0, NULL, NULL),

    (23, 'escapades',     'Escapades',     NULL, NULL, 'escapades', NULL, 'escapades.png', 1, 0, 0, 0, 0, NULL, NULL),
    (24, 'deals',         'Deals',         NULL, NULL, 'deals', NULL, 'deals.png', 1, 0, 0, 0, 0, NULL, NULL),
    (25, 'courses',       'Courses',       NULL, NULL, 'courses', NULL, 'courses.png', 0, 0, 0, 0, 0, NULL, NULL),
    (26, 'wallet',        'Portefeuille',  NULL, NULL, 'wallet', NULL, 'wallet.png', 0, 0, 0, 0, 0, NULL, NULL),

    (27, 'payer',         'Payer',         NULL, NULL, 'payer', NULL, 'payer.png', 0, 0, 1, 0, 0, NULL, NULL),
    (28, 'transfert',     'Transfert',     NULL, NULL, 'transfert', NULL, 'transfert.png', 0, 0, 1, 0, 0, NULL, NULL),
    (29, 'jeux',          'Jeux',          NULL, NULL, 'jeux', NULL, 'jeux.png', 0, 0, 1, 0, 0, NULL, NULL),
    (30, 'agenda',        'Agenda',        NULL, NULL, 'agenda', NULL, 'agenda.png', 0, 0, 1, 0, 0, NULL, NULL),
    (31, 'rencontres',    'Social',        NULL, NULL, 'rencontre', 'Rencontrer du monde, activités à plusieurs', 'rencontres.png', 0, 0, 1, 0, 0, NULL, NULL),
    (32, 'sorties-premier-rendez-vous', 'Idées date', NULL, NULL, 'sorties-premier-rendez-vous', 'Idées de sorties pour un rendez-vous', 'couple.png', 1, 0, 0, 0, 0, NULL, NULL),
    (33, 'activites-enfants', 'Pour enfants', NULL, NULL, 'activites-enfants', "Idées d'activités pour les enfants", 'espace-enfants.png', 1, 0, 0, 0, 0, NULL, NULL),
    (34, 'jobs',          'Jobs', NULL, NULL, 'job', NULL, 'job-etudiant.png', 0, 0, 0, 0, 0, NULL, NULL),
    (35, 'au-quotidien',  'Au quotidien',  NULL, NULL, NULL, NULL, 'services-locaux.png', 0, 0, 0, 0, 0, NULL, NULL),
    (36, 'equipements',   'Équipements',   NULL, NULL, NULL, NULL, 'equipements.png', 0, 0, 0, 0, 0, NULL, NULL),
    (37, 'shopping',      'Shopping',      NULL, NULL, NULL, NULL, 'shopping.png', 1, 0, 0, 0, 0, NULL, NULL),
    (38, 'chiner',        'Chiner',        NULL, NULL, NULL, NULL, 'chiner.png', 1, 0, 0, 0, 0, NULL, NULL),
    (39, 'flaner',        'Flâner',        NULL, NULL, NULL, NULL, 'flaner.png', 1, 0, 0, 0, 0, NULL, NULL),
    (40, 'aider',         'Aider',         NULL, NULL, NULL, NULL, 'solidaire.png', 1, 0, 0, 0, 0, NULL, NULL),
    (41, 'comedie',     'Comédie',         NULL, NULL, NULL, 'One man show, Comédy Clubs, ...', 'comedy.png', 1, 0, 0, 0, 0, NULL, NULL),
    (42, 'rooftops',      'Rooftops',      NULL, NULL, NULL, NULL, 'rooftop.png', 1, 0, 0, 0, 0, NULL, NULL),
    (43, 'guinguettes',   'Guinguettes',   NULL, NULL, NULL, NULL, 'guinguette.png', 1, 0, 0, 0, 0, NULL, NULL),
    (44, 'live-sessions', 'Sessions', NULL, NULL, 'live-sessions', 'Jams, petits concerts, scènes locales', 'live.png', 1, 0, 0, 0, 0, NULL, NULL),
    (45, 'terrasses',     'Terrasses',     NULL, NULL, 'terrasses', 'Terrasses, guinguettes, rooftops…', 'terrasse.png', 1, 0, 0, 0, 1, 4, 9),
    (46, 'etudiants',     'Étudiants',     NULL, 5, 'etudiants', 'Soirées, offres étudiantes, lieux adaptés, events campus', 'etudiants.png', 1, 0, 0, 0, 0, NULL, NULL)
    
;


/* ============================================================
   2) SOUS-CATEGORIES (parent_id en dur)
   ============================================================ */

INSERT INTO `NavigationCategory`
(`id`, `string_id`, `name`, `parent_id`, `linked_profile_type_id`, `special_management_url`, `show_text`, `icon_file_name`,
 `is_active`, `is_search_result`, `is_app_section`, `not_visible_for_child`, `is_temporary`, `active_month_from`, `active_month_to`)
VALUES
    /* MANGER (parent=1) */
    (47, 'petit-dejeuner',      'Petit-Déjeuner',      1, NULL, NULL, NULL, 'petit-dejeuner.png', 1, 0, 0, 0, 0, NULL, NULL),
    (48, 'restaurants',         'Restaurants',         1, NULL, NULL, NULL, 'dejeuner.png',       1, 0, 0, 0, 0, NULL, NULL),
    (49, 'street-fast-foods',   'Street & Fast Food',  1, NULL, NULL, NULL, 'street-food.png',    1, 0, 0, 0, 0, NULL, NULL),
    (50, 'gastronomie',         'Gastronomie',         1, NULL, NULL, 'Restaurants gastronomiques', 'diner-table.png', 1, 0, 0, 0, 0, NULL, NULL),
    (51, 'food-trucks',         'Food-trucks',         1, NULL, NULL, NULL, 'food-truck.png',     1, 0, 0, 0, 0, NULL, NULL),

    /* BOIRE (parent=4) */
    (52, 'en-terrasse',         'En terrasse',         4, NULL, NULL, 'Boire un verre en terrasse', 'terrasse.png', 1, 0, 0, 0, 1, NULL, NULL),
    (53, 'aperos',              'Apéro',               4, NULL, NULL, NULL, 'aperitif.png',        1, 0, 0, 0, 0, NULL, NULL),
    (54, 'boire-et-jouer',      'Boire & Jouer',       4, NULL, NULL, 'Bars pour boire & jouer', 'flechettes.png', 1, 0, 0, 0, 1, NULL, NULL),

    /* BALADES (parent=6) */
    (55, 'balades-en-ville',        'En ville',        6, NULL, NULL, 'Balades en ville',         'ville.png', 1, 0, 0, 0, 0, NULL, NULL),
    (56, 'balades-culturelles',     'Culturelles',     6, NULL, NULL, 'Balades culturelles',      'monument.png', 1, 0, 0, 0, 0, NULL, NULL),
    (57, 'balades-nature',          'Nature',          6, NULL, NULL, 'Balades nature',           'nature.png', 1, 0, 0, 0, 0, NULL, NULL),
    (58, 'balades-au-bord-de-l-eau',"Au bord de l'eau",6, NULL, NULL, "Balades au bord de leau",'au-bord-de-leau.png', 1, 0, 0, 0, 0, NULL, NULL),

    /* SORTIR (parent=7) */
    (59, 'sorties-culturelles-et-artistiques', 'Art & Culture', 7, NULL, NULL, 'Sorties culturelles & Artistiques', 'art-et-culture.png', 1, 0, 0, 0, 0, NULL, NULL),
    (60, 'sorties-autour-de-la-cuisine',       'Cuisine',       7, NULL, NULL, 'Autour de la cuisine',             'activites-cuisine.png', 1, 0, 0, 0, 0, NULL, NULL),
    (61, 'sorties-autour-des-boissons',        'Boissons',      7, NULL, NULL, 'Autour des boissons',             'activites-cuisine.png', 1, 0, 0, 0, 0, NULL, NULL),
    (62, 'cinema',                             'Cinéma',        7, NULL, NULL, 'Sorties Cinéma',                  'cinema.png', 1, 0, 0, 0, 0, NULL, NULL),
    (63, 'casinos-et-club-de-jeux',            'Casinos',       7, NULL, NULL, 'Casinos & Clubs de jeux',         'casino.png', 1, 0, 0, 0, 0, NULL, NULL),
    (64, 'spectacles',                         'Spectacles',    7, NULL, NULL, 'Spectacles',                      'spectacles.png', 1, 0, 0, 0, 0, NULL, NULL),
    (65, 'concerts',                           'Concerts',      7, NULL, NULL, 'Concerts',                        'concert.png', 1, 0, 0, 0, 0, NULL, NULL),
    (66, 'festivals',                          'Festivals',     7, NULL, NULL, 'Festivals',                       'concert.png', 1, 0, 0, 0, 0, NULL, NULL),
    (67, 'theatres',                           'Théâtre',       7, NULL, NULL, 'Théâtres',                        'theatres.png', 1, 0, 0, 0, 0, NULL, NULL),

    /* EXPERIENCES (parent=16) */
    (68, 'experiences-artistiques',    'Artistiques', 16, NULL, NULL, 'Activités artistiques', 'art.png', 1, 0, 0, 0, 0, NULL, NULL),
    (69, 'experiences-culturelles',    'Culturelles', 16, NULL, NULL, 'Activités culturelles', 'monument.png', 1, 0, 0, 0, 0, NULL, NULL),
    (70, 'experiences-urbaines',       'Urbaines',    16, NULL, NULL, 'Activités urbaines',    'ville.png', 1, 0, 0, 0, 0, NULL, NULL),
    (71, 'experiences-en-nature',      'Nature',      16, NULL, NULL, 'Activités en nature',   'nature.png', 1, 0, 0, 0, 0, NULL, NULL),
    (72, 'experiences-aquatiques',     'Aquatiques',  16, NULL, NULL, 'Activités aquatiques',  'experience-aquatique.png', 1, 0, 0, 0, 0, NULL, NULL),
    (73, 'experiences-aeriennes',      'Aériennes',   16, NULL, NULL, 'Activités aériennes',   'experiences.png', 1, 0, 0, 0, 0, NULL, NULL),
    (74, 'experiences-sportives',      'Sportives',   16, NULL, NULL, 'Activités sportives',   'escalade.png', 1, 0, 0, 0, 0, NULL, NULL),
    (75, 'experiences-avec-neige',     'Neige',       16, NULL, NULL, 'Activités sur neige',   'activites-neige.png', 1, 0, 0, 0, 0, NULL, NULL),
    (76, 'experiences-de-pilotage',    'Pilotage',    16, NULL, NULL, 'Activités de pilotage', 'pilotage.png', 1, 0, 0, 0, 0, NULL, NULL),

    /* EVENEMENTS (parent=17) */
    (77, 'evenements-festifs',    'Festifs',    17, NULL, NULL, 'Événements festifs', 'concert.png', 1, 0, 0, 0, 0, NULL, NULL),
    (78, 'evenements-culturels',  'Culturels',  17, NULL, NULL, 'Événements culturels', 'monument.png', 1, 0, 0, 0, 0, NULL, NULL),
    (79, 'soirees-etudiantes',    'Étudiants',  17, 5, 'soirees-etudiantes', NULL, 'danser.png', 1, 0, 0, 1, 0, NULL, NULL),
    (80, 'evenements-cinema',     'Cinéma',     17, NULL, NULL, 'Événements liés au cinéma', 'cinema.png', 1, 0, 0, 0, 0, NULL, NULL),
    (81, 'evenements-theatre-et-humour', 'Théâtre & Humour', 17, NULL, NULL, 'Théâtre & Humour', 'theatres.png', 1, 0, 0, 0, 0, NULL, NULL),
    (82, 'evenements-spectacles', 'Spectacles', 17, NULL, NULL, 'Spectacles', 'spectacles.png', 1, 0, 0, 0, 0, NULL, NULL),
    (83, 'evenements-mode',       'Mode',       17, NULL, NULL, 'Mode', 'mode.png', 1, 0, 0, 0, 0, NULL, NULL),
    (84, 'evenements-sportifs',   'Sportifs',   17, NULL, NULL, 'Événements sportifs', 'evenement-sportif.png', 1, 0, 0, 0, 0, NULL, NULL),
    (85, 'evenements-alimentaires','Alimentaires',17, NULL, NULL, 'Événements alimentaires', 'evenement-alimentaire.png', 1, 0, 0, 0, 0, NULL, NULL),
    (86, 'evenements-de-rencontres','Rencontres', 17, NULL, NULL, 'Événements pour rencontrer du monde', 'rencontres.png', 1, 0, 0, 0, 0, NULL, NULL),
    (87, 'evenements-marches-braderies-brocantes', 'Braderies & Brocantes', 17, NULL, NULL, 'Marchés, Braderies & Brocantes', 'marche.png', 1, 0, 0, 0, 0, NULL, NULL),
    (88, 'autres-evenements',     'Autres',     17, NULL, NULL, 'Autres', 'trois-points.png', 1, 0, 0, 0, 0, NULL, NULL),

    /* BIEN-ÊTRE (parent=14) */
    (89, 'hygiene-et-beaute',     'Hygiène & Beauté', 14, NULL, NULL, NULL, 'hygiene-et-beaute.png', 1, 0, 0, 0, 0, NULL, NULL),
    (90, 'spas-hammams-et-saunas','Spas',             14, NULL, NULL, 'Spas, hammams & Saunas', 'bien-etre.png', 1, 0, 0, 0, 0, NULL, NULL),
    (91, 'massages',             'Massages',          14, NULL, NULL, NULL, 'massage.png', 1, 0, 0, 0, 0, NULL, NULL),
    (92, 'meditation',           'Méditation',        14, NULL, NULL, NULL, 'meditation.png', 1, 0, 0, 0, 0, NULL, NULL),

    /* DORMIR (parent=15) */
    (93, 'hotels',           'Hôtels',          15, NULL, NULL, NULL, 'hotel.png', 1, 0, 0, 0, 0, NULL, NULL),
    (94, 'chambre-dhotes',   "Chambres d'hôtes",15, NULL, NULL, NULL, 'chambre-hote.png', 1, 0, 0, 0, 0, NULL, NULL),
    (95, 'gites',            'Gîtes',           15, NULL, NULL, NULL, 'gites.png', 1, 0, 0, 0, 0, NULL, NULL),
    (96, 'campings',         'Campings',        15, NULL, NULL, NULL, 'camping.png', 1, 0, 0, 0, 0, NULL, NULL),
    (97, 'logements-insolites','Insolites',     15, NULL, NULL, 'Cabanes, bulles, dômes et autres hébergements atypiques', 'insolite.png', 0, 0, 0, 0, 0, NULL, NULL),

    /* AU QUOTIDIEN (parent=35) */
    (98,  'toilettes',              'Toilettes',              35, NULL, NULL, NULL, 'toilettes-publiques.png', 1, 1, 0, 0, 0, NULL, NULL),
    (99,  'se-garer',               'Se garer',               35, NULL, 'park', NULL, 'se-garer.png', 0, 0, 1, 0, 0, NULL, NULL),
    (100, 'station-services',       'Station service',        35, NULL, NULL, NULL, 'station-service.png', 1, 1, 0, 0, 0, NULL, NULL),
    (101, 'distributeurs-de-billets','Distributeurs de billets',35, NULL, NULL, NULL, 'distributeur-de-billet.png', 1, 1, 0, 0, 0, NULL, NULL),
    (102, 'transports',             'Transports',             35, NULL, 'transport', NULL, 'metro.png', 0, 0, 1, 0, 0, NULL, NULL),

    /* ✅ DANSER (parent=12) — version “niche / écoles / communautés” */
    (103, 'danse-communautes', 'Communautés & groupes', 12, NULL, NULL, 'Groupes, assos, pratiques libres, crews', 'danser.png', 1, 0, 0, 0, 0, NULL, NULL),
    (104, 'danse-ecoles-clubs', 'Écoles & clubs',        12, NULL, NULL, 'Écoles, studios, associations, cours',  'cours-danse.png', 1, 0, 0, 0, 0, NULL, NULL),
    (156, 'danse-evenements-niches', 'Événements niche',  12, NULL, NULL, 'Battles, stages, jams danse (pas boîte)', 'danser.png', 0, 0, 0, 0, 0, NULL, NULL),

    /* ✅ SPORT (parent=11) — version “communautés / clubs / niche” */
    (105, 'sport-communautes', 'Communautés & groupes', 11, NULL, NULL, 'Groupes running, vélo, rando, sorties clubs', 'fitness.png', 1, 0, 0, 0, 0, NULL, NULL),
    (106, 'sport-clubs-dojos',  'Clubs, dojos, salles',  11, NULL, NULL, 'Clubs, dojos, associations, infrastructures', 'fitness.png', 1, 0, 0, 0, 0, NULL, NULL),
    (107, 'sport-evenements-niches', 'Événements niche', 11, NULL, NULL, 'Compets locales, tournois, challenges (pas “sorties”)', 'fitness.png', 0, 0, 0, 0, 0, NULL, NULL),
    (108, 'sport-entrainements', 'Entraînements',        11, NULL, NULL, 'Sessions, créneaux, rendez-vous réguliers', 'fitness.png', 0, 0, 0, 0, 0, NULL, NULL),
    (109, 'sport-disciplines',   'Disciplines',          11, NULL, NULL, 'Liste de sports (macro tags / filtres)', 'fitness.png', 0, 0, 0, 0, 0, NULL, NULL),
    (110, 'sport-equipements',   'Équipements',          11, NULL, NULL, 'Terrains, stades, spots, locations', 'fitness.png', 0, 0, 0, 0, 0, NULL, NULL),

    /* FLÂNER (parent=39) */
    (111, 'espaces-verts', 'Espaces verts', 39, NULL, NULL, 'Parcs, Jardis & autres espaces verts pour se détendre ou marcher', 'parc.png', 1, 0, 0, 0, 0, NULL, NULL),
    (112, 'places-et-lieux-vivants', 'Places & Lieux vivants', 39, NULL, NULL, 'Places publiques, ruelles piétonnes & quartiers animés', 'place.png', 1, 0, 0, 0, 0, NULL, NULL),
    (113, 'flaner-au-bord-de-leau', 'Bords de l’eau', 39, NULL, NULL, 'Quais, berges, canaux, lacs', 'au-bord-de-leau.png', 1, 0, 0, 0, 0, NULL, NULL),
    (114, 'marches-et-brocantes', 'Marchés & Brocantes', 39, NULL, NULL, 'Pour flâner et chiner', 'marche.png', 1, 0, 0, 0, 0, NULL, NULL),
    (115, 'cours-cachees-et-squares', 'Cours cachées & squares', 39, NULL, NULL, 'Espaces discrets pour se promener', 'square.png', 1, 0, 0, 0, 0, NULL, NULL),
    (116, 'terrasses-tranquilles', 'Terrasses tranquilles', 39, NULL, NULL, 'Pour observer, lire, ou profiter du temps', 'terrasse-livre.png', 1, 0, 0, 0, 0, NULL, NULL),
    (117, 'centres-et-zones-commerciaux', 'Centres & Zones commerciaux agréables', 39, NULL, NULL, 'Espaces ouverts à ciel ouvert ou végétalisés', 'centre-commercial.png', 1, 0, 0, 0, 0, NULL, NULL),
    (118, 'flaner-en-villes', 'Flaner en ville', 39, NULL, NULL, 'Flâner dans la ville', 'ville.png', 1, 0, 0, 0, 0, NULL, NULL),

    /* JOUER (parent=8) */
    (119, 'bars-a-jeux-et-cafes-ludiques', 'Bars à jeux & Cafés ludiques', 8, NULL, NULL, 'Cafés jeux, bars à jeux, soirées jeux de société', 'bar-jeux.png', 1, 0, 0, 0, 0, NULL, NULL),
    (120, 'flechettes-billard-babyfoot', 'Fléchettes, billard, baby-foot', 8, NULL, NULL, 'Jeux classiques en bars & loisirs', 'billard.png', 1, 0, 0, 0, 0, NULL, NULL),
    (121, 'laser-game-paintball', 'Laser Game & Paintball', 8, NULL, NULL, 'Jeux d’action par équipes', 'laser-paintball.png', 1, 0, 0, 0, 0, NULL, NULL),
    (122, 'bowlings', 'Bowling', 8, NULL, NULL, 'Bowling', 'sortir.png', 1, 0, 0, 0, 0, NULL, NULL),
    (123, 'arcade-et-vr', 'Arcade & Réalité virtuelle', 8, NULL, NULL, 'Bornes rétro, salles VR, simulateurs', 'arcade-vr.png', 1, 0, 0, 0, 0, NULL, NULL),
    (124, 'escape-games', 'Escape games', 8, NULL, NULL, 'Jeux d’évasion en équipe', 'escape-game.png', 1, 0, 0, 0, 0, NULL, NULL),
    (125, 'aires-de-jeux', 'Aires de jeux & ludothèques', 8, NULL, NULL, 'Espaces ludiques pour enfants & familles', 'aire-jeux.png', 1, 0, 0, 0, 0, NULL, NULL),
    (126, 'karting-simulateurs', 'Karting & simulateurs', 8, NULL, NULL, 'Courses indoor, simulateurs de conduite', 'karting.png', 1, 0, 0, 0, 0, NULL, NULL),
    (127, 'parcs-dattractions', 'Parcs d’attractions', 8, NULL, NULL, 'Petits ou grands parcs de loisirs', 'parc-attraction.png', 1, 0, 0, 0, 0, NULL, NULL),
    (128, 'skateparks-et-trampolines', 'Skateparks & Trampolines', 8, NULL, NULL, 'Rollers, trampolines, parcours ludiques', 'skate-trampo.png', 1, 0, 0, 0, 0, NULL, NULL),

    /* S'ÉVADER (parent=9) */
    (129, 'escapades-weekend', 'Escapades week-end', 9, NULL, NULL, 'Idées pour partir 1 à 3 jours', 'weekend.png', 1, 0, 0, 0, 0, NULL, NULL),
    (130, 'micro-aventures', 'Micro-aventures', 9, NULL, NULL, 'Aventures proches, courtes & dépaysantes', 'micro-aventure.png', 1, 0, 0, 0, 0, NULL, NULL),
    (131, 'lieux-insolites', 'Lieux insolites', 9, NULL, NULL, 'Endroits atypiques, secrets ou surprenants', 'insolite.png', 1, 0, 0, 0, 0, NULL, NULL),
    (132, 'en-pleine-nature', 'En pleine nature', 9, NULL, NULL, 'Se ressourcer loin de la ville', 'nature-retraite.png', 1, 0, 0, 0, 0, NULL, NULL),
    (133, 'sejour-bien-etre', 'Séjours bien-être', 9, NULL, NULL, 'Spa, yoga, ressourcement', 'bien-etre.png', 1, 0, 0, 0, 0, NULL, NULL),
    (134, 'roadtrips-et-circuits', 'Roadtrips & circuits', 9, NULL, NULL, 'Itinéraires d’exploration en voiture ou vélo', 'roadtrip.png', 1, 0, 0, 0, 0, NULL, NULL),
    (135, 'retraites-et-silence', 'Retraites & silence', 9, NULL, NULL, 'Déconnexion totale, retraites spirituelles ou detox digitales', 'retraite.png', 1, 0, 0, 0, 0, NULL, NULL),

    /* CHINER (parent=38) */
    (136, 'brocantes-et-vide-greniers', 'Brocantes & vide-greniers', 38, NULL, NULL, 'Trouver des objets anciens et bonnes affaires', 'brocante.png', 1, 0, 0, 0, 0, NULL, NULL),
    (137, 'marches-aux-puces', 'Marchés aux puces', 38, NULL, NULL, 'Objets rétro, antiquités, vêtements vintage', 'puces.png', 0, 0, 0, 0, 0, NULL, NULL),
    (138, 'friperies-et-vintage', 'Friperies & vintage', 38, NULL, NULL, 'Mode d’occasion, vêtements uniques', 'friperie.png', 1, 0, 0, 0, 0, NULL, NULL),
    (139, 'ressourceries', 'Ressourceries', 38, NULL, NULL, 'Objets de seconde main remis en état à bas prix', 'ressourcerie.png', 1, 0, 0, 0, 0, NULL, NULL),
    (140, 'artisanat-local', 'Artisanat local', 38, NULL, NULL, 'Créateurs, objets faits main & produits uniques', 'artisanat.png', 0, 0, 0, 0, 0, NULL, NULL),
    (141, 'salons-et-foires', 'Salons & foires', 38, NULL, NULL, 'Événements autour de l’objet ou de la déco', 'salon.png', 0, 0, 0, 0, 0, NULL, NULL),

    /* SHOPPING (parent=37) */
    (142, 'shopping-mode-accessoires', 'Mode & Accessoires', 37, NULL, NULL, 'Vêtements, chaussures, sacs, bijouterie...', 'shopping-mode.png', 1, 0, 0, 0, 0, NULL, NULL),
    (143, 'shopping-beaute', 'Beauté', 37, NULL, NULL, 'Cosmétiques, parfumeries, soins...', 'shopping-beaute.png', 1, 0, 0, 0, 0, NULL, NULL),
    (144, 'shopping-maison-deco', 'Maison & Déco', 37, NULL, NULL, 'Objets de décoration, petits meubles, bougies...', 'shopping-maison.png', 1, 0, 0, 0, 0, NULL, NULL),
    (145, 'shopping-librairies', 'Librairies', 37, NULL, NULL, 'Librairies indépendantes, BD, papeterie...', 'shopping-librairie.png', 1, 0, 0, 0, 0, NULL, NULL),
    (146, 'shopping-cadeaux', 'Cadeaux & Idées originales', 37, NULL, NULL, 'Concept stores, gadgets, jeux, objets personnalisés...', 'shopping-cadeaux.png', 1, 0, 0, 0, 0, NULL, NULL),

    /* LIVE & SESSIONS (parent=44) */
    (147, 'live-sessions-jams', 'Jams', 44, NULL, NULL, 'Sessions ouvertes, bœufs, impro', 'jam.png', 0, 0, 0, 0, 0, NULL, NULL),
    (148, 'live-sessions-petits-concerts', 'Petits concerts', 44, NULL, NULL, 'Bars, petites salles, concerts roots', 'concert.png', 0, 0, 0, 0, 0, NULL, NULL),
    (149, 'live-sessions-scenes-locales', 'Scènes locales', 44, NULL, NULL, 'Artistes locaux + agendas', 'scene-locale.png', 0, 0, 0, 0, 0, NULL, NULL),
    (150, 'live-sessions-collectifs', 'Collectifs', 44, NULL, NULL, 'Collectifs / assos musique live', 'collectif.png', 0, 0, 0, 0, 0, NULL, NULL),
    (151, 'live-sessions-ecoles', 'Écoles (caché)', 44, NULL, NULL, 'Cours, assos, apprentissage', 'ecole.png', 0, 0, 0, 1, 0, NULL, NULL),

    /* ÉTUDIANTS (parent=46) */
    (152, 'etudiants-soirees', 'Soirées', 46, 5, NULL, 'Soirées & sorties étudiantes', 'soiree.png', 0, 0, 0, 0, 0, NULL, NULL),
    (153, 'etudiants-offres', 'Offres étudiantes', 46, 5, NULL, 'Avantages / réductions / offres', 'offre-etudiant.png', 0, 0, 0, 0, 0, NULL, NULL),
    (154, 'etudiants-lieux', 'Lieux adaptés', 46, 5, NULL, 'Bars, cafés, spots pour étudiants', 'lieu.png', 0, 0, 0, 0, 0, NULL, NULL),
    (155, 'etudiants-campus', 'Events campus', 46, 5, NULL, 'BDE, assos, événements campus', 'campus.png', 0, 0, 0, 0, 0, NULL, NULL),

    /* ✅ ART (parent=22) — “à la place des sous-cats Circuits” */
    (157, 'art-musees-galeries', 'Musées & Galeries', 22, NULL, NULL, 'Musées, galeries, centres d’art', 'art-et-culture.png', 1, 0, 0, 0, 0, NULL, NULL),
    (158, 'art-street-art',      'Street-art',        22, NULL, NULL, 'Fresques, spots, parcours street-art', 'art.png', 1, 0, 0, 0, 0, NULL, NULL),
    (159, 'art-ateliers',        'Ateliers',          22, NULL, NULL, 'Ateliers créatifs, workshops, makers', 'activites-cuisine.png', 0, 0, 0, 0, 0, NULL, NULL),
    (160, 'art-artisans',        'Artisans & créateurs', 22, NULL, NULL, 'Créateurs locaux, studios, ateliers', 'artisanat.png', 0, 0, 0, 0, 0, NULL, NULL), 

    /* SE DÉTENDRE (parent = 13) - Intention = calme / pause / ralentir */

    (161, 'se-detendre-spas-detente', 'Spas détente', 13, NULL, NULL, 'Spas axés relaxation & détente', 'bien-etre.png', 1, 0, 0, 0, 0, NULL, NULL),
    (162, 'se-detendre-hammams-saunas', 'Hammams & saunas', 13, NULL, NULL, 'Hammams, saunas, bains chauds', 'bien-etre.png', 1, 0, 0, 0, 0, NULL, NULL),
    (163, 'se-detendre-massages-relax', 'Massages relax', 13, NULL, NULL, 'Massages orientés relaxation', 'massage.png', 1, 0, 0, 0, 0, NULL, NULL),
    (164, 'se-detendre-yoga-doux', 'Yoga & slow', 13, NULL, NULL, 'Yoga doux, respiration, pratiques lentes', 'meditation.png', 1, 0, 0, 0, 0, NULL, NULL),
    (165, 'se-detendre-lieux-calmes', 'Lieux calmes', 13, NULL, NULL, 'Jardins, lieux silencieux, lecture', 'parc.png', 1, 0, 0, 0, 0, NULL, NULL),
    (166, 'se-detendre-journee-detox', 'Journée déconnexion', 13, NULL, NULL, 'Retraites & journées déconnexion', 'retraite.png', 0, 0, 0, 0, 0, NULL, NULL),


    /* BIEN-ÊTRE / PRENDRE SOIN DE SOI (parent = 14) - Logique annuaire / business  */

    (167, 'coiffure', 'Coiffure', 14, NULL, NULL, 'Salons de coiffure & prestations', 'hygiene-et-beaute.png', 1, 0, 0, 0, 0, NULL, NULL),
    (168, 'barbers', 'Barbers', 14, NULL, NULL, 'Barbiers & soins barbe', 'hygiene-et-beaute.png', 1, 0, 0, 0, 0, NULL, NULL),
    (169, 'onglerie', 'Onglerie', 14, NULL, NULL, 'Manucure, pédicure, nail art', 'hygiene-et-beaute.png', 1, 0, 0, 0, 0, NULL, NULL),
    (170, 'instituts-esthetique', 'Instituts', 14, NULL, NULL, 'Instituts de beauté & soins esthétiques', 'hygiene-et-beaute.png', 1, 0, 0, 0, 0, NULL, NULL),
    (171, 'soins-visage', 'Soins visage', 14, NULL, NULL, 'Soins visage & traitements', 'hygiene-et-beaute.png', 1, 0, 0, 0, 0, NULL, NULL),
    (172, 'soins-corps', 'Soins corps', 14, NULL, NULL, 'Soins corps & modelages', 'hygiene-et-beaute.png', 1, 0, 0, 0, 0, NULL, NULL),
    (173, 'epilation', 'Épilation', 14, NULL, NULL, 'Épilation cire, laser, définitive', 'hygiene-et-beaute.png', 1, 0, 0, 0, 0, NULL, NULL),
    (174, 'maquillage', 'Maquillage', 14, NULL, NULL, 'Maquillage événement & prestations', 'hygiene-et-beaute.png', 0, 0, 0, 0, 0, NULL, NULL),
    (175, 'medecines-douces', 'Médecines douces', 14, NULL, NULL, 'Naturopathie, réflexologie, sophrologie…', 'bien-etre.png', 0, 0, 0, 0, 0, NULL, NULL)
;


create table if not exists ProfileNavigationCategories (
    navigation_category_id smallint not null, 
    profile_id tinyint not null, 
    position tinyint not null, 

    foreign key(navigation_category_id) references NavigationCategory(id),
    foreign key(profile_id) references UserTourismProfileType(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci; 


INSERT IGNORE INTO `ProfileNavigationCategories` (`profile_id`, `navigation_category_id`, `position`) VALUES
    (1, (SELECT id FROM NavigationCategory WHERE string_id='activites-enfants'), 1),
    (1, (SELECT id FROM NavigationCategory WHERE string_id='jouer'), 2),
    (1, (SELECT id FROM NavigationCategory WHERE string_id='sortir'), 3),

    (1, (SELECT id FROM NavigationCategory WHERE string_id='izilife-plus'), 4),
    (1, (SELECT id FROM NavigationCategory WHERE string_id='spotlights'), 5),

    (1, (SELECT id FROM NavigationCategory WHERE string_id='manger'), 6),
    (1, (SELECT id FROM NavigationCategory WHERE string_id='gouter'), 7),
    (1, (SELECT id FROM NavigationCategory WHERE string_id='bruncher'), 8),
    (1, (SELECT id FROM NavigationCategory WHERE string_id='cafe-the'), 9),

    (1, (SELECT id FROM NavigationCategory WHERE string_id='flaner'), 10),
    (1, (SELECT id FROM NavigationCategory WHERE string_id='balades'), 11),
    (1, (SELECT id FROM NavigationCategory WHERE string_id='marches'), 12),
    (1, (SELECT id FROM NavigationCategory WHERE string_id='art'), 13),

    (1, (SELECT id FROM NavigationCategory WHERE string_id='evenements'), 14),
    (1, (SELECT id FROM NavigationCategory WHERE string_id='experiences'), 15),

    (1, (SELECT id FROM NavigationCategory WHERE string_id='live-sessions'), 16),
    (1, (SELECT id FROM NavigationCategory WHERE string_id='boire'), 17),
    (1, (SELECT id FROM NavigationCategory WHERE string_id='terrasses'), 18),
    (1, (SELECT id FROM NavigationCategory WHERE string_id='rooftops'), 19),
    (1, (SELECT id FROM NavigationCategory WHERE string_id='guinguettes'), 20),

    (1, (SELECT id FROM NavigationCategory WHERE string_id='sport'), 21),
    (1, (SELECT id FROM NavigationCategory WHERE string_id='se-detendre'), 22),
    (1, (SELECT id FROM NavigationCategory WHERE string_id='prendre-soin-de-soi'), 23),

    (1, (SELECT id FROM NavigationCategory WHERE string_id='happy-hour'), 24),

    (1, (SELECT id FROM NavigationCategory WHERE string_id='shopping'), 25),
    (1, (SELECT id FROM NavigationCategory WHERE string_id='courses'), 26),
    (1, (SELECT id FROM NavigationCategory WHERE string_id='s-evader'), 27),
    (1, (SELECT id FROM NavigationCategory WHERE string_id='dormir'), 28),

    (1, (SELECT id FROM NavigationCategory WHERE string_id='chiner'), 29),

    (1, (SELECT id FROM NavigationCategory WHERE string_id='au-quotidien'), 30);
;
-- Seul (profil 2) - même set de catégories, ordre optimisé
INSERT IGNORE INTO `ProfileNavigationCategories` (`profile_id`, `navigation_category_id`, `position`) VALUES
  (2, (SELECT id FROM NavigationCategory WHERE string_id='spotlights'), 1),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='nouveaux-lieux'), 2),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='happy-hour'), 3),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='izilife-plus'), 4),

  (2, (SELECT id FROM NavigationCategory WHERE string_id='boire'), 5),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='sortir'), 6),

  (2, (SELECT id FROM NavigationCategory WHERE string_id='live-sessions'), 7),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='comedie'), 7),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='sport'), 8),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='danser'), 9),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='jouer'), 10),

  (2, (SELECT id FROM NavigationCategory WHERE string_id='evenements'), 11),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='experiences'), 12),

  (2, (SELECT id FROM NavigationCategory WHERE string_id='manger'), 13),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='bruncher'), 14),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='gouter'), 15),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='cafe-the'), 16),

  (2, (SELECT id FROM NavigationCategory WHERE string_id='sorties-premier-rendez-vous'), 17),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='s-evader'), 18),

  (2, (SELECT id FROM NavigationCategory WHERE string_id='deals'), 19),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='rencontres'), 20),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='dormir'), 21),

  (2, (SELECT id FROM NavigationCategory WHERE string_id='flaner'), 22),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='marches'), 23),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='balades'), 24),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='shopping'), 25),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='chiner'), 26),

  (2, (SELECT id FROM NavigationCategory WHERE string_id='art'), 27),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='aider'), 28),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='travailler'), 29),

  (2, (SELECT id FROM NavigationCategory WHERE string_id='se-detendre'), 30),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='prendre-soin-de-soi'), 31),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='terrasses'), 32),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='rooftops'), 33),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='guinguettes'), 34),

  (2, (SELECT id FROM NavigationCategory WHERE string_id='courses'), 35),
  (2, (SELECT id FROM NavigationCategory WHERE string_id='au-quotidien'), 36);

-- En couple (profil 3) - ordre optimisé, sans "que-faire"
INSERT IGNORE INTO `ProfileNavigationCategories` (`profile_id`, `navigation_category_id`, `position`) VALUES
  (3, (SELECT id FROM NavigationCategory WHERE string_id='sorties-premier-rendez-vous'), 1),

  (3, (SELECT id FROM NavigationCategory WHERE string_id='spotlights'), 2),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='nouveaux-lieux'), 3),

  (3, (SELECT id FROM NavigationCategory WHERE string_id='boire'), 4),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='sortir'), 5),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='jouer'), 6),

  (3, (SELECT id FROM NavigationCategory WHERE string_id='happy-hour'), 7),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='izilife-plus'), 8),

  (3, (SELECT id FROM NavigationCategory WHERE string_id='manger'), 9),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='bruncher'), 10),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='gouter'), 11),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='cafe-the'), 12),

  (3, (SELECT id FROM NavigationCategory WHERE string_id='evenements'), 13),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='live-sessions'), 14),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='comedie'), 14),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='experiences'), 15),

  (3, (SELECT id FROM NavigationCategory WHERE string_id='sport'), 16),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='danser'), 17),

  (3, (SELECT id FROM NavigationCategory WHERE string_id='marches'), 18),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='flaner'), 19),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='balades'), 20),

  (3, (SELECT id FROM NavigationCategory WHERE string_id='chiner'), 21),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='shopping'), 22),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='art'), 23),

  (3, (SELECT id FROM NavigationCategory WHERE string_id='s-evader'), 24),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='se-detendre'), 25),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='prendre-soin-de-soi'), 26),

  (3, (SELECT id FROM NavigationCategory WHERE string_id='terrasses'), 27),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='rooftops'), 28),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='guinguettes'), 29),

  (3, (SELECT id FROM NavigationCategory WHERE string_id='deals'), 30),

  (3, (SELECT id FROM NavigationCategory WHERE string_id='dormir'), 31),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='aider'), 32),
  (3, (SELECT id FROM NavigationCategory WHERE string_id='au-quotidien'), 33);

-- Entre amis (profil 4)
INSERT IGNORE INTO `ProfileNavigationCategories` (`profile_id`, `navigation_category_id`, `position`) VALUES
    (4, (SELECT id FROM NavigationCategory WHERE string_id='spotlights'), 1),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='nouveaux-lieux'), 2),

    (4, (SELECT id FROM NavigationCategory WHERE string_id='boire'), 3),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='sortir'), 4),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='jouer'), 5),

    (4, (SELECT id FROM NavigationCategory WHERE string_id='sport'), 6),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='danser'), 7),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='live-sessions'), 8),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='comedie'), 8),

    (4, (SELECT id FROM NavigationCategory WHERE string_id='happy-hour'), 9),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='deals'), 10),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='izilife-plus'), 11),

    (4, (SELECT id FROM NavigationCategory WHERE string_id='evenements'), 12),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='experiences'), 13),

    (4, (SELECT id FROM NavigationCategory WHERE string_id='manger'), 14),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='bruncher'), 15),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='gouter'), 16),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='cafe-the'), 17),

    (4, (SELECT id FROM NavigationCategory WHERE string_id='s-evader'), 18),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='se-detendre'), 19),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='prendre-soin-de-soi'), 20),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='shopping'), 21),

    (4, (SELECT id FROM NavigationCategory WHERE string_id='courses'), 22),

    (4, (SELECT id FROM NavigationCategory WHERE string_id='flaner'), 23),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='balades'), 24),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='art'), 25),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='marches'), 26),

    (4, (SELECT id FROM NavigationCategory WHERE string_id='dormir'), 27),

    (4, (SELECT id FROM NavigationCategory WHERE string_id='terrasses'), 28),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='rooftops'), 29),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='guinguettes'), 30),

    (4, (SELECT id FROM NavigationCategory WHERE string_id='chiner'), 31),
    (4, (SELECT id FROM NavigationCategory WHERE string_id='aider'), 32),

    (4, (SELECT id FROM NavigationCategory WHERE string_id='au-quotidien'), 33);
;

-- Étudiants (profil 5)
INSERT IGNORE INTO `ProfileNavigationCategories` (`profile_id`, `navigation_category_id`, `position`) VALUES
  (5, (SELECT id FROM NavigationCategory WHERE string_id='etudiants'), 1),

  (5, (SELECT id FROM NavigationCategory WHERE string_id='boire'), 2),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='happy-hour'), 3),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='deals'), 4),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='izilife-plus'), 5),

  (5, (SELECT id FROM NavigationCategory WHERE string_id='spotlights'), 6),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='nouveaux-lieux'), 7),

  (5, (SELECT id FROM NavigationCategory WHERE string_id='sortir'), 8),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='jouer'), 9),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='rencontres'), 10),

  (5, (SELECT id FROM NavigationCategory WHERE string_id='live-sessions'), 11),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='comedie'), 11),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='sport'), 12),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='danser'), 13),

  (5, (SELECT id FROM NavigationCategory WHERE string_id='evenements'), 14),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='experiences'), 15),

  (5, (SELECT id FROM NavigationCategory WHERE string_id='manger'), 16),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='bruncher'), 17),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='gouter'), 18),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='cafe-the'), 19),

  (5, (SELECT id FROM NavigationCategory WHERE string_id='flaner'), 20),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='balades'), 21),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='art'), 22),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='marches'), 23),

  (5, (SELECT id FROM NavigationCategory WHERE string_id='se-detendre'), 24),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='prendre-soin-de-soi'), 25),

  (5, (SELECT id FROM NavigationCategory WHERE string_id='shopping'), 26),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='courses'), 27),

  (5, (SELECT id FROM NavigationCategory WHERE string_id='s-evader'), 28),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='dormir'), 29),

  (5, (SELECT id FROM NavigationCategory WHERE string_id='chiner'), 30),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='aider'), 31),

  (5, (SELECT id FROM NavigationCategory WHERE string_id='travailler'), 32),
  (5, (SELECT id FROM NavigationCategory WHERE string_id='au-quotidien'), 33)
;

-- Touriste (profil 6)
INSERT IGNORE INTO `ProfileNavigationCategories` (`profile_id`, `navigation_category_id`, `position`) VALUES
  (6, (SELECT id FROM NavigationCategory WHERE string_id='spotlights'), 1),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='nouveaux-lieux'), 2),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='dormir'), 3),

  (6, (SELECT id FROM NavigationCategory WHERE string_id='boire'), 4),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='sortir'), 5),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='jouer'), 6),

  (6, (SELECT id FROM NavigationCategory WHERE string_id='evenements'), 7),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='experiences'), 8),

  (6, (SELECT id FROM NavigationCategory WHERE string_id='manger'), 9),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='bruncher'), 10),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='gouter'), 11),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='cafe-the'), 12),

  (6, (SELECT id FROM NavigationCategory WHERE string_id='shopping'), 13),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='balades'), 14),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='flaner'), 15),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='art'), 16),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='marches'), 17),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='chiner'), 18),

  (6, (SELECT id FROM NavigationCategory WHERE string_id='live-sessions'), 19),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='comedie'), 19),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='sport'), 20),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='danser'), 21),

  (6, (SELECT id FROM NavigationCategory WHERE string_id='deals'), 22),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='izilife-plus'), 23),

  (6, (SELECT id FROM NavigationCategory WHERE string_id='se-detendre'), 24),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='prendre-soin-de-soi'), 25),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='s-evader'), 26),

  (6, (SELECT id FROM NavigationCategory WHERE string_id='terrasses'), 27),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='rooftops'), 28),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='guinguettes'), 29),

  (6, (SELECT id FROM NavigationCategory WHERE string_id='travailler'), 30),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='aider'), 31),

  (6, (SELECT id FROM NavigationCategory WHERE string_id='courses'), 32),
  (6, (SELECT id FROM NavigationCategory WHERE string_id='au-quotidien'), 33);


create table if not exists DirectoryCategoryGroup (
    id tinyint not null primary key AUTO_INCREMENT,
    name varchar(100) not null,
    string_id varchar(100) not null unique,

    icon_file_name varchar(50) default null,
    special_link varchar(20) default null,

    is_active boolean default 1
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


create table if not exists DirectoryCategory (
    id tinyint not null primary key AUTO_INCREMENT,
    name varchar(100) not null,
    string_id varchar(100) not null unique, 
    categrory_group_id tinyint not null, 
    special_link varchar(20) default null,
    is_active boolean default 1,
    foreign key(categrory_group_id) references DirectoryCategoryGroup(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



INSERT INTO `DirectoryCategoryGroup` (`id`, `name`, `string_id`, icon_file_name, is_active, special_link) VALUES
        (1, 'Restauration', 'restauration', NULL, 1, NULL),
        (2, 'Alimentation', 'alimentation',NULL, 1, NULL),
        (3, 'Shopping', 'shopping', NULL, 1, NULL),
        (4, 'Hygiène, Beauté & Bien-être', 'hygiene-beaute-et-bien-etre', NULL, 1, NULL),
        (5, 'Balades & Visites', 'balades-et-visites', NULL, 1, NULL),
        (6, 'Jeux & Loisirs', 'jeux-et-loisirs',NULL, 1, NULL),
        (7, 'Vie nocturne', 'vie-nocturne', NULL, 1, NULL),
        (8, 'Evènements', 'evenements', NULL, 1, NULL),
        (9, 'Expériences',  'experiences',NULL, 1, NULL),
        (10, 'Commerces de proximité', 'commerces-de-proximite',NULL, 1, NULL),
        (11, 'Services au quotidien', 'au-quotidien', NULL, 1, NULL), 
        (12, 'Artisans & Services', 'artisans-et-services', NULL, 1, NULL),
        (13, 'Culture & Divertissement', 'culture-et-divertissement', NULL, 1, NULL),
        (14, 'Institutions', 'institutions', NULL, 0, NULL)

        ;


    INSERT INTO `DirectoryCategory` (`name`, string_id, is_active, categrory_group_id) VALUES
    -- Restauration
        ('Restaurants', 'restaurants', 1, 1),
        ('Cafés, Salons de thé', 'cafes-salons-de-the', 1, 1),
        ('Boulangeries, Patisseries', 'boulangeries-patisseries', 1, 1),
        ('Glaces, Gaufres & Crêpes', 'glaces-gaufres-et-crepes', 1, 1),
        ('Chocolateries, Sucreries', 'chocolateries-sucreries', 1, 1),
    -- Alimentation
        ('Boucheries, Poissonneries & Fromageries', 'boucheries-poissonnerie-et-fromageries', 1, 2),
        ('Supermarchés, Hypermarchés', 'supermarches-hypermarches', 1, 2),
        ('Epiceries, Superettes & Night shop', 'epiceries-superettes-night-shops',  1, 2),
        ('Primeurs, Fermes', 'primeurs-fermes', 1, 2),
        ("Marchés", 'marches', 1, 2),
        ("Alcools", 'alcools', 1, 2), --
    -- Shopping
        ('Centre commerciaux', 'centre-commerciaux', 1, 3),
        ('Mode', 'mode', 1, 3),
        ('Hygiène & Beauté', 'hygiene-et-beaute', 1, 3),
        ('Maison & Jardin', 'maison-et-jardin', 1, 3),
        ('Electronique', 'electronique', 1, 3),
        ('Magasins de bricolage', 'bricolage', 1, 3),
    -- Hygiène, beauté & Bien-être
        ('Salons, instituts de beauté', 'salons-et-instituts-de-beaute', 1, 4),
        ('Spas, jaccuzzi, Hammam', 'spas-jaccuzzi-hammam', 1, 4),
    -- Balades & Visites
        ('Places & lieux de vie', 'places-et-lieux-de-vie', 1, 5),
        ('Parcs & Jardins', 'parcs-et-jardins', 1, 5),
        ("Aires de jeux, parc d'attractions", 'airs-de-jeux-parcs-d-attraction', 1, 5),
        ("Fermes & Animaux", 'fermes-et-animaux', 1, 5),
        ("Monuments & Attractions touristiques", 'monuments-et-attractions-touristiques', 1, 5),
        ("Musées", 'musees', 1, 5),
        ("Plages, Lacs, Fleuves & autres", 'plages-lac-fleuves-autres', 1, 5),
    -- Jeux & Loisirs
        ('Escalade, Accrobranche', 'escalade-accrobranche', 1, 6),
        ('Bowling, Billard & Karting', 'bowling-billard-et-karting', 1, 6),
        ('Paintball, Laser Game et réalité virtuelle', 'paintball-lasergame-et-realite-virtuelle', 1, 6),
        ('Escape games & Aventures', 'escape-games-et-aventures', 1, 6),
        ('BMX, Skateboard & Autres', 'bmx-skateboard-et-autres', 1, 6),
        ('Parc de loisirs', 'parcs-de-loisirs', 1, 6),
    -- Bars, Discothèques & Autres
        ('Bars', 'bars', 1, 7),
        ('Discothèques', 'discotheques', 1, 7),
        ('Théâtres & Comedy clubs', 'theatres-et-comedy-clubs', 1, 7),
        ('Karaoké, billard & flechettes', 'karaoke-billard-et-flechettes', 1, 7), --

    -- Commerces de proximité 
        ('Librairies & Papeteries', 'librairies-et-papeteries', 1, 10),
        ('Magasins de jouets', 'magasins-de-jouets', 1, 10),
        ('Fleuristes', 'fleuristes', 1, 10),
        ('Disquaires', 'disquaires', 1, 10),
        ('Tabacs', 'tabacs', 1, 11),    
    -- Services au quotidien (Hôtels, Dab, Pressing, Station service, Parkings, Pharmacies, 
        ('Parkings', 'parkings', 1, 11),
        ('Toilettes', 'toilettes', 1, 11),
        ('Pharmacies', 'pharmacies', 1, 11),
        ('Station services', 'station-services', 1, 11),
        ('Pressings', 'pressings', 1, 11),
        ('DAB', 'distributeurs-de-billets', 1, 11), 
        ('Banques', 'banques', 1, 11),
    -- Artisans & Services
        ('Artisans', 'artisans', 1, 12),
        ('Plombiers & Electriciens', 'plombiers-et-electriciens', 1, 12),
        ('Serruriers', 'serruriers', 1, 12),
        ('Menuisiers', 'menuisiers', 1, 12),
        ('Peintres & Décorateurs', 'peintres-et-decorateurs', 1, 12),
        ('Jardiniers & Paysagistes', 'jardiniers-et-paysagistes', 1, 12),
        ('Dépannage & Urgence', 'depannage-et-urgence', 1, 12),
        ('Assistance informatique', 'assistance-informatique', 1, 12),
        ('Réparateurs & Réparation mobile', 'reparation-mobile', 1, 12),
    -- Culture & Divertissement
        ('Cinémas', 'cinemas', 1, 13),
        ('Théâtres', 'theatres', 1, 13),
        ('Bibliothèques & Médiathèques', 'bibliotheques-mediatheques', 1, 13),    
        ('Salles de spectacle', 'salles-de-spectacle', 1, 13), 
    -- Institutions
        ('Bureaux de poste', 'bureaux-de-poste', 0, 14),
        ('Mairies & services publics', 'mairies-et-services-publics', 0, 14)
        
    ;

    /** create table if not exists DirectoryCategoryContents (
        directory_category_id tinyint not null, 
        shop_category_id smallint default NULL, 
        place_type_id smallint default null, 

        position tinyint not null, 

        foreign key(directory_category_id) references DirectoryCategory(id),
        foreign key(shop_category_id) references ShopCategory(id),
        foreign key(place_type_id) references PlaceType(id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci; **/ 


    create table if not exists NavigationSubCategory (
        id smallint not null primary key AUTO_INCREMENT,
        name varchar(50) not null,
        string_id varchar(50) not null unique,
        is_active boolean default 1
    )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    create table if not exists NavigationSubCategoryContent (
        navigation_category_id smallint not null, 
        navigation_sub_category_id smallint not null, 
        position tinyint not null, 

        foreign key(navigation_sub_category_id) references NavigationSubCategory(id),
        foreign key(navigation_category_id) references NavigationCategory(id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    INSERT INTO `NavigationSubCategory` (`name`, `string_id`) values
        ('Lieux de vie', 'lieux-de-vie'),
        ('Parcs & espaces verts', 'parcs-et-espaces-verts'),
        ("Centres commerciaux", "centres-commerciaux"),
        ("Boutiques", "boutiques"),

        ('Attractions touristiques', 'attractions-touristiques'),
        ('Sites historiques & Monuments', 'sites-touristiques-et-monuments'),
        ("Musées", 'musees'),
        ('Édifices religieux', 'edifices-religieux'), -- 
        ('Marchés, Brocantes & Braderies', 'marches-brocantes-et-braderies'),
        ('Parcs d\'attractions & Aires de jeux', 'parcs-d-attractions-et-aires-de-jeux'), -- Parcs d'attractions, aires de jeux, petites animations dans les villes

        ('Activités culinaires', 'activites-culinaires'), -- Cours de cuisine, Dégustation, Circuit Alimentaire, Jeux de piste alimentaires - Evènement alimentaire (Street-food)
        ('Boissons', 'boissons'), -- Dégustation de vins, bières, boissons - circuit bières - BAL - ....
        ("Activités artistiques", "activites-artistiques"), -- Circuit Street-art - Activité lié à l'art (Musée,)  - Cours Stage sur l'art 

        ('Zoo & Aquariums', 'zoos-aquariums'),
        ('Fermes et animaux', 'fermes-et-animaux'),
        ("Au bord de l'eau", "au-bord-de-l-eau"),
        ("Activités aquatiques", "activites-aquatiques"),

        ("Plages", "plages"),
        ("Fleuves, lacs et etangs", "fleuves-lacs-et-etangs"),

        ("Street-art", "street-art"),
        ("Activités litteraires", "activites-litteraires"),
        ("Théâtre", "theatre"),
        ("Humour, Comedy clubs", "humour-et-comedy-clubs"),
        ("Galéries & Œuvres d'art", "galeries-et-oeuvres-d-art"),
        ("Spectacles", "spectacles"),
        ("Expositions", "expositions"),
        ("Créations manuelles", "creations-manuelles"),
        ("Balades & Visites guidées", "balades-et-visites-guidees"),

    -- Shopping
        ("Mode", "mode"),
        ("Hygiène & Beauté", "hygiene-et-beaute"),
        ("Lingerie", "lingerie"),
        ("Bijoux", "bijoux"),
        ("Boutiques de créateurs", "boutiques-de-createurs"),
        ("Boutiques artisanales", "boutiques-artisanales"),
        ("Maison & Déco", "maison-et-deco"),
        ("Livres & BD", "livres-et-bds"),
        ("Hypermarchés & Supermarchés", "hypermarches-et-supermarches"),

    -- Jeux & Divertissement 
        ("Jeux d'aventure & Escape games", "jeux-d-aventure-et-escape-games"),
        ("Jeux de société", "jeux-de-societe"),
        ('Bowling, Billard & Karting', 'bowling-billard-et-karting'),
        ("Laser game, Airsoft & Paintball", "laser-game-airsoft-et-paintball"),
        ("Réalité virtuelle", "realite-virtuelle"),
        ('Escalade & Accrobranche', 'escalade-et-accrobranche'),
        ('Vélo, BMX, Skateboard & Autres', 'velo-bmx-skateboard-et-autres'),
        ('Autres jeux', 'autres-jeux'),

    -- Sorties sportives
        ("Randonnées & running", "randonnees-et-running"),
        ("Cross training, Fitness & Musculation", "cross-training-fitness-et-musculation"),
        ('Danses', 'danses'),
        ('Vélos', 'velos'),
        ('Football', 'football'),
        ('Basket-ball', 'basket-ball'),

        ('Sports de raquettes', 'sports-de-raquette'),
        ('Autres sports collectifs', 'autres-sports-collectifs'),
        ('Sports de combat', 'sports-de-combat'),
        ('Sports aquatiques', 'sports-aquatiques'),
        ("Matchs & Compétitions à voir", "matchs-et-competitions-a-voir"),
    -- Sorties Danses

    -- Petit-Déjeûner
        ('Boulangeries & Patisseries', 'boulangeries-et-patisseries'),
        ("Cafés", "cafes"),
        ("Bars tabacs", "bars-tabacs"),
        ("hôtels", "hotels"),

    -- Déjeuners
        ("Restaurants", "restaurants"),
        ("Salons de thé", "salons-de-the"),
        ("Cafés & Tabacs", "cafes-et-tabacs"),
        ("Brasseries & Bistros", "brasseries-et-bistros"),
        ("Street-foods", "street-foods"),
        ("Food-trucks", "food-trucks")

    -- Brunch
    -- Dîner


    ALTER TABLE `SessionConfigurationContent`
    ADD COLUMN `catalog_work_id` BIGINT UNSIGNED DEFAULT NULL AFTER `day_list`,
    ADD COLUMN `movie_diffusion_id` BIGINT UNSIGNED DEFAULT NULL AFTER `catalog_work_id`,
    ADD COLUMN `equipment_id` BIGINT DEFAULT NULL AFTER `place_id`,

    ADD COLUMN `movie_session_source` ENUM('manual', 'configuration', 'scraping', 'api', 'partner') DEFAULT 'configuration' AFTER `equipment_id`,
    ADD COLUMN `movie_external_id` VARCHAR(100) DEFAULT NULL AFTER `movie_session_source`,
    ADD COLUMN `movie_booking_url` TEXT DEFAULT NULL AFTER `movie_external_id`,
    ADD COLUMN `movie_language_version` ENUM('VF', 'VO', 'VOST', 'VOSTFR', 'MULTI') DEFAULT NULL AFTER `movie_booking_url`,
    ADD COLUMN `movie_screening_format` ENUM('2D', '3D', 'IMAX', 'DOLBY_CINEMA', 'ICE', '4DX', 'OTHER') DEFAULT NULL AFTER `movie_language_version`,

    ADD CONSTRAINT `fk_scc_catalog_work`
        FOREIGN KEY (`catalog_work_id`) REFERENCES `CatalogWork`(`id`) ON DELETE SET NULL,

    ADD CONSTRAINT `fk_scc_movie_diffusion`
        FOREIGN KEY (`movie_diffusion_id`) REFERENCES `MovieDiffusion`(`id`) ON DELETE SET NULL,

    ADD CONSTRAINT `fk_scc_equipment`
        FOREIGN KEY (`equipment_id`) REFERENCES `Equipment`(`id`) ON DELETE SET NULL;

ALTER TABLE `Session`
    ADD INDEX `idx_session_catalog_work_date` (`catalog_work_id`, `date`, `time_start`),
    ADD INDEX `idx_session_movie_diffusion` (`movie_diffusion_id`),
    ADD INDEX `idx_session_place_date` (`place_id`, `date`, `time_start`),
    ADD INDEX `idx_session_movie_source_external` (`movie_session_source`, `movie_external_id`);

ALTER TABLE `SessionConfigurationContent`
    ADD INDEX `idx_scc_catalog_work` (`catalog_work_id`),
    ADD INDEX `idx_scc_movie_diffusion` (`movie_diffusion_id`),
    ADD INDEX `idx_scc_equipment` (`equipment_id`);

    ;


CREATE TABLE LocationOtherCategory (
    shop_id BIGINT default null,
    place_id bigint default null,

    place_type_id  INT default NULL,
    shop_category_id smallint default null, 

    position tinyint unsigned default null,

    FOREIGN KEY (`shop_id`) REFERENCES `Shop`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`place_id`) REFERENCES `Place`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`place_type_id`) REFERENCES `PlaceType`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`shop_category_id`) REFERENCES `ShopCategory`(`id`) ON DELETE CASCADE
);


-- Objet contenant les configuration réservation simple : Bars, Restos, autres commerces
CREATE TABLE `BookingConfiguration` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `is_current` BOOLEAN DEFAULT 0, -- Est-elle active actuellement

    is_active boolean default 0,

    `temporary_type` TINYINT UNSIGNED DEFAULT NULL,
    `with_annual_recurrence` BOOLEAN DEFAULT 0,

    `start_date` DATE DEFAULT NULL, -- Si applicable à une période spécifique
    `end_date` DATE DEFAULT NULL,

    `month_start` TINYINT UNSIGNED DEFAULT NULL, -- Si applicable à un intervalle de mois (ex: été)
    `month_end` TINYINT UNSIGNED DEFAULT NULL,

    `description` TINYTEXT DEFAULT NULL, 

    `place_id` BIGINT DEFAULT NULL,
    `shop_id` BIGINT DEFAULT NULL,
    `animation_id` BIGINT DEFAULT NULL, 
    `equipment_id` BIGINT DEFAULT NULL,
    `event_id` BIGINT DEFAULT NULL, 

    shop_category_id smallint default null, 
    place_type_id int default null, 

    FOREIGN KEY (`shop_category_id`) REFERENCES `ShopCategory`(`id`),
    FOREIGN KEY (`place_type_id`) REFERENCES `PlaceType`(`id`),

    FOREIGN KEY (`temporary_type`) REFERENCES `TemporaryHourlyType`(`id`),
    FOREIGN KEY (`month_start`) REFERENCES `Month`(`id`),
    FOREIGN KEY (`month_end`) REFERENCES `Month`(`id`),

    FOREIGN KEY (`place_id`) REFERENCES `Place`(`id`),
    FOREIGN KEY (`shop_id`) REFERENCES `Shop`(`id`),
    FOREIGN KEY (`animation_id`) REFERENCES `Animation`(`id`),
    FOREIGN KEY (`equipment_id`) REFERENCES `Equipment`(`id`),
    FOREIGN KEY (`event_id`) REFERENCES `LocalEvent`(`id`),
  
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Contenus
CREATE TABLE `BookingConfigurationContent` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    booking_conf_id bigint unsigned default null, 

    `repetition_type` TINYINT UNSIGNED NOT NULL, -- Heures fixes ou répétition
    `repetition_time_measurement` TINYINT UNSIGNED DEFAULT NULL, -- Si EVERY_X - minutes / heures
    `repetition_time` SMALLINT UNSIGNED DEFAULT NULL, -- Valeur numérique (ex: toutes les 15 minutes)

    `min_booking_notice_minutes` SMALLINT UNSIGNED DEFAULT NULL, -- délai minimum avant résa
    `max_people_per_slot` SMALLINT UNSIGNED DEFAULT NULL,
    `max_people_per_hour` SMALLINT UNSIGNED DEFAULT NULL,

    `is_for_all_days` BOOLEAN DEFAULT 0,
    `day_list` JSON DEFAULT NULL, -- liste des jours concernés [1,2,3,4,5]  
    `hour_list` JSON DEFAULT NULL, -- Liste d'heures fixes si conf_type = FIXED_HOURS

    is_special_for_brunch boolean default 0, 
    `have_multi_services` BOOLEAN DEFAULT 0, -- plusieurs services proposés sur la plage
    `have_slots_in_services` BOOLEAN DEFAULT 0, -- choix obligatoire d'un créneau spécifique

    is_active BOOLEAN DEFAULT 1,

    `duration_time_measurement` TINYINT UNSIGNED DEFAULT NULL, -- minutes / heures
    `duration` SMALLINT UNSIGNED DEFAULT NULL, 

    repetition_time_hour_from TIME default null,
    repetition_time_hour_to TIME default null,

    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (`booking_conf_id`) REFERENCES `BookingConfiguration`(`id`),
    FOREIGN KEY (`repetition_time_measurement`) REFERENCES `TimeMeasurementUnity`(`id`),
    FOREIGN KEY (`duration_time_measurement`) REFERENCES `TimeMeasurementUnity`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
     


CREATE TABLE `MealType` (
   id tinyint unsigned not null primary key auto_increment,
   string_id varchar(30) not null,
);
    
INSERT INTO `MealType` (name, string_id, is_principal) VALUES ('Petit déjeuner', 'petit-dejeuner', 1);
INSERT INTO `MealType` (name, string_id, is_principal) VALUES ('Déjeuner', 'dejeuner', 1);
INSERT INTO `MealType` (name, string_id, is_principal) VALUES ('Dîner', 'diner', 1);
INSERT INTO `MealType` (name, string_id, is_principal) VALUES ('Brunch', 'brunch', 1);
INSERT INTO `MealType` (name, string_id, is_principal) VALUES ('Goûter', 'gouter', 1);
INSERT INTO `MealType` (name, string_id, is_principal) VALUES ('Apéritif', 'aperitif', 1);


  CREATE TABLE `ShopMealType` (
    `meal_type_id` tinyint unsigned NOT NULL ,
    `shop_id` bigint NOT NULL,

    foreign key(meal_type_id) references MealType(id),
    foreign key(shop_id) references Shop(id)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

  CREATE TABLE `PlaceMealType` (
    `meal_type_id` tinyint unsigned NOT NULL ,
    `place_id` bigint NOT NULL,

    foreign key(meal_type_id) references MealType(id),
    foreign key(place_id) references Place(id)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


  CREATE TABLE `BarType` (
    `id` tinyint unsigned NOT NULL primary key auto_increment,
    `name` varchar(30) NOT NULL,
    `string_id` varchar(30) NOT NULL unique,
    icone_url varchar(50) default null
);

INSERT INTO `BarType` (`name`, `string_id`) values('Bar posé', 'bar-pose');
INSERT INTO `BarType` (`name`, `string_id`) values('Bar ambiance', 'bar-ambiance');
INSERT INTO `BarType` (`name`, `string_id`) values('Bar dansant', 'bar-dansant');

-- BarType
  CREATE TABLE `ShopBarType` (
    `bar_type_id` tinyint unsigned NOT NULL ,
    `shop_id` bigint NOT NULL,

    foreign key(bar_type_id) references BarType(id),
    foreign key(shop_id) references Shop(id)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

  CREATE TABLE `PlaceBarType` (
    `bar_type_id` tinyint unsigned NOT NULL ,
    `place_id` bigint NOT NULL,

    foreign key(bar_type_id) references BarType(id),
    foreign key(place_id) references Place(id)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


  CREATE TABLE `ItinerantShopPlace` (
  `id` bigint NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `address` varchar(100) default NULL,
  `additional_address` varchar(100) DEFAULT NULL,
  `zip_code` varchar(5) default NULL,
  `town` varchar(100) default NULL,
  `longitude` float default NULL,
  `latitude` float default NULL,
  `shop_id` bigint NOT NULL,
  event_id bigint not null, 
  `name` varchar(50) NOT NULL,

  city_id bigint not null,
  administrative_division_id bigint unsigned default null,
  on_place_id bigint default null,
  on_shop_id bigint default null
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `ItinerantShopPlaces`
--

CREATE TABLE `ItinerantShopPlaces` (
  `id` bigint NOT NULL,
  `shop_id` bigint NOT NULL,
  `day_id` int(1) default NULL,
  `slot_id` int(1) NOT NULL,
  `place_id` bigint not NULL,
  `opening_hour` varchar(5) DEFAULT NULL,
  `closure_hour` varchar(5) DEFAULT NULL,
  `closed_slot` tinyint(1) NOT NULL, 
  hourly_id bigint unsigned default null,

  exceptional_hourly_day date default null
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


#region Loyalty, Mission, BenefitPolicy
    /* =========================
        DROP
    ========================= */
    DROP TABLE IF EXISTS MissionProgress;
    DROP TABLE IF EXISTS Mission;
    DROP TABLE IF EXISTS PriorityTableUse;
    DROP TABLE IF EXISTS PromoRedemption;
    DROP TABLE IF EXISTS LoyaltyProgramType;


    DROP TABLE IF EXISTS IzilifeAccessPolicy;
    DROP TABLE IF EXISTS IzilifeAccessPolicyTier;

    DROP TABLE IF EXISTS BenefitPolicyRule;
    DROP TABLE IF EXISTS BenefitPolicyRulePlan;
    DROP TABLE IF EXISTS LoyaltyProgramMemberGroup; 

    DROP TABLE IF EXISTS MissionReward;
    
    DROP TABLE IF EXISTS LoyaltyProgram;
    DROP TABLE IF EXISTS LoyaltyProgramReward;
    DROP TABLE IF EXISTS MissionClaim;
    DROP TABLE IF EXISTS IzilifeGlobalLoyaltyProgram;
    DROP TABLE IF EXISTS PlanBenefitTemporality;


    /* =========================
       PROMOS: utilisations + valeur (budget)
       ========================= */
    CREATE TABLE PriorityTableUse (
      id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
      user_id BIGINT UNSIGNED NOT NULL,

      partner_id BIGINT UNSIGNED NULL,
      place_id BIGINT UNSIGNED NULL,

      requested_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      status ENUM('requested','accepted','rejected','expired') NOT NULL DEFAULT 'requested',

      meta JSON NULL,

      INDEX idx_ptu_user_week (user_id, requested_at),
      INDEX idx_ptu_place (place_id, requested_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    /* =========================
       MISSIONS / BADGES (minimal)
       ========================= */
    CREATE TABLE Mission (
        id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        unique_id varchar(32) not null,
        name VARCHAR(120) NOT NULL,
        
        description tinytext NULL,

        start_at DATETIME NULL,
        end_at DATETIME NULL,

        cycle_type ENUM(
            'once',
            'monthly',
            'yearly',
            'reusable_after_claim'
        ) NOT NULL DEFAULT 'once',

        goal_type ENUM(
            'visit_place',
            'attend_event',
            'buy_selection',
            'order_online',
            'payment_count',
            'amount_spent_cents',
            'write_review',
            'izilife_listing_participation',
            'join_meetz',
            'izilife_activities',
            'multi_objectif'
        ) NOT NULL,
        scope_level ENUM(
            'global',
            'partner',
            'page',
            'place',
            'Shop'
        ) NOT NULL,

        scope_id BIGINT NULL,

        target_count tinyint UNSIGNED NOT NULL DEFAULT 1,
        target_amount_value decimal(10,2) NULL,
        unity_minimum_pay_value decimal(10,2) default null, 

        number_of_rewards tinyint unsigned default 1,  -- Nombre de récompense après le challenge 
        promotion_game_type_id tinyint unsigned default null, -- Est-ce qu'il obtient avec un système de jeu (Roulettes, lancées de dés)

        is_active TINYINT(1) NOT NULL DEFAULT 1
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    CREATE TABLE MissionReward (
        id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        unique_id varchar(32) NOT NULL UNIQUE,
        mission_id BIGINT UNSIGNED NOT NULL,

        reward_type ENUM(
            'credit',
            'product_free',
            'product_category_free',
            'benefit_rule'
        ) NOT NULL,

        value_int INT NULL,
        currency SMALLINT UNSIGNED DEFAULT 1,

        product_id BIGINT NULL,
        product_category_id BIGINT NULL,
        coupon_id BIGINT NULL,
        benefit_rule_id BIGINT NULL,

        is_active TINYINT(1) NOT NULL DEFAULT 1,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

        priority_order TINYINT UNSIGNED DEFAULT 1,

        CONSTRAINT fk_mrw_mission
            FOREIGN KEY (mission_id) REFERENCES Mission(id) ON DELETE CASCADE,

        INDEX idx_mrw_mission (mission_id, is_active, priority_order)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    CREATE TABLE MissionProgress (
        id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        user_id BIGINT UNSIGNED NOT NULL,
        mission_id BIGINT UNSIGNED NOT NULL,

        cycle_key VARCHAR(20) NOT NULL DEFAULT 'all',

        current_count INT UNSIGNED NOT NULL DEFAULT 0,
        completed_at DATETIME NULL,
        claimed_at DATETIME NULL,

        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

        UNIQUE KEY uq_mp_user_mission_cycle (user_id, mission_id, cycle_key),
        CONSTRAINT fk_mp_mission FOREIGN KEY (mission_id) REFERENCES Mission(id) ON DELETE CASCADE,

        INDEX idx_mp_user (user_id),
        INDEX idx_mp_mission_cycle (mission_id, cycle_key)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    /*CREATE TABLE MissionClaim (
        id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        unique_id varchar(32) NOT NULL UNIQUE,
        mission_id INT UNSIGNED NOT NULL,
        user_id BIGINT UNSIGNED NOT NULL,

        cycle_key VARCHAR(20) NOT NULL DEFAULT 'all',

        status ENUM('earned','consumed','expired') NOT NULL DEFAULT 'earned',
        meta JSON NULL,

        earned_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        consumed_at DATETIME NULL,

        CONSTRAINT fk_mc_mission FOREIGN KEY (mission_id) REFERENCES Mission(id) ON DELETE CASCADE,

        INDEX idx_mc_user_status (user_id, status, earned_at),
        INDEX idx_mc_mission_user_cycle (mission_id, user_id, cycle_key, status)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;*/


    CREATE TABLE IF NOT EXISTS MissionObjective (
      id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
      mission_id BIGINT UNSIGNED NOT NULL,

      goal_type ENUM(
        'visit_place',
        'attend_event',
        'buy_selection',
        'order_online',
        'payment_count',
        'amount_spent_cents',
        'write_review',
        'izilife_listing_participation',
        'join_meetz',
        'izilife_activities'
      ) NOT NULL,

      qty INT UNSIGNED DEFAULT NULL,
      amount_cents INT UNSIGNED DEFAULT NULL,
      amount_min_cents INT UNSIGNED DEFAULT NULL,

      is_active TINYINT(1) NOT NULL DEFAULT 1,
      sort_order INT NOT NULL DEFAULT 0,

      created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,

      KEY idx_mission (mission_id, is_active, sort_order),
      CONSTRAINT fk_mo_mission FOREIGN KEY (mission_id) REFERENCES Mission(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    CREATE TABLE IF NOT EXISTS MissionObjectiveProgress (
      id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
      objective_id BIGINT UNSIGNED NOT NULL,
      user_id BIGINT NOT NULL,

      progress_qty INT UNSIGNED NOT NULL DEFAULT 0,
      progress_amount_cents INT UNSIGNED NOT NULL DEFAULT 0,

      is_completed TINYINT(1) NOT NULL DEFAULT 0,
      completed_at DATETIME NULL DEFAULT NULL,

      created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,

      UNIQUE KEY uq_objective_user (objective_id, user_id),
      KEY idx_objective (objective_id),
      KEY idx_user (user_id),

      CONSTRAINT fk_mop_objective FOREIGN KEY (objective_id) REFERENCES MissionObjective(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    CREATE TABLE `LoyaltyProgramType` (
        `id` TINYINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `name` VARCHAR(30) NOT NULL,

        `string_id` VARCHAR(30) NOT NULL UNIQUE,
        `is_active` BOOLEAN NOT NULL DEFAULT 0
    );

    INSERT INTO `LoyaltyProgramType` (`name`, `string_id`, `is_active`) VALUES
        ('Par points', 'par-points', 1),
        ('Cashback', 'cashback', 0),
        ('Pallier', 'pallier', 0)
        ;

    /* =========================
       LOYALTY PROGRAM (corrigé)
       ========================= */

    CREATE TABLE LoyaltyProgram (
        id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        unique_id varchar(32) NOT NULL UNIQUE,

        commercial_name VARCHAR(60) DEFAULT NULL,

        scope_level ENUM('global', 'place','shop','page','partner') NOT NULL,
        scope_id BIGINT NOT NULL,

        loyalty_type_id TINYINT UNSIGNED NOT NULL,

        is_active TINYINT(1) NOT NULL DEFAULT 1,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            ON UPDATE CURRENT_TIMESTAMP,

        UNIQUE KEY uq_lp_scope (scope_level, scope_id),
        INDEX idx_lp_active (is_active, scope_level, scope_id),
        INDEX idx_lp_type (loyalty_type_id, is_active)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    INSERT INTO LoyaltyProgram (
        id,
      unique_id,
      commercial_name,
      scope_level,
      scope_id,
      loyalty_type_id,
      is_active
    )
    VALUES (
        1,
        "izilife-global-loyalty",
        'Programme de fidélité Izilife',
        'global',
        0,
        1,
        1
    );


    CREATE TABLE LoyaltyProgramMemberGroup (
      id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
      unique_id VARCHAR(32) NOT NULL UNIQUE,
      loyalty_program_id BIGINT UNSIGNED not null, 

      name VARCHAR(60) NOT NULL,
      string_id VARCHAR(60) NOT NULL UNIQUE,

      description TINYTEXT NULL,

      -- seuils (tu peux en utiliser 1 seul selon ton modèle)
      min_points INT UNSIGNED NULL,
      min_amount_cents INT UNSIGNED NULL,
      min_payment_count SMALLINT UNSIGNED NULL,

      badge_id SMALLINT UNSIGNED NULL, -- option: si tu veux lier à UserBadge plus tard

      is_active TINYINT(1) NOT NULL DEFAULT 1,
      sort_order INT NOT NULL DEFAULT 0,

      created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

      INDEX idx_lpmg_active (is_active, sort_order),
      INDEX idx_lpmg_string (string_id)
    );


    CREATE TABLE LoyaltyProgramReward (
        id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        loyalty_program_id BIGINT UNSIGNED NOT NULL,
        unique_id varchar(32) NOT NULL UNIQUE,

        label VARCHAR(255) NULL,

        loyalty_type_id TINYINT UNSIGNED NOT NULL,
        reward_type ENUM('member', 'credit',
            'product_free',
            'product_category_free',
            'benefit_rule') NOT NULL,

        benefit_rule_id BIGINT NULL, -- Si ce sont des promos de type: Reduc montant, %, un acheté un offert, ....
        program_member_group_id BIGINT NULL,
        value_int INT NULL,

        goal_type ENUM(
            'visit_place',
            'attend_event',
            'buy_selection',
            'order_online',
            'payment_count',
            'amount_spent_cents',
            'write_review',
            'izilife_listing_participation',
            'join_meetz',
            'izilife_activities',
            'multi_objectif'
        ) NOT NULL,

        expense_step_from_value INT NULL, -- Montant de dépense auquel la récompense est débloqué
        number_of_paiement_value tinyint unsigned default null, -- Nombre de paiement auquel la récompense est déclenché
        number_of_place_visited smallint unsigned null, -- En fonction de l'appartenance 
        number_of_meetz_realized smallint unsigned null, -- Champs spécial izilife meetz
        number_of_izilife_activities smallint unsigned null, -- Champs spécial izilife

        currency SMALLINT UNSIGNED DEFAULT 1,
        
        is_active TINYINT(1) NOT NULL DEFAULT 1,
        sort_order INT NOT NULL DEFAULT 0,

        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

        CONSTRAINT fk_lpr_lp FOREIGN KEY (loyalty_program_id) REFERENCES LoyaltyProgram(id) ON DELETE CASCADE,
        INDEX idx_lpr_lp (loyalty_program_id, is_active, sort_order)
    );

    /* Compteur user par programme */
    CREATE TABLE IF NOT EXISTS LoyaltyUserCounter (
        id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        loyalty_program_id BIGINT UNSIGNED NOT NULL,
        user_id BIGINT UNSIGNED NOT NULL,

        current_value INT NOT NULL DEFAULT 0,
        current_amount_cents INT NOT NULL DEFAULT 0,

        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

        UNIQUE KEY uq_luc (loyalty_program_id, user_id),
        CONSTRAINT fk_luc_lp FOREIGN KEY (loyalty_program_id) REFERENCES LoyaltyProgram(id) ON DELETE CASCADE,
        INDEX idx_luc_user (user_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    /* Claim = récompense disponible (à consommer/afficher front) */
    /*CREATE TABLE IF NOT EXISTS LoyaltyClaim (
        id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        unique_id varchar(32) NOT NULL UNIQUE,
        loyalty_program_id BIGINT UNSIGNED NOT NULL,
        user_id BIGINT UNSIGNED NOT NULL,

        status ENUM('earned','consumed','expired') NOT NULL DEFAULT 'earned',
        meta JSON NULL,

        earned_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        consumed_at DATETIME NULL,

        CONSTRAINT fk_lc_lp FOREIGN KEY (loyalty_program_id) REFERENCES LoyaltyProgram(id) ON DELETE CASCADE,
        INDEX idx_lc_user_status (user_id, status, earned_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;*/


    CREATE TABLE PlanBenefitTemporality (
        id TINYINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(30) NOT NULL,
        string_id VARCHAR(30) NOT NULL UNIQUE,
        is_active BOOLEAN NOT NULL DEFAULT 0,
        is_for_all_plans BOOLEAN DEFAULT 0
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    INSERT INTO PlanBenefitTemporality (name, string_id, is_active, is_for_all_plans) VALUES
    ('Offre permanente', 'offre-permanente', 1, 0),
    ('Anniversaire', 'anniversaire', 1, 1),
    ('Cadeaux', 'offre-cadeaux-ponctuels', 1, 0),
    ('Surprise', 'surprise', 1, 0);


    CREATE TABLE BenefitPolicyRule (
        id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        unique_id varchar(32) NOT NULL UNIQUE,

        benefit_resume VARCHAR(100) NULL,

        plan_id BIGINT UNSIGNED DEFAULT NULL,
        plan_temporality_id TINYINT UNSIGNED DEFAULT NULL,

        order_method_ids varchar(10) default NULL, 

        scope_level ENUM(
            'global',
            'partner',
            'page',
            'place',
            'shop',
            'event',
            'event_serie',
            'experience'
        ) NOT NULL,
        scope_id BIGINT NULL,

        benefit_target ENUM(
            'all',
            'eap',
            'service',
            'product',
            'equipment'            
        ) NOT NULL,

        on_izilife_object ENUM('meetz','selections') NOT NULL DEFAULT 'selections',

        owner_type ENUM('plan','mission_reward','loyalty_reward', 'offer') NOT NULL DEFAULT 'plan',
        owner_id BIGINT NULL,

        coupon_id BIGINT NULL,
        
        product_id BIGINT NULL,
        product_category_id BIGINT NULL,

        promotion_mechanic_id TINYINT UNSIGNED NOT NULL,
        x_qty TINYINT UNSIGNED NULL,
        y_qty TINYINT UNSIGNED NULL,
        external_promotion_code varchar(20) default NULL,

        value_int SMALLINT UNSIGNED NOT NULL,
        currency SMALLINT UNSIGNED DEFAULT 1,

        is_active TINYINT(1) NOT NULL DEFAULT 1,

        valid_from DATETIME NULL,
        valid_to DATETIME NULL,

        priority SMALLINT UNSIGNED NOT NULL DEFAULT 100,

        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            ON UPDATE CURRENT_TIMESTAMP,

        INDEX idx_bpr_lookup (scope_level, scope_id, is_active, priority),
        INDEX idx_bpr_owner (owner_type, owner_id, is_active),
        INDEX idx_bpr_plan (plan_id, plan_temporality_id, is_active),
        INDEX idx_bpr_active (is_active, promotion_mechanic_id, priority)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    /** Ici je veux juste configurer que sur certains event en fonction de ton abos, t'as un prio d'accès à un event **/
    CREATE TABLE IzilifeAccessPolicy (
        id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        unique_id varchar(32) NOT NULL UNIQUE,

        scope_level ENUM('event', 'event_serie') NOT NULL,
        scope_id BIGINT NULL, -- NULL si global

        -- pour activer/désactiver un bloc de règles
        is_active TINYINT(1) NOT NULL DEFAULT 1,

        -- Anti “mêmes gagnants” (si tu l’utilises)
        fairness_window_days SMALLINT UNSIGNED NOT NULL DEFAULT 60,
        fairness_penalty_score SMALLINT UNSIGNED NOT NULL DEFAULT 100,

        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );

    CREATE TABLE IzilifeAccessPolicyTier (
        access_policy_id BIGINT UNSIGNED not null,

        plan_id BIGINT UNSIGNED not null, 
        number_of_day_before tinyint unsigned not null, -- je veux pouvoir dire, plan le plus fort (3 jours avant, puis 2, puis 1 - Puis ouvert à tout le monde 
            -- ça implique qu'il faut une date d'ouverture officielle )
        discount_percent tinyint unsigned not null,
        max_tickets smallint unsigned not null,

        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );


    CREATE TABLE IF NOT EXISTS BenefitPolicyRuleTargetItem (
      id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
      rule_id BIGINT UNSIGNED NOT NULL,

      target_type ENUM('product','product_category','eap','service','equipment','animation') NOT NULL,
      target_id BIGINT UNSIGNED DEFAULT NULL,

      x_y_type ENUM('x','y','both') DEFAULT NULL,

      apply_all TINYINT(1) NOT NULL DEFAULT 0,

      created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

      -- Généré : si apply_all=1 => key=0, sinon key=target_id
      target_key BIGINT UNSIGNED
        GENERATED ALWAYS AS (IF(apply_all=1, 0, IFNULL(target_id,0))) STORED,

      UNIQUE KEY uq_rule_type_xy_mode_item (rule_id, target_type, x_y_type, apply_all, target_key),
      KEY idx_rule (rule_id, target_type),

      CONSTRAINT fk_bprti_rule FOREIGN KEY (rule_id) REFERENCES BenefitPolicyRule(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


    DROP TABLE IF EXISTS BenefitGrant;
    DROP TABLE IF EXISTS BenefitLedger;

    CREATE TABLE BenefitGrant (
      id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
      unique_id VARCHAR(32) NOT NULL UNIQUE,              -- idempotence / external ref

      user_id BIGINT UNSIGNED NOT NULL,

      -- D'où vient le gain ?
      source_type ENUM(
        'mission',
        'loyalty',
        'contest',
        'referral',
        'support',
        'admin',
        'plan',          -- si tu veux persister certains droits plan (rare)
        'manual'
      ) NOT NULL,
      source_id BIGINT UNSIGNED NULL,                     -- mission_id / loyalty_program_id / contest_id / referral_event_id ...

      -- Quelle récompense exacte dans la source (roulette, multiple rewards, etc.)
      source_reward_type ENUM('mission_reward','loyalty_reward','contest_reward','none') NOT NULL DEFAULT 'none',
      source_reward_id BIGINT UNSIGNED NULL,

      -- Le droit concret : soit un BenefitPolicyRule, soit un crédit wallet, soit une Offer, soit autre
      benefit_kind ENUM('benefit_rule','offer','wallet_credit','feature_unlock','custom') NOT NULL,
      benefit_rule_id BIGINT UNSIGNED NULL,
      offer_id BIGINT UNSIGNED NULL,

      -- Pour "bon d'achat" / crédit
      wallet_id BIGINT UNSIGNED NULL,
      credit_amount_cents INT UNSIGNED NULL,
      currency SMALLINT UNSIGNED NOT NULL DEFAULT 1,

      -- Scope d’usage (où le droit peut être consommé)
      scope_level ENUM('global','partner','page','place','shop','event','event_serie','experience') NOT NULL DEFAULT 'global',
      scope_id BIGINT UNSIGNED NULL,

      -- Lifecycle du droit
      status ENUM('earned','active','reserved','consumed','expired','revoked') NOT NULL DEFAULT 'earned',
      earned_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      activates_at DATETIME NULL,
      expires_at DATETIME NULL,
      consumed_at DATETIME NULL,
      revoked_at DATETIME NULL,
      revoke_reason VARCHAR(120) NULL,

      -- Snapshot (figer la promesse) / meta
      benefit_snapshot_json JSON NULL,
      meta JSON NULL,

      -- Contraintes d’usage propres au grant (ex: usage unique, N fois, etc.)
      max_uses_total INT UNSIGNED NULL,
      max_uses_per_user INT UNSIGNED NULL,                -- souvent 1 pour un grant nominatif

      created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

      INDEX idx_bg_user_status (user_id, status, earned_at),
      INDEX idx_bg_source (source_type, source_id),
      INDEX idx_bg_benefit_rule (benefit_rule_id),
      INDEX idx_bg_offer (offer_id),
      INDEX idx_bg_scope (scope_level, scope_id, status),
      INDEX idx_bg_exp (status, expires_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    -- (Optionnel) Ajoute ensuite les FK quand tes tables source sont stabilisées.
    -- Ex: FOREIGN KEY (benefit_rule_id) REFERENCES BenefitPolicyRule(id)
    -- Ex: FOREIGN KEY (offer_id) REFERENCES Offer(id)
    -- Ex: FOREIGN KEY (wallet_id) REFERENCES Wallet(id)

    CREATE TABLE BenefitLedger (
      id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
      unique_id VARCHAR(32) NOT NULL UNIQUE,          -- idempotence event
      group_id VARCHAR(32) NULL,                      -- regroupe plusieurs lignes (1 checkout)

      user_id BIGINT UNSIGNED NULL,                   -- parfois NULL si event system
      event_type ENUM(
        'check',          -- tentative / simulation
        'apply',          -- appliqué (prix calculé)
        'consume',        -- consommé (usage confirmé)
        'deny',           -- refusé (quota/eligibility/expired)
        'reserve',        -- réservation (optionnel)
        'release',        -- release réservation
        'earn',           -- un droit est gagné (si tu veux aussi tracer ici)
        'expire',         -- expiration automatique
        'revoke'          -- révocation
      ) NOT NULL,

      -- Références métier (ce qui a été appliqué/consommé)
      benefit_rule_id BIGINT UNSIGNED NULL,
      offer_id BIGINT UNSIGNED NULL,
      grant_id BIGINT UNSIGNED NULL,
      access_code_id BIGINT UNSIGNED NULL,            -- OfferAccessCode.id si code

      -- Contexte d’usage (pour tes scopes + anti-abus)
      scope_level ENUM('global','partner','page','place','shop','event','event_serie','experience') NOT NULL DEFAULT 'global',
      scope_id BIGINT UNSIGNED NULL,

      -- Cible (si tu veux tracker quoi exactement a été touché)
      target_type ENUM('all','product','product_category','eap','service','equipment','cart','order') NOT NULL DEFAULT 'all',
      target_id BIGINT UNSIGNED NULL,

      -- Valeur réellement accordée (utile pour budget quotas)
      value_cents INT UNSIGNED NOT NULL DEFAULT 0,
      currency SMALLINT UNSIGNED NOT NULL DEFAULT 1,

      -- Dédup / rate limit (ta logique "1 fois/jour/lieu")
      bucket_key VARCHAR(120) NULL,                   -- ex: "place:123|day:2026-01-16|rule:77|user:9"
      bucket_date DATE NULL,                          -- accélère les requêtes "par jour"
      bucket_count INT UNSIGNED NOT NULL DEFAULT 1,   -- en général 1

      -- Statut / raisons (deny)
      result ENUM('ok','ko') NOT NULL DEFAULT 'ok',
      deny_reason VARCHAR(80) NULL,                   -- ex: "quota_reached", "expired", "not_eligible"

      -- Lien transactionnel
      order_id BIGINT UNSIGNED NULL,
      payment_tx_id BIGINT UNSIGNED NULL,

      meta JSON NULL,
      created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

      INDEX idx_bl_user_time (user_id, created_at),
      INDEX idx_bl_scope_time (scope_level, scope_id, created_at),
      INDEX idx_bl_rule_time (benefit_rule_id, created_at),
      INDEX idx_bl_grant_time (grant_id, created_at),
      INDEX idx_bl_offer_time (offer_id, created_at),
      INDEX idx_bl_bucket (bucket_date, bucket_key),
      INDEX idx_bl_code (access_code_id, created_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
#endregion



#region Moteur de proposition d'escapades 
    CREATE TABLE EscapadeProposalReason (
        id SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(80) NOT NULL,
        string_id VARCHAR(80) NOT NULL UNIQUE,
        category ENUM('nature','activity','culture','event','rest') NOT NULL,
        is_active BOOLEAN NOT NULL DEFAULT 1
    );

    CREATE TABLE EscapadeProposal (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,

        scope_level ENUM(
            'CITY',
            'ADMINISTRATIVE_DIVISION',
            'PLACE',
            'SHOP',
            'ANNUAL_CELEBRATION',
            'EVENT_SERIE'
        ) NOT NULL,

        scope_id BIGINT UNSIGNED NOT NULL,

        proposal_types SET(
            'micro_escape',
            'half_day_trip',
            'day_trip',
            'weekend_trip',
            'city_trip'
        ) NOT NULL,

        profiles SET(
            'seul',
            'entre-amis',
            'en-couple',
            'etudiant',
            'en-famille',
            'touriste',
            'avec-enfants'
        ) DEFAULT NULL,

        weather SET('sunny','hot','rainy','cold') DEFAULT NULL,

        start_month TINYINT UNSIGNED DEFAULT NULL,
        end_month TINYINT UNSIGNED DEFAULT NULL,

        priority INT NOT NULL DEFAULT 0,
        is_active BOOLEAN NOT NULL DEFAULT 1,

        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

        UNIQUE KEY uq_escapade_scope (scope_level, scope_id),

        INDEX idx_escapade_active (is_active),
        INDEX idx_escapade_types (proposal_types),
        INDEX idx_escapade_profiles (profiles),
        INDEX idx_escapade_months (start_month, end_month),
        INDEX idx_escapade_priority (priority)
    );


    CREATE TABLE EscapadeProposalConfigReason (
        config_id BIGINT UNSIGNED NOT NULL,
        reason_id SMALLINT UNSIGNED NOT NULL,
        weight TINYINT UNSIGNED NOT NULL DEFAULT 1,

        PRIMARY KEY (config_id, reason_id),

        FOREIGN KEY (config_id) REFERENCES EscapadeProposal(id) ON DELETE CASCADE,
        FOREIGN KEY (reason_id) REFERENCES EscapadeProposalReason(id)
    );


    INSERT INTO EscapadeProposalReason (name, string_id, category) VALUES
    -- Nature
    ('Mer', 'mer', 'nature'),
    ('Plage', 'plage', 'nature'),
    ('Lac', 'lac', 'nature'),
    ('Canal', 'canal', 'nature'),
    ('Forêt', 'foret', 'nature'),
    ('Montagne', 'montagne', 'nature'),
    ('Nature', 'nature', 'nature'),

    -- Activité simple
    ('Balade', 'balade', 'activity'),
    ('Randonnée', 'randonnee', 'activity'),
    ('Vélo', 'velo', 'activity'),
    ('Pique-nique', 'pique-nique', 'activity'),
    ('Se poser', 'se-poser', 'rest'),

    -- Culture / ville
    ('Visiter la ville', 'visiter-la-ville', 'culture'),
    ('Patrimoine', 'patrimoine', 'culture'),
    ('Village de charme', 'village-de-charme', 'culture'),

    -- Événementiel
    ('Événement', 'evenement', 'event'),
    ('Marché', 'marche', 'event'),
    ('Marché de Noël', 'marche-de-noel', 'event'),
    ('Festival', 'festival', 'event');
#endregion


CREATE TABLE `PageInterventionArea` (
  `id` bigint NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `page_id` bigint NOT NULL,

  `city_id` bigint DEFAULT NULL,
  `administrative_division_id` bigint DEFAULT NULL,

  `radius_km` smallint unsigned DEFAULT NULL,
  `is_primary` tinyint(1) NOT NULL DEFAULT 0,

  FOREIGN KEY (`page_id`) REFERENCES `Page`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



CREATE TABLE `Page` (
  `id` bigint NOT NULL PRIMARY KEY AUTO_INCREMENT,

  `username` varchar(50) NOT NULL UNIQUE,
  `name` varchar(80) NOT NULL,
  `page_category_id` smallint unsigned NOT NULL,

  `principal_picture` bigint unsigned DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,

  `creation_date` datetime NOT NULL DEFAULT current_timestamp(),
  `short_description` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 0,

  -- Page créée par un user
  `user_id` bigint DEFAULT NULL,

  -- Ville centrale / zone principale de la page
  `location_city_id` bigint DEFAULT NULL,

  -- Page officielle d’une entité territoriale ou système
  `official_city_id` bigint DEFAULT NULL,
  `official_administrative_division_id` bigint DEFAULT NULL,
  `official_network_id` bigint DEFAULT NULL,
  `official_brand_id` bigint DEFAULT NULL,

  -- Si la page représente directement un partner
  -- Exemple : association, artisan, profession libérale
  `partner_id` bigint DEFAULT NULL,

  -- Si la page est possédée / administrée par un partner
  -- Exemple : DJ, artiste, média, page de ville gérée par une mairie
  `property_partner_id` bigint DEFAULT NULL,

  -- Optionnel mais utile pour tes cas spéciaux
  `is_verified` tinyint(1) NOT NULL DEFAULT 0,
  `is_official` tinyint(1) NOT NULL DEFAULT 0,

  FOREIGN KEY (`page_category_id`) REFERENCES `PageCategory`(`id`),
  FOREIGN KEY (`user_id`) REFERENCES `User`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `PageCategory` (
  `id` smallint unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  `string_id` varchar(80) NOT NULL UNIQUE,

  -- Famille
  `family` enum(
    'creator',
    'organization',
    'professional',
    'institution',
    'media',
    'community',
    'brand',
    'other'
  ) NOT NULL DEFAULT 'other',

  -- Usage
  `is_usable_by_users` boolean NOT NULL DEFAULT 0,
  `is_active` boolean NOT NULL DEFAULT 1,

  -- Cas institutionnels / officiels
  `is_local_state_category` boolean NOT NULL DEFAULT 0,
  `is_tourist_office` boolean NOT NULL DEFAULT 0,
  `can_be_official_page` boolean NOT NULL DEFAULT 0,

  -- Profils pro spéciaux
  `is_professional_profile` boolean NOT NULL DEFAULT 0,
  `is_health_profile` boolean NOT NULL DEFAULT 0,
  `is_artisan_profile` boolean NOT NULL DEFAULT 0,
  `is_liberal_profession_profile` boolean NOT NULL DEFAULT 0,
  `is_event_provider` boolean NOT NULL DEFAULT 0,

  -- Capacités opérationnelles
  `capabilities` SET(
    'sell_products',
    'sell_services',
    'receive_bookings',
    'intervention_area',
    'create_events',
    'create_experiences',
    'partner_verification_required',
    'license_verification_required'
  ) NOT NULL DEFAULT '',

  `parent_id` smallint unsigned DEFAULT NULL,

  FOREIGN KEY (`parent_id`) REFERENCES `PageCategory`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


INSERT INTO PageCategory (id, name, string_id, family, is_active, is_usable_by_users, is_professional_profile, is_health_profile, is_artisan_profile, is_liberal_profession_profile, is_event_provider, is_local_state_category, is_tourist_office, can_be_official_page, capabilities) VALUES
(1, 'Association', 'association', 'organization', 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 'create_events,create_experiences'),
(2, 'Club', 'club', 'organization', 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 'create_events,create_experiences'),
(3, 'Artiste/Groupe', 'artiste-groupe', 'creator', 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 'sell_services,receive_bookings,create_events,create_experiences'),
(4, 'DJ', 'dj', 'creator', 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 'sell_services,receive_bookings,create_events,create_experiences'),
(5, 'Artisan', 'artisan', 'professional', 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 'sell_products,sell_services,receive_bookings,intervention_area,partner_verification_required'),
(6, 'Médecin', 'medecin', 'professional', 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 'receive_bookings,intervention_area,partner_verification_required,license_verification_required'),
(7, 'Infirmier/Infirmière', 'infirmier-infirmiere-liberale', 'professional', 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 'receive_bookings,intervention_area,partner_verification_required,license_verification_required'),
(8, 'Photographe', 'photographe', 'professional', 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 'sell_products,sell_services,receive_bookings,intervention_area,partner_verification_required'),
(9, 'Coach', 'coach', 'professional', 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 'sell_services,receive_bookings,intervention_area,create_experiences,partner_verification_required'),
(10, 'Office de tourisme', 'office-de-tourisme', 'institution', 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 'create_events,create_experiences'),
(11, 'Collectivité locale', 'collectivite-locale', 'institution', 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 'create_events'),
(12, 'Marque', 'marque', 'brand', 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, ''),
(13, 'Entreprise', 'entreprise', 'organization', 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, ''),
(14, 'Service public et gouvernemental', 'service-public-gouvernemental', 'institution', 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 'create_events'),
(15, 'Personnalité publique', 'personnalite-publique', 'creator', 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, ''),
(16, 'Acteur/Actrice', 'acteur-actrice', 'creator', 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'sell_services,receive_bookings,create_events'),
(17, 'Humoriste', 'humoriste', 'creator', 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 'sell_services,receive_bookings,create_events'),
(18, 'Athlète', 'athlete', 'creator', 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'sell_services,receive_bookings,create_events,create_experiences'),
(19, 'Troupe', 'troupe', 'organization', 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 'sell_services,receive_bookings,create_events'),
(20, 'Équipe sportive', 'equipe-sportive', 'organization', 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 'create_events,create_experiences'),
(21, 'Équipe amateur', 'equipe-amateur', 'organization', 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 'create_events'),
(22, 'Média local', 'media-local', 'media', 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 'create_events'),
(23, 'Créateur digital', 'createur-digital', 'creator', 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'sell_services,receive_bookings'),
(24, 'Organisateur d’évènements', 'organisateur-d-evenements', 'organization', 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 'create_events,create_experiences'),
(25, 'Prestataire événementiel', 'prestataire-evenementiel', 'professional', 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 'sell_services,receive_bookings,intervention_area,create_events,partner_verification_required'),
(26, 'Chaîne TV/Web TV', 'chaine-tv-web-tv', 'media', 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, '');


#region User COntents
    CREATE TABLE `UserList` (
      `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
      `unique_id` VARCHAR(32) NOT NULL UNIQUE,

      `user_id` BIGINT DEFAULT NULL,
      `page_id` BIGINT DEFAULT NULL,

      `title` VARCHAR(255) NOT NULL,
      `description` TINYTEXT DEFAULT NULL,

      `confidentiality` TINYINT UNSIGNED DEFAULT 1,

      `cover_media_id` BIGINT UNSIGNED DEFAULT NULL,
      `creation_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
      `is_active` BOOLEAN DEFAULT TRUE,

      FOREIGN KEY (`user_id`) REFERENCES `User`(`id`),
      FOREIGN KEY (`page_id`) REFERENCES `Page`(`id`),
      FOREIGN KEY (`cover_media_id`) REFERENCES `Media`(`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    CREATE TABLE `UserListItem` (
      `list_id` BIGINT UNSIGNED NOT NULL,

      `scope_level` ENUM(
        'place',
        'shop',
        'event',
        'event_serie',
        'experience',
        'annual_celebration',
        'equipment',
        'circuit',
        'collection',
        'top'
      ) NOT NULL,
      `scope_id` BIGINT NOT NULL,

      `display_order` SMALLINT UNSIGNED DEFAULT 0,
      `note` TINYTEXT DEFAULT NULL,
      `creation_date` DATETIME DEFAULT CURRENT_TIMESTAMP,

      PRIMARY KEY (`list_id`, `scope_level`, `scope_id`),

      INDEX `idx_user_list_item_scope` (`scope_level`, `scope_id`),

      FOREIGN KEY (`list_id`) REFERENCES `UserList`(`id`) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    CREATE TABLE LocalTip (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        unique_id VARCHAR(32) NOT NULL UNIQUE,

        title VARCHAR(120) NOT NULL,
        description TEXT NOT NULL,

        target_type ENUM('place','shop','equipment','experience','event_serie') NOT NULL,
        target_id BIGINT UNSIGNED NOT NULL,

        author_type ENUM('user','page','partner','izilife') NOT NULL DEFAULT 'user',
        author_id BIGINT UNSIGNED NOT NULL,

        main_media_id BIGINT UNSIGNED DEFAULT NULL,

        mood ENUM('solo','couple','friends','family','kids','date','work','sport','chill') DEFAULT NULL,
        budget_level ENUM('free','cheap','medium','premium') DEFAULT NULL,

        best_moment ENUM('morning','lunch','afternoon','sunset','evening','night','anytime') DEFAULT 'anytime',
        duration_minutes SMALLINT UNSIGNED DEFAULT NULL,

        status ENUM('draft','pending','published','rejected','archived') NOT NULL DEFAULT 'pending',
        moderation_note VARCHAR(255) DEFAULT NULL,

        creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

        INDEX idx_local_tip_target (target_type, target_id),
        INDEX idx_local_tip_author (author_type, author_id),
        INDEX idx_local_tip_status (status, creation_date),

        FOREIGN KEY (main_media_id) REFERENCES Media(id)
    );

    CREATE TABLE LocalTipHobby (
        local_tip_id BIGINT UNSIGNED NOT NULL,
        hobby_id INT NOT NULL,

        PRIMARY KEY (local_tip_id, hobby_id),
        FOREIGN KEY (local_tip_id) REFERENCES LocalTip(id) ON DELETE CASCADE,
        FOREIGN KEY (hobby_id) REFERENCES Hobby(id)
    );

    CREATE TABLE LocalTipMedias (
        local_tip_id BIGINT UNSIGNED NOT NULL,
        media_id BIGINT UNSIGNED NOT NULL,
        position SMALLINT UNSIGNED NOT NULL DEFAULT 0,

        PRIMARY KEY (local_tip_id, media_id),
        FOREIGN KEY (local_tip_id) REFERENCES LocalTip(id) ON DELETE CASCADE,
        FOREIGN KEY (media_id) REFERENCES Media(id)
    );


    CREATE TABLE OutingIdea (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        unique_id VARCHAR(32) NOT NULL UNIQUE,

        title VARCHAR(150) NOT NULL,
        subtitle VARCHAR(180) DEFAULT NULL,
        description TEXT DEFAULT NULL,

        author_type ENUM('user','page','partner','izilife') NOT NULL DEFAULT 'user',
        author_id BIGINT UNSIGNED NOT NULL,

        scope_level ENUM('country','area','city','place') NOT NULL DEFAULT 'city',
        scope_id BIGINT UNSIGNED NOT NULL,

        outing_kind ENUM('afternoon','evening','day','weekend','date','family','friends','sport','custom') NOT NULL DEFAULT 'custom',

        min_duration_minutes SMALLINT UNSIGNED DEFAULT NULL,
        max_duration_minutes SMALLINT UNSIGNED DEFAULT NULL,

        budget_level ENUM('free','cheap','medium','premium','mixed') DEFAULT 'mixed',
        mobility_mode ENUM('walk','bike','car','public_transport','mixed') DEFAULT 'mixed',

        main_media_id BIGINT UNSIGNED DEFAULT NULL,

        status ENUM('draft','pending','published','rejected','archived') NOT NULL DEFAULT 'pending',
        is_editorial_pick BOOLEAN NOT NULL DEFAULT 0,

        creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

        INDEX idx_outing_scope (scope_level, scope_id),
        INDEX idx_outing_author (author_type, author_id),
        INDEX idx_outing_status (status, creation_date),

        FOREIGN KEY (main_media_id) REFERENCES Media(id)
    );

    CREATE TABLE OutingIdeaStep (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        outing_id BIGINT UNSIGNED NOT NULL,

        step_order SMALLINT UNSIGNED NOT NULL,
        title VARCHAR(120) NOT NULL,
        description TINYTEXT DEFAULT NULL,

        action_kind ENUM('eat','drink','play','walk','visit','shop','event','chill','sleep','other') NOT NULL DEFAULT 'other',
        is_required BOOLEAN NOT NULL DEFAULT 1,

        estimated_duration_minutes SMALLINT UNSIGNED DEFAULT NULL,

        UNIQUE KEY uq_outing_step_order (outing_id, step_order),
        FOREIGN KEY (outing_id) REFERENCES OutingIdea(id) ON DELETE CASCADE
    );

    CREATE TABLE OutingIdeaStepOption (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        step_id BIGINT UNSIGNED NOT NULL,

        option_order SMALLINT UNSIGNED NOT NULL DEFAULT 0,

        target_type ENUM('place','shop','event','event_serie','experience','equipment','free_text') NOT NULL,
        target_id BIGINT UNSIGNED DEFAULT NULL,

        title VARCHAR(150) DEFAULT NULL,
        description TINYTEXT DEFAULT NULL,

        price_hint VARCHAR(50) DEFAULT NULL,
        booking_recommended BOOLEAN NOT NULL DEFAULT 0,

        UNIQUE KEY uq_step_option_order (step_id, option_order),
        INDEX idx_step_option_target (target_type, target_id),

        FOREIGN KEY (step_id) REFERENCES OutingIdeaStep(id) ON DELETE CASCADE
    );

    CREATE TABLE OutingIdeaHobby (
        outing_id BIGINT UNSIGNED NOT NULL,
        hobby_id INT NOT NULL,

        PRIMARY KEY (outing_id, hobby_id),
        FOREIGN KEY (outing_id) REFERENCES OutingIdea(id) ON DELETE CASCADE,
        FOREIGN KEY (hobby_id) REFERENCES Hobby(id)
    );
#endregion 

-- Question, Anecdocte, 
CREATE TABLE PlayfulContent (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    unique_id VARCHAR(32) NOT NULL UNIQUE,

    content_type ENUM(
        'anecdote',
        'savais_tu',
        'blague',
        'devinette',
        'charade',
        'fait_patrimonial'
    ) NOT NULL,

    title VARCHAR(120) DEFAULT NULL,
    body TEXT NOT NULL,
    answer TEXT DEFAULT NULL,
    explanation TEXT DEFAULT NULL,

    target_type ENUM('global','place','city','country','event','event_serie','knowledge','art_piece') NOT NULL DEFAULT 'global',
    target_id BIGINT UNSIGNED DEFAULT NULL,

    minimal_age TINYINT UNSIGNED DEFAULT NULL,
    language_id INT NOT NULL DEFAULT 1,

    author_type ENUM('izilife','user','page','partner') NOT NULL DEFAULT 'izilife',
    author_id BIGINT UNSIGNED DEFAULT NULL,

    status ENUM('draft','pending','published','rejected','archived') NOT NULL DEFAULT 'draft',

    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_playful_type (content_type, status),
    INDEX idx_playful_target (target_type, target_id)
);

#region Promo & Code Promo 

    CREATE TABLE PromoSource (
        id SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(80) NOT NULL,
        string_id VARCHAR(80) NOT NULL UNIQUE,

        source_type ENUM('izilife','local_partner','affiliate_network','brand','influencer','community','manual_web') NOT NULL,

        website_url VARCHAR(255) DEFAULT NULL,
        is_active BOOLEAN NOT NULL DEFAULT 1
    );

    CREATE TABLE PromoBrand (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        unique_id VARCHAR(32) NOT NULL UNIQUE,

        name VARCHAR(120) NOT NULL,
        string_id VARCHAR(120) NOT NULL UNIQUE,
        website_url VARCHAR(255) DEFAULT NULL,
        logo_media_id BIGINT UNSIGNED DEFAULT NULL,

        is_active BOOLEAN NOT NULL DEFAULT 1,

        FOREIGN KEY (logo_media_id) REFERENCES Media(id)
    );

    CREATE TABLE ExternalPromo (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        unique_id VARCHAR(32) NOT NULL UNIQUE,

        source_id SMALLINT UNSIGNED NOT NULL,
        brand_id BIGINT UNSIGNED DEFAULT NULL,

        owner_type ENUM('izilife','influencer','page','partner','user') NOT NULL DEFAULT 'izilife',
        owner_id BIGINT UNSIGNED DEFAULT NULL,

        title VARCHAR(160) NOT NULL,
        description TEXT DEFAULT NULL,

        promo_kind ENUM('code','deal','cashback','affiliate_link','student','local','happy_hour','member_benefit') NOT NULL,

        code VARCHAR(80) DEFAULT NULL,
        landing_url VARCHAR(500) DEFAULT NULL,
        affiliate_url VARCHAR(800) DEFAULT NULL,

        discount_type ENUM('percent','amount','free_product','free_shipping','special_price','unknown') NOT NULL DEFAULT 'unknown',
        discount_value DECIMAL(10,2) DEFAULT NULL,
        currency CHAR(3) DEFAULT NULL,

        scope_level ENUM('online','country','city','shop','place','global') NOT NULL DEFAULT 'online',
        scope_id BIGINT UNSIGNED DEFAULT NULL,

        start_at DATETIME DEFAULT NULL,
        end_at DATETIME DEFAULT NULL,

        status ENUM('draft','pending','published','expired','rejected','archived') NOT NULL DEFAULT 'pending',
        is_verified BOOLEAN NOT NULL DEFAULT 0,
        verified_at DATETIME DEFAULT NULL,

        priority INT NOT NULL DEFAULT 0,

        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

        INDEX idx_external_promo_active (status, end_at),
        INDEX idx_external_promo_brand (brand_id),
        INDEX idx_external_promo_owner (owner_type, owner_id),
        INDEX idx_external_promo_scope (scope_level, scope_id),

        FOREIGN KEY (source_id) REFERENCES PromoSource(id),
        FOREIGN KEY (brand_id) REFERENCES PromoBrand(id)
    );

    CREATE TABLE ExternalPromoClick (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,

        promo_id BIGINT UNSIGNED NOT NULL,
        user_id BIGINT DEFAULT NULL,

        clicked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        referrer_context VARCHAR(80) DEFAULT NULL,

        FOREIGN KEY (promo_id) REFERENCES ExternalPromo(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES User(id)
    );

    CREATE TABLE ExternalPromoValidation (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,

        promo_id BIGINT UNSIGNED NOT NULL,
        user_id BIGINT DEFAULT NULL,

        validation_status ENUM('works','does_not_work','unknown') NOT NULL,
        comment VARCHAR(255) DEFAULT NULL,

        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (promo_id) REFERENCES ExternalPromo(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES User(id)
    );
#endregion 

CREATE TABLE `CircuitType` (
  `id` tinyint unsigned NOT NULL primary key auto_increment,
  `name` varchar(20) NOT NULL,
  `string_id` varchar(20) NOT NULL unique
);

INSERT INTO `CircuitType` (`name`, `string_id`) values('Parcours Touristique', 'balade-touristique');
INSERT INTO `CircuitType` (`name`, `string_id`) values('Sortie sportive', 'sortie-sportive');

-- Type de sortie sportive
CREATE TABLE `SportCircuitType` (
  `id` tinyint unsigned NOT NULL primary key auto_increment,
  `name` varchar(20) NOT NULL,
  `string_id` varchar(20) NOT NULL unique
);

INSERT INTO `SportCircuitType` (`name`, `string_id`) values('Marche', 'marche');
INSERT INTO `SportCircuitType` (`name`, `string_id`) values('Randonnée', 'randonnee');
INSERT INTO `SportCircuitType` (`name`, `string_id`) values('Running', 'running');
INSERT INTO `SportCircuitType` (`name`, `string_id`) values('Vélo', 'velo');
INSERT INTO `SportCircuitType` (`name`, `string_id`) values('Roller', 'roller');

-- Type de sortie sportive
CREATE TABLE `CircuitTheme` (
  `id` tinyint unsigned NOT NULL primary key auto_increment,
  `name` varchar(20) NOT NULL,
  `string_id` varchar(20) NOT NULL unique,

  is_usable_for_tourism_circuit boolean default 0,
  is_usable_for_sport_circuit boolean default 0
);

INSERT INTO `CircuitTheme` (`name`, `string_id`,is_usable_for_tourism_circuit, is_usable_for_sport_circuit) values('Aventure', 'aventure', 1, 1);
INSERT INTO `CircuitTheme` (`name`, `string_id`,is_usable_for_tourism_circuit, is_usable_for_sport_circuit) values('Urbain', 'urbain', 1, 1);
INSERT INTO `CircuitTheme` (`name`, `string_id`,is_usable_for_tourism_circuit, is_usable_for_sport_circuit) values('Faune', 'faune', 1, 1);
INSERT INTO `CircuitTheme` (`name`, `string_id`,is_usable_for_tourism_circuit, is_usable_for_sport_circuit) values('Flore', 'flore', 1, 1);
INSERT INTO `CircuitTheme` (`name`, `string_id`,is_usable_for_tourism_circuit, is_usable_for_sport_circuit) values('Gourmande', 'gourmande', 1, 1);

INSERT INTO `CircuitTheme` (`name`, `string_id`,is_usable_for_tourism_circuit, is_usable_for_sport_circuit) values('Panorama', 'panorama', 0, 1);
INSERT INTO `CircuitTheme` (`name`, `string_id`,is_usable_for_tourism_circuit, is_usable_for_sport_circuit) values('Bivouac', 'bivouac', 1, 1);
INSERT INTO `CircuitTheme` (`name`, `string_id`,is_usable_for_tourism_circuit, is_usable_for_sport_circuit) values('Zen', 'zen', 1, 1);

INSERT INTO `CircuitTheme` (`name`, `string_id`,is_usable_for_tourism_circuit, is_usable_for_sport_circuit) values('Architecture', 'architecture', 1, 0);
INSERT INTO `CircuitTheme` (`name`, `string_id`,is_usable_for_tourism_circuit, is_usable_for_sport_circuit) values('Culture', 'culture', 1, 0);
INSERT INTO `CircuitTheme` (`name`, `string_id`,is_usable_for_tourism_circuit, is_usable_for_sport_circuit) values('Histoire', 'histoire', 1, 0);
INSERT INTO `CircuitTheme` (`name`, `string_id`,is_usable_for_tourism_circuit, is_usable_for_sport_circuit) values('Art', 'art', 1, 0);
INSERT INTO `CircuitTheme` (`name`, `string_id`,is_usable_for_tourism_circuit, is_usable_for_sport_circuit) values('Street-art', 'street-art', 1, 0);


-- Catégories principales des activités de sorties. Permettra de relier entre eux les évents, les expériences ....
CREATE TABLE `ActivityPrincipalCategory` (
  `id` smallint unsigned NOT NULL primary key auto_increment,
  `name` varchar(50) NOT NULL,
  `string_id` varchar(50) NOT NULL unique, 

  use_for_course boolean default 0, -- Utiliser pour les Cours, Ateliers & Stage 
  use_for_visit boolean default 0,  -- Utiliser pour les visites guidées, les balades, circuits touristiques
  use_for_visit_and_tasting boolean default 0, -- utiliser pour les Balades & Dégustations
  use_for_tasting boolean default 0, -- utiliser pour les évents de dégustation (Vins, Cuisine, Alcools, ...)

  use_for_profesional_category boolean default 0, -- Si c'est un Domaine professionel. On stocke aussi ces infos dans cette table une classification des domaines professionnels (Restauration, Commerce, ....)
  use_for_festival boolean default 0,

  usable boolean default 1, -- Utilisable pour ajouter comme lien avec une activité 

  is_activity boolean default 0,
  is_service_to_people boolean default 0,
  is_sport_activity boolean default 0,

  parent_id smallint unsigned default null,
  second_parent_id tinyint unsigned default null,
  third_parent_id tinyint unsigned default null,
  foreign key (parent_id) references ActivityPrincipalCategory(id)
);


INSERT INTO `ActivityPrincipalCategory` (id, `name`, `string_id`, usable, use_for_course, use_for_visit, use_for_tasting, use_for_visit_and_tasting, use_for_profesional_category, 
  use_for_festival) values 
  (1, 'Art', 'art', 1, 0, 1, 0, 1, 1, 1),
  (2, 'Culture', 'culture', 1, 0, 1, 0, 0, 0, 1),
  (3, 'Artisanat', 'artisanat', 1, 0, 1, 0, 1, 1, 1),
  (4, 'Musique', 'musique', 1, 1, 0, 0, 1, 1, 1),
  (5, 'Cinéma', 'cinema', 1, 1, 0, 0, 0, 1, 1),
  (6, 'Sport', 'sport', 1, 1, 1, 0, 0, 1, 1),
  (7, 'Danse', 'danse', 1, 1, 0, 0, 0, 1, 1),

  (8, 'Litterature', 'litterature', 1, 1, 0, 0, 0, 1, 1),
  (9, 'Spectacle', 'spectacle', 1, 1, 1, 0, 0, 1, 1),
  (10, 'Théâtre', 'theatre', 1, 1, 1, 0, 0, 1, 1),

  (11, 'Science', 'science', 1, 1, 1, 0, 0, 1, 1),
  (12, 'Mode', 'mode', 1, 1, 1, 0, 0, 1, 1),
  (13, 'Bien-être', 'bien-etre', 1, 1, 1, 0, 0, 1, 1),
  (14, 'Jeux', 'jeux', 1, 1, 1, 0, 0, 1, 1),
  (15, 'Hygiène & Beauté', 'hygiene-et-beaute', 1, 1, 1, 0, 1, 0, 1),
  (16, 'A manger', 'a-manger', 1, 1, 1, 1, 1, 0, 1),
  (17, 'Boissons', 'boissons', 1, 1, 1, 1, 1, 1, 1),
  (18, 'Loisirs', 'loisirs', 1, 1, 1, 0, 0, 1, 1),
  (19, 'Marchés & Brocantes', 'marches-et-brocantes', 1, 1, 1, 0, 0, 1, 1),
  (20, 'Professions', 'professions', 0, 0, 0, 0, 0, 0, 1);


INSERT INTO `ActivityPrincipalCategory` (id, `name`, `string_id`, parent_id, second_parent_id, use_for_course, use_for_visit, use_for_tasting, use_for_visit_and_tasting, use_for_profesional_category, 
  use_for_festival) values 
-- Art 
  (21, 'Architecture', 'architecture', 1, 2, 1, 1, 0, 1, 1, 1),
  (22, 'Sculpture', 'sculpture', 1, 2, 1, 1, 0, 1, 1, 1),
  (23, 'Peinture', 'peinture', 1, 2, 1, 1, 0, 1, 1, 1),
  (24, 'Dessin', 'dessin', 1, 2, 1, 1, 0, 1, 1, 1),
  (25, 'Street Art', 'street-art', 1, 2, 1, 1, 0, 1, 1, 1),
  (26, 'Calligraphie', 'calligraphie', 1, 2, 1, 1, 0, 1, 1, 1),
  (27, 'Photographie', 'photographie', 1, 2, 1, 1, 0, 1, 1, 1),
-- Culture 
-- Artisanat
-- Musique

-- Cinéma
  (28, 'Film', 'film', 5, 2, 0, 0, 0, 0, 1, 1),
  (29, 'Série', 'serie', 5, 2, 0, 0, 0, 0, 1, 1),
  (30, "Film d'animation", 'film-d-animation', 5, 2, 1, 0, 0, 0, 1, 1),
  (31, "Documentaire", 'documentaire', 5, 2, 1, 0, 0, 0, 1, 1),

-- Littérature
  (32, 'Ecriture', 'ecriture', 8, 1, 1, 0, 0, 0, 1, 1),
  (33, 'Poésie', 'poesie', 8, 1, 1, 0, 0, 0, 1, 1),

-- Spectacle
  (34, 'Ballet', 'ballet', 9, 1, 1, 1, 0, 0, 1, 1),
  (35, 'Cabaret', 'cabaret', 9, 1, 1, 1, 0, 0, 1, 1),
  (36, 'Cirque', 'cirque', 9, 1, 1, 1, 0, 0, 1, 1),
  (37, 'Illusion', 'spectacle-illusion', 9, 1, 1, 0, 0, 0, 1, 1),
  (38, 'Comédie', 'spectacle-comedie', 9, 1, 1, 0, 0, 0, 1, 1),
  (39, 'Hypnose', 'spectacle-hypnose', 9, 1, 1, 0, 0, 0, 1, 1),
  (40, 'Marionnettes, contes, mimes', 'marionnettes-contes-mimes', 9, 1, 1, 0, 0, 0, 1, 1),
  (41, 'Magie', 'spectacle-magie', 9, 1, 1, 0, 0, 0, 1, 1),
  (42, 'Stand up & One man show', 'stand-up-et-one-man-show', 9, 1, 1, 0, 0, 0, 1, 1),

-- Théâtre
  (43, 'Opéra', 'opera', 10, 1, 1, 1, 0, 0, 1, 1),
  (44, 'Théâtre Poésie', 'theatre-poesie', 10, 1, 1, 0, 0, 0, 1, 1),
  (45, 'Improvisation', 'improvisation', 10, 1, 1, 0, 0, 0, 1, 1),

-- Science
  (46, 'Physique', 'physique', 11, NULL, 1, 0, 0, 0, 1, 0),
  (47, 'Mathématiques', 'mathematique', 11, NULL, 1, 0, 0, 0, 1, 0),
  (48, 'Chimie', 'chimie', 11, NULL, 1, 0, 0, 0, 1, 0),
  (49, 'Astronomie', 'astronomie', 11, NULL, 1, 0, 0, 0, 1, 0),
  (50, 'Informatique & IA', 'informatique-et-ia', 11, NULL, 1, 0, 0, 0, 1, 0),
  (51, 'Robotique', 'robotique', 11, NULL, 1, 0, 0, 0, 1, 0),
  (52, 'Biologie', 'biologie', 11, NULL, 1, 0, 0, 0, 1, 0),
  (53, 'Géologie', 'geologie', 11, NULL, 1, 0, 0, 0, 1, 0),
  (54, 'Géographie', 'geographie', 11, NULL, 1, 0, 0, 0, 1, 0),
  (55, 'Histoire', 'histoire', 11, NULL, 1, 0, 0, 0, 1, 0),
  (56, '--', '----s', 11, NULL, 1, 0, 0, 0, 1, 0),
  (57, 'Autre sciences', 'autres-sciences', 11, NULL, 1, 0, 0, 0, 1, 0),
-- Moode 

-- Bien-être
  (59, 'Yoga', 'yoga', 13, 6, 1, 0, 0, 0, 1, 1),
  (60, 'Pilate', 'pilate', 13, 6, 1, 0, 0, 0, 1, 1),
  (61, 'Méditation', 'meditation', 13, 6,1, 0, 0, 0, 1, 1),
  (62, 'Hypnose', 'hypnose-bien-etre', 13, 6,1, 0, 0, 0, 1, 1),
-- Jeux
  (63, 'Jeux vidéos', 'jeux-videos', 14, 18, 1, 1, 0, 0, 1, 1),
  (64, 'Jeux de société', 'jeux-de-societe', 14, 18, 1, 1, 0, 0, 1, 1),
  (65, 'Jeux de plateaux', 'jeux-de-plateaux', 14, 18, 1, 1, 0, 0, 1, 1),
  (66, 'VR', 'vr', 14, 18, 1, 1, 0, 0, 1, 1),
  (67, 'Quizz', 'quizz', 14, 18, 1, 1, 0, 0, 1, 1),
  (68, 'Jeux en plein air', 'jeux-en-plein-air', 14, 18, 1, 1, 0, 0, 1, 1),

-- Hygiène & beauté 
  (69, 'Cosmétique', 'cosmetique', 15, 13, 1, 1, 0, 0, 1, 1),
  (70, 'Parfum', 'parfum', 15, 13, 1, 1, 0, 0, 1, 1),
  (71, 'Coiffure', 'coiffure', 15, 13, 1, 1, 0, 0, 1, 1),
  (72, 'Maquillage', 'maquillage', 15, 13, 1, 1, 0, 0, 1, 1),
 
-- A manger
  (73, 'Cuisine', 'cuisine', 16, 2, 1, 1, 1, 1, 1, 1),
  (74, 'Pâtisserie', 'patisserie', 16, 2, 1, 1, 1, 1, 1, 1),
  (75, 'Boulangerie', 'boulangerie', 16, 2, 1, 1, 1, 1, 1, 1),
  (76, 'Viennoiserie', 'viennoiserie', 16, 2, 1, 1, 1, 1, 1, 1),
  (77, 'Chocolaterie', 'chocolaterie', 16, 2, 1, 1, 1, 1, 1, 1),
  (78, 'Confiserie', 'confiserie', 16, 2, 1, 1, 1, 1, 1, 1),
  (79, 'Fromagerie', 'fromagerie', 16, 2, 1, 1, 1, 1, 1, 1),
  (80, 'Crèmerie', 'cremerie', 16, 2, 1, 1, 1, 1, 1, 1),
  (81, 'Glace', 'glace', 16, 2, 1, 1, 1, 1, 1, 1),
  (82, 'Boucherie', 'boucherie', 16, 2, 1, 1, 1, 1, 1, 1),
  (83, 'Charcuterie', 'charcuteire', 16, 2, 1, 1, 1, 1, 1, 1),
  (84, 'Possonnerie', 'poissonnerie', 16, 2, 1, 1, 1, 1, 1, 1),

-- Boissons
  (85, 'Café', 'cafe', 17, 2, 1, 1, 1, 1, 1, 1),
  (86, 'Thé', 'the', 17, 2, 1, 1, 1, 1, 1, 1),
  (87, 'Sans alcool', 'sans-alcool', 17, 2, 1, 1, 1, 1, 1, 1),
  (88, 'Cocktail', 'cocktail', 17, 2, 1, 1, 1, 1, 1, 1),
  (89, 'Bière', 'biere', 17, 2, 1, 1, 1, 1, 1, 1),
  (90, 'Vin', 'vin', 17, 2, 0, 1, 1, 1, 1, 1),
  (91, 'Champagne', 'champagne', 17, 2, 1, 1, 1, 1, 1, 1),
  (92, 'Boissons fermentées', 'boissons-fermentees', 17, 2, 1, 1, 1, 1, 1, 1),
  (93, 'Autres alcools', 'autres-alcools', 17, 2, 1, 1, 1, 1, 1, 1),

--  Loisirs
  (94, 'Bowling', 'bowling', 18, 6, 1, 0, 0, 0, 0, 1),
  (95, 'karting', 'karting', 18, 6, 1, 0, 0, 0, 0, 1),
  (96, "Laser game", 'laser-game', 18, 6, 1, 0, 0, 0, 0, 1),
  (97, "Paintball", 'paintball', 18, 6, 1, 0, 0, 0, 0, 1),
  (98, "Airsoft", 'airsoft', 18, 6, 1, 0, 0, 0, 0, 1),
  (99, "Mini golf", 'mini-golf', 18, 6, 1, 0, 0, 0, 0, 1),

  (100, 'Lancer de hache', 'lancer-de-hache', 18, NULL, 1, 0, 0, 0, 0, 1),
  (101, 'Skateboard', 'skateboard', 18, NULL, 1, 0, 0, 0, 0, 1),
  (102, 'Accrobranche', 'accrobranche', 18, NULL, 1, 0, 0, 0, 0, 1),
  (103, 'Archery Tag', 'archery-tag', 18, NULL, 1, 0, 0, 0, 0, 1),
  (105, 'Escalade', 'escalade', 18, 6, 1, 0, 0, 0, 0, 1),
  (106, 'Escape Game', 'escape-game', 18, NULL, 1, 0, 0, 0, 0, 1),
  (107, 'Action Game', 'action-game', 18, NULL, 1, 0, 0, 0, 0, 1),  

  (108, 'Vol en avion', 'vol-en-avion', 18, NULL, 1, 0, 0, 0, 0, 1),
  (109, 'Vol en montgolfière', 'vol-en-montgolfiere', 18, NULL, 1, 0, 0, 0, 0, 1),
  (110, 'Parapente', 'parapente', 18, NULL, 1, 0, 0, 0, 0, 1),
  (111, 'Saut en parachute', 'saut-en-parachute', 18, NULL, 1, 0, 0, 0, 0, 1),
  (112, 'Simulateur de chute libre', 'simulateur-de-chute-libre', 18, NULL, 1, 0, 0, 0, 0, 1),
  (113, 'Hélicoptère', 'helicoptere', 18, NULL, 1, 0, 0, 0, 0, 1),
  (114, 'Simulateur d\'avion', 'simulateur-avion', 18, NULL, 1, 0, 0, 0, 0, 1),
  (115, 'ULM', 'ulm', 18, 6, 1, 0, 0, 0, 0, 1),
  (116, 'Pilotage de drône', 'pilotage-de-drone', 18, NULL, 1, 0, 0, 0, 0, 1),
  (117, 'Vol en planeur', 'vol-en-planeur', 18, NULL, 1, 0, 0, 0, 0, 1),
  (118, 'Paramoteur', 'paramoteur', 18, NULL, 1, 0, 0, 0, 0, 1),
  (119, 'Vol en deltaplane', 'vol-en-deltaplane', 18, NULL, 1, 0, 0, 0, 0, 1),
  (120, "Saut à l'élastique", 'saut-a-l-elastique', 18, NULL, 1, 0, 0, 0, 0, 1),

  (121, 'Bateau', 'bateau', 18, NULL, 1, 0, 0, 0, 0, 1),
  (122, 'Blob Jump', 'blob-jump', 18, NULL, 1, 0, 0, 0, 0, 1),
  (123, 'Bouées tractées', 'bouees-tractees', 18, NULL, 1, 0, 0, 0, 0, 1),
  (124, 'Canoë Kayak', 'canoe-kayak', 18, 6, 1, 0, 0, 0, 0, 1),
  (125, 'Canyoning', 'canyoning', 18, 6, 1, 0, 0, 0, 0, 1),
  (126, 'Char à voile', 'char-a-voile', 18, NULL, 1, 0, 0, 0, 0, 1),
  (127, 'Flyboard', 'flyboard', 18, NULL, 1, 0, 0, 0, 0, 1),
  (128, 'Hydrospeed', 'hydrospeed', 18, NULL, 1, 0, 0, 0, 0, 1),
  (129, 'Jet ski', 'jet-ski', 18, NULL, 1, 0, 0, 0, 0, 1),
  (130, 'Pêche', 'peche', 18, NULL, 1, 0, 0, 0, 0, 1),
  (131, 'Rafting', 'rafting', 18, NULL, 1, 0, 0, 0, 0, 1),
  (132, 'Ski nautique & Wakeboard', 'ski-nautique-et-wakeboard', 18, NULL, 1, 0, 0, 0, 0, 1),
  (133, 'Stand Up Paddle', 'stand-up-paddle', 18, 6, 1, 0, 0, 0, 0, 1),
  (134, 'Surf', 'surf', 18, 6, 1, 0, 0, 0, 0, 1),

  (135, 'Auto', 'auto', 18, NULL, 1, 0, 0, 0, 0, 1),
  (136, '4x4', '4x4', 18, NULL, 1, 0, 0, 0, 0, 1),
  (137, 'Moto', 'moto', 18, NULL, 1, 0, 0, 0, 0, 1),
  (138, 'Quad & Buggy', 'quad-et-buggy', 18, NULL, 1, 0, 0, 0, 0, 1),
  (139, 'Formule 1', 'formule-1', 18, NULL, 1, 0, 0, 0, 0, 1),
  (140, 'Rallye-terre', 'rallye-terre', 18, NULL, 1, 0, 0, 0, 0, 1),
  (141, 'Rallye-glace', 'rallye-glace', 18, NULL, 1, 0, 0, 0, 0, 1),
  (142, 'Simulateur de voiture de course', 'simulateur-de-voiture-de-course', 18, NULL, 1, 0, 0, 0, 0, 1),

  (144, 'Motoneige', 'motoneige', 18, NULL, 1, 0, 0, 0, 0, 1),
  (145, 'Snowkite', 'snowkite', 18, NULL, 1, 0, 0, 0, 0, 1),
  (146, 'Chien de traîneaux', 'chien-de-traineaux', 18, NULL, 1, 0, 0, 0, 0, 1),
  (147, 'Raquette à neige', 'raquette-a-neige', 18, NULL, 1, 0, 0, 0, 0, 1),
  (148, 'Ski freeride', 'ski-freeride', 18, NULL, 1, 0, 0, 0, 0, 1),

-- Fêtes 
-- Professions
  (149, 'Restauration', 'restauration', 20, NULL, 0, 0, 0, 0, 0, 1),
  (150, 'Hôtellerie', 'hotellerie', 20, NULL, 1, 0, 0, 0, 0, 1),
  (151, 'Entrepreneurs', 'entrepreneurs', 20, NULL, 1, 0, 0, 0, 0, 1),
  (152, 'Agriculture & Elevage', 'agriculture-et-elevage', 20, NULL, 1, 0, 0, 0, 0, 1),
  (153, 'Assurance', 'assurance', 20, NULL, 1, 0, 0, 0, 0, 1),
  (154, 'Commerce', 'commerce', 20, NULL, 1, 0, 0, 0, 0, 1);

INSERT INTO `ActivityPrincipalCategory` (id, `name`, `string_id`, usable, use_for_course, use_for_visit, use_for_tasting, use_for_visit_and_tasting, use_for_profesional_category, 
  use_for_festival) values 
-- Catégories principales 
  (156, 'Maison', 'maison', 1, 1, 1, 0, 0, 1, 1),
  (157, 'Jardinage', 'jardinage', 1, 1, 1, 0, 0, 1, 1),
  (158, 'Event Business', 'event-business', 1, 0, 0, 0, 0, 0, 0)
;

INSERT INTO `ActivityPrincipalCategory` (id, `name`, `string_id`, parent_id, second_parent_id, use_for_course, use_for_visit, use_for_tasting, use_for_visit_and_tasting, use_for_profesional_category, 
  use_for_festival) values 
(159, 'Bubble foot', 'bubble-foot', 18, 6, 1, 0, 0, 0, 0, 1),

-- Bien-être
  (160, 'Massage', 'massage', 13, 6, 1, 0, 0, 0, 1, 1),
  (161, 'Gommage', 'gommage', 13, 6, 1, 0, 0, 0, 1, 1),
  (162, 'Cryothérapie', 'cryotherapie', 13, 6,1, 0, 0, 0, 1, 1),
  (163, 'Sauna', 'sauna', 13, 6,1, 0, 0, 0, 1, 1),

  (164, 'Hammam', 'hammam', 13, 6, 1, 0, 0, 0, 1, 1),
  (165, 'Flotaison', 'flotaison', 13, 6, 1, 0, 0, 0, 1, 1)
;


-- Groupe de rôle
    CREATE TABLE GroupMemberRole (
        id TINYINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,

        string_id VARCHAR(64) UNIQUE NOT NULL,     -- "owner", "admin", "moderator", "member"
        name VARCHAR(128) NOT NULL
    );

    -- Rôle
    INSERT INTO GroupMemberRole (string_id, name) VALUES
        ('owner','Owner'),
        ('administrateur','Administrateur'),
        ('moderateur','Modérateur'),
        ('membre','Membre');


    -- Communauté Izilife - A l'image de WhatsApp - Sauf qu'on pourra gérer par ville, par area (donc pays)
    CREATE TABLE Community (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        unique_id VARCHAR(32) NOT NULL UNIQUE,

        parent_community_id BIGINT UNSIGNED DEFAULT NULL,

        name VARCHAR(255) NOT NULL,
        string_id VARCHAR(255) UNIQUE NOT NULL,

        description TINYTEXT DEFAULT NULL,
        picture_id BIGINT UNSIGNED DEFAULT NULL,

        owner_user_id BIGINT DEFAULT NULL,
        owner_page_id BIGINT DEFAULT NULL,

        scope_level ENUM('global','country','area','city') NOT NULL DEFAULT 'global',
        scope_id BIGINT UNSIGNED DEFAULT NULL,

        community_kind ENUM('brand','local','sport','interest','partner','official') NOT NULL DEFAULT 'local',

        is_public BOOLEAN NOT NULL DEFAULT TRUE,
        join_policy ENUM('open','request','invite_only') NOT NULL DEFAULT 'open',

        status TINYINT UNSIGNED DEFAULT 1,
        creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,

        INDEX idx_community_parent (parent_community_id),
        INDEX idx_community_scope (scope_level, scope_id),
        INDEX idx_community_kind (community_kind),

        FOREIGN KEY (parent_community_id) REFERENCES Community(id),
        FOREIGN KEY (owner_user_id) REFERENCES User(id),
        FOREIGN KEY (owner_page_id) REFERENCES Page(id),
        FOREIGN KEY (picture_id) REFERENCES Media(id)
    );

    CREATE TABLE CommunityMember (
        community_id BIGINT UNSIGNED NOT NULL,
        user_id BIGINT NOT NULL,

        role_id TINYINT UNSIGNED DEFAULT 4,

        is_muted BOOLEAN DEFAULT FALSE,
        is_banned BOOLEAN DEFAULT FALSE,

        invited_by_user_id BIGINT DEFAULT NULL,
        approved_by_user_id BIGINT DEFAULT NULL,

        join_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        join_demand_status TINYINT UNSIGNED NOT NULL DEFAULT 1,

        UNIQUE KEY uq_comm_user (community_id, user_id),

        FOREIGN KEY (community_id) REFERENCES Community(id),
        FOREIGN KEY (user_id) REFERENCES User(id),
        FOREIGN KEY (role_id) REFERENCES GroupMemberRole(id),
        FOREIGN KEY (join_demand_status) REFERENCES GroupJoinStatus(id)
    );

    -- Groupes internes à une communauté (option : un groupe peut aussi être indépendant => community_id NULL)
    CREATE TABLE UserGroup (
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        unique_id VARCHAR(32) NOT NULL UNIQUE,

        community_id BIGINT UNSIGNED DEFAULT NULL, -- IMPORTANT

        name VARCHAR(255) NOT NULL,
        string_id VARCHAR(255) UNIQUE NOT NULL,

        description TINYTEXT DEFAULT NULL,
        picture_id BIGINT DEFAULT NULL,

        owner_user_id BIGINT NOT NULL,
        owner_page_id BIGINT DEFAULT NULL,

        scope_level ENUM('global','country','area','city','place','shop') NOT NULL DEFAULT 'city',
        scope_id BIGINT UNSIGNED DEFAULT NULL,

        group_kind ENUM('chatless_feed','sport','outing','private','official') NOT NULL DEFAULT 'outing',

        join_policy ENUM('open','request','invite_only') NOT NULL DEFAULT 'request',
        event_creation_policy ENUM('admins_only','members','moderated') NOT NULL DEFAULT 'members',

        confidentiality TINYINT UNSIGNED DEFAULT 1,

        status TINYINT UNSIGNED DEFAULT 1,
        creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,

        INDEX idx_group_scope (scope_level, scope_id),
        INDEX idx_group_community (community_id),

        FOREIGN KEY (community_id) REFERENCES Community(id),
        FOREIGN KEY (owner_user_id) REFERENCES User(id),
        FOREIGN KEY (owner_page_id) REFERENCES Page(id)
    );

    CREATE TABLE UserGroupMember (
        group_id BIGINT UNSIGNED NOT NULL,
        user_id BIGINT NOT NULL,

        role_id TINYINT UNSIGNED DEFAULT 4, -- membre

        is_banned BOOLEAN DEFAULT FALSE,
        is_muted BOOLEAN NOT NULL DEFAULT 0,

        invited_by_user_id BIGINT DEFAULT NULL,
        approved_by_user_id BIGINT DEFAULT NULL,

        join_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        join_demand_status TINYINT UNSIGNED NOT NULL DEFAULT 1,

        UNIQUE KEY uq_group_user (group_id, user_id),

        FOREIGN KEY (group_id) REFERENCES UserGroup(id),
        FOREIGN KEY (user_id) REFERENCES User(id),
        FOREIGN KEY (role_id) REFERENCES GroupMemberRole(id)
    );

 CREATE TABLE `ShopCharactTag` (
    `charact_tag_id` int unsigned NOT NULL ,
    `shop_id` bigint NOT NULL,

    foreign key(charact_tag_id) references ShopAndPlaceCharactTag(id),
    foreign key(shop_id) references Shop(id)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

  CREATE TABLE `PlaceCharactTag` (
    `charact_tag_id` int unsigned NOT NULL,
    `place_id` bigint NOT NULL,

    foreign key(charact_tag_id) references ShopAndPlaceCharactTag(id),
    foreign key(place_id) references Place(id)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

  
CREATE TABLE `ShopCategory` (
  `id` smallint NOT NULL,
  `name` varchar(100) NOT NULL,
  `name_id` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,

  is_bookable_service_category boolean default 0,
  etablishment_type tinyint unsigned default NULL,
  second_etablishment_type tinyint unsigned default NULL,

  parent_id smallint default null,
  can_be_itinerant_category boolean default 0,

  is_privatizable boolean default 0,
  can_have_origin boolean default 0,

  is_service_prestation_category boolean default 0,
  receive_people boolean default 1,

  foreign key(etablishment_type) references EtablishmentType(id),
  foreign key(second_etablishment_type) references EtablishmentType(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `ShopCategory`
--

INSERT INTO `ShopCategory` (`id`, `name`, `name_id`, `is_active`, parent_id, is_bookable_service_category, etablishment_type, 
  second_etablishment_type, can_be_itinerant_category, is_privatizable, can_have_origin) VALUES
(1, 'Librairie', 'librairie', 1, NULL, 0, 20, NULL, 1, 1, 1),

(2, 'Restaurant', 'restaurant', 1, NULL, 1, 1, 2, 0, 1, 1),
(3, 'Boulangerie', 'boulangerie', 1, NULL, 0, 3, NULL, 1, 1, 1),
(4, 'Pâtisserie', 'patisserie', 1, NULL, 0, 3, NULL, 1, 1, 1),
(5, 'Salon de thé', 'salon-de-the', 1, NULL, 0, 3, NULL, 0, 1, 1),
(6, 'Café', 'cafe', 1, NULL, 0, 3, NULL, 1, 1, 1),

(7, 'Salle d\'escalade', 'salle-d-escalade', 1, NULL, 1, 4, NULL, 0, 1, 0),

(8, 'Chocolaterie', 'chocolaterie', 1, NULL, 0, 21, NULL, 1, 1, 0),

(9, 'Superette', 'superette', 1, NULL, 0, 10, NULL, 0, 0, 1),
(10, 'Supermarché', 'supermarche', 1, NULL, 0, 9, NULL, 0, 0, 1),
(11, 'Hypermarché', 'hypermarche', 1, NULL, 0, 9, NULL, 0, 0, 1),

(12, 'Bar', 'bar', 1, NULL, 0, 14, NULL, 1, 1, 1),
(13, 'Brasserie', 'brasserie', 1, 2, 0, 1, 14, 1, 1, 1),

(14, 'Friterie', 'friterie', 1, 2, 0, 2, NULL, 1, 0, 1),
(15, 'Marchand de glace', 'marchand-de-glace', 1, NULL, 0, 21, NULL, 1, 0, 1),
(16, 'Crêperie', 'creperie', 1, NULL, 0, 21, NULL, 1 , 1, 1),

(17, 'Bar à jus', 'bar-a-jus', 1, 12, 0, 14, NULL, 0, 1, 1),

(18, 'Discothèque', 'discotheque', 1, NULL, 0, 15, NULL, 0, 0, 1),

(19, 'Pub', 'pub', 1, 12, 0, 14, NULL, 0, 1, 1),
(20, 'Bar à coktails', 'bar-a-cocktails', 1, 12, 0, 14, NULL, 0, 1, 1),
(21, 'Karaoké', 'karaoke', 1, NULL, 1, 4, 4, 0, 1, 1),

(22, 'Salle de sport', 'salle-de-sport', 1, NULL, 0, 23, NULL, 0, 0, 0),

(23, 'Bar à chicha', 'bar-a-chicha', 1, 12, 0, 14, NULL, 0, 1, 1),
(24, 'Restaurant traditionnel', 'restaurant-traditionnel', 1, NULL, 1, 1, NULL, 0, 1, 1),

(25, 'Escape Game', 'escape-game', 1, NULL, 1, 4, NULL, 0, 1, 0),

(26, 'Steakhouse', 'steakhouse', 1, 2, 1, 1, NULL, 0, 1, 1),
(27, 'Bowling', 'bowling', 1, NULL, 1, 4, NULL, 0, 1, 0),
(28, 'Karting', 'karting', 1, NULL, 1, 4, NULL, 0, 1, 0),

(29, 'Barbier', 'barbier', 1, NULL, 1, 8, NULL, 1, 0, 1),
(30, 'Salon de coiffure', 'salon-de-coiffure', 1, NULL, 1, 8, NULL, 1, 0, 1),

(31, 'Boutique', 'boutique', 1, NULL, 0, 13, NULL, 1, 0, 1),

(32, 'Institut de beauté', 'institut-de-beaute', 1, NULL, 1, 8, NULL, 0, 1, 1),
(33, 'Spa', 'spa', 1, NULL, 1, 8, NULL, 0, 1, 1),
(34, 'Salon de tatouage', 'salon-de-tatouage', 1, NULL, 1, 8, NULL, 1, 0, 0),
(35, 'Institut esthétique', 'institut-esthetique', 1, NULL, 1, 8, NULL, 0, 1, 1),

(36, 'Artisan', 'artisan', 1, 12, 0, 16, NULL, 1, 0, 1),

(37, 'Bar à bière', 'bar-a-bieres', 1, 12, 0, 14, NULL, 1, 1, 1),
(38, 'Bar à jeux', 'bar-a-jeux', 1, 12, 0, 14, NULL, 1, 1, 1),
(39, 'Bar à vin', 'bar-a-vins', 1, 12, 0, 14, NULL, 1, 1, 1),
(40, 'Bar Tabac', 'bar-tabac', 1, 12, 0, 14, 3, 0, 1, 1),

(41, 'Pizzeria', 'pizzeria', 1, 2, 0, 2, NULL, 1, 1, 1),
(42, 'Restaurant rapide', 'restaurant-rapide', 1, 2, 0, 2, NULL, 1, 0, 1),
(43, 'Bistro', 'bistro', 1, 12, 0, 14, 3, 1, 1, 1),

(44, 'Boucherie', 'boucherie', 1, NULL, 0, 11, NULL, 1, 0, 1),
(45, 'Fromagerie', 'fromagerie', 1, NULL, 0, 11, NULL, 1, 0, 1),
(46, 'Poissonnerie', 'poissonnerie', 1, NULL, 0, 11, NULL, 1, 0, 0),

(47, 'Epicerie', 'epicerie', 1, NULL, 0, 10, NULL, 1, 0, 1),
(48, 'Epicerie fine', 'epicerie-fine', 1, 47, 0, 10, NULL, 1, 0, 1),
(49, 'Fleuriste', 'fleuriste', 1, NULL, 0, 40, NULL, 1, 0, 0),

(50, 'Caviste', 'caviste', 1, NULL, 0, 24, NULL, 1, 0, 1),

(51, 'Simulateur de chute libre', 'simulateurs-de-chute-libre', 1, NULL, 1, 4, NULL, 0, 1, 0),

(52, 'Boutique de souvenirs', 'boutique-de-souvenirs', 0, 31, 0, 13, NULL, 0, 0, 1),
(53, "Confiserie", 'confiserie', 1, NULL, 0, 21, NULL, 1, 0, 1),
(54, 'Pharmacie', 'pharmacie', 1, NULL, 0, 25, NULL, 0, 0, 0),
(55, 'Laser Game', 'laser-game', 1, NULL, 1, 4, NULL, 0, 1, 0),
(56, 'Réalité Virtuelle', 'realite-virtuelle', 1, NULL, 1, 4, NULL, 0, 1, 0),

(57, 'Paintball', 'paintball', 1, NULL, 1, 4, NULL, 0, 1, 0),
(58, 'Traiteur', 'traiteur', 1, NULL, 0, 41, 2, 0, 1, 1),

(59, 'Service de location', 'service-de-location', 1, NULL, 0, 46, NULL, 0, 0, 0), -- Spécial

(60, 'Mini-golf', 'mini-golf', 1, NULL, 1, 4, NULL, 0, 1, 0),

(61, 'Forain', 'forain', 1, NULL, 0, 4, 42, 1, 0, 0), -- Shop Itinéraire spécial
(62, 'Food Truck', 'food-truck', 1, NULL, 0, 2, 2, 1, 1, 1), -- itinéraire

(63, "Salle d'arcade", 'salle-d-arcade', 1, NULL, 0, 4, NULL, 0, 1, 0),

(64, 'Magasin de vêtements', 'magasin-de-vetements', 1, NULL, 0, 12, NULL, 0, 0, 1),
(65, 'Magasin de chaussures', 'magasin-de-chaussures', 1, NULL, 0, 12, NULL, 0, 0, 1),
(66, 'Magasin de décoration', 'magasin-de-decoration', 1, NULL, 0, 12, NULL, 0, 0, 1),
(67, 'Magasin de lingerie', 'magasin-de-lingerie', 1, NULL, 0, 12, NULL, 0, 0, 1),

(68, 'Bijouterie', 'bijouterie', 1, NULL, 0, 12, NULL, 0, 0, 1),

(69, 'Magasin de meubles', 'magasin-de-meubles', 1, NULL, 0, 12, NULL, 0, 0, 1),
(77, 'Magasin de jeux vidéos', 'magasin-de-jeux-videos', 1, NULL, 0, 12, NULL, 0, 0, 1),
(78, 'Magasin de jouets', 'magasin-de-jouets', 1, NULL, 0, 12, NULL, 0, 0, 1),
(79, 'Magasin de sports', 'magasin-articles-de-sport', 1, NULL, 0, 12, NULL, 0, 0, 1),

(80, 'Opticien', 'opticien', 1, NULL, 0, 43, NULL, 0, 0, 0),

(81, 'Parfumerie', 'parfumerie', 1, NULL, 0, 12, NULL, 0, 0, 0),

(82, 'Réparation de téléphones', 'reparation-telephones', 1, NULL, 0, 18, NULL, 0, 0, 0),

(83, 'FAI', 'fai', 1, NULL, 0, 46, NULL, 0, 0, 0),

(84, 'Night shop', 'night-shop', 1, NULL, 0, 10, NULL, 0, 0, 0),
(85, 'Magasin de cosmétiques', 'magasin-de-cosmetique', 1, NULL, 0, 12, NULL, 0, 0, 1),
(86, 'Autres magasins', 'autres-magasins', 1, NULL, 0, 12, NULL, 0, 0, 0),

(87, 'Para-pharmacie', 'para-pharmacie', 1, NULL, 0, 25, NULL, 0, 0, 0),

(88, 'Café-théâtre', 'cafe-theatre', 0, 12, 0, 26, 14, 0, 1, 0),

(89, 'Marchand de bières', 'marchand-de-bieres', 1, NULL, 0, 24, NULL, 1, 0, 1),
(90, 'Bar lounge', 'bar-lounge', 1, 12, 0, 14, NULL, 0, 1, 1),
(91, 'Primeur', 'primeur', 1, NULL, 0, 11, NULL, 1, 0, 1),
(92, 'Magasin de jardinage', 'magasn-de-jardinage', 1, NULL, 0, 12, NULL, 0, 0, 0),

(93, 'Bar à huitres', 'bar-a-huitres', 1, 12, 0, 14, NULL, 0, 1, 0),
(94, 'Magasin de bricolage', 'magasin-de-bricolage', 1, NULL, 0, 12, NULL, 0, 0, 0),
(95, 'Crèmerie', 'cremerie', 1, NULL, 0, 21, NULL, 0, 0, 1),

(96, 'Magasin de ferme', 'magasin-de-ferme', 1, NULL, 0, 22, NULL, 0, 0, 0),

(97, 'Maquis', 'maquis', 1, 12, 0, 14, NULL, 0, 1, 1),
(98, 'CBD shop', 'cbd-shop', 1, NULL, 0, 39, NULL, 0, 0, 0), 
(99, 'Boutique de e-cigarette', 'boutique-e-cigarette',1, NULL, 0, 39, NULL, 0, 0, 0),

(100, 'Restaurant Gastronomique', 'restaurant-gastronomique', 1, 2, 1, 1, NULL, 0, 1, 1),
(101, 'Kebab', 'kebab', 1, 2, 0, 2, NULL, 0, 0, 0),
(102, 'Tacos', 'tacos', 1, 2, 0, 2, NULL, 0, 0, 0),
(103, 'Bar karaoké', 'bar-karaoke', 1, 12, 0, 14, 3, 0, 1, 1),

(104, 'Sandwicherie', 'sandwicherie', 1, 2, 0, 2, NULL, 1, 0, 1),

(105, 'Restaurant végétarien', 'restaurant-vegetarien', 1, 2, 1, 1, NULL, 0, 1, 1),
(106, 'Restaurant végétalien', 'restaurant-vegetalien', 1, 2, 1, 1, NULL, 0, 1, 1),
(107, 'Hamburger', 'hamburger', 1, 2, 0, 2, 1, 1, 1, 1),

(108, 'Toilettes', 'toilettes', 1, NULL, 0, 21, NULL, 0, 0, 0),
(109, 'Restaurant routier', 'restaurant-routier', 1, 2, 0, 2, NULL, 0, 0, 1),

(110, 'Brocanteur', 'brocanteur', 1, NULL, 0, 42, NULL, 1, 0, 0),
(111, 'Antiquaire', 'antiquaire', 0, NULL, 1, 42, NULL, 1, 0, 0),

(112, 'Boutique de cadeaux', 'boutique-de-cadeaux', 1, 31, 0, 13, NULL, 0, 0, 1),

(113, 'cafétéria', 'cafeteria', 0, NULL, 0, 3, NULL, 0, 0, 1),

(114, 'Boucherie-Charcuterie', 'boucherie-charcuterie', 1, 44, 0, 11, NULL, 1, 0, 1),
(115, "Magasin d'électronique", 'magasin-d-electronique', 1, NULL, 0, 12, NULL, 0, 0, 0),

(117, "Station-service", 'station-service', 1, NULL, 0, 46, NULL, 0, 0, 0), -- Special

(118, "Pressing", 'pressing', 1, NULL, 0, 19, NULL, 0, 0, 0),
(119, 'Lavage auto', 'lavage-auto', 1, NULL, 0, 46, NULL, 0, 0, 0),

(120, 'Bar à fléchettes', 'bar-a-flechettes', 1, NULL, 0, 14, NULL, 0, 1, 1),
(121, 'Salle de billard', 'salle-de-billard', 1, NULL, 0, 14, NULL, 0, 1, 1), 

(122, 'Atelier d\'art', 'atelier-d-art', 1, 31, 0, 16, NULL, 0, 1, 1),
(123, 'Boutique d\'articles de mode', 'boutique-d-article-de-mode', 1, 31, 0, 13, NULL, 0, 0, 1),
(124, 'Boutique d\'artisan', 'boutique-d-artisan', 1, 31, 0, 13, NULL, 0, 0, 1),

(125, 'Boutique de vêtements', 'boutique-de-vetements', 1, 31, 0, 13, NULL, 0, 0, 1),
(126, 'Boutique de chaussures', 'boutique-de-chaussures', 1, 31, 0, 13, NULL, 0, 0, 1),
(127, 'Boutique de décoration', 'boutique-de-decoration', 1, 31, 0, 13, NULL, 0, 0, 1),

(128, 'Boutique de lingerie', 'boutique-de-lingerie', 1, 31, 0, 12, NULL, 0, 0, 0),

(129, 'Service de retouche', 'service-de-retouche', 1, 36, 0, 46, NULL, 0, 0, 0),
(130, 'Garage automobile', 'garage-automobile', 1, NULL, 0, 46, NULL, 0, 0, 0),
(131, 'Magasin de pièces auto', 'magasin-de-pieces-auto', 1, NULL, 0, 12, NULL, 0, 0, 0),
(132, 'Magasin de motos', 'magasin-de-motos', 1, NULL, 0, 12, NULL, 0, 0, 0),

(133, 'Magasin de vélos', 'magasin-de-velos', 1, NULL, 0, 16, NULL, 0, 0, 0),

(134, 'Service de réparation', 'service-de-reparation', 1, NULL, 0, 18, NULL, 0, 0, 0),
(135, 'Concessionnaire automobile', 'concessionnaire-automobile', 1, NULL, 0, 46, NULL, 0, 0, 0),

(136, 'Lancé de hâches', 'lancer-de-haches', 1, NULL, 1, 4, NULL, 0, 1, 0),
(137, 'Accrobranche', 'accrobranche', 1, NULL, 1, 4, NULL, 0, 1, 0),

(138, "Salle de jeux vidéos", 'salle-de-jeux-videos', 1, NULL, 0, 4, NULL, 0, 1, 0),
(139, "Salle de jeux", 'salle-de-jeux', 1, NULL, 0, 4, NULL, 0, 1, 0),
(140, "Ludothèque", 'ludotheque', 1, NULL, 0, 20, NULL, 0, 1, 0),
(141, "oeuvre de Street-art", 'oeuvre-de-street-art', 1, NULL, 0, 50, NULL, 0, 1, 0),
(142, "Boutique de cosmétique", 'boutique-de-cosmetique', 1, NULL, 0, 12, NULL, 0, 1, 0),
(143, "Boutique de produits d'hygiène", 'boutique-de-produits-dhygiene', 1, NULL, 0, 12, NULL, 0, 1, 0),
(144, "Magasin de mode", 'magasin-de-mode', 1, NULL, 0, 12, NULL, 0, 1, 0),
(145, "Boutique de mode", 'boutique-de-mode', 1, NULL, 0, 12, NULL, 0, 1, 0),

(146, 'Salle de crossfit', 'salle-de-crossfit', 1, NULL, 0, 23, NULL, 0, 0, 0),
(147, 'Magasin de musique', 'magasin-de-musique', 1, NULL, 0, 12, NULL, 0, 1, 0),

(148, 'Magasin de thé', 'magasin-de-the', 1, NULL, 0, 3, NULL, 1, 1, 1),
(149, 'Café à chiens', 'cafe-a-chiens', 1, NULL, 0, 3, NULL, 1, 1, 1),
(150, 'Cookies', 'cookies', 1, NULL, 0, 3, NULL, 1, 1, 1),

(151, 'Esthéticien', 'estheticien', 1, 36, 0, 16, NULL, 1, 0, 1),
(152, 'Salon de manucure', 'salon-de-manucure', 1, NULL, 1, 8, NULL, 1, 0, 1),
(153, 'Centre d\'épilation', 'centre-d-epilation', 1, NULL, 1, 8, NULL, 1, 0, 1),
(154, 'Institut de massage', 'institut-de-massage', 1, NULL, 1, 8, NULL, 1, 0, 1),
(155, 'Institut de bronzage', 'institut-de-bronzage', 1, NULL, 1, 8, NULL, 1, 0, 1),

(156, 'Coiffeur à domicile', 'coiffeur-a-domicile', 1, 36, 0, 16, NULL, 1, 0, 1),
(157, 'Hammam', 'hammam', 1, NULL, 1, 8, NULL, 0, 1, 1),

(158, 'Magasin bio', 'magasin-bio', 1, NULL, 0, 10, NULL, 0, 0, 1),
(159, 'Café à chats', 'cafe-a-chats', 1, NULL, 0, 3, NULL, 1, 1, 1),

(160, 'Salle de fitness', 'salle-de-fitness', 1, NULL, 0, 23, NULL, 0, 0, 0),
(161, 'Centre de fitness', 'centre-de-fitness', 1, NULL, 0, 23, NULL, 0, 0, 0),
(162, 'Salle de boxe', 'salle-de-boxe', 1, NULL, 0, 23, NULL, 0, 0, 0),
(163, 'Salle de boxe thaïlandaise', 'salle-de-boxe-thailandaise', 1, NULL, 0, 23, NULL, 0, 0, 0),

(164, "Magasin d'articles d'airsoft", 'magasin-articles-d-airsoft', 1, NULL, 0, 12, NULL, 0, 0, 1),
(165, "Magasin de matériel artistique", 'magasin-de-materiel-artistique', 1, NULL, 0, 12, NULL, 0, 0, 1),


(166, "Magasin de sous-vêtements", 'magasin-de-sous-vetements', 1, NULL, 0, 12, NULL, 0, 0, 1),
(167, "Magasin pour enfants", 'magasin-pour-enfants', 1, NULL, 0, 12, NULL, 0, 0, 1),
(168, "Magasin de meubles & Décoration", 'magasin-de-meubles-et-decoration', 1, NULL, 0, 12, NULL, 0, 0, 1),
(169, "Mercerie", 'mercerie', 1, NULL, 0, 12, NULL, 0, 0, 1),

(170, "Magasin de maroquinerie", 'magasin-de-maroquinerie', 1, NULL, 0, 12, NULL, 0, 0, 1),
(171, "Boutique érotique", 'boutique-erotique', 1, NULL, 0, 12, NULL, 0, 0, 1),
(172, 'Magasin de jeux', 'magasin-de-jeux', 1, NULL, 0, 12, NULL, 0, 0, 1),

(173, 'Chapellerie', 'chapellerie', 1, NULL, 0, 12, NULL, 0, 0, 1),
(174, 'Horlogerie', 'horlogerie', 1, NULL, 0, 12, NULL, 0, 0, 1),
(175, "Magasin de matériel de cuisine", 'magasin-de-materiel-de-cuisine', 1, NULL, 0, 12, NULL, 0, 0, 1),
(176, "Magasin de narguilé", 'magasin-de-narguile', 1, NULL, 0, 12, NULL, 0, 0, 1),

(177, 'Librairie de BD', 'librairie-de-bd', 1, 1, 0, 20, NULL, 1, 1, 1),
(178, "Boutique de saris", 'boutique-de-saris', 1, NULL, 0, 12, NULL, 0, 0, 1),
(179, 'Vêtements pour femmes', 'vetements-pour-femmes', 1, 64, 0, 12, NULL, 0, 0, 1),

(180, 'Magasin de vêtements pour enfants', 'magasin-de-vetements-pour-enfants', 1, 64, 0, 12, NULL, 0, 0, 1),
(181, 'Magasin de vêtements pour hommes', 'magasin-de-vetements-pour-hommes', 1, 64, 0, 12, NULL, 0, 0, 1),
(182, 'Magasin de vêtements pour bébés', 'magasin-de-vetements-pour-bebes', 1, 64, 0, 12, NULL, 0, 0, 1),
(183, "Magasin de puériculture", 'magasin-de-puericulture', 1, NULL, 0, 12, NULL, 0, 0, 1),

(184, 'Bijoutier', 'bijoutier', 1, 36, 0, 16, NULL, 0, 0, 1),
(185, 'Joaillier', 'Joaillier', 1, NULL, 0, 16, NULL, 0, 0, 1),
(186, "Marchand d'or", 'marchand-d-or', 1, NULL, 0, 12, NULL, 0, 0, 1),
(187, 'Rachat de bijoux', 'rachat-de-bijoux', 1, NULL, 0, 12, NULL, 0, 0, 1),
(188, 'Bijouterie fantaisie', 'bijouterie-fantaisie', 1, NULL, 0, 12, NULL, 0, 0, 1), 

(189, 'Boutique de loisirs créatifs', 'boutique-de-loisirs-creatifs', 1, NULL, 0, 12, NULL, 0, 0, 1),
(190, 'Magasin de photo', 'magasin-de-photo', 1, NULL, 0, 12, NULL, 0, 0, 1),

(191, 'Magasin de matériel DJ', 'magasin-de-materiel-pour-dj', 1, NULL, 0, 12, NULL, 0, 0, 1),
(192, 'Magasin de matériel Son', 'magasin-de-materiel-pour-son', 1, NULL, 0, 12, NULL, 0, 0, 1),
(193, 'Magasin de gros', 'magasin-de-gros', 1, NULL, 0, 12, NULL, 0, 0, 1),

(194, "Magasin d'antiquités", 'magasin-d-antiquites', 1, NULL, 0, 12, NULL, 0, 0, 1),
(195, "Magasin de literie", 'magasin-de-literie', 1, NULL, 0, 12, NULL, 0, 0, 1),
(196, "Magasin de rideaux et stores", 'magasin-de-rideaux-et-stores', 1, NULL, 0, 12, NULL, 0, 0, 1),
(197, "Magasin de linge de maison", 'magasin-de-linge-de-maison', 1, NULL, 0, 12, NULL, 0, 0, 1),

(198, "Magasin de vêtements vintage", 'magasin-de-vetements-vintage', 1, NULL, 0, 12, NULL, 0, 0, 1),
(199, "Magasin d'articles d'occasion", 'magasin-d-articles-d-occasion', 1, NULL, 0, 12, NULL, 0, 0, 1),
(200, "Boutique de tenues de soirée", 'boutique-de-tenues-de-soiree', 1, NULL, 0, 12, NULL, 0, 0, 1),
(201, "Friperie", 'friperie', 1, NULL, 0, 12, NULL, 0, 0, 1),
(202, "Magasin de canapé", 'magasin-de-canape', 1, NULL, 0, 12, NULL, 0, 0, 1),
(203, "Boutique d'accessoires de mode", 'boutique-d-accessoires-de-mode', 1, NULL, 0, 12, NULL, 0, 0, 1),
(204, 'Atelier de couture', 'atelier-de-couture', 1, 36, 0, 16, NULL, 0, 0, 1),
(205, "Boutique de t-shirts personnalisés", 'boutique-de-t-shirts-personnalises', 1, NULL, 0, 12, NULL, 0, 0, 1),

(206, "Cuisiniste", 'cuisiniste', 1, NULL, 0, 12, NULL, 0, 0, 1),
(207, "Boutique de mariage", 'boutique-de-mariage', 1, NULL, 0, 12, NULL, 0, 0, 1),
(208, "Magasin d'articles pour animaux", "magasin-d-articles-pour-animaux", 1, NULL, 0, 12, NULL, 0, 0, 1),
(209, 'Galerie d\'art', 'galerie-d-art', 1, 31, 0, 16, NULL, 0, 1, 1),

(210, 'Sauna', 'sauna', 1, NULL, 1, 8, NULL, 0, 1, 1),
(211, 'Bar sportif', 'bar-sportif', 1, NULL, 1, 8, NULL, 0, 1, 1),
(212, 'Restaurant à buffet', 'restaurant-a-buffet', 1, 2, 1, 1, NULL, 0, 1, 1),

(213, "Magasins de boissons alcoolisées", 'magasin-de-boissons-alcoolisees', 1, NULL, 0, 12, NULL, 0, 0, 1),

(214, 'Restaurant à fondue', 'restaurant-a-fondue', 1, 2, 1, 1, 2, 0, 1, 1),
(215, 'Restaurant à raclette', 'restaurant-a-raclette', 1, 2, 1, 1, 2, 0, 1, 1),
(216, 'Restaurant afghan', 'restaurant-afghan', 1, 2, 1, 1, 2, 0, 1, 1),
(217, 'Restaurant africain', 'restaurant-africain', 1, 2, 1, 1, 2, 0, 1, 1),
(218, 'Restaurant allemand', 'restaurant-allemand', 1, 2, 1, 1, 2, 0, 1, 1),
(219, 'Restaurant Alsace', 'restaurant-alsace', 1, 2, 1, 1, 2, 0, 1, 1),
(220, 'Restaurant américain', 'restaurant-americain', 1, 2, 1, 1, 2, 0, 1, 1),
(221, 'Restaurant américain traditionnel', 'restaurant-americain-traditionnel', 1, 2, 1, 1, 2, 0, 1, 1),
(222, 'Restaurant amérindien', 'restaurant-amerindien', 1, 2, 1, 1, 2, 0, 1, 1),
(223, 'Restaurant An Hui', 'restaurant-an-hui', 1, 2, 1, 1, 2, 0, 1, 1),
(224, 'Restaurant Anago', 'restaurant-anago', 1, 2, 1, 1, 2, 0, 1, 1),
(225, 'Restaurant andalou', 'restaurant-andalou', 1, 2, 1, 1, 2, 0, 1, 1),
(226, 'Restaurant anglais', 'restaurant-anglais', 1, 2, 1, 1, 2, 0, 1, 1),
(227, 'Restaurant argentin', 'restaurant-argentin', 1, 2, 1, 1, 2, 0, 1, 1),
(228, 'Restaurant arménien', 'restaurant-armenien', 1, 2, 1, 1, 2, 0, 1, 1),
(229, 'Restaurant asiatique', 'restaurant-asiatique', 1, 2, 1, 1, 2, 0, 1, 1),
(230, 'Restaurant asiatique du sud-est', 'restaurant-asiatique-du-sud-est', 1, 2, 1, 1, 2, 0, 1, 1),
(231, 'Restaurant asturien', 'restaurant-asturien', 1, 2, 1, 1, 2, 0, 1, 1),
(232, 'Restaurant australien', 'restaurant-australien', 1, 2, 1, 1, 2, 0, 1, 1),
(233, 'Restaurant autrichien', 'restaurant-autrichien', 1, 2, 1, 1, 2, 0, 1, 1),
(234, 'Restaurant bangladais', 'restaurant-bangladais', 1, 2, 1, 1, 2, 0, 1, 1),
(235, 'Restaurant Bar à Huîtres', 'restaurant-bar-a-huîtres', 1, 2, 1, 1, 2, 0, 1, 1),
(236, 'Restaurant barbecue', 'restaurant-barbecue', 1, 2, 1, 1, 2, 0, 1, 1),
(237, 'Restaurant barbecue au mouton', 'restaurant-barbecue-au-mouton', 1, 2, 1, 1, 2, 0, 1, 1),
(238, 'Restaurant barbecue coréen', 'restaurant-barbecue-coreen', 1, 2, 1, 1, 2, 0, 1, 1),
(239, 'Restaurant barbecue d’abats', 'restaurant-barbecue-dabats', 1, 2, 1, 1, 2, 0, 1, 1),
(240, 'Restaurant barbecue mongol', 'restaurant-barbecue-mongol', 1, 2, 1, 1, 2, 0, 1, 1),
(241, 'Restaurant basque', 'restaurant-basque', 1, 2, 1, 1, 2, 0, 1, 1),
(242, 'Restaurant bateau à vapeur', 'restaurant-bateau-a-vapeur', 1, 2, 1, 1, 2, 0, 1, 1),
(243, 'Restaurant belge', 'restaurant-belge', 1, 2, 1, 1, 2, 0, 1, 1),
(244, 'Restaurant Berry', 'restaurant-berry', 1, 2, 1, 1, 2, 0, 1, 1),
(245, 'Restaurant bio', 'restaurant-bio', 1, 2, 1, 1, 2, 0, 1, 1),
(246, 'Restaurant birman', 'restaurant-birman', 1, 2, 1, 1, 2, 0, 1, 1),
(247, 'Restaurant brésilien', 'restaurant-bresilien', 1, 2, 1, 1, 2, 0, 1, 1),
(248, 'Restaurant britannique', 'restaurant-britannique', 1, 2, 1, 1, 2, 0, 1, 1),
(249, 'Restaurant britannique moderne', 'restaurant-britannique-moderne', 1, 2, 1, 1, 2, 0, 1, 1),
(250, 'Restaurant brunch', 'restaurant-brunch', 1, 2, 1, 1, 2, 0, 1, 1),
(251, 'Restaurant buffet', 'restaurant-buffet', 1, 2, 1, 1, 2, 0, 1, 1),
(252, 'Restaurant bulgare', 'restaurant-bulgare', 1, 2, 1, 1, 2, 0, 1, 1),
(253, 'Restaurant Burrito', 'restaurant-burrito', 1, 2, 1, 1, 2, 0, 1, 1),
(254, 'Restaurant cachemirien', 'restaurant-cachemirien', 1, 2, 1, 1, 2, 0, 1, 1),
(255, 'Restaurant cajun', 'restaurant-cajun', 1, 2, 1, 1, 2, 0, 1, 1),
(256, 'Restaurant californien', 'restaurant-californien', 1, 2, 1, 1, 2, 0, 1, 1),
(257, 'Restaurant cambodgien', 'restaurant-cambodgien', 1, 2, 1, 1, 2, 0, 1, 1),
(258, 'Restaurant canadien', 'restaurant-canadien', 1, 2, 1, 1, 2, 0, 1, 1),
(259, 'Restaurant cantabrique', 'restaurant-cantabrique', 1, 2, 1, 1, 2, 0, 1, 1),
(260, 'Restaurant cantonais', 'restaurant-cantonais', 1, 2, 1, 1, 2, 0, 1, 1),
(261, 'Restaurant cap-verdien', 'restaurant-cap-verdien', 1, 2, 1, 1, 2, 0, 1, 1),
(262, 'Restaurant casher', 'restaurant-casher', 1, 2, 1, 1, 2, 0, 1, 1),
(263, 'Restaurant castillan', 'restaurant-castillan', 1, 2, 1, 1, 2, 0, 1, 1),
(264, 'Restaurant catalan', 'restaurant-catalan', 1, 2, 1, 1, 2, 0, 1, 1),
(265, 'Restaurant Chanko', 'restaurant-chanko', 1, 2, 1, 1, 2, 0, 1, 1),
(266, 'Restaurant Cheesesteak', 'restaurant-cheesesteak', 1, 2, 1, 1, 2, 0, 1, 1),
(267, 'Restaurant Chesapeake', 'restaurant-chesapeake', 1, 2, 1, 1, 2, 0, 1, 1),
(268, 'Restaurant chilien', 'restaurant-chilien', 1, 2, 1, 1, 2, 0, 1, 1),
(269, 'Restaurant chinois', 'restaurant-chinois', 1, 2, 1, 1, 2, 0, 1, 1),
(270, 'Restaurant Chophouse', 'restaurant-chophouse', 1, 2, 1, 1, 2, 0, 1, 1),
(271, 'Restaurant colombien', 'restaurant-colombien', 1, 2, 1, 1, 2, 0, 1, 1),
(272, 'Restaurant continental', 'restaurant-continental', 1, 2, 1, 1, 2, 0, 1, 1),
(273, 'Restaurant coréen', 'restaurant-coreen', 1, 2, 1, 1, 2, 0, 1, 1),
(274, 'Restaurant coréen de boeuf', 'restaurant-coreen-de-boeuf', 1, 2, 1, 1, 2, 0, 1, 1),
(275, 'Restaurant costaricain', 'restaurant-costaricain', 1, 2, 1, 1, 2, 0, 1, 1),
(276, 'Restaurant Couscous', 'restaurant-couscous', 1, 2, 1, 1, 2, 0, 1, 1),
(277, 'Restaurant créole', 'restaurant-creole', 1, 2, 1, 1, 2, 0, 1, 1),
(278, 'Restaurant croate', 'restaurant-croate', 1, 2, 1, 1, 2, 0, 1, 1),
(279, 'Restaurant cubain', 'restaurant-cubain', 1, 2, 1, 1, 2, 0, 1, 1),
(280, 'Restaurant d’Afrique de l’Est', 'restaurant-dafrique-de-lest', 1, 2, 1, 1, 2, 0, 1, 1),
(281, 'Restaurant d’ailes de poulet', 'restaurant-dailes-de-poulet', 1, 2, 1, 1, 2, 0, 1, 1),
(282, 'Restaurant d’aliments crus', 'restaurant-daliments-crus', 1, 2, 1, 1, 2, 0, 1, 1),
(283, 'Restaurant d’Amérique centrale', 'restaurant-damerique-centrale', 1, 2, 1, 1, 2, 0, 1, 1),
(284, 'Restaurant d’Europe de l’Est', 'restaurant-deurope-de-lest', 1, 2, 1, 1, 2, 0, 1, 1),
(285, 'Restaurant danois', 'restaurant-danois', 1, 2, 1, 1, 2, 0, 1, 1),
(286, 'Restaurant de bonbons japonais', 'restaurant-de-bonbons-japonais', 1, 2, 1, 1, 2, 0, 1, 1),
(287, 'Restaurant de bouillie', 'restaurant-de-bouillie', 1, 2, 1, 1, 2, 0, 1, 1),
(288, 'Restaurant de boulettes', 'restaurant-de-boulettes', 1, 2, 1, 1, 2, 0, 1, 1),
(289, 'Restaurant de côtes coréennes', 'restaurant-de-côtes-coreennes', 1, 2, 1, 1, 2, 0, 1, 1),
(290, 'Restaurant de crêpes', 'restaurant-de-crêpes', 1, 2, 1, 1, 2, 0, 1, 1),
(291, 'Restaurant de cuisine à domicile', 'restaurant-de-cuisine-a-domicile', 1, 2, 1, 1, 2, 0, 1, 1),
(292, 'Restaurant de cuisine champêtre', 'restaurant-de-cuisine-champêtre', 1, 2, 1, 1, 2, 0, 1, 1),
(293, 'Restaurant de cuisine d’abats', 'restaurant-de-cuisine-dabats', 1, 2, 1, 1, 2, 0, 1, 1),
(294, 'Restaurant de cuisine Xiang', 'restaurant-de-cuisine-xiang', 1, 2, 1, 1, 2, 0, 1, 1),
(295, 'Restaurant de danse', 'restaurant-de-danse', 1, 2, 1, 1, 2, 0, 1, 1),
(296, 'Restaurant de desserts', 'restaurant-de-desserts', 1, 2, 1, 1, 2, 0, 1, 1),
(297, 'Restaurant de fruits de mer', 'restaurant-de-fruits-de-mer', 1, 2, 1, 1, 2, 0, 1, 1),
(298, 'Restaurant de grillades françaises', 'restaurant-de-grillades-françaises', 1, 2, 1, 1, 2, 0, 1, 1),
(299, 'Restaurant de hamburgers', 'restaurant-de-hamburgers', 1, 2, 1, 1, 2, 0, 1, 1),
(300, 'Restaurant de homard', 'restaurant-de-homard', 1, 2, 1, 1, 2, 0, 1, 1),
(301, 'Restaurant de hot-dogs', 'restaurant-de-hot-dogs', 1, 2, 1, 1, 2, 0, 1, 1),
(302, 'Restaurant de la Nouvelle-Angleterre', 'restaurant-de-la-nouvelle-angleterre', 1, 2, 1, 1, 2, 0, 1, 1),
(303, 'Restaurant de langue', 'restaurant-de-langue', 1, 2, 1, 1, 2, 0, 1, 1),
(304, 'Restaurant de nouilles Champon', 'restaurant-de-nouilles-champon', 1, 2, 1, 1, 2, 0, 1, 1),
(305, 'Restaurant de nouilles chinoises', 'restaurant-de-nouilles-chinoises', 1, 2, 1, 1, 2, 0, 1, 1),
(306, 'Restaurant de nouilles Dan Dan', 'restaurant-de-nouilles-dan-dan', 1, 2, 1, 1, 2, 0, 1, 1),
(307, 'Restaurant de nouilles froides', 'restaurant-de-nouilles-froides', 1, 2, 1, 1, 2, 0, 1, 1),
(308, 'Restaurant de nouilles Udon', 'restaurant-de-nouilles-udon', 1, 2, 1, 1, 2, 0, 1, 1),
(309, 'Restaurant de petites assiettes', 'restaurant-de-petites-assiettes', 1, 2, 1, 1, 2, 0, 1, 1),
(310, 'Restaurant de pizza', 'restaurant-de-pizza', 1, 2, 1, 1, 2, 0, 1, 1),
(311, 'Restaurant de plats de viande', 'restaurant-de-plats-de-viande', 1, 2, 1, 1, 2, 0, 1, 1),
(312, 'Restaurant de poisson pêcheur', 'restaurant-de-poisson-pêcheur', 1, 2, 1, 1, 2, 0, 1, 1),
(313, 'Restaurant de poulet', 'restaurant-de-poulet', 1, 2, 1, 1, 2, 0, 1, 1),
(314, 'Restaurant de restauration rapide de style hongkongais', 'restaurant-de-restauration-rapide-de-style-hongkongais', 1, 2, 1, 1, 2, 0, 1, 1),
(315, 'Restaurant de riz', 'restaurant-de-riz', 1, 2, 1, 1, 2, 0, 1, 1),
(316, 'Restaurant de soupe', 'restaurant-de-soupe', 1, 2, 1, 1, 2, 0, 1, 1),
(317, 'Restaurant de sushi', 'restaurant-de-sushi', 1, 2, 1, 1, 2, 0, 1, 1),
(318, 'Restaurant de sushis à tapis roulant', 'restaurant-de-sushis-a-tapis-roulant', 1, 2, 1, 1, 2, 0, 1, 1),
(319, 'Restaurant de tacos', 'restaurant-de-tacos', 1, 2, 1, 1, 2, 0, 1, 1),
(320, 'Restaurant de tapas', 'restaurant-de-tapas', 1, 2, 1, 1, 2, 0, 1, 1),
(321, 'Restaurant de tofu', 'restaurant-de-tofu', 1, 2, 1, 1, 2, 0, 1, 1),
(322, 'Restaurant déjeuner', 'restaurant-dejeuner', 1, 2, 1, 1, 2, 0, 1, 1),
(323, 'Restaurant des Caraïbes', 'restaurant-des-caraïbes', 1, 2, 1, 1, 2, 0, 1, 1),
(324, 'Restaurant des Seychelles', 'restaurant-des-seychelles', 1, 2, 1, 1, 2, 0, 1, 1),
(325, 'Restaurant diététique', 'restaurant-dietetique', 1, 2, 1, 1, 2, 0, 1, 1),
(326, 'Restaurant Dim Sum', 'restaurant-dim-sum', 1, 2, 1, 1, 2, 0, 1, 1),
(327, 'Restaurant Dojo', 'restaurant-dojo', 1, 2, 1, 1, 2, 0, 1, 1),
(328, 'Restaurant dominicain', 'restaurant-dominicain', 1, 2, 1, 1, 2, 0, 1, 1),
(329, 'Restaurant Donburi aux fruits de mer', 'restaurant-donburi-aux-fruits-de-mer', 1, 2, 1, 1, 2, 0, 1, 1),
(330, 'Restaurant du Hunan', 'restaurant-du-hunan', 1, 2, 1, 1, 2, 0, 1, 1),
(331, 'Restaurant du Moyen-Orient', 'restaurant-du-moyen-orient', 1, 2, 1, 1, 2, 0, 1, 1),
(332, 'Restaurant du nord-ouest du Pacifique (Canada)', 'restaurant-du-nord-ouest-du-pacifique-(canada)', 1, 2, 1, 1, 2, 0, 1, 1),
(333, 'Restaurant du Sichuan', 'restaurant-du-sichuan', 1, 2, 1, 1, 2, 0, 1, 1),
(334, 'Restaurant éclectique', 'restaurant-eclectique', 1, 2, 1, 1, 2, 0, 1, 1),
(335, 'Restaurant égyptien', 'restaurant-egyptien', 1, 2, 1, 1, 2, 0, 1, 1),
(336, 'Restaurant en libre-service', 'restaurant-en-libre-service', 1, 2, 1, 1, 2, 0, 1, 1),
(337, 'Restaurant équatorien', 'restaurant-equatorien', 1, 2, 1, 1, 2, 0, 1, 1),
(338, 'Restaurant érythréen', 'restaurant-erythreen', 1, 2, 1, 1, 2, 0, 1, 1),
(339, 'Restaurant espagnol', 'restaurant-espagnol', 1, 2, 1, 1, 2, 0, 1, 1),
(340, 'Restaurant éthiopien', 'restaurant-ethiopien', 1, 2, 1, 1, 2, 0, 1, 1),
(341, 'Restaurant ethnique', 'restaurant-ethnique', 1, 2, 1, 1, 2, 0, 1, 1),
(342, 'Restaurant européen', 'restaurant-europeen', 1, 2, 1, 1, 2, 0, 1, 1),
(343, 'Restaurant européen moderne', 'restaurant-europeen-moderne', 1, 2, 1, 1, 2, 0, 1, 1),
(344, 'Restaurant Falafel', 'restaurant-falafel', 1, 2, 1, 1, 2, 0, 1, 1),
(345, 'Restaurant familial', 'restaurant-familial', 1, 2, 1, 1, 2, 0, 1, 1),
(346, 'Restaurant finlandais', 'restaurant-finlandais', 1, 2, 1, 1, 2, 0, 1, 1),
(347, 'Restaurant Fish & Chips', 'restaurant-fish-&-chips', 1, 2, 1, 1, 2, 0, 1, 1),
(348, 'Restaurant floridien', 'restaurant-floridien', 1, 2, 1, 1, 2, 0, 1, 1),
(349, 'Restaurant français', 'restaurant-français', 1, 2, 1, 1, 2, 0, 1, 1),
(350, 'Restaurant français moderne', 'restaurant-français-moderne', 1, 2, 1, 1, 2, 0, 1, 1),
(351, 'Restaurant Fu Jian', 'restaurant-fu-jian', 1, 2, 1, 1, 2, 0, 1, 1),
(352, 'Restaurant Fugu', 'restaurant-fugu', 1, 2, 1, 1, 2, 0, 1, 1),
(353, 'Restaurant fusion', 'restaurant-fusion', 1, 2, 1, 1, 2, 0, 1, 1),
(354, 'Restaurant fusion asiatique', 'restaurant-fusion-asiatique', 1, 2, 1, 1, 2, 0, 1, 1),
(355, 'Restaurant galicien', 'restaurant-galicien', 1, 2, 1, 1, 2, 0, 1, 1),
(356, 'Restaurant gallois', 'restaurant-gallois', 1, 2, 1, 1, 2, 0, 1, 1),
(357, 'A changer', 'restaurant-gastronomique-a-changer', 0, 2, 1, 1, 2, 0, 1, 1),
(358, 'Restaurant géorgien', 'restaurant-georgien', 1, 2, 1, 1, 2, 0, 1, 1),
(359, 'Restaurant grec', 'restaurant-grec', 1, 2, 1, 1, 2, 0, 1, 1),
(360, 'Restaurant guatémaltèque', 'restaurant-guatemaltèque', 1, 2, 1, 1, 2, 0, 1, 1),
(361, 'Restaurant Gui Zhou', 'restaurant-gui-zhou', 1, 2, 1, 1, 2, 0, 1, 1),
(362, 'Restaurant Gyro', 'restaurant-gyro', 1, 2, 1, 1, 2, 0, 1, 1),
(363, 'Restaurant Gyudon', 'restaurant-gyudon', 1, 2, 1, 1, 2, 0, 1, 1),
(364, 'Restaurant haïtien', 'restaurant-haïtien', 1, 2, 1, 1, 2, 0, 1, 1),
(365, 'Restaurant Hakka', 'restaurant-hakka', 1, 2, 1, 1, 2, 0, 1, 1),
(366, 'Restaurant halal', 'restaurant-halal', 1, 2, 1, 1, 2, 0, 1, 1),
(367, 'Restaurant Haute Française', 'restaurant-haute-française', 1, 2, 1, 1, 2, 0, 1, 1),
(368, 'Restaurant hawaïen', 'restaurant-hawaïen', 1, 2, 1, 1, 2, 0, 1, 1),
(369, 'Restaurant Hoagie', 'restaurant-hoagie', 1, 2, 1, 1, 2, 0, 1, 1),
(370, 'Restaurant hondurien', 'restaurant-hondurien', 1, 2, 1, 1, 2, 0, 1, 1),
(371, 'Restaurant hongrois', 'restaurant-hongrois', 1, 2, 1, 1, 2, 0, 1, 1),
(372, 'Restaurant Hot Pot', 'restaurant-hot-pot', 1, 2, 1, 1, 2, 0, 1, 1),
(373, 'Restaurant indien', 'restaurant-indien', 1, 2, 1, 1, 2, 0, 1, 1),
(374, 'Restaurant indonésien', 'restaurant-indonesien', 1, 2, 1, 1, 2, 0, 1, 1),
(375, 'Restaurant irlandais', 'restaurant-irlandais', 1, 2, 1, 1, 2, 0, 1, 1),
(376, 'Restaurant islandais', 'restaurant-islandais', 1, 2, 1, 1, 2, 0, 1, 1),
(377, 'Restaurant israélien', 'restaurant-israelien', 1, 2, 1, 1, 2, 0, 1, 1),
(378, 'Restaurant italien', 'restaurant-italien', 1, 2, 1, 1, 2, 0, 1, 1),
(379, 'Restaurant italien du nord', 'restaurant-italien-du-nord', 1, 2, 1, 1, 2, 0, 1, 1),
(380, 'Restaurant italien du sud', 'restaurant-italien-du-sud', 1, 2, 1, 1, 2, 0, 1, 1),
(381, 'Restaurant Izakaya', 'restaurant-izakaya', 1, 2, 1, 1, 2, 0, 1, 1)


--  Allocodrome - Bar à salade - Bouillon - Brestaurant -  - Camion Bar - Cantine - Curry House - Diner - grotto - Kaitenzushi - Métairie - Pont-restaurant 
-- R panoramique - r tournant - R universitaire - underground - restoroute - Snack-bar - Taquería - Teppanyaki Thermopolium Trattoria
;

CREATE TABLE `PlaceType` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `place_type_string_id` varchar(100) NOT NULL,
  is_service_prestation_category boolean default 0,
  receive_people boolean default 1,

  is_road_entity_type boolean default 0, 
  is_transport_entity_type boolean default 0,
  is_water_entity_type boolean default 0,
  is_subdivision_entity_type boolean default 0,

  is_access_type_category boolean default 0,
  is_bookable_service_category boolean default 0, -- Si c'est une catégorie pour laquelle on réserve un service
  is_visitable_category boolean default 0, 

  with_hourly boolean default 1,

  necessarily_on_other_place boolean default 0,
  is_privatizable boolean default 0, 

  is_active boolean default 1,

  etablishment_type tinyint unsigned default NULL,
  foreign key(etablishment_type) references EtablishmentType(id)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `PlaceType`
--

INSERT INTO `PlaceType` (`id`, `name`, `place_type_string_id`, is_road_entity_type, is_transport_entity_type, is_water_entity_type, is_subdivision_entity_type, 
  is_access_type_category, is_bookable_service_category, etablishment_type, is_visitable_category, with_hourly, is_privatizable) VALUES

(1, 'Multi activités', 'place-multi-activites', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 1), -- Spécial
(2, 'Désignation géographique', 'designation-geographique', 0, 0, 0, 1, 0, 0, NULL, 0, 0, 0), -- Spécial
(3, 'Coworking', 'espace-de-coworking', 0, 0, 0, 0, 1, 1, 38, 0, 1, 1),
(4, 'Food court', 'food-court', 0, 0, 0, 0, 0, 0, 2, 0, 1, 1), -- Spécial
(5, 'Marché', 'marche', 0, 0, 0, 0, 0, 0, 37, 1, 1, 0), -- Spécial
(6, 'Cinéma ', 'cinema', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 1), -- Spécial

-- Place, Jardins & Autres espaces verts 
(7, 'Place', 'place', 0, 0, 0, 0, 0, 0, 27, 1, 0, 0),
(8, 'Parc', 'parc', 0, 0, 0, 0, 1, 1, 27, 1, 1, 0),
(9, 'Jardin', 'jardin', 0, 0, 0, 0, 1, 1, 27, 1, 1, 1),
(10, 'Square', 'square', 0, 0, 0, 0, 1, 0, 27, 1, 0, 0),
(11, 'Jardin botanique', 'jardin-botanique', 0, 0, 0, 0, 1, 1, 27, 1, 1, 0),

-- Transport
(12, 'Aéroport', 'aeroport', 0, 1, 0, 0, 0, 0, NULL, 0, 1, 0), -- Transport
(13, 'Gare', 'gare', 0, 1, 0, 0, 0, 0, 33, 0, 1, 0), -- Transport
(14, 'Station de métro', 'station-de-metro', 0, 1, 0, 0, 0, 0, 33, 0, 1, 0), -- Transport
(15, 'Gare routière', 'gare-routiere', 0, 1, 0, 0, 0, 0, 33, 0, 1, 0), -- Transport

(16, "Aire d'autoroute", 'aire-autoroute', 1, 0, 0, 0, 0, 0, NULL, 0, 0, 0),
(17, 'Aire de covoiturage', 'aire-de-covoiturage', 1, 0, 0, 0, 0, 0, NULL, 0, 0, 0),

(18, 'Rue', 'rue', 1, 0, 0, 0, 0, 0, NULL, 1, 0, 0), -- Rue (Spéciale)

-- Attractions Touristiques & Historiques 
(19, 'Musée', 'musee', 0, 0, 0, 0, 1, 1, 7, 1, 1, 1),
(20, 'Monument', 'monument', 0, 0, 0, 0, 1, 1, 7, 1, 1, 0),
(21, 'Site historique', 'site-historique', 0, 0, 0, 0, 1, 1, 7, 1, 1, 0),
(22, 'Site Touristique', 'site-touristique', 0, 0, 0, 0, 1, 0, 7, 1, 1, 1),
(23, 'Bâtiment Architectural', 'batiment-architectural', 0, 0, 0, 0, 1, 1, 7, 1, 1, 0),
(24, 'Monument Historique', 'monument-historique', 0, 0, 0, 0, 1, 1, 7, 1, 1, 0),

(25, 'Beffroi', 'beffroi', 0, 0, 0, 0, 1, 1, 7, 0, 1, 0),
(26, 'Château', 'chateau', 0, 0, 0, 0, 1, 1, 7, 1, 1, 1),
(27, 'Attraction touristique', 'attraction-touristique', 0, 0, 0, 0, 1, 1, 7, 1, 1, 0),
(28, 'Fort', 'Fort', 0, 0, 0, 0, 1, 1, 7, 1, 0, 0),
(29, 'Pont', 'pont', 0, 0, 0, 0, 0, 0, 7, 1, 0, 0),

-- Aires de jeux & Parcs d'amusement 
(30, 'Aire de jeux', 'aire-de-jeux', 0, 0, 0, 0, 1, 1, 6, 0, 1, 0),
(31, 'Parc d\'attractions', 'parc-d-attractions', 0, 0, 0, 0, 1, 1, 6, 0, 1, 1),
(32, 'Parc de loisirs', 'parc-de-loisirs', 0, 0, 0, 0, 1, 1, 6, 0, 1, 1),
(33, 'Centre de Loisirs', 'centre-de-loisirs', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 0), -- Spécial

-- Centre commercial & Shopping
(34, 'Centre commercial', 'centre-commercial', 0, 0, 0, 0, 0, 0, 28, 0, 1, 0),
(35, 'Zone Commerciale', 'zone-commerciale', 0, 0, 0, 0, 0, 0, 28, 0, 1, 0),

-- Sites Réligieux 
(36, 'Cathédrale', 'cathedrale', 0, 0, 0, 0, 1, 1, 7, 1, 1, 1),
(37, 'Eglise', 'eglise', 0, 0, 0, 0, 1, 1, 7, 1, 1, 1),
(38, 'Abbaye', 'abbaye', 0, 0, 0, 0, 1, 1, 7, 1, 1, 0),

(39, 'Mosquée', 'mosquee', 0, 0, 0, 0, 0, 0, NULL, 0, 1, 0),
(40, 'Synagogue', 'synagogue', 0, 0, 0, 0, 0, 0, NULL, 0, 1, 0),
(41, 'Temple', 'temple', 0, 0, 0, 0, 0, 0, NULL, 0, 1, 0),
(42, 'Paroisse', 'paroisse', 0, 0, 0, 0, 0, 0, NULL, 0, 1, 0),

-- Plage, Lacs & Eaux 
(43, 'Plage', 'plage', 0, 0, 1, 0, 0, 0, 32, 1, 0, 0),
(44, 'Etang', 'etang', 0, 0, 1, 0, 0, 0, 32, 0, 0, 0),
(45, 'Canal', 'canal', 0, 0, 1, 0, 0, 0, 32, 1, 0, 0),
(46, 'Lac', 'lac', 0, 0, 1, 0, 0, 0, 32, 1, 0, 0),
(47, 'Port', 'port', 0, 0, 1, 0, 0, 0, 32, 1, 0, 0),

(48, 'Port de plaisance', 'port-de-plaisance', 0, 0, 1, 0, 0, 0, 32, 1, 0, 0),
(49, 'Marina', 'marina', 0, 0, 1, 0, 0, 0, 32, 1, 0, 0),
(50, 'Quai', 'quai', 0, 0, 1, 0, 1, 0, NULL, 0, 1, 0),

(51, 'Falaise', 'falaise', 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0),
(52, 'Baie', 'baie', 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0),
(53, 'Dune', 'dune', 0, 0, 0, 0, 0, 0, NULL, 1, 0, 0),

-- Zoos, Aquariums, Fermes & Animaux 
(54, 'Zoo', 'zoo', 0, 0, 0, 0, 1, 1, 35, 1, 1, 0),
(55, 'Aquarium', 'aquarium', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 0),
(56, 'Aquarium public', 'aquarium-public', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 0),

(57, 'Ferme', 'ferme', 0, 0, 0, 0, 0, 0, 22, 0, 1, 1),
(58, 'Ferme pédagogique', 'ferme-pedagogique', 0, 0, 0, 0, 0, 0, 22, 0, 1, 1),
(59, 'Ferme agricole', 'ferme-agricole', 0, 0, 0, 0, 0, 0, 22, 0, 1, 1),

(60, 'Marais', 'marais', 0, 0, 0, 0, 0, 0, 32, 0, 0, 0),
(61, 'Marécage', 'marecage', 0, 0, 0, 0, 0, 0, 32, 0, 0, 0),
(62, 'Marigot', 'marigot', 0, 0, 0, 0, 0, 0, 32, 0, 1, 0),

(63, 'Galet', 'galet', 0, 0, 0, 0, 0, 0, NULL, 0, 0, 0),
(64, 'verger', 'verger', 0, 0, 0, 0, 0, 0, 32, 0, 0, 0), 
(65, 'Terril', 'terril', 0, 0, 0, 0, 0, 0, 7, 1, 0, 0),

-- Spectacle
(66, 'Salle de spectacle', 'salle-de-spectacle', 0, 0, 0, 0, 0, 0, 26, 0, 0, 1),
(67, 'Salle de concert', 'salle-de-concert', 0, 0, 0, 0, 0, 0, 26, 0, 0, 1),
(68, 'Théâtre', 'theatre', 0, 0, 0, 0, 1, 1, 26, 1, 1, 1),
(69, 'Centre Culturel', 'centre-culturel', 0, 0, 0, 0, 1, 0, NULL, 0, 1, 1),
(70, 'Palais des congrès', 'palais-des-congres', 0, 0, 0, 0, 1, 1, 26, 1, 1, 1),

-- Hotels & Hebergements 
(71, 'Hotel', 'hotel', 0, 0, 0, 0, 1, 1, 5, 0, 1, 1),
(72, 'Résidence hôtelière', 'residence-hoteliere', 0, 0, 0, 0, 1, 1, 5, 0, 1, 1),
(73, 'Camping', 'camping', 0, 0, 0, 0, 1, 1, 5, 0, 1, 1),
(74, 'Gîte', 'gite', 0, 0, 0, 0, 1, 1, 5, 0, 1, 1),

-- Amusements & Sports 
(75, 'Piscine', 'piscine',  0, 0, 0, 0, 1, 1, 34, 0, 1, 1),
(76, 'Skatepark', 'skatepark', 0, 0, 0, 0, 1, 1, 34, 0, 1, 1),
(77, 'Patinoire', 'patinoire', 0, 0, 0, 0, 1, 1, 6, 0, 1, 1),
(78, 'Hippodrome', 'hippodrome',  0, 0, 0, 0, 1, 1, 4, 0, 1, 0),

-- Sport & Danse
(79, 'Stade', 'stade', 0, 0, 0, 0, 1, 0, NULL, 1, 0, 1),
(80, 'Gymnase', 'gymnase', 0, 0, 0, 0, 1, 0, NULL, 0, 1, 0),
(81, 'Complexe sportif', 'complexe-sportif', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 0),
(82, 'Complexe de loisirs', 'complexe-de-loisirs', 0, 0, 0, 0, 1, 1, 6, 0, 1, 0),

(83, 'Ecole de danse', 'ecole-de-danse', 0, 1, 0, 0, 0, 0, 29, 0, 0, 1),
(84, 'Ecole de musique', 'ecole-de-musique', 1, 0, 0, 0, 0, 0, 29, 0, 0, 0),
(85, 'Centre de Yoga', 'centre-de-yoga', 0, 0, 0, 0, 0, 0, 29, 0, 1, 1),

(86, 'Parcours de golf', 'parcours-de-golf', 0, 0, 0, 0, 1, 1, 4, 0, 1, 1),
(87, 'Centre de sports d\'aventure', 'centre-de-sport-d-aventure', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 1),
(88, 'Club de Canoë-Kayak', 'club-de-canoe-kayak', 0, 0, 0, 0, 0, 1, NULL, 0, 1, 1),
(89, 'Terrain de sport', 'terrain-de-sport', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 0), -- Ensemble contenant Court de tennis, Terrain basket, Terrain de foot à 5, Terrain de Pétanque
(90, 'Salle de Tennis', 'salle-de-tennis', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 0),
(91, 'Domaine de ski', 'domaine-de-ski', 0, 0, 0, 0, 0, 1, NULL, 0, 1, 0),

(92, 'Jardin partagé', 'jardin-partage', 0, 0, 0, 0, 1, 0, 27, 0, 1, 0),
(93, 'Casino', 'casino', 0, 0, 0, 0, 1, 1, 26, 0, 1, 0),

-- AUtres Parcs 
(94, 'Base de plein air et de loisirs', 'base-de-plein-air-et-de-loisirs', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 1),
(95, 'Parc aventure', 'parc-aventure', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 1),
(96, 'Parc scientifique', 'parc-scientifique', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 1),

(97, 'Parc de miniatures', 'parc-de-miniatures', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 1),
(98, 'Parc animalier', 'parc-animalier', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 1),
(99, 'Parc safari', 'parc-safari', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 1),
(100, 'Parc zoologique', 'parc-zoologique', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 1),
(101, 'Parc d\'attractions et animalier', 'parc-d-attractions-et-animalier', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 1),
(102, 'Parc aquatique', 'parc-aquatique', 0, 0, 0, 0, 1, 0, NULL, 0, 1, 1),
(103, 'Aire protégée', 'aire-protegee', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 1),

-- Parkings & Stationnement
(104, 'Parking', 'parking', 0, 0, 0, 0, 1, 1, 36, 0, 1, 0),
(105, 'Parking relais', 'parking-relais', 0, 0, 0, 0, 1, 1, 36, 0, 1, 0),

-- Bâtiments & Services Locaux
(106, 'Hotel de ville', 'hotel-de-ville', 0, 0, 0, 0, 0, 0, 30, 1, 1, 0),
(107, 'service administratif local', 'service-administratif-local', 0, 0, 0, 0, 0, 0, 30, 0, 1, 0),

(108, 'Ecole', 'ecole', 0, 0, 0, 0, 0, 0, 31, 0, 1, 0),
(109, 'Université', 'universite', 0, 0, 0, 0, 0, 0, 31, 0, 1, 0),

(110, 'Banque', 'banque', 0, 0, 0, 0, 0, 0, NULL, 0, 1, 0),
(111, 'Cuisine centrale', 'cuisine-centrale', 0, 0, 0, 0, 0, 0, NULL, 0, 1, 0),

(112, 'Halle', 'halle', 0, 0, 0, 0, 0, 0, 37, 0, 1, 0),
(113, 'Bureaux', 'bureaux', 0, 0, 0, 0, 0, 0, NULL, 0, 1, 0),
(114, 'Thermes', 'thermes', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 1), 

(115, 'Auberge de jeunesse ', 'auberge-de-jeunesse', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 0),
(116, 'Auditorium', 'auditorium', 0, 0, 0, 0, 1, 1, 7, 0, 1, 1),
(117, 'Amphitheatre', 'amphitheatre', 0, 0, 0, 0, 1, 1, 7, 0, 1, 1), 

(118, 'Cascade', 'cascade', 0, 0, 1, 0, 1, 1, NULL, 0, 1, 0), 
(119, 'Base Nautique', 'base-nautique', 0, 0, 1, 0, 1, 0, 6, 0, 1, 1),

(120, 'Parc agricole', 'parc-agricole', 0, 0, 0, 0, 0, 0, 27, 0, 0, 0), -- Place, Jardins & Autres espaces vert
(121, 'Parc de loisirs à thèmes', 'parc-de-loisirs-a-theme', 0, 0, 0, 0, 1, 1, 6, 0, 1, 0), -- Autres Parcs

(122, 'Déchèterie', 'decheterie', 0, 0, 0, 0, 1, 1, NULL, 0, 1, 0),
(123, 'Relais Nature', 'relais-nature', 0, 0, 0, 0, 1, 1, 27, 0, 1, 0),
(124, 'Grotte', 'grotte', 0, 0, 0, 0, 1, 1, 7, 0, 1, 0);

INSERT INTO `PlaceType` (`id`, `name`, `place_type_string_id`, is_road_entity_type, is_transport_entity_type, is_water_entity_type, is_subdivision_entity_type, 
  is_access_type_category, is_bookable_service_category, etablishment_type, is_visitable_category, with_hourly, necessarily_on_other_place, is_privatizable) VALUES

(125, 'Aire de pique-nique', 'aire-de-pique-nique', 0, 0, 0, 0, 0, 0, 27, 0, 0, 1, 0),
(126, 'Panorama', 'panorama', 0, 0, 0, 0, 0, 0, 27, 0, 0, 0, 0),
(127, 'Coin de nature', 'coin-de-nature', 0, 0, 0, 0, 0, 0, 27, 0, 0, 1, 0),
(128, 'Coin de biodiversité', 'coin-de-biodiversite', 0, 0, 0, 0, 0, 0, 27, 0, 0, 1, 0),

(129, 'Centre social', 'centre-social', 0, 0, 0, 0, 0, 0, NULL, 0, 1, 0, 0); -- Spécial

INSERT INTO `PlaceType` (`id`, `name`, `place_type_string_id`, is_road_entity_type, is_transport_entity_type, is_water_entity_type, is_subdivision_entity_type, 
  is_access_type_category, is_bookable_service_category, etablishment_type, is_visitable_category, with_hourly, is_privatizable) VALUES
(130, 'Salle de réception', 'salle-de-reception', 0, 0, 0, 0, 0, 0, 26, 0, 0, 1),
(131, 'Salle polyvalente', 'salle-polyvalente', 0, 0, 0, 0, 0, 0, 26, 0, 0, 1),
(132, 'Studio Pilates', 'studio-pilates', 0, 0, 0, 0, 1, 1, 6, 0, 1, 0),
(133, "Centre d'affaires", 'centre-d-affaires', 0, 0, 0, 0, 1, 1, 28, 0, 1, 0),
(134, 'Lodge', 'lodge', 0, 0, 0, 0, 1, 1, 5, 0, 1, 1), 


(135, 'Bibliothèque', 'bibliotheque', 0, 0, 0, 0, 1, 0, 20, 1, 1, 0),
(136, 'Médiathèque', 'mediatheque', 0, 0, 0, 0, 1, 0, 20, 1, 1, 0),
(137, 'Bibliothèque municipale', 'bibliotheque-municipale', 0, 0, 0, 0, 1, 0, 20, 1, 1, 0)
;
  

-- -  Caravansérail Centre de vacances naturiste Condotel Écohôtel Fondouk Gîte d'étape Hôtel-boutique Hôtel Hôtel capsule Hôtellerie de plein air
-- Île-hôtel Loge de safari Love hotel Minshuku Motel Palace Pourvoirie Refuge de montagne Résidence de tourisme Resort Ryokan Village de vacances
;
