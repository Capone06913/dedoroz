=== EXCALIBUR (SEO/GEO СТАТЬИ БЛОГА) ===

date: 2026-10-29
topic_id: BT13
status: article_ready_local
publish: not_published

Путь: teya-memory/blog/articles/BT13-ded-moroz-na-novyj-god/
H1: Дед Мороз на Новый год: заказ или песня
char_count: 9350
QA verdict: PASS 90/100
core_eeat_lite: 19/20
volume_gap: no
cover status: COVER BLOCKER
publish status: not_published

incident_report:
- severity: no_article_failure
- COVER BLOCKER: в user-mcp-kv нет gpt-image-2. AURA_BLOG_COVER_PROMPTS.json пуст (topics: [], awaiting_topics). Сцена BT13 не собрана. Подмена модели не делалась. Лица не рисовались. cover.png нет.
- volume_gap: no. 9350 знаков, внутри 8500–9500. Водой не доливалось. Декабрьская частота точной фразы в рыночном файле отсутствует и в текст не ставилась.
- publish: status=not_published, reason=allow_publish=no, deploy_mode=local-only. WordPress не вызывался.
- fact_bank_stale: суммы 14 920 / 19 920 / 24 920 / 34 920 checker не нашёл в fact-bank (там 8 000 / 10 000 / 15 000). В текст взяты живые карточки сайта и шапка волны. Старые рубли не писались. 194 показа взяты из wordstat-raw, окно 28 октября 2026, не из fact-bank.
- fact_holes_kept: текст песни и стихи, цена 31 декабря и 1 января, часы трубки, процент на 3+ корпоратива, email, ИНН, НДС, ООО, УПД, выезд на дом, сад и школа, декабрьская частота фразы «дед мороз на новый год».
- links: /blog/v-kakom-formate-ded-moroz-poyot/, /, /kontakty/. Чужие статьи, llms.txt, index.html и handoff не менялись.
- authors-registry.json не использован: dummy-персоны другой тематики.
