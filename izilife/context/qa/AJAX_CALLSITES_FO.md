# FO — AJAX/HTTP call sites

Static source candidates only: verify the rendered URL and method before using as a runtime test. Paths are generated through app helpers; never hard-code a local subdirectory prefix. FO controller names previously identified as inactive are flagged and excluded from the active test set pending owner confirmation.

| Scope | Method (inferred) | API | Endpoint expression | Source |
|---|---|---|---|---|
| Reachability unverified | GET* | fetch | `loadMore.getAttribute('data-next-url'` | `app/Views/benefits/history.php:199` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>author/follow/"` | `app/Views/books/author.php:563` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>book/changeAgeFilter/"` | `app/Views/books/category.php:1045` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>book/changeAgeFilter2/"` | `app/Views/books/category.php:1062` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>book/changeContentTypeFilter/"` | `app/Views/books/category.php:1078` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>book/changeContentTypeFilter2/"` | `app/Views/books/category.php:1095` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>book/postReview"` | `app/Views/books/show_book.php:1549` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>author/follow/"` | `app/Views/books/show_book.php:1570` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>book/postReview"` | `app/Views/books/show_imported_book.php:942` |
| Reachability unverified | POST | fetch | `url` | `app/Views/cart/show_cart_js_and_css.php:49` |
| Reachability unverified | GET* | fetch | `button.dataset.urlTemplate.replace('{offset}'` | `app/Views/catalogue/browse.php:45` |
| Reachability unverified | GET* | fetch | `modal.dataset.previewUrl` | `app/Views/catalogue/product_modal_loader.php:22` |
| Reachability unverified | GET* | fetch | `modal.dataset.previewUrl` | `app/Views/catalogue/product_modal_loader.php:29` |
| Reachability unverified | GET | XMLHttpRequest | `path` | `app/Views/coming-soon.php:57` |
| Reachability unverified | POST | jQuery | `"<?= base_url() . "location/save"; ?>"` | `app/Views/common_components/get_user_position_js_script - Copie.php:18` |
| Reachability unverified | POST | jQuery | `"<?= base_url() . "location/failed"; ?>"` | `app/Views/common_components/get_user_position_js_script - Copie.php:33` |
| Reachability unverified | POST | jQuery | `"<?= base_url() . "location/failed"; ?>"` | `app/Views/common_components/get_user_position_js_script - Copie.php:78` |
| Reachability unverified | POST | jQuery | `"<?= base_url() . "location/failed"; ?>"` | `app/Views/common_components/get_user_position_js_script - Copie.php:111` |
| Reachability unverified | POST | jQuery | `"<?= base_url() . "location/use_user_position"; ?>"` | `app/Views/common_components/get_user_position_js_script - Copie.php:146` |
| Reachability unverified | POST | jQuery | `"<?= base_url() . "location/failed"; ?>"` | `app/Views/common_components/get_user_position_js_script - Copie.php:158` |
| Reachability unverified | POST | jQuery | `"<?= base_url() . "location/failed"; ?>"` | `app/Views/common_components/get_user_position_js_script - Copie.php:199` |
| Reachability unverified | POST | jQuery | `"<?= base_url() . "location/failed"; ?>"` | `app/Views/common_components/get_user_position_js_script - Copie.php:229` |
| Reachability unverified | POST | jQuery | `computed/dynamic — inspect source` | `app/Views/common_components/get_user_position_js_script.php:44` |
| Reachability unverified | GET* | fetch | `'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=' + encodeURIComponent(lat` | `app/Views/common_components/location/geolocation_picker.php:55` |
| Reachability unverified | POST | jQuery | `ENDPOINT_SAVE` | `app/Views/common_components/location_tracking.php:32` |
| Reachability unverified | GET* | fetch | `ajaxUrl+'?offset='+offset+'&filter='+encodeURIComponent(filter` | `app/Views/common_components/medias/show_mixed_media_swiper.php:149` |
| Reachability unverified | GET* | fetch | `endpoint` | `app/Views/common_components/show_offer_action_modal.php:48` |
| Reachability unverified | POST | fetch | `'<?= base_url('review/react'` | `app/Views/common_components/show_reviews.php:623` |
| Reachability unverified | POST | fetch | `url` | `app/Views/common_components/show_vecus.php:47` |
| Reachability unverified | POST | fetch | `<?=json_encode(base_url('vecu/react'` | `app/Views/common_components/show_vecus.php:48` |
| Reachability unverified | POST | fetch | `'<?= base_url('community/searchTargets/'.$targetType.'/'.$target->string_id` | `app/Views/communities/components/community_modals_and_js.php:9` |
| Reachability unverified | POST | fetch | `'<?= base_url('community/react'` | `app/Views/communities/components/community_modals_and_js.php:9` |
| Reachability unverified | GET* | fetch | `\`<?= base_url('communityActivity/targets'` | `app/Views/communities/personal_activity_form.php:35` |
| Reachability unverified | POST | fetch | `'<?= base_url('localhabit/react'` | `app/Views/editorial_objects/_local_habit_reactions.php:26` |
| Reachability unverified | POST | fetch | `'<?= base_url('elementNews/react'` | `app/Views/element_news/news_feed.php:24` |
| Reachability unverified | POST | jQuery | `"<?= base_url() . "event/user_registration"; ?>"` | `app/Views/events/components/show_event_modals_css_and_js.php:79` |
| Reachability unverified | POST | jQuery | `"<?= base_url('event/set_interest_status'); ?>"` | `app/Views/events/components/show_event_modals_css_and_js.php:121` |
| Reachability unverified | POST | fetch | `choices.dataset.url` | `app/Views/experiences/components/show_experience_booking.php:500` |
| Reachability unverified | GET* | fetch | `'https://nominatim.openstreetmap.org/search?format=jsonv2&addressdetails=1&limit=5&q=' + encodeURIComponent(query` | `app/Views/experiences/select_purchased_booking.php:88` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>activity/load_more/"` | `app/Views/home_news_feed.php:176` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>kidactivity/changeAgeFilter/"` | `app/Views/kids/activities_category.php:924` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>kidactivity/changeAgeFilter2/"` | `app/Views/kids/activities_category.php:941` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>kidactivity/changeLevelFilter/"` | `app/Views/kids/activities_category.php:960` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>kidactivity/changeParticipationFilter/"` | `app/Views/kids/activities_category.php:977` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>kidactivity/changeLevelFilter2/"` | `app/Views/kids/activities_category.php:994` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>kidactivity/changeParticipationFilter2/"` | `app/Views/kids/activities_category.php:1009` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>kidactivity/changePlayTypeFilter/"` | `app/Views/kids/activities_category.php:1024` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>kidactivity/changePlayTypeFilter2/"` | `app/Views/kids/activities_category.php:1041` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter/"` | `app/Views/kids/contents_category.php:715` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter2/"` | `app/Views/kids/contents_category.php:732` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>home/service_choosed/"` | `app/Views/kids/home.php:246` |
| Reachability unverified | POST | fetch | `endpoint` | `app/Views/layouts/client_analytics.php:33` |
| Reachability unverified | POST | jQuery | `"<?= base_url() . 'user/toggle_favorite'; ?>"` | `app/Views/layouts/common_js_methods.php:128` |
| Reachability unverified | GET | XMLHttpRequest | `path` | `app/Views/layouts/common_js_methods.php:363` |
| Reachability unverified | POST | jQuery | `baseUrl + "user/toggle_follow"` | `app/Views/layouts/common_js_methods.php:601` |
| Reachability unverified | POST | jQuery | `baseUrl + "user/toggle_follow"` | `app/Views/layouts/common_js_methods.php:650` |
| Reachability unverified | POST | jQuery | `base_site + '/map/preview'` | `app/Views/layouts/common_js_methods.php:787` |
| Reachability unverified | POST | jQuery | `"<?= base_url('user/save_object_modal'); ?>"` | `app/Views/layouts/common_js_methods.php:909` |
| Reachability unverified | POST | jQuery | `"<?= base_url('user/toggle_list_item'); ?>"` | `app/Views/layouts/common_js_methods.php:931` |
| Reachability unverified | POST | jQuery | `"<?= base_url('user/create_user_list_ajax'); ?>"` | `app/Views/layouts/common_js_methods.php:973` |
| Reachability unverified | GET | jQuery | `"<?= base_url('user/save_object_modal'); ?>"` | `app/Views/layouts/common_js_methods.php:1028` |
| Reachability unverified | POST | jQuery | `"<?= base_url('user/toggle_list_item'); ?>"` | `app/Views/layouts/common_js_methods.php:1057` |
| Reachability unverified | POST | jQuery | `"<?= base_url('user/create_user_list_ajax'); ?>"` | `app/Views/layouts/common_js_methods.php:1104` |
| Reachability unverified | GET | jQuery | `"<?= base_url('user/event_calendar_links'); ?>"` | `app/Views/layouts/common_js_methods.php:1141` |
| Reachability unverified | POST | jQuery | `"<?= base_url('user/toggle_object_status'); ?>"` | `app/Views/layouts/common_js_methods.php:1225` |
| Reachability unverified | GET* | fetch | `endpoint + '?q=' + encodeURIComponent(query` | `app/Views/layouts/common_js_methods.php:1442` |
| Reachability unverified | GET | fetch | `url` | `app/Views/meetz/onboarding/onboarding_personnality.php:256` |
| Reachability unverified | POST | fetch | `\`<?=esc(base_url('offer/'` | `app/Views/offers/purchase_cart.php:5` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>home/service_choosed/"` | `app/Views/old_welcome/connected_welcome_page_books.php:622` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>home/service_choosed/"` | `app/Views/old_welcome/welcome_page.php:188` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>home/service_choosed/"` | `app/Views/old_welcome/welcome_page_books.php:632` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>home/service_choosed/"` | `app/Views/old_welcome/welcome_parents.php:298` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>home/service_choosed/"` | `app/Views/old_welcome/welcome_parents_old.php:308` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>location/searchCity"` | `app/Views/old_welcome_outings.php:257` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>location/changeCity"` | `app/Views/old_welcome_outings.php:276` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>location/searchCity"` | `app/Views/old_welcome_outings.php:301` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>location/changeCity"` | `app/Views/old_welcome_outings.php:320` |
| Reachability unverified | POST | jQuery | `"<?= base_url() . "location/use_user_position"; ?>"` | `app/Views/old_welcome_outings.php:344` |
| Reachability unverified | POST | jQuery | `"<?= base_url() . "location/failed"; ?>"` | `app/Views/old_welcome_outings.php:355` |
| Reachability unverified | POST | jQuery | `"<?= base_url() . "location/failed"; ?>"` | `app/Views/old_welcome_outings.php:386` |
| Reachability unverified | POST | jQuery | `"<?= base_url() . "location/failed"; ?>"` | `app/Views/old_welcome_outings.php:400` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>outing/search_city/"` | `app/Views/outings/home.php:132` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>outing/changeOutingCity/"` | `app/Views/outings/home.php:151` |
| Reachability unverified | POST | fetch | `"<?= base_url('payment/intent/create'` | `app/Views/payment/page_v2.php:57` |
| Reachability unverified | POST | fetch | `"<?= base_url('payment/intent/confirm_saved'` | `app/Views/payment/page_v2.php:92` |
| Reachability unverified | GET* | fetch | `<?= json_encode(base_url('payment/status/'` | `app/Views/payment/return_processing.php:25` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>product/productCharacteristicInfos"` | `app/Views/plans/home.php:407` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>plan/addToBasket/"` | `app/Views/plans/home.php:504` |
| Reachability unverified | POST | jQuery | `"<?= base_url(); ?>cart/addEventAndExperienceProducts"` | `app/Views/products/show_product_modals_js_and_css.php:545` |
| Reachability unverified | POST | jQuery | `"<?= base_url(); ?>cart/addEventAndExperienceProducts"` | `app/Views/products/show_product_modals_js_and_css.php:790` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>reading/like_post/"` | `app/Views/reading/activity.php:872` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>reading/dislike_post/"` | `app/Views/reading/activity.php:884` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>reading/like_activity/"` | `app/Views/reading/activity.php:900` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>reading/dislike_activity/"` | `app/Views/reading/activity.php:912` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>reading/comment/"` | `app/Views/reading/activity.php:929` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>reading/like_post/"` | `app/Views/reading/reading.php:1037` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>reading/dislike_post/"` | `app/Views/reading/reading.php:1049` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>reading/like_activity/"` | `app/Views/reading/reading.php:1065` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>reading/dislike_activity/"` | `app/Views/reading/reading.php:1077` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>reading/comment/"` | `app/Views/reading/reading.php:1094` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>reading/follow/"` | `app/Views/reading/reading.php:1137` |
| Reachability unverified | POST | fetch | `'<?=base_url('reservation/postTrack'` | `app/Views/reservations/booking_page.php:83` |
| Reachability unverified | POST | fetch | `u` | `app/Views/reservations/booking_page.php:86` |
| Reachability unverified | POST | fetch | `url` | `app/Views/reservations/booking_page.php:90` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter/"` | `app/Views/search_engine/activities_search.php:556` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter2/"` | `app/Views/search_engine/activities_search.php:573` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter/"` | `app/Views/search_engine/contents_search.php:502` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter2/"` | `app/Views/search_engine/contents_search.php:519` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter/"` | `app/Views/search_engine/personages_search.php:408` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter2/"` | `app/Views/search_engine/personages_search.php:425` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter/"` | `app/Views/search_engine/universes_search.php:408` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter2/"` | `app/Views/search_engine/universes_search.php:425` |
| Reachability unverified | GET* | fetch | `\`<?= base_url('home/discovery-blocks'` | `app/Views/second_welcome_outings.php:167` |
| Reachability unverified | GET* | fetch | `url.toString(` | `app/Views/selections/components/trip_details/participations.php:209` |
| Reachability unverified | GET* | fetch | `url.toString(` | `app/Views/selections/components/trip_details/participations.php:255` |
| Reachability unverified | GET | fetch | `url` | `app/Views/selections/components/trip_details/participations.php:327` |
| Reachability unverified | GET* | fetch | `url` | `app/Views/selections/components/trip_details/participations_items.php:81` |
| Reachability unverified | GET* | fetch | `url + '?entitlement_uid=' + encodeURIComponent(entitlementUid` | `app/Views/selections/components/trip_details/participations_items.php:117` |
| Reachability unverified | GET* | fetch | `url.toString(` | `app/Views/selections/components/trip_details/reviews.php:278` |
| Reachability unverified | GET* | fetch | `url` | `app/Views/selections/selection_purchase_detail.php:198` |
| Reachability unverified | GET* | fetch | `url + '?entitlement_uid=' + encodeURIComponent(entitlementUid` | `app/Views/selections/selection_purchase_detail.php:232` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>shop/postReview"` | `app/Views/shops/components/show_shop_modals_css_and_js.php:261` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>shop/add_favourite"` | `app/Views/shops/components/show_shop_modals_css_and_js.php:284` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>product/productCharacteristicInfos"` | `app/Views/shops/components/show_shop_modals_css_and_js.php:303` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>shop/createRestaurantBooking"` | `app/Views/shops/components/show_shop_modals_css_and_js.php:424` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>product/productCharacteristicGroups"` | `app/Views/shops/shop_old_js_function.php:19` |
| Reachability unverified | GET | jQuery | `"<?php echo base_url(); ?>location/searchCity"` | `app/Views/some_js_scripts.php:76` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>location/changeCity"` | `app/Views/some_js_scripts.php:95` |
| Reachability unverified | GET | jQuery | `"<?php echo base_url(); ?>location/searchCity"` | `app/Views/some_js_scripts.php:115` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>location/changeCity"` | `app/Views/some_js_scripts.php:134` |
| Reachability unverified | GET | jQuery | `"<?php echo base_url(); ?>location/searchCity"` | `app/Views/some_js_scripts.php:154` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>location/changeCity"` | `app/Views/some_js_scripts.php:173` |
| Reachability unverified | POST | jQuery | `"<?= base_url('location/changeRadius') ?>"` | `app/Views/some_js_scripts.php:196` |
| Reachability unverified | POST | jQuery | `"<?= base_url() . "location/use_user_position"; ?>"` | `app/Views/some_js_scripts.php:216` |
| Reachability unverified | POST | jQuery | `"<?= base_url() . "location/failed"; ?>"` | `app/Views/some_js_scripts.php:232` |
| Reachability unverified | POST | jQuery | `"<?= base_url() . "location/failed"; ?>"` | `app/Views/some_js_scripts.php:266` |
| Reachability unverified | POST | jQuery | `"<?= base_url() . "location/failed"; ?>"` | `app/Views/some_js_scripts.php:283` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter/"` | `app/Views/spaces/kidactivities_learning_space.php:525` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter2/"` | `app/Views/spaces/kidactivities_learning_space.php:542` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter/"` | `app/Views/spaces/kidactivities_personage_space.php:579` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter2/"` | `app/Views/spaces/kidactivities_personage_space.php:596` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter/"` | `app/Views/spaces/kidactivities_theme_space.php:539` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter2/"` | `app/Views/spaces/kidactivities_theme_space.php:556` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter/"` | `app/Views/spaces/kidactivities_universe_space.php:569` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter2/"` | `app/Views/spaces/kidactivities_universe_space.php:586` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter/"` | `app/Views/spaces/kidcontents_learning_space.php:503` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter2/"` | `app/Views/spaces/kidcontents_learning_space.php:520` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter/"` | `app/Views/spaces/kidcontents_personage_space.php:523` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter2/"` | `app/Views/spaces/kidcontents_personage_space.php:540` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter/"` | `app/Views/spaces/kidcontents_theme_space.php:510` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter2/"` | `app/Views/spaces/kidcontents_theme_space.php:527` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter/"` | `app/Views/spaces/kidcontents_universe_space.php:547` |
| Inactive candidate — exclude pending confirmation | POST | jQuery | `"<?php echo base_url(); ?>kidcontent/changeAgeFilter2/"` | `app/Views/spaces/kidcontents_universe_space.php:564` |
| Reachability unverified | inspect | jQuery | `"https://api-adresse.data.gouv.fr/search/?q="+$("input[name='address']").val()` | `app/Views/users/user_personal_informations.php:325` |
| Reachability unverified | POST | jQuery | `<?= json_encode(base_url('user/follow/')` | `app/Views/users/user_profile.php:278` |
| Reachability unverified | POST | jQuery | `<?= json_encode(base_url('activity/load_more_user_activities/')` | `app/Views/users/user_profile.php:297` |
| Reachability unverified | inspect | jQuery | `"https://api-adresse.data.gouv.fr/search/?q="+$("input[name='address']").val()` | `app/Views/users/user_subscription.php:220` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>home/service_choosed/"` | `app/Views/welcome_outings_test.php:312` |
| Reachability unverified | GET | jQuery | `settings.jsonFile` | `statics/js/map-category.js:61` |
