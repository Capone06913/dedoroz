=== EXCALIBUR (SEO/GEO СТАТЬИ БЛОГА) ===

date: 2026-10-29
topic_id: BT07
slug: ded-moroz-na-korporativ-ne-utrennik
article: teya-memory/blog/articles/BT07-ded-moroz-na-korporativ-ne-utrennik/article.html
h1: Дед Мороз на корпоратив в Нижнем Новгороде: это не детский утренник
char_count: 9410
qa_verdict: PASS
qa_score: 92/100
core_eeat_lite: 19/20
volume_gap: no
cover_status: COVER BLOCKER
publish_status: not_published
allow_publish: no

Цены до 1 декабря 2026 взяты с живого прайса: выход 20–25 минут 14 370 ₽, шоу 30 минут 19 640 ₽, Welcome 60 минут 26 480 ₽, по столикам 60 минут 37 900 ₽. Старые 8 000 / 10 000 / 15 000 не писались. Дом, сад и школа не продаются.

incident_report:
- severity: no_article_failure
- COVER BLOCKER: в user-mcp-kv нет gpt-image-2; AURA_BLOG_COVER_PROMPTS.json пуст (awaiting_topics, topics []). Подмена модели не делалась. Лица не рисовались. cover.png нет.
- volume_gap: no. 9410 знаков, коридор 8500–9500.
- publish: status=not_published, reason=allow_publish=no, deploy_mode=local-only. WordPress не вызывался. Домена нет.
- fact_bank_stale_prices: четыре живые цены не найдены скриптом в fact-bank от 28 октября. В текст взяты с карточек и FAQ сайта от 29 октября 2026. Герой страниц с 15 000 / 20 000 / 25 000 / 35 000 проигнорирован.
- fact_holes_kept: ИНН, НДС, ООО, УПД, отзывы, число гостей, процент скидки, цена 31 декабря и 1 января, часы трубки, вывески Миража и Джамэла.
- link_note: ВК текстом. Внутренние URL относительные, живой домен не проверялся.
- interlink_apply: не запускался, чужие статьи не менялись. llms.txt, index.html и handoff не трогались.
- authors-registry.json не использован: dummy-персоны другой тематики.
