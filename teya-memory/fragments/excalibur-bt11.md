=== EXCALIBUR (SEO/GEO СТАТЬИ БЛОГА) ===

date: 2026-10-29
topic_id: BT11
status: article_ready_local
publish: not_published

Путь: teya-memory/blog/articles/BT11-kak-zakazat-deda-moroza/
H1: Как заказать Деда Мороза в Нижнем Новгороде
char_count: 9393
QA verdict: PASS 90/100
core_eeat_lite: 19/20
volume_gap: no
cover status: COVER BLOCKER
publish status: not_published

incident_report:
- severity: no_article_failure
- COVER BLOCKER: в user-mcp-kv нет gpt-image-2. AURA_BLOG_COVER_PROMPTS.json пуст (topics: [], awaiting_topics). Сцена BT11 не собрана. Подмена модели не делалась. Лица не рисовались. cover.png нет.
- volume_gap: no. 9393 знака, внутри 8500–9500. Водой не доливалось.
- publish: status=not_published, reason=allow_publish=no, deploy_mode=local-only. WordPress не вызывался.
- fact_bank_stale: суммы 14 370 / 19 640 / 26 480 / 37 900 checker не нашёл в fact-bank (там 8 000 / 10 000 / 15 000). В текст взяты шапка волны ключей и живые карточки сайта. Старые рубли не писались. Боковые 15 000 / 20 000 / 25 000 / 35 000 не копировались.
- fact_holes_kept: часы трубки, число выходов в день, фраза «даты разлетаются», минуты раннего приезда, процент на 3+ корпоратива, цена 31 декабря, 1 января и ночи, email, ИНН цифрой, НДС, ООО, УПД, отзывы, число гостей. На дом не продаётся.
- cannibalization: скрипт по всей папке articles вернул fail из-за чужой пары BT01/BT12 (один primary «стоимость деда мороза»). Эти файлы не менялись. У BT11 свой ключ. Warning 75% только со secondary BT10 «заказать деда мороза на дату».
- links: / и /kontakty/. Чужие статьи, llms.txt, index.html, run log и handoff не менялись. Interlinker --apply не запускался.
- authors-registry.json не использован: dummy-персоны другой тематики.
