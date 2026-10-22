# Partner — AJAX/HTTP call sites

Static source candidates only: verify the rendered URL and method before using as a runtime test. Paths are generated through app helpers; never hard-code a local subdirectory prefix. FO controller names previously identified as inactive are flagged and excluded from the active test set pending owner confirmation.

| Scope | Method (inferred) | API | Endpoint expression | Source |
|---|---|---|---|---|
| Reachability unverified | POST | jQuery | `$form.attr('action')` | `app/Views/common_components/access_prices/add_access_price_modal.php:314` |
| Reachability unverified | POST | jQuery | `'<?= base_url('/accessPrice/addGroupedPrice'` | `app/Views/common_components/access_prices/element_access_price_group_modal.php:75` |
| Reachability unverified | POST | jQuery | `'<?= base_url('/accessPrice/updateGroupedPrice'` | `app/Views/common_components/access_prices/element_access_price_group_modal.php:96` |
| Reachability unverified | POST | jQuery | `'<?= base_url('/accessPrice/deleteGroupedPrice'` | `app/Views/common_components/access_prices/element_access_price_group_modal.php:116` |
| Reachability unverified | POST | jQuery | `'<?= base_url('/accessPrice/addPackItem'` | `app/Views/common_components/access_prices/element_access_price_pack_composition.php:78` |
| Reachability unverified | POST | jQuery | `'<?= base_url('/accessPrice/updatePackItem'` | `app/Views/common_components/access_prices/element_access_price_pack_composition.php:99` |
| Reachability unverified | POST | jQuery | `'<?= base_url('/accessPrice/deletePackItem'` | `app/Views/common_components/access_prices/element_access_price_pack_composition.php:120` |
| Reachability unverified | POST | jQuery | `action` | `app/Views/common_components/access_prices/show_eaps_content.php:240` |
| Reachability unverified | POST | jQuery | `'<?= site_url('accessPrice/linkEAPToCategories'` | `app/Views/common_components/access_prices/show_eaps_content.php:286` |
| Reachability unverified | POST | jQuery | `'<?= site_url('accessPrice/unlinkEAPFromCategory'` | `app/Views/common_components/access_prices/show_eaps_content.php:300` |
| Reachability unverified | POST | jQuery | `'<?= site_url('accessPrice/linkEAPToEquipments'` | `app/Views/common_components/access_prices/show_eaps_content.php:323` |
| Reachability unverified | POST | jQuery | `'<?= site_url('accessPrice/postUnlinkEAPFromEquipment'` | `app/Views/common_components/access_prices/show_eaps_content.php:337` |
| Reachability unverified | GET* | fetch | `url` | `app/Views/common_components/izi_credit_payment_modal.php:17` |
| Reachability unverified | POST | fetch | `<?=json_encode(site_url('partner-assistant/interpret'` | `app/Views/common_components/partner_ai_assistant.php:18` |
| Reachability unverified | POST | fetch | `<?=json_encode(site_url('partner-assistant/create-booking'` | `app/Views/common_components/partner_ai_assistant.php:19` |
| Reachability unverified | POST | fetch | `u` | `app/Views/common_components/qr_code_and_link.php:19` |
| Reachability unverified | POST | fetch | `<?=json_encode(base_url('trackedLink/create'` | `app/Views/common_components/qr_code_and_link.php:20` |
| Reachability unverified | POST | jQuery | `url` | `app/Views/layouts/common_js_methods.php:256` |
| Reachability unverified | POST | jQuery | `endpoint` | `app/Views/layouts/common_js_methods.php:301` |
| Reachability unverified | GET* | fetch | `'<?= base_url('meetz/ajax/occurrence/group-users'` | `app/Views/meetz/occurrence_show.php:206` |
| Reachability unverified | POST | fetch | `url` | `app/Views/partners/billing/payment.php:14` |
| Reachability unverified | POST | jQuery | `"<?php echo base_url() . "index.php/product/createProduct";?>"` | `app/Views/shops/library_shop_page.php:836` |
