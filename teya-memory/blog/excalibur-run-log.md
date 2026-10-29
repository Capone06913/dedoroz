# Excalibur run log

date: 2026-10-28
wave: BT01, BT02, BT05
deploy_mode: local-only
allow_publish: no
handoff_01: not_written

## Сделано

Три статьи написаны локально. WordPress не вызывался. `01-handoff.md` не менялся. Дизайн и семантика сайта не менялись. Субагенты не запускались.

| topic_id | slug | знаков | QA | объём | обложка | публикация |
|---|---|---:|---|---|---|---|
| BT01 | skolko-stoit-ded-moroz-v-nizhnem-novgorode | 8833 | PASS 94/100 | внутри 8500–9500 | COVER BLOCKER | not_published |
| BT02 | chto-vhodit-v-korporativnyj-vyhod | 8235 | PASS 91/100 | разрыв 265 до 8500 | COVER BLOCKER | not_published |
| BT05 | oplata-deda-moroza-dlya-yurlica | 6124 | PASS 88/100 | разрыв 2376 до 8500 | COVER BLOCKER | not_published |

HTML-линтер, slop detector и fact-checker: PASS. Каннибализация primary query: PASS. Ссылки: pass. Внутренние пути не открывались на живом домене, домена нет. ВК в `<a>` не ставился: проверяльщик получал HTTP 418. Адрес оставлен текстом.

## Отложено следующей волной, это не провал

- BT03 Дед Мороз на дом: минуты, 31 декабря и ночь → `/blog/ded-moroz-na-dom-31-dekabrya/`
- BT04 Дед Мороз на утренник в детском саду → `/blog/utrennik-v-detskom-sadu/`
- BT06 Дед Мороз на Новый год: заказ или песня → `/blog/ded-moroz-na-novyj-god/`

## COVER BLOCKER

`gpt-image-2` в namespace `user-mcp-kv` нет. Рядом есть flux, grok-imagine, nano_banana_pro, seedream и z-image. Они не вызывались. `AURA_BLOG_COVER_PROMPTS.json` в статусе `awaiting_topics`, массив `topics` пуст. Семейство `macro_detail` в концепте есть, но сцены тем не собраны. Лица не генерировались. Тексты сданы без `cover.png`.

## Публикация

`wp-publish-result.json` у каждой статьи: `status=not_published`, `reason=allow_publish=no`. Скилл `excalibur-wp-publish` не выполнялся.

## Дыры фактов, которые остались дырами

- ИНН, имя самозанятого, ОГРН, юридический адрес, email
- НДС, ООО, УПД, расчётный счёт организации
- Часы ответа телефона
- Процент скидки на 3+ корпоратива
- Цена юрлица после 1 декабря, на 31 декабря и ночью
- Закрываются ли три выхода одним документом
- Отзывы, цитаты, даты выходов, диплом
- Вывески и юридические имена Миража и Джамэла
- Корпоративная надбавка за область отдельной строкой не опубликована
- Авторы из `authors-registry.json` не использованы: это заглушки другой тематики с dummy sameAs

## Проверки

- `teya_excalibur_html_linter.py` PASS
- `teya_excalibur_slop_detector.py` PASS
- `teya_excalibur_fact_checker.py` PASS
- `excalibur_link_verify.py` pass
- `teya_excalibur_cannibalization_guard.py` PASS
- interlinker: 0 новых вставок, перекрёстные ссылки уже стояли в HTML
- `llms.txt` и `llms-full.txt` лежат в `teya-memory/blog/`, не в корне сайта. Префикс `unpublished`: живого домена нет

## BT07, 2026-10-29

Статья `teya-memory/blog/articles/BT07-ded-moroz-na-korporativ-ne-utrennik/`. H1: «Дед Мороз на корпоратив в Нижнем Новгороде: это не детский утренник». 9410 знаков. QA PASS 92/100. volume_gap нет. COVER BLOCKER: gpt-image-2 нет, промпты пустые, лица не рисовались. publish not_published, WordPress не вызывался. Чужие статьи, llms.txt, index.html и handoff не менялись. Фрагмент: `teya-memory/fragments/excalibur-bt07.md`.
