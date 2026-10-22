<?php

use CodeIgniter\Router\RouteCollection;

/** @var RouteCollection $routes */

// REVIEW DRAFT: grouped by controller from existing explicit declarations.
// Auto-routing remains enabled; this file alone is not a complete migration.

// AccessPrice
$routes->post('accessPrice/addGroupedPrice', 'AccessPrice::postAddGroupedPrice', ['filter' => 'adminauthcsrf']);
$routes->post('accessPrice/updateGroupedPrice', 'AccessPrice::postUpdateGroupedPrice', ['filter' => 'adminauthcsrf']);
$routes->post('accessPrice/deleteGroupedPrice', 'AccessPrice::postDeleteGroupedPrice', ['filter' => 'adminauthcsrf']);
$routes->post('accessPrice/addPackItem', 'AccessPrice::postAddPackItem', ['filter' => 'adminauthcsrf']);
$routes->post('accessPrice/updatePackItem', 'AccessPrice::postUpdatePackItem', ['filter' => 'adminauthcsrf']);
$routes->post('accessPrice/deletePackItem', 'AccessPrice::postDeletePackItem', ['filter' => 'adminauthcsrf']);
$routes->post('accessPrice/linkEAPToCategories', 'AccessPrice::postLinkEAPToCategories', ['filter' => 'adminauthcsrf']);
$routes->post('accessPrice/unlinkEAPFromCategory', 'AccessPrice::postUnlinkEAPFromCategory', ['filter' => 'adminauthcsrf']);
$routes->post('accessPrice/linkEAPToEquipments', 'AccessPrice::postLinkEAPToEquipments', ['filter' => 'adminauthcsrf']);
$routes->post('accessPrice/unlinkEAPFromEquipment', 'AccessPrice::postUnlinkEAPFromEquipment', ['filter' => 'adminauthcsrf']);

// AnnualCelebration
$routes->get('annualCelebration', 'AnnualCelebration::getIndex', ['filter' => 'adminauth']);
$routes->get('annualCelebration/list', 'AnnualCelebration::getList', ['filter' => 'adminauth']);
$routes->get('annualCelebration/show/(:any)', 'AnnualCelebration::getShow/$1', ['filter' => 'adminauth']);
$routes->get('annualCelebration/add', 'AnnualCelebration::getAdd', ['filter' => 'adminauth']);
$routes->get('annualCelebration/edit/(:any)', 'AnnualCelebration::getEdit/$1', ['filter' => 'adminauth']);
$routes->post('annualCelebration/addObject/(:num)', 'AnnualCelebration::postAddObject/$1', ['filter' => 'adminauthcsrf']);
$routes->post('annualCelebration/removeHobby/(:num)/(:num)', 'AnnualCelebration::postRemoveHobby/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('annualCelebration/removeEventObject/(:num)/(:num)', 'AnnualCelebration::postRemoveEventObject/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('annualCelebration/publishEdition/(:num)', 'AnnualCelebration::postPublishEdition/$1', ['filter' => 'csrf']);

// Authz
$routes->get('authz', 'Authz::getIndex', ['filter' => 'adminauth']);
$routes->get('authz/roleCreate', 'Authz::getRoleCreate', ['filter' => 'adminauth']);
$routes->get('authz/roleEdit/(:num)', 'Authz::getRoleEdit/$1', ['filter' => 'adminauth']);
$routes->get('authz/permissions', 'Authz::getPermissions', ['filter' => 'adminauth']);
$routes->get('authz/permissionCreate', 'Authz::getPermissionCreate', ['filter' => 'adminauth']);
$routes->get('authz/permissionEdit/(:num)', 'Authz::getPermissionEdit/$1', ['filter' => 'adminauth']);
$routes->get('authz/rolePermissions/(:num)', 'Authz::getRolePermissions/$1', ['filter' => 'adminauth']);
$routes->post('authz/roleSave', 'Authz::postRoleSave', ['filter' => 'csrf']);
$routes->post('authz/permissionSave', 'Authz::postPermissionSave', ['filter' => 'csrf']);
$routes->post('authz/rolePermissionsSave/(:num)', 'Authz::postRolePermissionsSave/$1', ['filter' => 'csrf']);

// BoMissions
$routes->get('boMissions', 'BoMissions::getIndex', ['filter' => 'adminauth']);
$routes->get('boMissions/list', 'BoMissions::getList', ['filter' => 'adminauth']);
$routes->get('boMissions/form', 'BoMissions::getForm', ['filter' => 'adminauth']);
$routes->get('boMissions/form/(:num)', 'BoMissions::getForm/$1', ['filter' => 'adminauth']);
$routes->post('boMissions/save', 'BoMissions::postSave', ['filter' => 'csrf']);
$routes->post('boMissions/saveReward', 'BoMissions::postSaveReward', ['filter' => 'csrf']);
$routes->post('boMissions/deleteReward/(:num)/(:num)', 'BoMissions::postDeleteReward/$1/$2', ['filter' => 'csrf']);
$routes->post('boMissions/addObjective/(:num)', 'BoMissions::postAddObjective/$1', ['filter' => 'csrf']);
$routes->post('boMissions/deleteObjective/(:num)/(:num)', 'BoMissions::postDeleteObjective/$1/$2', ['filter' => 'csrf']);

// BoSportCompetition
$routes->get('boSportCompetition', 'BoSportCompetition::getIndex', ['filter' => 'adminauth']);
$routes->get('boSportCompetition/list', 'BoSportCompetition::getList', ['filter' => 'adminauth']);
$routes->get('boSportCompetition/editions/(:num)', 'BoSportCompetition::getEditions/$1', ['filter' => 'adminauth']);
$routes->get('boSportCompetition/matchList', 'BoSportCompetition::getMatchList', ['filter' => 'adminauth']);
$routes->get('boSportCompetition/matches/(:num)', 'BoSportCompetition::getMatches/$1', ['filter' => 'adminauth']);
$routes->get('boSportCompetition/participations/(:num)', 'BoSportCompetition::getParticipations/$1', ['filter' => 'adminauth']);
$routes->get('boSportCompetition/matchEvents/(:num)', 'BoSportCompetition::getMatchEvents/$1', ['filter' => 'adminauth']);
$routes->post('boSportCompetition/saveCompetitionUrl/(:num)', 'BoSportCompetition::postSaveCompetitionUrl/$1', ['filter' => 'adminauthcsrf']);
$routes->post('boSportCompetition/saveEdition', 'BoSportCompetition::postSaveEdition', ['filter' => 'adminauthcsrf']);
$routes->post('boSportCompetition/saveMatch', 'BoSportCompetition::postSaveMatch', ['filter' => 'adminauthcsrf']);
$routes->post('boSportCompetition/importSchedule/(:num)', 'BoSportCompetition::postImportSchedule/$1', ['filter' => 'adminauthcsrf']);
$routes->post('boSportCompetition/createParticipation/(:segment)', 'BoSportCompetition::postCreateParticipation/$1', ['filter' => 'adminauthcsrf']);
$routes->post('boSportCompetition/participationContext', 'BoSportCompetition::postParticipationContext', ['filter' => 'adminauthcsrf']);

// Circuit
$routes->get('circuit', 'Circuit::getIndex', ['filter' => 'adminauth']);
$routes->get('circuit/list', 'Circuit::getList', ['filter' => 'adminauth']);
$routes->get('circuit/show/(:any)', 'Circuit::getShow/$1', ['filter' => 'adminauth']);
$routes->post('circuit/quickAdd', 'Circuit::postQuickAdd', ['filter' => 'adminauthcsrf']);
$routes->post('circuit/uploadRoute/(:num)', 'Circuit::postUploadRoute/$1', ['filter' => 'adminauthcsrf']);
$routes->post('circuit/addStep/(:segment)', 'Circuit::postAddStep/$1', ['filter' => 'adminauthcsrf']);
$routes->post('circuit/updateStep/(:segment)/(:segment)', 'Circuit::postUpdateStep/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('circuit/removeStep/(:num)/(:num)', 'Circuit::postRemoveStep/$1/$2', ['filter' => 'adminauthcsrf']);

// City
$routes->get('city', 'City::getIndex', ['filter' => 'adminauth']);
$routes->get('city/show/(:any)', 'City::getShow/$1', ['filter' => 'adminauth']);
$routes->get('city/ajaxGetPlacesAndShops/(:num)', 'City::getAjaxGetPlacesAndShops/$1', ['filter' => 'adminauth']);
$routes->post('city/update/(:num)', 'City::postUpdate/$1', ['filter' => 'csrf']);
$routes->post('city/addMedia/(:num)', 'City::postAddMedia/$1', ['filter' => 'csrf']);
$routes->post('city/updateMedia/(:num)/(:num)', 'City::postUpdateMedia/$1/$2', ['filter' => 'csrf']);
$routes->post('city/addAnecdote/(:num)', 'City::postAddAnecdote/$1', ['filter' => 'csrf']);
$routes->post('city/addQuestion/(:num)', 'City::postAddQuestion/$1', ['filter' => 'csrf']);
$routes->post('city/addCircuit/(:num)', 'City::postAddCircuit/$1', ['filter' => 'csrf']);
$routes->post('city/addNeighbor/(:num)', 'City::postAddNeighbor/$1', ['filter' => 'csrf']);
$routes->post('city/addEquipment/(:num)', 'City::postAddEquipment/$1', ['filter' => 'csrf']);

// ContentProgram
$routes->get('contentProgram', 'ContentProgram::getIndex', ['filter' => 'adminauth']);
$routes->post('contentProgram/deleteParticipation/(:num)/(:alpha)/(:num)', 'ContentProgram::postDeleteParticipation/$1/$2/$3', ['filter' => 'adminauthcsrf']);

// Country
$routes->get('country', 'Country::getIndex', ['filter' => 'adminauth']);
$routes->get('country/show/(:any)', 'Country::getShow/$1', ['filter' => 'adminauth']);
$routes->get('country/cities/(:num)', 'Country::getCities/$1', ['filter' => 'adminauth']);
$routes->get('country/cities/(:num)/(:num)', 'Country::getCities/$1/$2', ['filter' => 'adminauth']);
$routes->get('country/knowledgesInfos/(:num)/(:num)', 'Country::getKnowledgesInfos/$1/$2', ['filter' => 'adminauth']);
$routes->post('country/city_search/(:num)', 'Country::postCity_search/$1', ['filter' => 'csrf']);
$routes->post('country/addAnecdote/(:num)', 'Country::postAddAnecdote/$1', ['filter' => 'csrf']);
$routes->post('country/addQuestion/(:num)', 'Country::postAddQuestion/$1', ['filter' => 'csrf']);

// EditorialCharacts
$routes->post('editorialCharacts/addCharact/(:segment)/(:num)', 'EditorialCharacts::postAddCharact/$1/$2', ['filter' => 'csrf']);
$routes->post('editorialCharacts/deleteCharact/(:segment)/(:num)/(:segment)/(:segment)/(:num)', 'EditorialCharacts::postDeleteCharact/$1/$2/$3/$4/$5', ['filter' => 'csrf']);

// Employee
$routes->get('employee/connexion', 'Employee::getConnexion');
$routes->post('employee/connect', 'Employee::postConnect', ['filter' => 'csrf']);
$routes->post('employee/disconnect', 'Employee::postDisconnect', ['filter' => 'adminauthcsrf']);
$routes->get('employee', 'Employee::getIndex', ['filter' => 'adminauth']);
$routes->get('employee/show/(:any)', 'Employee::getShow/$1', ['filter' => 'adminauth']);
$routes->post('employee/create', 'Employee::postCreate', ['filter' => 'adminauthcsrf']);
$routes->post('employee/update/(:num)', 'Employee::postUpdate/$1', ['filter' => 'adminauthcsrf']);

// EmployeeAccess
$routes->get('employeeAccess', 'EmployeeAccess::getIndex', ['filter' => 'adminauth']);
$routes->get('employeeAccess/edit/(:num)', 'EmployeeAccess::getEdit/$1', ['filter' => 'adminauth']);
$routes->post('employeeAccess/save/(:num)', 'EmployeeAccess::postSave/$1', ['filter' => 'csrf']);
$routes->post('employeeAccess/ajaxSearchEmployees', 'EmployeeAccess::postAjaxSearchEmployees');

// EquipmentManagement
$routes->get('equipmentManagement', 'EquipmentManagement::getIndex', ['filter' => 'adminauth']);
$routes->get('equipmentManagement/list', 'EquipmentManagement::getList', ['filter' => 'adminauth']);
$routes->get('equipmentManagement/show/(:any)', 'EquipmentManagement::getShow/$1', ['filter' => 'adminauth']);
$routes->post('equipmentManagement/saveEventUsage', 'EquipmentManagement::postSaveEventUsage', ['filter' => 'adminauthcsrf']);
$routes->post('equipmentManagement/updateCharacteristics/(:num)', 'EquipmentManagement::postUpdateCharacteristics/$1', ['filter' => 'adminauthcsrf']);
$routes->post('equipmentManagement/addBookingConf/(:num)', 'EquipmentManagement::postAddBookingConf/$1', ['filter' => 'adminauthcsrf']);
$routes->post('equipmentManagement/updateBookingConf/(:num)/(:num)', 'EquipmentManagement::postUpdateBookingConf/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('equipmentManagement/addBookingConfContent/(:num)/(:num)', 'EquipmentManagement::postAddBookingConfContent/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('equipmentManagement/updateBookingConfContent/(:num)/(:num)', 'EquipmentManagement::postUpdateBookingConfContent/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('equipmentManagement/activateBookingConf/(:num)/(:num)', 'EquipmentManagement::postActivateBookingConf/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('equipmentManagement/deactivateBookingConf/(:num)/(:num)', 'EquipmentManagement::postDeactivateBookingConf/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('equipmentManagement/useBookingConf/(:num)/(:num)', 'EquipmentManagement::postUseBookingConf/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('equipmentManagement/disableBookingConfContent/(:num)/(:num)', 'EquipmentManagement::postDisableBookingConfContent/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('equipmentManagement/toggleActive/(:num)', 'EquipmentManagement::postToggleActive/$1', ['filter' => 'csrf']);

// Event
$routes->get('event', 'Event::getIndex', ['filter' => 'adminauth']);
$routes->get('event/show/(:any)', 'Event::getShow/$1', ['filter' => 'adminauth']);
$routes->get('event/add', 'Event::getAdd', ['filter' => 'adminauth']);
$routes->get('event/add/(:num)', 'Event::getAdd/$1', ['filter' => 'adminauth']);
$routes->get('event/participants/(:num)', 'Event::getParticipants/$1', ['filter' => 'adminauth']);
$routes->get('event/recurrenceOverrides/(:num)', 'Event::getRecurrenceOverrides/$1', ['filter' => 'adminauth']);
$routes->get('event/addLinkedEvent/(:num)/(:num)', 'Event::getAddLinkedEvent/$1/$2', ['filter' => 'adminauth']);
$routes->get('event/addLinkedToRepresentationEvent/(:num)/(:num)', 'Event::getAddLinkedToRepresentationEvent/$1/$2', ['filter' => 'adminauth']);
$routes->get('event/showEntityToInterest/(:num)/(:num)', 'Event::getShowEntityToInterest/$1/$2', ['filter' => 'adminauth']);
$routes->post('event/addAccessPrice/(:num)', 'Event::postAddAccessPrice/$1', ['filter' => 'adminauthcsrf']);
$routes->post('event/updateAccessPrice/(:num)/(:num)', 'Event::postUpdateAccessPrice/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/addEventOrganizer/(:num)', 'Event::postAddEventOrganizer/$1', ['filter' => 'adminauthcsrf']);
$routes->post('event/addEventHobby/(:num)', 'Event::postAddEventHobby/$1', ['filter' => 'adminauthcsrf']);
$routes->post('event/updateEventHobby/(:num)/(:num)', 'Event::postUpdateEventHobby/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/accessInfos/(:num)/(:segment)', 'Event::postAccessInfos/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/addOtherDate/(:num)', 'Event::postAddOtherDate/$1', ['filter' => 'adminauthcsrf']);
$routes->post('event/addEventObject/(:num)', 'Event::postAddEventObject/$1', ['filter' => 'adminauthcsrf']);
$routes->post('event/updateAnecdote/(:num)/(:num)', 'Event::postUpdateAnecdote/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/updateQuestion/(:num)/(:num)', 'Event::postUpdateQuestion/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/createLinkedEvent/(:num)/(:num)', 'Event::postCreateLinkedEvent/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/createRepresentationLinkedEvent/(:num)/(:num)', 'Event::postCreateRepresentationLinkedEvent/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/addProgrammation/(:num)', 'Event::postAddProgrammation/$1', ['filter' => 'adminauthcsrf']);
$routes->post('event/updateProgrammation/(:num)/(:num)', 'Event::postUpdateProgrammation/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/createHourly/(:num)/(:num)', 'Event::postCreateHourly/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/addHourlyContentsByText/(:num)', 'Event::postAddHourlyContentsByText/$1', ['filter' => 'adminauthcsrf']);
$routes->post('event/updateHourlyContentsByText/(:num)', 'Event::postUpdateHourlyContentsByText/$1', ['filter' => 'adminauthcsrf']);
$routes->post('event/createDayHourly/(:num)/(:segment)', 'Event::postCreateDayHourly/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/updateHourly/(:num)/(:num)', 'Event::postUpdateHourly/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/updateDayHourly/(:num)/(:segment)', 'Event::postUpdateDayHourly/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/addArea/(:num)', 'Event::postAddArea/$1', ['filter' => 'adminauthcsrf']);
$routes->post('event/updateArea/(:num)/(:num)', 'Event::postUpdateArea/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/addInterest/(:num)', 'Event::postAddInterest/$1', ['filter' => 'adminauthcsrf']);
$routes->post('event/updateInterest/(:num)/(:num)', 'Event::postUpdateInterest/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/addeventAnimal/(:num)', 'Event::postAddeventAnimal/$1', ['filter' => 'adminauthcsrf']);
$routes->post('event/addEntityToInterest/(:num)/(:num)', 'Event::postAddEntityToInterest/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/addEventParticipant/(:num)', 'Event::postAddEventParticipant/$1', ['filter' => 'adminauthcsrf']);
$routes->post('event/addPlaceRemuneration/(:num)', 'Event::postAddPlaceRemuneration/$1', ['filter' => 'adminauthcsrf']);
$routes->post('event/updatePlaceRemuneration/(:segment)/(:segment)', 'Event::postUpdatePlaceRemuneration/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/addRecurrenceOverride/(:segment)', 'Event::postAddRecurrenceOverride/$1', ['filter' => 'adminauthcsrf']);
$routes->post('event/cancel/(:num)', 'Event::postCancel/$1', ['filter' => 'csrf']);
$routes->post('event/kill_recurrency/(:num)', 'Event::postKillRecurrency/$1', ['filter' => 'csrf']);
$routes->post('event/removeMultiObjectOccupation/(:num)/(:num)/(:num)', 'Event::postRemoveMultiObjectOccupation/$1/$2/$3', ['filter' => 'adminauthcsrf']);
$routes->post('event/removeEventOrganizerPage/(:num)/(:num)', 'Event::postRemoveEventOrganizerPage/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/removeEventOrganizerPartner/(:num)/(:num)', 'Event::postRemoveEventOrganizerPartner/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/removeEventOrganizerPlace/(:num)/(:num)', 'Event::postRemoveEventOrganizerPlace/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/removeEventOrganizerShop/(:num)/(:num)', 'Event::postRemoveEventOrganizerShop/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/removeUserParticipant/(:num)/(:num)', 'Event::postRemoveUserParticipant/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/removeShopParticipant/(:num)/(:num)', 'Event::postRemoveShopParticipant/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/removePlaceParticipant/(:num)/(:num)', 'Event::postRemovePlaceParticipant/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/removePageParticipant/(:num)/(:num)', 'Event::postRemovePageParticipant/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/removeHobby/(:num)/(:num)', 'Event::postRemoveHobby/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/removeEventObject/(:num)/(:num)', 'Event::postRemoveEventObject/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/removeAnimal/(:num)/(:num)', 'Event::postRemoveAnimal/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/updateRegistrationState/(:num)/(:num)', 'Event::postUpdateRegistrationState/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/eventCheckTransition/(:num)/(:num)/(:num)', 'Event::postEventCheckTransition/$1/$2/$3', ['filter' => 'adminauthcsrf']);
$routes->post('event/disableRecurrenceOverride/(:num)/(:num)', 'Event::postDisableRecurrenceOverride/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('event/deleteCharact/(:segment)/(:segment)/(:num)/(:num)', 'Event::postDeleteCharact/$1/$2/$3/$4', ['filter' => 'adminauthcsrf']);

// EventOrganizer
$routes->post('eventOrganizer/deleteParticipant/(:num)', 'EventOrganizer::postDeleteParticipant/$1', ['filter' => 'adminauthcsrf']);
$routes->get('eventOrganizer', 'EventOrganizer::getIndex', ['filter' => 'adminauth']);
$routes->get('eventOrganizer/tariffs', 'EventOrganizer::getTariffs', ['filter' => 'adminauth']);

// EventSerie
$routes->get('eventSerie', 'EventSerie::getIndex', ['filter' => 'adminauth']);
$routes->get('eventSerie/list', 'EventSerie::getList', ['filter' => 'adminauth']);
$routes->get('eventSerie/show/(:any)', 'EventSerie::getShow/$1', ['filter' => 'adminauth']);
$routes->get('eventSerie/add', 'EventSerie::getAdd', ['filter' => 'adminauth']);
$routes->get('eventSerie/edit/(:num)', 'EventSerie::getEdit/$1', ['filter' => 'adminauth']);
$routes->post('eventSerie/addObject/(:num)', 'EventSerie::postAddObject/$1', ['filter' => 'adminauthcsrf']);
$routes->post('eventSerie/publishEdition/(:num)', 'EventSerie::postPublishEdition/$1', ['filter' => 'csrf']);
$routes->post('eventSerie/removeHobby/(:num)/(:num)', 'EventSerie::postRemoveHobby/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('eventSerie/removeEventObject/(:num)/(:num)', 'EventSerie::postRemoveEventObject/$1/$2', ['filter' => 'adminauthcsrf']);

// EventSerieReview
$routes->post('eventSerieReview/decide/(:num)', 'EventSerieReview::postDecide/$1', ['filter' => 'csrf']);
$routes->get('eventSerieReview', 'EventSerieReview::getIndex', ['filter' => 'adminauth']);

// Experience
$routes->get('experience', 'Experience::getIndex', ['filter' => 'adminauth']);
$routes->get('experience/show/(:any)', 'Experience::getShow/$1', ['filter' => 'adminauth']);
$routes->get('experience/add', 'Experience::getAdd', ['filter' => 'adminauth']);
$routes->get('experience/add/(:num)', 'Experience::getAdd/$1', ['filter' => 'adminauth']);
$routes->get('experience/addEventExperience/(:num)', 'Experience::getAddEventExperience/$1', ['filter' => 'adminauth']);
$routes->post('experience/createLocalVariation/(:num)', 'Experience::postCreateLocalVariation/$1', ['filter' => 'adminauthcsrf']);
$routes->post('experience/updateExperience/(:num)', 'Experience::postUpdateExperience/$1', ['filter' => 'adminauthcsrf']);
$routes->post('experience/addExperience/(:num)/(:segment)', 'Experience::postAddExperience/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('experience/addOpportunity/(:num)', 'Experience::postAddOpportunity/$1', ['filter' => 'adminauthcsrf']);
$routes->post('experience/addExperienceHobby/(:num)', 'Experience::postAddExperienceHobby/$1', ['filter' => 'adminauthcsrf']);
$routes->post('experience/updateExperienceHobby/(:num)/(:num)', 'Experience::postUpdateExperienceHobby/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('experience/addLanguage/(:num)', 'Experience::postAddLanguage/$1', ['filter' => 'adminauthcsrf']);
$routes->post('experience/addSessionConf/(:num)', 'Experience::postAddSessionConf/$1', ['filter' => 'adminauthcsrf']);
$routes->post('experience/updateSessionConf/(:num)/(:num)', 'Experience::postUpdateSessionConf/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('experience/addSessionException/(:num)/(:num)', 'Experience::postAddSessionException/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('experience/addSessionRecurrenceOverride/(:num)/(:num)', 'Experience::postAddSessionRecurrenceOverride/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('experience/addSessionConfContent/(:num)/(:num)', 'Experience::postAddSessionConfContent/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('experience/updateSessionConfContent/(:num)/(:num)', 'Experience::postUpdateSessionConfContent/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('experience/removeLanguage/(:num)/(:num)', 'Experience::postRemoveLanguage/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('experience/activateSessionConf/(:num)/(:num)', 'Experience::postActivateSessionConf/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('experience/deactivateSessionConf/(:num)/(:num)', 'Experience::postDeactivateSessionConf/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('experience/useSessionConf/(:num)/(:num)', 'Experience::postUseSessionConf/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('experience/disableSessionConfContent/(:num)/(:num)', 'Experience::postDisableSessionConfContent/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('experience/disableSessionRecurrenceOverride/(:num)/(:num)', 'Experience::postDisableSessionRecurrenceOverride/$1/$2', ['filter' => 'adminauthcsrf']);

// Exploitation
$routes->get('', 'Exploitation::getIndex');
$routes->get('exploitation/paiements', 'Exploitation::getPaiements', ['filter' => 'adminauth']);
$routes->get('exploitation/revenus', 'Exploitation::getRevenus', ['filter' => 'adminauth']);
$routes->get('exploitation/resume', 'Exploitation::getResume', ['filter' => 'adminauth']);
$routes->get('exploitation/resume/(:segment)', 'Exploitation::getResume/$1', ['filter' => 'adminauth']);

// FeePolicy
$routes->post('feepolicy/add', 'FeePolicy::postAdd', ['filter' => 'adminauthcsrf']);

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
$routes->get('izilifeSelection', 'IzilifeSelection::getIndex', ['filter' => 'adminauth']);
$routes->get('izilifeSelection/list', 'IzilifeSelection::getList', ['filter' => 'adminauth']);
$routes->get('izilifeSelection/show/(:segment)', 'IzilifeSelection::getShow/$1', ['filter' => 'adminauth']);

// LocalHabit
$routes->get('localHabit', 'LocalHabit::getIndex', ['filter' => 'adminauth']);
$routes->get('localHabit/list', 'LocalHabit::getList', ['filter' => 'adminauth']);
$routes->get('localHabit/show/(:any)', 'LocalHabit::getShow/$1', ['filter' => 'adminauth']);
$routes->get('localHabit/form', 'LocalHabit::getForm', ['filter' => 'adminauth']);
$routes->get('localHabit/form/(:num)', 'LocalHabit::getForm/$1', ['filter' => 'adminauth']);
$routes->post('localHabit/removeHobby/(:num)/(:num)', 'LocalHabit::postRemoveHobby/$1/$2', ['filter' => 'csrf']);
$routes->post('localHabit/removeMedia/(:num)/(:num)', 'LocalHabit::postRemoveMedia/$1/$2', ['filter' => 'csrf']);
$routes->post('localHabit/save', 'LocalHabit::postSave', ['filter' => 'csrf']);
$routes->post('localHabit/delete', 'LocalHabit::postDelete', ['filter' => 'csrf']);
$routes->post('localHabit/addHobby/(:num)', 'LocalHabit::postAddHobby/$1', ['filter' => 'csrf']);
$routes->post('localHabit/addMedia/(:num)', 'LocalHabit::postAddMedia/$1', ['filter' => 'csrf']);
$routes->post('localHabit/updateMedia/(:num)/(:num)', 'LocalHabit::postUpdateMedia/$1/$2', ['filter' => 'csrf']);

// Locality
$routes->get('locality/adChildren', 'Locality::getAdChildren', ['filter' => 'adminauth']);
$routes->get('locality/adCities', 'Locality::getAdCities', ['filter' => 'adminauth']);
$routes->post('locality/searchLocation', 'Locality::postSearchLocation', ['filter' => 'adminauthcsrf']);

// Location
$routes->post('location/ajaxSearchCities', 'Location::postAjaxSearchCities');
$routes->get('location/ajaxSearchPlaces', 'Location::getAjaxSearchPlaces');
$routes->get('location/ajaxSearchShops', 'Location::getAjaxSearchShops');
$routes->post('location/ajaxSearchLocations', 'Location::postAjaxSearchLocations');
$routes->post('location/ajaxSearchPlaces', 'Location::postAjaxSearchPlaces');
$routes->post('location/ajaxSearchShops', 'Location::postAjaxSearchShops');
$routes->post('location/ajaxSearchOrganizers', 'Location::postAjaxSearchOrganizers');

// Media
$routes->get('media', 'Media::getIndex', ['filter' => 'adminauth']);
$routes->get('media/list', 'Media::getList', ['filter' => 'adminauth']);
$routes->get('media/list/(:segment)', 'Media::getList/$1', ['filter' => 'adminauth']);
$routes->get('media/list/(:segment)/(:num)', 'Media::getList/$1/$2', ['filter' => 'adminauth']);
$routes->get('media/jsonList', 'Media::getJsonList', ['filter' => 'adminauth']);
$routes->get('media/jsonList/(:segment)', 'Media::getJsonList/$1', ['filter' => 'adminauth']);
$routes->get('media/jsonList/(:segment)/(:num)', 'Media::getJsonList/$1/$2', ['filter' => 'adminauth']);
$routes->post('media/addGlobal', 'Media::postAddGlobal', ['filter' => 'adminauthcsrf']);
$routes->post('media/setContext/(:num)', 'Media::postSetContext/$1', ['filter' => 'adminauthcsrf']);
$routes->post('media/updateGlobal/(:num)', 'Media::postUpdateGlobal/$1', ['filter' => 'adminauthcsrf']);
$routes->post('media/setTags/(:segment)/(:num)/(:num)', 'Media::postSetTags/$1/$2/$3', ['filter' => 'adminauthcsrf']);
$routes->post('media/removeFromBrunch/(:segment)/(:num)/(:num)', 'Media::postRemoveFromBrunch/$1/$2/$3', ['filter' => 'adminauthcsrf']);
$routes->post('media/remove/(:segment)/(:num)/(:num)', 'Media::postRemove/$1/$2/$3', ['filter' => 'csrf']);

// Monitoring
$routes->get('monitoring/metier', 'Monitoring::getIndex');
$routes->get('monitoring', 'Monitoring::getIndex', ['filter' => 'adminauth']);

// Newsletter
$routes->get('newsletter', 'Newsletter::getIndex', ['filter' => 'adminauth']);
$routes->get('newsletter/create', 'Newsletter::getCreate', ['filter' => 'adminauth']);
$routes->get('newsletter/edit/(:segment)', 'Newsletter::getEdit/$1', ['filter' => 'adminauth']);
$routes->get('newsletter/preview/(:segment)', 'Newsletter::getPreview/$1', ['filter' => 'adminauth']);
$routes->post('newsletter/send/(:segment)', 'Newsletter::postSend/$1', ['filter' => 'adminauthcsrf']);

// Offer
$routes->post('offer/save', 'Offer::postSave', ['filter' => 'adminauthcsrf']);
$routes->post('offer/saveByJson', 'Offer::postSaveByJson', ['filter' => 'adminauthcsrf']);
$routes->post('offers/toggle', 'Offer::postToggle', ['filter' => 'adminauthcsrf']);
$routes->post('offers/delete', 'Offer::postDelete', ['filter' => 'adminauthcsrf']);

// OfferManagement
$routes->get('offerManagement', 'OfferManagement::getIndex', ['filter' => 'adminauth']);
$routes->get('offerManagement/create', 'OfferManagement::getCreate', ['filter' => 'adminauth']);
$routes->get('offerManagement/show/(:segment)', 'OfferManagement::getShow/$1', ['filter' => 'adminauth']);
$routes->get('offerManagement/edit/(:segment)', 'OfferManagement::getEdit/$1', ['filter' => 'adminauth']);
$routes->post('offerManagement/duplicate/(:segment)', 'OfferManagement::postDuplicate/$1', ['filter' => 'adminauthcsrf']);
$routes->post('offerManagement/save', 'OfferManagement::postSave', ['filter' => 'adminauthcsrf']);
$routes->post('offerManagement/effectSave/(:num)', 'OfferManagement::postEffectSave/$1', ['filter' => 'adminauthcsrf']);
$routes->post('offerManagement/decision/(:num)', 'OfferManagement::postDecision/$1', ['filter' => 'adminauthcsrf']);

// OpeningCampain
$routes->post('openingCampain/save', 'OpeningCampain::postSave', ['filter' => 'adminauthcsrf']);
$routes->post('opening-campains/save', 'OpeningCampain::postSave', ['filter' => 'adminauthcsrf']);
$routes->post('opening-campains/toggle', 'OpeningCampain::postToggle', ['filter' => 'adminauthcsrf']);
$routes->post('opening-campains/delete', 'OpeningCampain::postDelete', ['filter' => 'adminauthcsrf']);

// Page
$routes->get('page', 'Page::getIndex', ['filter' => 'adminauth']);
$routes->get('page/show/(:any)', 'Page::getShow/$1', ['filter' => 'adminauth']);
$routes->post('page/addInProgram/(:num)', 'Page::postAddInProgram/$1', ['filter' => 'adminauthcsrf']);
$routes->post('page/addInProgramFromList/(:num)', 'Page::postAddInProgramFromList/$1', ['filter' => 'adminauthcsrf']);
$routes->post('page/add', 'Page::postAdd', ['filter' => 'csrf']);

// PartnerObjectRequest
$routes->post('partnerObjectRequest/createTransfer', 'PartnerObjectRequest::postCreateTransfer', ['filter' => 'csrf']);
$routes->post('partnerObjectRequest/decide/(:num)', 'PartnerObjectRequest::postDecide/$1', ['filter' => 'csrf']);
$routes->post('partnerObjectRequest/execute/(:num)', 'PartnerObjectRequest::postExecute/$1', ['filter' => 'csrf']);
$routes->get('partnerObjectRequest', 'PartnerObjectRequest::getIndex', ['filter' => 'adminauth']);

// Place
$routes->get('place', 'Place::getIndex', ['filter' => 'adminauth']);
$routes->get('place/show/(:any)', 'Place::getShow/$1', ['filter' => 'adminauth']);
$routes->get('place/add', 'Place::getAdd', ['filter' => 'adminauth']);
$routes->get('place/add/(:num)', 'Place::getAdd/$1', ['filter' => 'adminauth']);
$routes->get('place/showEntityToInterest/(:num)/(:num)', 'Place::getShowEntityToInterest/$1/$2', ['filter' => 'adminauth']);
$routes->post('place/addPlaceHobby/(:num)', 'Place::postAddPlaceHobby/$1', ['filter' => 'adminauthcsrf']);
$routes->post('place/updatePlaceHobby/(:num)/(:num)', 'Place::postUpdatePlaceHobby/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/addPlaceObject/(:num)', 'Place::postAddPlaceObject/$1', ['filter' => 'adminauthcsrf']);
$routes->post('place/addPlaceOtherToiletAccess/(:num)', 'Place::postAddPlaceOtherToiletAccess/$1', ['filter' => 'adminauthcsrf']);
$routes->post('place/addOtherCategory/(:num)', 'Place::postAddOtherCategory/$1', ['filter' => 'adminauthcsrf']);
$routes->post('place/addPlaceProximity/(:num)', 'Place::postAddPlaceProximity/$1', ['filter' => 'adminauthcsrf']);
$routes->post('place/addPlaceShopProximity/(:num)', 'Place::postAddPlaceShopProximity/$1', ['filter' => 'adminauthcsrf']);
$routes->post('place/updateAnecdote/(:num)/(:num)', 'Place::postUpdateAnecdote/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/accessInfos/(:num)/(:segment)', 'Place::postAccessInfos/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/updateQuestion/(:num)/(:num)', 'Place::postUpdateQuestion/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/addPlaceAnimal/(:num)', 'Place::postAddPlaceAnimal/$1', ['filter' => 'adminauthcsrf']);
$routes->post('place/addArtCollection/(:num)', 'Place::postAddArtCollection/$1', ['filter' => 'adminauthcsrf']);
$routes->post('place/updateArtCollection/(:num)/(:num)', 'Place::postUpdateArtCollection/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/addArtPiece/(:num)', 'Place::postAddArtPiece/$1', ['filter' => 'adminauthcsrf']);
$routes->post('place/updateArtPiece/(:num)/(:num)', 'Place::postUpdateArtPiece/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/addHourly/(:num)', 'Place::postAddHourly/$1', ['filter' => 'adminauthcsrf']);
$routes->post('place/updateHourly/(:num)/(:num)', 'Place::postUpdateHourly/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/addHourlyContentsByText/(:num)/(:num)', 'Place::postAddHourlyContentsByText/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/updateHourlyContentsByText/(:num)/(:num)', 'Place::postUpdateHourlyContentsByText/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/createHourlyContent/(:num)/(:num)/(:num)', 'Place::postCreateHourlyContent/$1/$2/$3', ['filter' => 'adminauthcsrf']);
$routes->post('place/updateHourlyContent/(:num)/(:num)/(:num)', 'Place::postUpdateHourlyContent/$1/$2/$3', ['filter' => 'adminauthcsrf']);
$routes->post('place/addExceptionalHourly/(:num)', 'Place::postAddExceptionalHourly/$1', ['filter' => 'adminauthcsrf']);
$routes->post('place/addMediasFromUrlList/(:num)', 'Place::postAddMediasFromUrlList/$1', ['filter' => 'adminauthcsrf']);
$routes->post('place/addBookingConf/(:num)', 'Place::postAddBookingConf/$1', ['filter' => 'adminauthcsrf']);
$routes->post('place/updateBookingConf/(:num)/(:num)', 'Place::postUpdateBookingConf/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/addBookingConfContent/(:num)/(:num)', 'Place::postAddBookingConfContent/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/updateBookingConfContent/(:num)/(:num)', 'Place::postUpdateBookingConfContent/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/addAccessAndBookingConfInfos/(:num)', 'Place::postAddAccessAndBookingConfInfos/$1', ['filter' => 'adminauthcsrf']);
$routes->post('place/updateAccessAndBookingConfInfos/(:num)/(:num)', 'Place::postUpdateAccessAndBookingConfInfos/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/addBuilding/(:num)', 'Place::postAddBuilding/$1', ['filter' => 'adminauthcsrf']);
$routes->post('place/updateBuilding/(:num)/(:num)', 'Place::postUpdateBuilding/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/addArea/(:num)', 'Place::postAddArea/$1', ['filter' => 'adminauthcsrf']);
$routes->post('place/updateArea/(:num)/(:num)', 'Place::postUpdateArea/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/addInterest/(:num)', 'Place::postAddInterest/$1', ['filter' => 'adminauthcsrf']);
$routes->post('place/updateInterest/(:num)/(:num)', 'Place::postUpdateInterest/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/addEntityToInterest/(:num)/(:num)', 'Place::postAddEntityToInterest/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/addUnderArea/(:num)', 'Place::postAddUnderArea/$1', ['filter' => 'adminauthcsrf']);
$routes->post('place/updateUnderArea/(:num)/(:num)', 'Place::postUpdateUnderArea/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/removeOtherCategory/(:num)/(:num)/(:alpha)', 'Place::postRemoveOtherCategory/$1/$2/$3', ['filter' => 'adminauthcsrf']);
$routes->post('place/removeHobby/(:num)/(:num)', 'Place::postRemoveHobby/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/removePlaceObject/(:num)/(:num)', 'Place::postRemovePlaceObject/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/removePlaceOtherToiletAccess/(:num)/(:num)', 'Place::postRemovePlaceOtherToiletAccess/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/removeAnimal/(:num)/(:num)', 'Place::postRemoveAnimal/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/deleteArea/(:num)/(:num)', 'Place::postDeleteArea/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/activateBookingConf/(:num)/(:num)', 'Place::postActivateBookingConf/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/deactivateBookingConf/(:num)/(:num)', 'Place::postDeactivateBookingConf/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/useBookingConf/(:num)/(:num)', 'Place::postUseBookingConf/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/disableBookingConfContent/(:num)/(:num)', 'Place::postDisableBookingConfContent/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('place/deleteCharact/(:segment)/(:segment)/(:num)/(:num)', 'Place::postDeleteCharact/$1/$2/$3/$4', ['filter' => 'adminauthcsrf']);
$routes->post('place/improvePlaceFromGoogle/(:segment)', 'Place::postImprovePlaceFromGoogle/$1', ['filter' => 'adminauthcsrf']);
$routes->post('place/removeMultiObjectOccupation/(:num)/(:num)/(:num)', 'Place::postRemoveMultiObjectOccupation/$1/$2/$3', ['filter' => 'adminauthcsrf']);

// PopupOccurrence
$routes->post('popupOccurrence/create/(:segment)/(:num)', 'PopupOccurrence::postCreate/$1/$2', ['filter' => 'csrf']);
$routes->post('popupOccurrence/update/(:segment)/(:num)/(:num)', 'PopupOccurrence::postUpdate/$1/$2/$3', ['filter' => 'csrf']);
$routes->post('popupOccurrence/delete/(:segment)/(:num)/(:num)', 'PopupOccurrence::postDelete/$1/$2/$3', ['filter' => 'csrf']);

// PspOnboarding
$routes->post('psp/onboarding/launch/(:segment)/(:segment)/(:segment)', 'PspOnboarding::launch/$1/$2/$3', ['filter' => 'adminauthcsrf']);
$routes->post('psp/onboarding/open/(:segment)/(:segment)/(:segment)', 'PspOnboarding::open/$1/$2/$3', ['filter' => 'adminauthcsrf']);
$routes->post('psp/onboarding/status/(:segment)/(:segment)/(:segment)', 'PspOnboarding::status/$1/$2/$3', ['filter' => 'adminauthcsrf']);
$routes->post('psp/onboarding/set-current/(:num)', 'PspOnboarding::setCurrent/$1', ['filter' => 'csrf']);
$routes->post('psp/onboarding/deactivate/(:num)', 'PspOnboarding::deactivate/$1', ['filter' => 'csrf']);

// Remuneration
$routes->post('remuneration/add', 'Remuneration::postAdd', ['filter' => 'adminauthcsrf']);
$routes->post('remuneration/add-multi-conf', 'Remuneration::postAddMultiRemunerationConf', ['filter' => 'adminauthcsrf']);
$routes->post('remuneration/activate-multi', 'Remuneration::postActivateMultiRemuneration', ['filter' => 'adminauthcsrf']);

// Representation
$routes->get('representation', 'Representation::getIndex', ['filter' => 'adminauth']);
$routes->get('representation/show/(:any)', 'Representation::getShow/$1', ['filter' => 'adminauth']);
$routes->post('representation/addRepresentationAnimal/(:num)', 'Representation::postAddRepresentationAnimal/$1', ['filter' => 'adminauthcsrf']);
$routes->post('representation/addRepresentationHobby/(:num)', 'Representation::postAddRepresentationHobby/$1', ['filter' => 'adminauthcsrf']);
$routes->post('representation/updateRepresentationHobby/(:num)/(:num)', 'Representation::postUpdateRepresentationHobby/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('representation/addPerfectFor/(:num)', 'Representation::postAddPerfectFor/$1', ['filter' => 'adminauthcsrf']);
$routes->post('representation/updatePerfectFor/(:num)', 'Representation::postUpdatePerfectFor/$1', ['filter' => 'adminauthcsrf']);
$routes->post('representation/removeHobby/(:num)/(:num)', 'Representation::postRemoveHobby/$1/$2', ['filter' => 'csrf']);
$routes->post('representation/removeAnimal/(:num)/(:num)', 'Representation::postRemoveAnimal/$1/$2', ['filter' => 'csrf']);

// Scopes
$routes->get('scopes', 'Scopes::getIndex');
$routes->get('scopes/create', 'Scopes::getCreate');
$routes->get('scopes/edit/(:num)', 'Scopes::getEdit/$1');
$routes->post('scopes/save', 'Scopes::postSave', ['filter' => 'csrf']);
$routes->post('scopes/addRule/(:num)', 'Scopes::postAddRule/$1', ['filter' => 'csrf']);
$routes->post('scopes/deleteRule/(:num)/(:num)', 'Scopes::postDeleteRule/$1/$2', ['filter' => 'csrf']);

// Scraper
$routes->get('scraper', 'Scraper::getIndex', ['filter' => 'adminauth']);
$routes->get('scraper/(:num)', 'Scraper::getIndex/$1', ['filter' => 'adminauth']);
$routes->get('scraper/home/(:num)', 'Scraper::getHome/$1', ['filter' => 'adminauth']);
$routes->get('scraper/choicePoiImport/(:num)', 'Scraper::getChoicePoiImport/$1', ['filter' => 'adminauth']);
$routes->get('scraper/events_review', 'Scraper::getEvents_review', ['filter' => 'adminauth']);
$routes->get('scraper/events_review/(:num)', 'Scraper::getEvents_review/$1', ['filter' => 'adminauth']);
$routes->get('scraper/experiences_review/(:num)', 'Scraper::getExperiences_review/$1', ['filter' => 'adminauth']);
$routes->get('scraper/validationRequests', 'Scraper::getValidationRequests', ['filter' => 'adminauth']);
$routes->get('scraper/validationRequests/(:num)', 'Scraper::getValidationRequests/$1', ['filter' => 'adminauth']);
$routes->get('scraper/googleImportLogs/(:num)', 'Scraper::getGoogleImportLogs/$1', ['filter' => 'adminauth']);
$routes->get('scraper/cityByStringId/(:segment)', 'Scraper::getCityByStringId/$1');
$routes->get('scraper/editionSourceUrl/(:num)', 'Scraper::getEditionSourceUrl/$1', ['filter' => 'adminauth']);
$routes->post('scraper/agentSuggestPlace/(:segment)', 'Scraper::postAgentSuggestPlace/$1', ['filter' => 'csrf']);
$routes->post('scraper/agentFetchAndStoreOnePlace/(:segment)', 'Scraper::postAgentFetchAndStoreOnePlace/$1');
$routes->post('scraper/agentFetchAndStorePlaces/(:segment)', 'Scraper::postAgentFetchAndStorePlaces/$1');
$routes->post('scraper/agentUploadEventSources/(:num)', 'Scraper::postAgentUploadEventSources/$1');
$routes->post('scraper/agentUploadEventImages/(:num)', 'Scraper::postAgentUploadEventImages/$1');
$routes->post('scraper/agentIngestPromo/(:num)', 'Scraper::postAgentIngestPromo/$1');
$routes->post('scraper/agentGetPlaceByStringId', 'Scraper::postAgentGetPlaceByStringId');
$routes->post('scraper/agentGetCity/(:segment)', 'Scraper::postAgentGetCity/$1');
$routes->post('scraper/agentGetPlacesToEnrich', 'Scraper::postAgentGetPlacesToEnrich');
$routes->post('scraper/prepareCompetitionEditionFromAgent', 'Scraper::postPrepareCompetitionEditionFromAgent');
$routes->post('scraper/enrichCompetitionTeamsFromAgent', 'Scraper::postEnrichCompetitionTeamsFromAgent');
$routes->post('scraper/importCompetitionScheduleApiFromAgent/(:num)', 'Scraper::postImportCompetitionScheduleApiFromAgent/$1');
$routes->post('scraper/competitionSyncPlanFromAgent', 'Scraper::postCompetitionSyncPlanFromAgent');
$routes->post('scraper/importCompetitionScheduleFromAgent/(:num)', 'Scraper::postImportCompetitionScheduleFromAgent/$1');
$routes->post('scraper/rejectScrapedEvent/(:num)', 'Scraper::postRejectScrapedEvent/$1', ['filter' => 'adminauthcsrf']);
$routes->post('scraper/rejectScrapedExperience/(:num)', 'Scraper::postRejectScrapedExperience/$1', ['filter' => 'adminauthcsrf']);
$routes->post('scraper/rejectValidationRequest/(:num)', 'Scraper::postRejectValidationRequest/$1', ['filter' => 'adminauthcsrf']);
$routes->post('scraper/confirmExperience/(:num)/(:num)', 'Scraper::postConfirmExperience/$1/$2', ['filter' => 'csrf']);
$routes->post('scraper/confirmEvent/(:num)/(:num)', 'Scraper::postConfirmEvent/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('scraper/classifyPoi/(:num)/(:num)', 'Scraper::postClassifyPoi/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('scraper/scrapEventsFromBloggerWebsite/(:num)', 'Scraper::postScrapEventsFromBloggerWebsite/$1', ['filter' => 'adminauthcsrf']);
$routes->post('scraper/uploadEventImages/(:num)', 'Scraper::postUploadEventImages/$1', ['filter' => 'adminauthcsrf']);
$routes->post('scraper/scrapExperiencesFromBloggerWebsite/(:num)', 'Scraper::postScrapExperiencesFromBloggerWebsite/$1', ['filter' => 'adminauthcsrf']);
$routes->post('scraper/importProducts/(:num)', 'Scraper::postImportProducts/$1', ['filter' => 'adminauthcsrf']);
$routes->post('scraper/fetchAndStoreOnePlace/(:segment)', 'Scraper::postFetchAndStoreOnePlace/$1', ['filter' => 'adminauthcsrf']);
$routes->post('scraper/uploadEventSources/(:num)', 'Scraper::postUploadEventSources/$1', ['filter' => 'adminauthcsrf']);
$routes->post('scraper/uploadEventSourcesReplacement/(:num)', 'Scraper::postUploadEventSourcesReplacement/$1', ['filter' => 'adminauthcsrf']);
$routes->post('scraper/approveValidationRequest/(:num)', 'Scraper::postApproveValidationRequest/$1', ['filter' => 'adminauthcsrf']);
$routes->post('scraper/home', 'Scraper::postHome', ['filter' => 'csrf']);
$routes->post('scraper/confirmEvent/(:num)/(:num)', 'Scraper::postConfirmEvent/$1/$2', ['filter' => 'csrf']);
$routes->post('scraper/classifyPoi/(:num)/(:num)', 'Scraper::postClassifyPoi/$1/$2', ['filter' => 'csrf']);

// ScrapingHub
$routes->post('scrapingHub/addCity/(:num)', 'ScrapingHub::postAddCity/$1', ['filter' => 'adminauthcsrf']);
$routes->post('scrapingHub/saveEndpoint/(:num)', 'ScrapingHub::postSaveEndpoint/$1', ['filter' => 'adminauthcsrf']);
$routes->post('scrapingHub/deleteEndpoint/(:num)/(:num)', 'ScrapingHub::postDeleteEndpoint/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('scrapingHub/savePlaceQuery/(:num)', 'ScrapingHub::postSavePlaceQuery/$1', ['filter' => 'adminauthcsrf']);
$routes->post('scrapingHub/runNow/(:num)', 'ScrapingHub::postRunNow/$1', ['filter' => 'adminauthcsrf']);
$routes->post('scrapingHub/runPlaceQuery/(:num)/(:num)', 'ScrapingHub::postRunPlaceQuery/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->get('scrapingHub', 'ScrapingHub::getIndex', ['filter' => 'adminauth']);
$routes->get('scrapingHub/create', 'ScrapingHub::getCreate', ['filter' => 'adminauth']);
$routes->get('scrapingHub/edit/(:num)', 'ScrapingHub::getEdit/$1', ['filter' => 'adminauth']);
$routes->get('scrapingHub/placeQueryRuns/(:num)/(:num)', 'ScrapingHub::getPlaceQueryRuns/$1/$2', ['filter' => 'adminauth']);

// Scrapping
$routes->post('scrapping/enrichCharactsAndOtherInformations/(:segment)', 'Scrapping::postEnrichCharactsAndOtherInformations/$1', ['filter' => 'adminauthcsrf']);

// Shop
$routes->get('shop', 'Shop::getIndex', ['filter' => 'adminauth']);
$routes->get('shop/show/(:any)', 'Shop::getShow/$1', ['filter' => 'adminauth']);
$routes->get('shop/create', 'Shop::getCreate', ['filter' => 'adminauth']);
$routes->get('shop/create/(:num)', 'Shop::getCreate/$1', ['filter' => 'adminauth']);
$routes->get('shop/places/(:num)', 'Shop::getPlaces/$1', ['filter' => 'adminauth']);
$routes->get('shop/characteristics/(:num)', 'Shop::getCharacteristics/$1', ['filter' => 'adminauth']);
$routes->get('shop/showAddInterest/(:num)', 'Shop::getShowAddInterest/$1', ['filter' => 'adminauth']);
$routes->get('shop/showEntityToInterest/(:num)/(:num)', 'Shop::getShowEntityToInterest/$1/$2', ['filter' => 'adminauth']);
$routes->post('shop/createShop', 'Shop::postCreateShop', ['filter' => 'adminauthcsrf']);
$routes->post('shop/updateShop/(:num)', 'Shop::postUpdateShop/$1', ['filter' => 'adminauthcsrf']);
$routes->post('shop/addOtherCategory/(:num)', 'Shop::postAddOtherCategory/$1', ['filter' => 'adminauthcsrf']);
$routes->post('shop/addShopOtherToiletAccess/(:num)', 'Shop::postAddShopOtherToiletAccess/$1', ['filter' => 'adminauthcsrf']);
$routes->post('shop/addHourly/(:num)', 'Shop::postAddHourly/$1', ['filter' => 'adminauthcsrf']);
$routes->post('shop/updateHourly/(:num)/(:num)', 'Shop::postUpdateHourly/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/addHourlyContentsByText/(:num)/(:num)', 'Shop::postAddHourlyContentsByText/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/updateHourlyContentsByText/(:num)/(:num)', 'Shop::postUpdateHourlyContentsByText/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/createHourlyContent/(:num)/(:num)/(:num)', 'Shop::postCreateHourlyContent/$1/$2/$3', ['filter' => 'adminauthcsrf']);
$routes->post('shop/updateHourlyContent/(:num)/(:num)/(:num)', 'Shop::postUpdateHourlyContent/$1/$2/$3', ['filter' => 'adminauthcsrf']);
$routes->post('shop/addExceptionalHourly/(:num)', 'Shop::postAddExceptionalHourly/$1', ['filter' => 'adminauthcsrf']);
$routes->post('shop/createItinerantHourlyPlace/(:num)/(:num)/(:num)', 'Shop::postCreateItinerantHourlyPlace/$1/$2/$3', ['filter' => 'adminauthcsrf']);
$routes->post('shop/updateItinerantHourlyPlace/(:num)/(:num)/(:num)/(:num)', 'Shop::postUpdateItinerantHourlyPlace/$1/$2/$3/$4', ['filter' => 'adminauthcsrf']);
$routes->post('shop/addExceptionalItinerantHourlyPlace/(:num)', 'Shop::postAddExceptionalItinerantHourlyPlace/$1', ['filter' => 'adminauthcsrf']);
$routes->post('shop/updateExceptionalItinerantHourlyPlace/(:num)/(:segment)/(:num)', 'Shop::postUpdateExceptionalItinerantHourlyPlace/$1/$2/$3', ['filter' => 'adminauthcsrf']);
$routes->post('shop/addSpecialMealTypeHourly/(:num)', 'Shop::postAddSpecialMealTypeHourly/$1', ['filter' => 'adminauthcsrf']);
$routes->post('shop/updateSpecialMealTypeHourly/(:num)/(:num)', 'Shop::postUpdateSpecialMealTypeHourly/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/createItinerantPlace/(:num)', 'Shop::postCreateItinerantPlace/$1', ['filter' => 'adminauthcsrf']);
$routes->post('shop/itinerantPlaceUpdate/(:num)/(:num)', 'Shop::postItinerantPlaceUpdate/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/addShopHobby/(:num)', 'Shop::postAddShopHobby/$1', ['filter' => 'adminauthcsrf']);
$routes->post('shop/updateShopHobby/(:num)/(:num)', 'Shop::postUpdateShopHobby/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/principalCharacteristics/(:num)/(:segment)', 'Shop::postPrincipalCharacteristics/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/addKaraokeRoom/(:num)', 'Shop::postAddKaraokeRoom/$1', ['filter' => 'adminauthcsrf']);
$routes->post('shop/updateKaraokeRoom/(:num)/(:num)', 'Shop::postUpdateKaraokeRoom/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/addBookableBoowling/(:num)', 'Shop::postAddBookableBoowling/$1', ['filter' => 'adminauthcsrf']);
$routes->post('shop/updateBookableBowlingAlley/(:num)/(:num)', 'Shop::postUpdateBookableBowlingAlley/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/addArea/(:num)', 'Shop::postAddArea/$1', ['filter' => 'adminauthcsrf']);
$routes->post('shop/updateArea/(:num)/(:num)', 'Shop::postUpdateArea/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/addInterest/(:num)', 'Shop::postAddInterest/$1', ['filter' => 'adminauthcsrf']);
$routes->post('shop/updateInterest/(:num)/(:num)', 'Shop::postUpdateInterest/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/addEntityToInterest/(:num)/(:num)', 'Shop::postAddEntityToInterest/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/addMediasFromUrlList/(:num)', 'Shop::postAddMediasFromUrlList/$1', ['filter' => 'adminauthcsrf']);
$routes->post('shop/addShopObject/(:num)', 'Shop::postAddShopObject/$1', ['filter' => 'adminauthcsrf']);
$routes->post('shop/addBookingConf/(:num)', 'Shop::postAddBookingConf/$1', ['filter' => 'adminauthcsrf']);
$routes->post('shop/updateBookingConf/(:num)/(:num)', 'Shop::postUpdateBookingConf/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/addBookingConfContent/(:num)/(:num)', 'Shop::postAddBookingConfContent/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/updateBookingConfContent/(:num)/(:num)', 'Shop::postUpdateBookingConfContent/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/addAccessAndBookingConfInfos/(:num)', 'Shop::postAddAccessAndBookingConfInfos/$1', ['filter' => 'adminauthcsrf']);
$routes->post('shop/updateAccessAndBookingConfInfos/(:num)/(:num)', 'Shop::postUpdateAccessAndBookingConfInfos/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/removeMultiObjectOccupation/(:num)/(:num)/(:num)', 'Shop::postRemoveMultiObjectOccupation/$1/$2/$3', ['filter' => 'adminauthcsrf']);
$routes->post('shop/activateBookingConf/(:num)/(:num)', 'Shop::postActivateBookingConf/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/deactivateBookingConf/(:num)/(:num)', 'Shop::postDeactivateBookingConf/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/useBookingConf/(:num)/(:num)', 'Shop::postUseBookingConf/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/disableBookingConfContent/(:num)/(:num)', 'Shop::postDisableBookingConfContent/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/deleteCharact/(:segment)/(:segment)/(:num)/(:num)', 'Shop::postDeleteCharact/$1/$2/$3/$4', ['filter' => 'adminauthcsrf']);
$routes->post('shop/createShopPage/(:num)', 'Shop::postCreateShopPage/$1', ['filter' => 'csrf']);
$routes->post('shop/improveShopFromGoogle/(:segment)', 'Shop::postImproveShopFromGoogle/$1', ['filter' => 'adminauthcsrf']);
$routes->post('shop/removeOtherCategory/(:num)/(:num)/(:alpha)', 'Shop::postRemoveOtherCategory/$1/$2/$3', ['filter' => 'adminauthcsrf']);
$routes->post('shop/removeShopOtherToiletAccess/(:num)/(:num)', 'Shop::postRemoveShopOtherToiletAccess/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/removeHobby/(:num)/(:num)', 'Shop::postRemoveHobby/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('shop/removeShopObject/(:num)/(:num)', 'Shop::postRemoveShopObject/$1/$2', ['filter' => 'adminauthcsrf']);

// SpatialGeometry
$routes->post('spatialGeometry/upload/(:segment)/(:num)', 'SpatialGeometry::postUpload/$1/$2', ['filter' => 'adminauthcsrf']);
$routes->post('spatialGeometry/delete/(:num)', 'SpatialGeometry::postDelete/$1', ['filter' => 'adminauthcsrf']);

// StripeWebhook
$routes->post('stripe/webhook', 'StripeWebhook::index');

// Terrace
$routes->get('terrace/show/(:any)', 'Terrace::getShow/$1', ['filter' => 'adminauth']);
$routes->post('terrace/removeMedia/(:num)/(:num)', 'Terrace::postRemoveMedia/$1/$2', ['filter' => 'adminauthcsrf']);

// User
$routes->get('user', 'User::getIndex', ['filter' => 'adminauth']);
$routes->get('user/show/(:any)', 'User::getShow/$1', ['filter' => 'adminauth']);
$routes->post('user/addInProgram/(:num)', 'User::postAddInProgram/$1', ['filter' => 'adminauthcsrf']);
$routes->post('user/addInProgramFromList/(:num)', 'User::postAddInProgramFromList/$1', ['filter' => 'adminauthcsrf']);
$routes->post('user/closeUnclosedValidations/(:num)', 'User::postCloseUnclosedValidations/$1', ['filter' => 'adminauthcsrf']);
