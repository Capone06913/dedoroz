# Система обложек

## Формат

- 16:9, целевой размер 1200×675.
- PNG или JPG без текста.
- Серия одна: `macro_detail`.
- Сборка промпта: `global_prompt_prefix` + сцена темы + `global_prompt_suffix`.

## MCP

Инструмент генерации по контракту — `user-mcp-kv` / `gpt-image-2`. Его нет в текущем namespace. Обложки не генерировать через flux, grok, seedream, nano banana или z-image.

Cutout для этой серии не нужен: макро лежит на своём тёмном фоне, `requires_background_removal: false`. `recraft_remove_background` не вызывать, пока в кадре нет отделяемого предмета на чужой подложке.

Style anchor: `teya-memory/design/assets/blog-cover-style-anchor.png` — файла нет, статус blocked.

## QA серии

- В кадре нет лица, бороды, рук, ребёнка.
- Нет букв и водяного знака.
- Нет снега на весь кадр.
- Палитра не уезжает в открыточный алый и в золотой плакат с бокалами.
- Две соседние темы отличаются предметом, не стилем.
- Превью 320px всё ещё показывает, что это ткань или металл, а не пятно.

## Темы

`AURA_BLOG_COVER_PROMPTS.json` в статусе `awaiting_topics`, пока нет `11-blog-topics.md`. Тексты статей не писать.
