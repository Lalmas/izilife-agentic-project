<?php

use CodeIgniter\Router\RouteCollection;

/** @var RouteCollection $routes */

// REVIEW DRAFT: grouped by controller from existing explicit declarations.
// Auto-routing remains enabled; this file alone is not a complete migration.

// AnnualCelebration
$routes->post('annualCelebration/review/(:segment)', 'AnnualCelebration::review/$1', ['filter' => 'csrf']);

// Cart
$routes->get('cart', 'Cart::index');
$routes->get('cart/content', 'Cart::content');
$routes->get('cart/modal', 'Cart::modal');
$routes->post('cart/add', 'Cart::add', ['filter' => 'csrf']);
$routes->post('cart/updateQty', 'Cart::updateQty', ['filter' => 'csrf']);
$routes->post('cart/changeQty', 'Cart::changeQty', ['filter' => 'csrf']);
$routes->post('cart/remove', 'Cart::remove', ['filter' => 'csrf']);
$routes->post('cart/clear', 'Cart::clear', ['filter' => 'csrf']);
$routes->get('cart/success', 'Cart::success');

// Circuit
$routes->post('circuit/postReview/(:segment)', 'Circuit::postReview/$1', ['filter' => 'csrf']);

// Community
$routes->post('community/join/(:segment)', 'Community::join/$1', ['filter' => 'csrf']);
$routes->post('community/leave/(:segment)', 'Community::leave/$1', ['filter' => 'csrf']);
$routes->post('community/joinGroup/(:segment)', 'Community::joinGroup/$1', ['filter' => 'csrf']);
$routes->post('community/publish/(:segment)/(:segment)', 'Community::publish/$1/$2', ['filter' => 'csrf']);
$routes->post('community/comment/(:segment)', 'Community::comment/$1', ['filter' => 'csrf']);
$routes->post('community/react', 'Community::react', ['filter' => 'csrf']);
$routes->post('community/createGroup/(:segment)', 'Community::createGroup/$1', ['filter' => 'csrf']);
$routes->post('community/uploadMedia/(:segment)/(:segment)', 'Community::uploadMedia/$1/$2', ['filter' => 'csrf']);
$routes->post('community/moderateMember/(:segment)/(:segment)', 'Community::moderateMember/$1/$2', ['filter' => 'csrf']);
$routes->post('community/updateGroupSettings/(:segment)', 'Community::updateGroupSettings/$1', ['filter' => 'csrf']);
$routes->post('community/setGroupAdmin/(:segment)', 'Community::setGroupAdmin/$1', ['filter' => 'csrf']);

// CommunityActivity
$routes->post('communityActivity/save', 'CommunityActivity::save', ['filter' => 'csrf']);
$routes->post('communityActivity/invite/(:segment)', 'CommunityActivity::invite/$1', ['filter' => 'csrf']);
$routes->post('communityActivity/respond/(:segment)', 'CommunityActivity::respond/$1', ['filter' => 'csrf']);

// Equipment
$routes->post('equipment/postReview/(:segment)', 'Equipment::postReview/$1', ['filter' => 'csrf']);

// Event
$routes->post('event/saveCommunityRsvp/(:segment)', 'Event::saveCommunityRsvp/$1', ['filter' => 'csrf']);
$routes->post('event/postReview/(:segment)', 'Event::postReview/$1', ['filter' => 'csrf']);
$routes->post('event/postReview/(:segment)/(:segment)', 'Event::postReview/$1/$2', ['filter' => 'csrf']);
$routes->post('event/user_registration', 'Event::user_registration', ['filter' => 'csrf']);
$routes->post('event/set_interest_status', 'Event::set_interest_status', ['filter' => 'csrf']);

// EventSerie
$routes->post('eventSerie/review/(:segment)', 'EventSerie::review/$1', ['filter' => 'csrf']);

// Experience
$routes->post('experience/savePurchasedBooking/(:segment)', 'Experience::savePurchasedBooking/$1', ['filter' => 'csrf']);
$routes->post('experience/saveCommunityRsvp/(:segment)', 'Experience::saveCommunityRsvp/$1', ['filter' => 'csrf']);
$routes->post('experience/postReview/(:segment)', 'Experience::postReview/$1', ['filter' => 'csrf']);

// Home
$routes->get('', 'Home::getIndex');
$routes->get('home/discovery-blocks', 'Home::getDiscoveryBlocks');

// HomeDebug
$routes->get('debug/home', 'HomeDebug::index', ['filter' => 'localdebug']);
$routes->get('debug/home/(:segment)', 'HomeDebug::index/$1', ['filter' => 'localdebug']);

// IzilifeMeetz
$routes->post('IzilifeMeetz/pay', 'IzilifeMeetz::pay', ['filter' => 'csrf']);

// IzilifePlan
$routes->post('izilifePlan/subscribe', 'IzilifePlan::subscribe', ['filter' => 'csrf']);
$routes->post('izilifePlan/changePay', 'IzilifePlan::changePay', ['filter' => 'csrf']);
$routes->get('plan/use/(:segment)', 'IzilifePlan::use/$1');
$routes->post('plan/consume', 'IzilifePlan::consume');
$routes->get('plan/proof/(:segment)', 'IzilifePlan::proof/$1');

// IzilifeSelection
$routes->post('izilifeSelections/postReview/(:segment)', 'IzilifeSelection::postReview/$1', ['filter' => 'csrf']);

// LocalHabit
$routes->post('localhabit/postReview/(:segment)', 'LocalHabit::postReview/$1', ['filter' => 'csrf']);
$routes->post('localhabit/react', 'LocalHabit::react', ['filter' => 'csrf']);

// Location
$routes->post('location/save', 'Location::save', ['filter' => 'csrf']);
$routes->post('location/use_user_position', 'Location::use_user_position', ['filter' => 'csrf']);
$routes->post('location/failed', 'Location::failed', ['filter' => 'csrf']);
$routes->get('location/searchCity', 'Location::searchCity');
$routes->post('location/changeCity', 'Location::changeCity', ['filter' => 'csrf']);
$routes->post('location/changeRadius', 'Location::changeRadius', ['filter' => 'csrf']);

// LocationResolver
$routes->get('l/(:segment)', 'LocationResolver::bySlug/$1');

// Map
$routes->post('map/preview', 'Map::preview', ['filter' => 'csrf']);

// Navigation
$routes->get('navigation/back', 'Navigation::back');
$routes->get('navigation/reset', 'Navigation::reset');

// Offer
$routes->post('offer/cartQuote/(:segment)', 'Offer::cartQuote/$1', ['filter' => 'csrf']);
$routes->post('offer/cartAdd/(:segment)', 'Offer::cartAdd/$1', ['filter' => 'csrf']);
$routes->post('offer/cartRemove/(:segment)', 'Offer::cartRemove/$1', ['filter' => 'csrf']);
$routes->post('offer/cartClear/(:segment)', 'Offer::cartClear/$1', ['filter' => 'csrf']);
$routes->post('offer/startCollective/(:segment)', 'Offer::startCollective/$1', ['filter' => 'csrf']);

// Page
$routes->post('page/postReview/(:segment)', 'Page::postReview/$1', ['filter' => 'csrf']);

// Payment
$routes->post('payment/pay', 'Payment::pay', ['filter' => 'csrf']);
$routes->get('payment/resume', 'Payment::resume');
$routes->get('payment/return', 'Payment::return');
$routes->get('payment/status/(:segment)', 'Payment::status/$1');
$routes->get('payment/cancel', 'Payment::cancel');
$routes->post('payment/cancel', 'Payment::confirmCancel', ['filter' => 'csrf']);
$routes->get('payment/page/(:segment)', 'Payment::page/$1');
$routes->post('payment/intent/create', 'Payment::createIntent', ['filter' => 'csrf']);
$routes->post('payment/intent/confirm_saved', 'Payment::confirmSavedPaymentMethod', ['filter' => 'csrf']);

// Place
$routes->post('place/postReview/(:segment)', 'Place::postReview/$1', ['filter' => 'csrf']);

// Product
$routes->post('product/productCharacteristicGroups', 'Product::productCharacteristicGroups', ['filter' => 'csrf']);
$routes->post('product/productCharacteristicInfos', 'Product::productCharacteristicInfos', ['filter' => 'csrf']);
$routes->post('product/productCompositionInfos', 'Product::productCompositionInfos', ['filter' => 'csrf']);

// Reservation
$routes->get('reservation/getAvailability/(:alpha)/(:num)', 'Reservation::getAvailability/$1/$2');
$routes->post('reservation/postCreate/(:alpha)/(:num)', 'Reservation::postCreate/$1/$2', ['filter' => 'csrf']);
$routes->post('reservation/postCreateRequest/(:alpha)/(:num)', 'Reservation::postCreateRequest/$1/$2', ['filter' => 'csrf']);
$routes->post('reservation/postTrack/(:alpha)/(:num)', 'Reservation::postTrack/$1/$2', ['filter' => 'csrf']);
$routes->get('reservation/getFollow/(:segment)', 'Reservation::getFollow/$1');
$routes->get('reservation/getFollow/(:segment)/(:segment)', 'Reservation::getFollow/$1/$2');
$routes->get('reservation/getBookingFollow/(:segment)', 'Reservation::getBookingFollow/$1');
$routes->get('reservation/getBookingFollow/(:segment)/(:segment)', 'Reservation::getBookingFollow/$1/$2');
$routes->post('reservation/postFollowMessage/(:segment)', 'Reservation::postFollowMessage/$1', ['filter' => 'csrf']);

// Review
$routes->post('review/react', 'Review::react', ['filter' => 'csrf']);

// RewardGame
$routes->get('rewards/game/start/(:segment)', 'RewardGame::start/$1');
$routes->get('rewards/game/play/(:segment)', 'RewardGame::play/$1');
$routes->get('rewards/game/resolve/(:segment)', 'RewardGame::resolve/$1');

// Search
$routes->get('search/bytext', 'Search::bytext');
$routes->get('search/results', 'Search::results');

// Shop
$routes->post('shop/postReview/(:segment)', 'Shop::postReview/$1', ['filter' => 'csrf']);

// ShortLink
$routes->get('go/(:segment)', 'ShortLink::resolve/$1');

// SuggestionDebug
$routes->get('suggestion-debug', 'SuggestionDebug::index', ['filter' => 'localdebug']);
$routes->get('suggestionDebub', 'SuggestionDebug::index', ['filter' => 'localdebug']);
$routes->get('suggestionDebug', 'SuggestionDebug::index', ['filter' => 'localdebug']);

// User
$routes->get('user/purchases', 'User::purchases');
$routes->get('user/purchases/selection/(:segment)', 'User::purchasesSelection/$1');
$routes->get('user/purchases/entitlement/use/(:segment)', 'User::purchasesUseEntitlement/$1');
$routes->post('user/purchases/redeem', 'User::purchasesCreateRedemption');
$routes->post('user/toggle_favorite', 'User::toggle_favorite', ['filter' => 'csrf']);
$routes->post('user/follow', 'User::follow', ['filter' => 'csrf']);
$routes->post('user/register', 'User::register', ['filter' => 'csrf']);
$routes->post('user/connect', 'User::connect', ['filter' => 'csrf']);
$routes->get('user/registration_validation/(:segment)', 'User::registration_validation/$1');
$routes->post('user/registration_validation/(:segment)/(:segment)', 'User::registration_validation/$1/$2', ['filter' => 'csrf']);
$routes->post('user/registration_resend_code/(:segment)/(:segment)', 'User::registration_resend_code/$1/$2', ['filter' => 'csrf']);
$routes->get('user/save_object_modal', 'User::save_object_modal');
$routes->post('user/toggle_list_item', 'User::toggle_list_item', ['filter' => 'csrf']);
$routes->post('user/create_user_list_ajax', 'User::create_user_list_ajax', ['filter' => 'csrf']);
$routes->post('user/toggle_follow', 'User::toggle_follow', ['filter' => 'csrf']);
$routes->get('user/event_calendar_links', 'User::event_calendar_links');
$routes->get('user/export_event_ics/(:num)', 'User::export_event_ics/$1');
$routes->post('user/toggle_object_status', 'User::toggle_object_status', ['filter' => 'csrf']);
$routes->post('user/toggleAutoRenewPlan', 'User::toggleAutoRenewPlan', ['filter' => 'csrf']);
$routes->post('user/subscription/cancelPlan', 'User::cancelPlan', ['filter' => 'csrf']);
$routes->post('user/subscription/pausePlan', 'User::pausePlan', ['filter' => 'csrf']);
$routes->post('user/subscription/resumePlan', 'User::resumePlan', ['filter' => 'csrf']);
$routes->get('user/password_reset', 'User::password_reset');
$routes->get('user/password_reset/choose', 'User::password_reset/choose');
$routes->post('user/password_reset/check', 'User::password_reset/check', ['filter' => 'csrf']);
$routes->post('user/password_reset/change', 'User::password_reset/change', ['filter' => 'csrf']);

// UserBenefits
$routes->get('user/benefits/history', 'UserBenefits::history');
$routes->get('user/benefits', 'UserBenefits::index');

// Stripe
$routes->post('webhooks/stripe', 'Webhooks\Stripe::index');

// Whattodo
$routes->get('que-faire', 'Whattodo::activity/evenements');
$routes->get('que-faire-a/(:segment)', 'Whattodo::activity/evenements?city=$1');
$routes->get('que-faire-a/(:segment)/(:segment)', 'Whattodo::activity/evenements?city=$1&when=$2');
$routes->get('que-faire-a/(:segment)/(:segment)/(:segment)', 'Whattodo::activity/evenements/$3?city=$1&when=$2');
