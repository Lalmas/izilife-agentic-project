# BO — AJAX/HTTP call sites

Static source candidates only: verify the rendered URL and method before using as a runtime test. Paths are generated through app helpers; never hard-code a local subdirectory prefix. FO controller names previously identified as inactive are flagged and excluded from the active test set pending owner confirmation.

| Scope | Method (inferred) | API | Endpoint expression | Source |
|---|---|---|---|---|
| Reachability unverified | POST | jQuery | `"<?= base_url('employeeAccess/ajaxSearchEmployees'); ?>"` | `app/Views/admin/access/index.php:34` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>index.php/editor/editor_choosed/"` | `app/Views/books/add_book.php:335` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url(); ?>index.php/editor/editor_choosed/"` | `app/Views/books/show_book.php:1806` |
| Reachability unverified | POST | jQuery | `$form.attr('action')` | `app/Views/common_components/access_prices/add_access_price_modal.php:349` |
| Reachability unverified | POST | jQuery | `'<?= base_url('/accessPrice/addGroupedPrice'` | `app/Views/common_components/access_prices/element_access_price_group_modal.php:75` |
| Reachability unverified | POST | jQuery | `'<?= base_url('/accessPrice/updateGroupedPrice'` | `app/Views/common_components/access_prices/element_access_price_group_modal.php:96` |
| Reachability unverified | POST | jQuery | `'<?= base_url('/accessPrice/deleteGroupedPrice'` | `app/Views/common_components/access_prices/element_access_price_group_modal.php:116` |
| Reachability unverified | POST | jQuery | `'<?= base_url('/accessPrice/addPackItem'` | `app/Views/common_components/access_prices/element_access_price_pack_composition.php:78` |
| Reachability unverified | POST | jQuery | `'<?= base_url('/accessPrice/updatePackItem'` | `app/Views/common_components/access_prices/element_access_price_pack_composition.php:99` |
| Reachability unverified | POST | jQuery | `'<?= base_url('/accessPrice/deletePackItem'` | `app/Views/common_components/access_prices/element_access_price_pack_composition.php:120` |
| Reachability unverified | POST | jQuery | `action` | `app/Views/common_components/access_prices/show_eaps_content.php:264` |
| Reachability unverified | POST | jQuery | `'<?= site_url('accessPrice/linkEAPToCategories'` | `app/Views/common_components/access_prices/show_eaps_content.php:310` |
| Reachability unverified | POST | jQuery | `'<?= site_url('accessPrice/unlinkEAPFromCategory'` | `app/Views/common_components/access_prices/show_eaps_content.php:324` |
| Reachability unverified | POST | jQuery | `'<?= site_url('accessPrice/linkEAPToEquipments'` | `app/Views/common_components/access_prices/show_eaps_content.php:347` |
| Reachability unverified | POST | jQuery | `'<?= site_url('accessPrice/unlinkEAPFromEquipment'` | `app/Views/common_components/access_prices/show_eaps_content.php:361` |
| Reachability unverified | GET* | fetch | `'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=' + encodeURIComponent(lat` | `app/Views/common_components/location/geolocation_picker.php:55` |
| Reachability unverified | POST | fetch | `u` | `app/Views/common_components/qr_code_and_link.php:82` |
| Reachability unverified | POST | fetch | `root.dataset.toggleBase+'/'+toggle.dataset.id` | `app/Views/common_components/qr_code_and_link.php:86` |
| Reachability unverified | GET | jQuery | `'https://api-adresse.data.gouv.fr/search/'` | `app/Views/common_components/sessions_and_bookings/session_location_fields.php:51` |
| Reachability unverified | POST | jQuery | `'<?= base_url('location/ajaxSearchCities'` | `app/Views/intercommunalities/form.php:22` |
| Reachability unverified | POST | jQuery | `url` | `app/Views/layouts/common_js_methods.php:324` |
| Reachability unverified | POST | jQuery | `endpoint` | `app/Views/layouts/common_js_methods.php:508` |
| Reachability unverified | POST | jQuery | `url` | `app/Views/layouts/common_js_methods.php:550` |
| Reachability unverified | GET | jQuery | `API_CHILDREN` | `app/Views/layouts/search_location_conf.php:169` |
| Reachability unverified | GET | jQuery | `API_CITIES` | `app/Views/layouts/search_location_conf.php:195` |
| Reachability unverified | GET | jQuery | `API_CHILDREN` | `app/Views/layouts/search_location_conf.php:231` |
| Reachability unverified | GET | jQuery | `API_CITIES` | `app/Views/layouts/search_location_conf.php:255` |
| Reachability unverified | GET* | fetch | `'<?= base_url('meetz/ajax/occurrence/group-users'` | `app/Views/meetz/occurrence_show.php:206` |
| Reachability unverified | POST | jQuery | `endpoint` | `app/Views/newsletter/html_editor.php:142` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url() . "index.php/product/createProduct";?>"` | `app/Views/partners/partner_page.php:529` |
| Reachability unverified | POST | jQuery | `"<?= base_url('location/ajaxSearchCities'); ?>"` | `app/Views/scraping/event_validation_modal.php:328` |
| Reachability unverified | POST | jQuery | `"<?= base_url('location/ajaxSearchLocations'); ?>"` | `app/Views/scraping/event_validation_modal.php:388` |
| Reachability unverified | POST | fetch | `scope.dataset.endpoint` | `app/Views/scraping/experience_validation_modal.php:107` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url() . "index.php/product/createProduct";?>"` | `app/Views/shops/library_shop_page.php:838` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url() . "index.php/product/createProduct";?>"` | `app/Views/shops/shop_page.php:3016` |
