=== AURORA-TEAM-ASSET-PACKAGER (ASSETS/CUTOUTS) ===

**Тема:** `dedmoroz-nn`  
**Вердикт:** BLOCKER  
**Собрано:** 2026-10-28T03:22:49+00:00

Живые jpg пяти страниц упакованы: 9 файлов, байты совпадают с `ded/`, сигнатура JPEG, Pillow `verify()` и `load()`, `decode_verified: true`. Лица не подменялись. Вырезка фона не вызывалась: дизайн её не просит.

Brand-kit и якорь обложек не собраны. В `user-mcp-kv` нет `gpt-image-2`, другой моделью их не генерировал.

## Что сдано

- `teya-memory/wp/theme/dedmoroz-nn/assets/images/` — 9 jpg
- `teya-memory/wp/theme/dedmoroz-nn/media-map.json`
- `teya-memory/wp/asset-packaging-report.md`
- `teya-memory/design/AURA_ASSET_REGISTRY.json` — пути упакованных кадров и статусы запаса

## Страницы

- `/` — 7 кадров при минимуме 6
- `/korporativ/` — 4 при минимуме 3
- `/na-dom/` — 2 при минимуме 2
- `/sad-i-shkola/` — 1 при минимуме 1
- `/zayavka/` — 1 при минимуме 1

Повторы между страницами взяты из чертежей дизайна: show-hero, show-dance, welcome-guest, stage-vocal, classic-studio. Это те же файлы, не новые лица.

## Запас и отложенные

show-sg-mic, stage-moon, club-clock, club-clock-2, ensemble-group, ensemble-dance в `ded/` целые и декодируются. В тему не клались: резерв или чужие знаки. Это не битый растр.

incident_report:
- open: нет инцидента по живым лицам и по файлам пяти страниц. Девять jpg лежат в теме и проходят decode.
- blocker: в user-mcp-kv нет gpt-image-2. Brand-kit и blog-cover-style-anchor не собраны. recraft_remove_background в списке tools есть, но не вызывался: requires_background_removal везде false, вырезка заменила бы живой кадр. Другой моделью графику не генерировал.
