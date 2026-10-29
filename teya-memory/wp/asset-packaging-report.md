# Отчёт упаковки ассетов — dedmoroz-nn

**Тема:** `dedmoroz-nn`  
**Собрано:** 2026-10-28T03:22:49+00:00  
**Источник живых кадров:** `ded/` — те же файлы, что в `AURA_ASSET_REGISTRY.json`  
**Проверка:** сигнатура байтов + Pillow `verify()` + повторный `load()`. Content-type HTTP не использовался.  
**Вердикт:** BLOCKER

Живые jpg для пяти страниц упакованы и проверены. Brand-kit и якорь обложек не собраны.

## Сводка

| Метрика | Значение |
| --- | ---: |
| Записей в реестре | 17 |
| Упаковано в тему, decode_verified | 9 |
| Сгенерировано через MCP | 0 |
| Фон снят | 0 |
| Запас и отложенные кадры, в тему не клались | 6 |
| Блокеры генерации | 2 |

## Пять страниц

Один и тот же файл на разных страницах — повтор, который уже записан в `AURA_SECTION_BLUEPRINTS.json`. Лица не подменялись.

| Страница | Кадры | Минимум | Факт |
| --- | --- | ---: | ---: |
| `/` | show-hero, classic-hero, show-dance, welcome-guest, hall-banquet, stage-vocal, classic-studio | 6 | 7 |
| `/korporativ/` | show-hero, show-dance, stage-vocal, welcome-guest | 3 | 4 |
| `/na-dom/` | family-home, family-visit | 2 | 2 |
| `/sad-i-shkola/` | classic-studio | 1 | 1 |
| `/zayavka/` | stage-vocal | 1 | 1 |

## Упакованные jpg

Каждый файл существует в `teya-memory/wp/theme/dedmoroz-nn/assets/images/`. Байты совпадают с исходником в `ded/`. Сигнатура `FF D8 FF` совпадает с расширением `.jpg`. Pillow `verify()` и `load()` прошли. `decode_verified: true`.

| id | формат | байты | размер | sha256 | путь |
| --- | --- | ---: | --- | --- | --- |
| show-hero | jpeg | 1607417 | 2560×1708 | `1ce0cab1b4feb67ec0aa157ade5b3bb59a12cc340aba06a7252c34c93a29aeb4` | `assets/images/show-hero.jpg` |
| classic-hero | jpeg | 1915272 | 1920×2560 | `2463913535fcfca1e8f90c9c0926ae9d14bd7a6c891a4af8a60f1391cbf59790` | `assets/images/classic-hero.jpg` |
| show-dance | jpeg | 315035 | 1280×853 | `06d18ed3b402b4474767940343559b992d6292bb5f97a12b1bebf1860024caa7` | `assets/images/show-dance.jpg` |
| welcome-guest | jpeg | 1245963 | 2560×1706 | `c0da09b2d0a3e8d988ed028248916c7f6d5be7d9fde544ec04f41f3323f5e9e8` | `assets/images/welcome-guest.jpg` |
| hall-banquet | jpeg | 1245025 | 2560×1706 | `f6280f522e26cfcafb505718b142f29c29e24d661ddc255f73734465467db68d` | `assets/images/hall-banquet.jpg` |
| stage-vocal | jpeg | 563264 | 1500×1000 | `673bc82fc659188733b1cf8910f7b8734423e2566a1e208decd2f9aa541617c2` | `assets/images/stage-vocal.jpg` |
| classic-studio | jpeg | 2753694 | 1920×2560 | `42caf74be9f521cf56a61f1f471dc3d825e5e143580648976eed06f81a74aee6` | `assets/images/classic-studio.jpg` |
| family-home | jpeg | 2536277 | 1920×2560 | `dc8c29520a2f165bab5464a8325a9de5412a02d5a857029d4655068bd93635f4` | `assets/images/family-home.jpg` |
| family-visit | jpeg | 2164457 | 1920×2560 | `d1e5b89b945b7e4526f114b698841658e7b73d6a37ab10737d9241d0808cfe4e` | `assets/images/family-visit.jpg` |

`show-dance` упакован без кропа: водяной знак фотографа остался в исходном кадре. `family-visit` только для `/na-dom/`: в кадре ребёнок. `hall-banquet` не подписывать именем площадки из списка кейсов.

Проверка после копирования: `teya/scripts/package_mcp_assets.py` без `--force`. Флага `--force` нет, потому что у живых кадров нет удалённого URL, а `--force` заставляет скрипт качать заново и помечает файл блокером. Скрипт заново прочитал уже лежащие jpg и подтвердил сигнатуру и Pillow.

## Вырезка фона

`recraft_remove_background` есть в `user-mcp-kv`. Вызов не делался. В реестре и инвентаре у всех кадров `requires_background_removal: false`, зон с `requires_cutout` нет. Лица на кадрах живые, замена лица запрещена. В тему легли оригинальные jpg.

## Не в теме, файлы в ded/ целые

Эти шесть jpg открываются: сигнатура JPEG, Pillow `verify()` и `load()` прошли. В тему их не копировал — так решил дизайн. Это не битые файлы.

| id | статус | байты | размер | почему не в теме |
| --- | --- | ---: | --- | --- |
| show-sg-mic | reserve | 419366 | 1280×853 | Запас шоу, не вместо героя |
| stage-moon | reserve | 812736 | 1500×1000 | Запас сцены, не дубль stage-vocal |
| club-clock | held | 262043 | 800×533 | Чужой логотип площадки |
| club-clock-2 | held | 257412 | 800×533 | Тот же клуб и чужие знаки |
| ensemble-group | held | 1436804 | 2560×1706 | Ансамбль, не витрина пары |
| ensemble-dance | held | 1335726 | 2560×1706 | Хоровод, не выход пары |

## Блокеры картинок

- **brand-kit** — файла нет. В `user-mcp-kv` нет `gpt-image-2`. Flux, Grok, Nano Banana, Seedream и Z-Image не вызывались.
- **blog-cover-style-anchor** — файла нет. Та же причина: без `gpt-image-2` якорь обложек не генерировался.

`generated_count: 0`. `background_removed_count: 0`.
