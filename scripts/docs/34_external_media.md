# 34 — ElementExternalMedia

## But

Attacher des médias externes à un objet : Instagram, Facebook, TikTok, YouTube, website embed.

## Sheet

```text
izilife/external_media/{zone}-zone/external_media.xlsx
```

## Champs

```text
target_ref
target_type
target_string_id
target_id
media_source
external_url
embed_code
author_username
author_page_ref
display_order
is_active
statut
last_result
```

## Règle

`target_ref` peut être une URL izilife ou un `string_id`.

Si `target_ref` est une URL izilife, le BO résout le scope.

Si `target_ref` est un `string_id`, `target_type` est obligatoire.
