<?php

use CodeIgniter\Router\RouteCollection;

/** @var RouteCollection $routes */

// REVIEW DRAFT: grouped by controller from existing explicit declarations.
// Auto-routing remains enabled; this file alone is not a complete migration.

// AnimationManagement
$routes->post('animationManagement/toggleActive/(:num)', 'AnimationManagement::postToggleActive/$1', ['filter' => 'csrf']);
$routes->post('animationManagement/activateBookingConf/(:segment)/(:num)/(:num)/(:num)', 'AnimationManagement::postActivateBookingConf/$1/$2/$3/$4', ['filter' => 'csrf']);
$routes->post('animationManagement/deactivateBookingConf/(:segment)/(:num)/(:num)/(:num)', 'AnimationManagement::postDeactivateBookingConf/$1/$2/$3/$4', ['filter' => 'csrf']);
$routes->post('animationManagement/useBookingConf/(:segment)/(:num)/(:num)/(:num)', 'AnimationManagement::postUseBookingConf/$1/$2/$3/$4', ['filter' => 'csrf']);
$routes->post('animationManagement/disableBookingConfContent/(:segment)/(:num)/(:num)/(:num)', 'AnimationManagement::postDisableBookingConfContent/$1/$2/$3/$4', ['filter' => 'csrf']);

// BoMissions
$routes->post('boMissions/save', 'BoMissions::postSave', ['filter' => 'csrf']);
$routes->post('boMissions/saveReward', 'BoMissions::postSaveReward', ['filter' => 'csrf']);
$routes->post('boMissions/deleteReward/(:num)/(:num)', 'BoMissions::postDeleteReward/$1/$2', ['filter' => 'csrf']);
$routes->post('boMissions/addObjective/(:num)', 'BoMissions::postAddObjective/$1', ['filter' => 'csrf']);
$routes->post('boMissions/deleteObjective/(:num)/(:num)', 'BoMissions::postDeleteObjective/$1/$2', ['filter' => 'csrf']);

// Circuit
$routes->post('circuit/removeStep/(:num)/(:num)', 'Circuit::postRemoveStep/$1/$2', ['filter' => 'csrf']);

// EditorialCharacts
$routes->post('editorialCharacts/addCharact/(:segment)/(:num)', 'EditorialCharacts::postAddCharact/$1/$2', ['filter' => 'csrf']);
$routes->post('editorialCharacts/deleteCharact/(:segment)/(:num)/(:segment)/(:segment)/(:num)', 'EditorialCharacts::postDeleteCharact/$1/$2/$3/$4/$5', ['filter' => 'csrf']);

// ElementNews
$routes->post('elementNews/removeMedia/(:num)/(:num)', 'ElementNews::postRemoveMedia/$1/$2', ['filter' => 'csrf']);

// Employee
$routes->get('employee/signin', 'Employee::getSignin');
$routes->get('employee/connexion', 'Employee::getSignin');
$routes->get('employee/connexion/(:segment)', 'Employee::getSignin/$1');
$routes->post('employee/connect', 'Employee::postConnect', ['filter' => 'csrf']);
$routes->post('employee/disconnect', 'Employee::postDisconnect', ['filter' => 'csrf']);
$routes->get('employee/password_choose/choose', 'Employee::getPassword_choose/choose');
$routes->post('employee/password_choose/resend', 'Employee::getPassword_choose/resend', ['filter' => 'csrf']);
$routes->post('employee/password_choose/change', 'Employee::postPassword_choose/change', ['filter' => 'csrf']);
$routes->get('employee/password_reset', 'Employee::getPassword_reset');
$routes->get('employee/password_reset/choose', 'Employee::getPassword_reset/choose');
$routes->post('employee/password_reset/check', 'Employee::postPassword_reset/check', ['filter' => 'csrf']);
$routes->post('employee/password_reset/change', 'Employee::postPassword_reset/change', ['filter' => 'csrf']);
$routes->get('employee/2fa_code/choose', 'Employee::get2fa_code/choose');
$routes->post('employee/2fa_code/check', 'Employee::post2fa_code/check', ['filter' => 'csrf']);
$routes->post('employee/2fa_code/resend', 'Employee::get2fa_code/resend', ['filter' => 'csrf']);

// Equipment
$routes->post('equipment/activateBookingConf/(:num)/(:num)', 'Equipment::postActivateBookingConf/$1/$2', ['filter' => 'csrf']);
$routes->post('equipment/deactivateBookingConf/(:num)/(:num)', 'Equipment::postDeactivateBookingConf/$1/$2', ['filter' => 'csrf']);
$routes->post('equipment/useBookingConf/(:num)/(:num)', 'Equipment::postUseBookingConf/$1/$2', ['filter' => 'csrf']);
$routes->post('equipment/disableBookingConfContent/(:num)/(:num)', 'Equipment::postDisableBookingConfContent/$1/$2', ['filter' => 'csrf']);

// EquipmentManagement
$routes->post('equipmentManagement/toggleActive/(:num)', 'EquipmentManagement::postToggleActive/$1', ['filter' => 'csrf']);
$routes->post('equipmentManagement/activateBookingConf/(:num)/(:num)', 'EquipmentManagement::postActivateBookingConf/$1/$2', ['filter' => 'csrf']);
$routes->post('equipmentManagement/deactivateBookingConf/(:num)/(:num)', 'EquipmentManagement::postDeactivateBookingConf/$1/$2', ['filter' => 'csrf']);
$routes->post('equipmentManagement/useBookingConf/(:num)/(:num)', 'EquipmentManagement::postUseBookingConf/$1/$2', ['filter' => 'csrf']);
$routes->post('equipmentManagement/disableBookingConfContent/(:num)/(:num)', 'EquipmentManagement::postDisableBookingConfContent/$1/$2', ['filter' => 'csrf']);

// Event
$routes->get('event', 'Event::getIndex');
$routes->get('event/show/(:segment)', 'Event::getShow/$1');
$routes->get('event/show/(:segment)/(:segment)', 'Event::getShow/$1/$2');

// EventSerie
$routes->post('eventSerie/removeHobby/(:num)/(:num)', 'EventSerie::postRemoveHobby/$1/$2', ['filter' => 'csrf']);
$routes->post('eventSerie/removeEventObject/(:num)/(:num)', 'EventSerie::postRemoveEventObject/$1/$2', ['filter' => 'csrf']);

// Experience
$routes->get('experience', 'Experience::getIndex');
$routes->get('experience/show/(:segment)', 'Experience::getShow/$1');
$routes->get('experience/show/(:segment)/(:segment)', 'Experience::getShow/$1/$2');

// IzilifeSelection
$routes->post('izilifeSelection/create', 'IzilifeSelection::postCreate', ['filter' => 'csrf']);
$routes->post('izilifeSelection/update/(:segment)', 'IzilifeSelection::postUpdate/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/addPrice/(:segment)', 'IzilifeSelection::postAddPrice/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/updatePrice/(:segment)', 'IzilifeSelection::postUpdatePrice/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/deactivatePrice/(:segment)', 'IzilifeSelection::postDeactivatePrice/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/upsertTier/(:segment)', 'IzilifeSelection::postUpsertTier/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/toggleTier/(:segment)', 'IzilifeSelection::postToggleTier/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/upsertComposition/(:segment)', 'IzilifeSelection::postUpsertComposition/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/deleteCompositionItem/(:segment)', 'IzilifeSelection::postDeleteCompositionItem/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/addParticipation/(:segment)', 'IzilifeSelection::postAddParticipation/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/updateParticipation/(:segment)', 'IzilifeSelection::postUpdateParticipation/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/toggleParticipation/(:segment)', 'IzilifeSelection::postToggleParticipation/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/deleteParticipation/(:segment)', 'IzilifeSelection::postDeleteParticipation/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/addVariant/(:segment)', 'IzilifeSelection::postAddVariant/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/updateVariant/(:segment)', 'IzilifeSelection::postUpdateVariant/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/addVariantPrice/(:segment)', 'IzilifeSelection::postAddVariantPrice/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/updateVariantPrice/(:segment)', 'IzilifeSelection::postUpdateVariantPrice/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/upsertParticipationVariantPrice/(:segment)', 'IzilifeSelection::postUpsertParticipationVariantPrice/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/toggleParticipationVariantPrice/(:segment)', 'IzilifeSelection::postToggleParticipationVariantPrice/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/upsertParticipationOverride/(:segment)', 'IzilifeSelection::postUpsertParticipationOverride/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/toggleParticipationOverride/(:segment)', 'IzilifeSelection::postToggleParticipationOverride/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/addMedia/(:num)', 'IzilifeSelection::postAddMedia/$1', ['filter' => 'csrf']);
$routes->post('izilifeSelection/updateMedia/(:num)/(:num)', 'IzilifeSelection::postUpdateMedia/$1/$2', ['filter' => 'csrf']);

// LocalHabit
$routes->post('localHabit/removeHobby/(:num)/(:num)', 'LocalHabit::postRemoveHobby/$1/$2', ['filter' => 'csrf']);
$routes->post('localHabit/removeMedia/(:num)/(:num)', 'LocalHabit::postRemoveMedia/$1/$2', ['filter' => 'csrf']);
$routes->post('localHabit/save', 'LocalHabit::postSave', ['filter' => 'csrf']);
$routes->post('localHabit/delete', 'LocalHabit::postDelete', ['filter' => 'csrf']);
$routes->post('localHabit/addHobby/(:num)', 'LocalHabit::postAddHobby/$1', ['filter' => 'csrf']);
$routes->post('localHabit/addMedia/(:num)', 'LocalHabit::postAddMedia/$1', ['filter' => 'csrf']);
$routes->post('localHabit/updateMedia/(:num)/(:num)', 'LocalHabit::postUpdateMedia/$1/$2', ['filter' => 'csrf']);

// PartnerAnalytics
$routes->get('partnerAnalytics', 'PartnerAnalytics::getHumanIndex');

// PartnerAssistant
$routes->post('partner-assistant/interpret', 'PartnerAssistant::postInterpret', ['filter' => 'csrf']);
$routes->post('partner-assistant/create-booking', 'PartnerAssistant::postCreateBooking', ['filter' => 'csrf']);

// PartnerCampaigns
$routes->get('campaigns', 'PartnerCampaigns::getIndex', ['filter' => 'csrf']);
$routes->post('campaigns/create', 'PartnerCampaigns::postCreate', ['filter' => 'csrf']);
$routes->get('campaigns/moment/(:num)', 'PartnerCampaigns::getMoment/$1', ['filter' => 'csrf']);
$routes->post('campaigns/moment/(:num)/join', 'PartnerCampaigns::postJoinCampaign/$1', ['filter' => 'csrf']);
$routes->get('campaigns/edition/(:num)', 'PartnerCampaigns::getEdition/$1', ['filter' => 'csrf']);
$routes->post('campaigns/edition/(:num)/join', 'PartnerCampaigns::postJoinEdition/$1', ['filter' => 'csrf']);
$routes->get('campaigns/(:num)', 'PartnerCampaigns::getShow/$1', ['filter' => 'csrf']);
$routes->post('campaigns/(:num)/update', 'PartnerCampaigns::postUpdate/$1', ['filter' => 'csrf']);
$routes->post('campaigns/(:num)/offer', 'PartnerCampaigns::postLinkOffer/$1', ['filter' => 'csrf']);
$routes->post('campaigns/(:num)/event', 'PartnerCampaigns::postLinkEvent/$1', ['filter' => 'csrf']);
$routes->post('campaigns/(:num)/boost', 'PartnerCampaigns::postLinkBoost/$1', ['filter' => 'csrf']);

// PartnerMediaLibrary
$routes->get('partnerMediaLibrary', 'PartnerMediaLibrary::getIndex');

// PartnerOffers
$routes->get('partnerOffers', 'PartnerOffers::getIndex');
$routes->get('partnerOffers/create', 'PartnerOffers::getCreate');
$routes->get('partnerOffers/edit/(:segment)', 'PartnerOffers::getEdit/$1');
$routes->post('partnerOffers/save', 'PartnerOffers::postSave', ['filter' => 'csrf']);
$routes->post('partnerOffers/publish/(:num)', 'PartnerOffers::postPublish/$1', ['filter' => 'csrf']);
$routes->post('partnerOffers/pause/(:num)', 'PartnerOffers::postPause/$1', ['filter' => 'csrf']);
$routes->post('partnerOffers/duplicate/(:num)', 'PartnerOffers::postDuplicate/$1', ['filter' => 'csrf']);
$routes->get('partnerOffers/targets/(:segment)', 'PartnerOffers::getTargets/$1');
$routes->post('partnerOffers/targetsSave/(:segment)', 'PartnerOffers::postTargetsSave/$1', ['filter' => 'csrf']);

// Place
$routes->get('place', 'Place::getIndex');
$routes->get('place/show/(:segment)', 'Place::getShow/$1');
$routes->get('place/show/(:segment)/(:segment)', 'Place::getShow/$1/$2');
$routes->post('place/updatePlace/(:segment)', 'Place::postUpdatePlace/$1', ['filter' => 'csrf']);

// PopupOccurrence
$routes->post('popupOccurrence/create/(:segment)/(:num)', 'PopupOccurrence::postCreate/$1/$2', ['filter' => 'csrf']);
$routes->post('popupOccurrence/update/(:segment)/(:num)/(:num)', 'PopupOccurrence::postUpdate/$1/$2/$3', ['filter' => 'csrf']);
$routes->post('popupOccurrence/delete/(:segment)/(:num)/(:num)', 'PopupOccurrence::postDelete/$1/$2/$3', ['filter' => 'csrf']);

// Product
$routes->get('product/category/(:segment)', 'Product::getCategory/$1');
$routes->post('product/transferCategory', 'Product::postTransferCategory', ['filter' => 'csrf']);
$routes->get('product', 'Product::getIndex');
$routes->get('product/show/(:segment)', 'Product::getShow/$1');

// PspOnboarding
$routes->get('psp/onboarding/launch/(:segment)/(:segment)/(:segment)', 'PspOnboarding::launch/$1/$2/$3');
$routes->get('psp/onboarding/open/(:segment)/(:segment)/(:segment)', 'PspOnboarding::open/$1/$2/$3');
$routes->get('psp/onboarding/status/(:segment)/(:segment)/(:segment)', 'PspOnboarding::status/$1/$2/$3');
$routes->post('psp/onboarding/set-current/(:num)', 'PspOnboarding::setCurrent/$1', ['filter' => 'csrf']);
$routes->post('psp/onboarding/deactivate/(:num)', 'PspOnboarding::deactivate/$1', ['filter' => 'csrf']);

// Representation
$routes->post('representation/removeAnimal/(:num)/(:num)', 'Representation::postRemoveAnimal/$1/$2', ['filter' => 'csrf']);
$routes->post('representation/removeHobby/(:num)/(:num)', 'Representation::postRemoveHobby/$1/$2', ['filter' => 'csrf']);

// ScopedElement
$routes->post('scopedElement/save', 'ScopedElement::postSave', ['filter' => 'csrf']);
$routes->post('scopedElement/delete', 'ScopedElement::postDelete', ['filter' => 'csrf']);

// Scraper
$routes->post('scraper/agentSuggestPlace/(:segment)', 'Scraper::postAgentSuggestPlace/$1', ['filter' => 'csrf']);
$routes->post('scraper/classifyPoi/(:num)/(:num)', 'Scraper::postClassifyPoi/$1/$2', ['filter' => 'csrf']);
$routes->post('scraper/confirmEvent/(:num)/(:num)', 'Scraper::postConfirmEvent/$1/$2', ['filter' => 'csrf']);
$routes->post('scraper/confirmExperience/(:num)/(:num)', 'Scraper::postConfirmExperience/$1/$2', ['filter' => 'csrf']);
$routes->post('scraper/scrapEventsFromBloggerWebsite/(:num)', 'Scraper::postScrapEventsFromBloggerWebsite/$1', ['filter' => 'csrf']);
$routes->post('scraper/scrapEventsFromBloggerWebsite/(:num)/(:segment)', 'Scraper::postScrapEventsFromBloggerWebsite/$1/$2', ['filter' => 'csrf']);
$routes->post('scraper/scrapEventsFromBloggerWebsite/(:num)/(:segment)/(:num)', 'Scraper::postScrapEventsFromBloggerWebsite/$1/$2/$3', ['filter' => 'csrf']);
$routes->post('scraper/uploadEventImages/(:num)', 'Scraper::postUploadEventImages/$1', ['filter' => 'csrf']);
$routes->post('scraper/uploadEventImages/(:num)/(:segment)', 'Scraper::postUploadEventImages/$1/$2', ['filter' => 'csrf']);
$routes->post('scraper/uploadEventImages/(:num)/(:segment)/(:num)', 'Scraper::postUploadEventImages/$1/$2/$3', ['filter' => 'csrf']);
$routes->post('scraper/scrapExperiencesFromBloggerWebsite/(:num)', 'Scraper::postScrapExperiencesFromBloggerWebsite/$1', ['filter' => 'csrf']);
$routes->post('scraper/scrapExperiencesFromBloggerWebsite/(:num)/(:segment)', 'Scraper::postScrapExperiencesFromBloggerWebsite/$1/$2', ['filter' => 'csrf']);
$routes->post('scraper/scrapExperiencesFromBloggerWebsite/(:num)/(:segment)/(:num)', 'Scraper::postScrapExperiencesFromBloggerWebsite/$1/$2/$3', ['filter' => 'csrf']);
$routes->post('scraper/importProducts/(:num)', 'Scraper::postImportProducts/$1', ['filter' => 'csrf']);
$routes->post('scraper/fetchAndStoreOnePlace/(:segment)', 'Scraper::postFetchAndStoreOnePlace/$1', ['filter' => 'csrf']);
$routes->post('scraper/fetchAndStoreOnePlace/(:segment)/(:segment)', 'Scraper::postFetchAndStoreOnePlace/$1/$2', ['filter' => 'csrf']);
$routes->post('scraper/fetchAndStorePlaces/(:segment)', 'Scraper::postFetchAndStorePlaces/$1', ['filter' => 'csrf']);
$routes->post('scraper/fetchAndStorePlaces/(:segment)/(:segment)', 'Scraper::postFetchAndStorePlaces/$1/$2', ['filter' => 'csrf']);
$routes->post('scraper/uploadEventSources/(:num)', 'Scraper::postUploadEventSources/$1', ['filter' => 'csrf']);
$routes->post('scraper/uploadEventSourcesReplacement/(:num)', 'Scraper::postUploadEventSourcesReplacement/$1', ['filter' => 'csrf']);
$routes->post('scraper/ingestJson', 'Scraper::postIngestJson', ['filter' => 'csrf']);
$routes->post('scraper/approveValidationRequest/(:num)', 'Scraper::postApproveValidationRequest/$1', ['filter' => 'csrf']);
$routes->post('scraper/rejectScrapedEvent/(:num)', 'Scraper::postRejectScrapedEvent/$1', ['filter' => 'csrf']);
$routes->post('scraper/rejectScrapedExperience/(:num)', 'Scraper::postRejectScrapedExperience/$1', ['filter' => 'csrf']);
$routes->post('scraper/rejectValidationRequest/(:num)', 'Scraper::postRejectValidationRequest/$1', ['filter' => 'csrf']);
$routes->post('scraper/saveEditionSourceUrl/(:num)', 'Scraper::postSaveEditionSourceUrl/$1', ['filter' => 'csrf']);
$routes->post('scraper/importCompetitionSchedule/(:num)', 'Scraper::postImportCompetitionSchedule/$1', ['filter' => 'csrf']);
$routes->post('scraper/agentUploadEventSources/(:num)', 'Scraper::postAgentUploadEventSources/$1');
$routes->post('scraper/agentUploadEventImages/(:num)', 'Scraper::postAgentUploadEventImages/$1');
$routes->post('scraper/agentIngestPromo/(:num)', 'Scraper::postAgentIngestPromo/$1');
$routes->post('scraper/agentFetchAndStoreOnePlace', 'Scraper::postAgentFetchAndStoreOnePlace');
$routes->post('scraper/agentFetchAndStoreOnePlace/(:segment)', 'Scraper::postAgentFetchAndStoreOnePlace/$1');
$routes->post('scraper/agentGetPlaceByStringId', 'Scraper::postAgentGetPlaceByStringId');
$routes->post('scraper/agentFetchAndStorePlaces/(:segment)', 'Scraper::postAgentFetchAndStorePlaces/$1');
$routes->post('scraper/agentGetCity/(:segment)', 'Scraper::postAgentGetCity/$1');
$routes->post('scraper/importCompetitionScheduleFromAgent/(:num)', 'Scraper::postImportCompetitionScheduleFromAgent/$1');
$routes->post('scraper/agentGetPlacesToEnrich', 'Scraper::postAgentGetPlacesToEnrich');
$routes->post('scraper/agentSubmitEnrichment', 'Scraper::postAgentSubmitEnrichment');
$routes->post('scraper/agentImproveFromGoogle', 'Scraper::postAgentImproveFromGoogle');
$routes->post('scraper/agentAnalyzeContent', 'Scraper::postAgentAnalyzeContent');
$routes->post('scraper/agentCheckPlace', 'Scraper::postAgentCheckPlace');
$routes->post('scraper/agentMarkPlaceClosed', 'Scraper::postAgentMarkPlaceClosed');
$routes->post('scraper/agentUpsertPage', 'Scraper::postAgentUpsertPage');
$routes->post('scraper/agentUpsertLink', 'Scraper::postAgentUpsertLink');
$routes->post('scraper/agentUpsertExternalMedia', 'Scraper::postAgentUpsertExternalMedia');
$routes->post('scraper/home', 'Scraper::postHome', ['filter' => 'csrf']);

// Shop
$routes->get('shop/show/(:segment)', 'Shop::getShow/$1');
$routes->get('shop/show/(:segment)/(:segment)', 'Shop::getShow/$1/$2');
$routes->post('shop/updateShop/(:segment)', 'Shop::postUpdateShop/$1', ['filter' => 'csrf']);

// StripeCallback
$routes->get('stripecallback/stripe/partner/refresh/(:segment)', 'StripeCallback::partnerOnboardingStripeRefresh/$1');
$routes->get('stripecallback/stripe/partner/return/(:segment)', 'StripeCallback::partnerOnboardingStripeReturn/$1');
$routes->get('stripecallback/stripe/place/refresh/(:segment)', 'StripeCallback::placeOnboardingStripeRefresh/$1');
$routes->get('stripecallback/stripe/place/return/(:segment)', 'StripeCallback::placeOnboardingStripeReturn/$1');
$routes->get('stripecallback/stripe/shop/refresh/(:segment)', 'StripeCallback::shopOnboardingStripeRefresh/$1');
$routes->get('stripecallback/stripe/shop/return/(:segment)', 'StripeCallback::shopOnboardingStripeReturn/$1');

// Terrace
$routes->post('terrace/removeMedia/(:num)/(:num)', 'Terrace::postRemoveMedia/$1/$2', ['filter' => 'csrf']);

// Stripe
$routes->post('webhooks/stripe', 'Webhooks\Stripe::postIndex');

// Welcome
$routes->get('', 'Welcome::getIndex');
