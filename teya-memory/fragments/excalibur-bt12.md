=== EXCALIBUR (SEO/GEO СТАТЬИ БЛОГА) ===

date: 2026-10-29
topic_id: BT12
article: teya-memory/blog/articles/BT12-skolko-stoit-ded-moroz/article.html
h1: Сколько стоит Дед Мороз в Нижнем Новгороде
char_count: 9497
qa_verdict: PASS
qa_score: 95/100
core_eeat_lite: 19/20
cover_status: COVER BLOCKER
publish_status: not_published
volume_gap: no

До 1 декабря 2026 в тексте: 14 370 / 19 640 / 26 480 / 37 900 ₽ для кафе, ресторана и корпоратива. Сумма зависит от минут и места в вечере. 31 декабря и 1 января в этот прайс не входят. Старые 8 000 / 10 000 / 15 000 и семейные 6 500 не использованы. «Дешевле всех» нет. На дом не продаётся. НДС, ООО, УПД, ИНН и отзывы не выдуманы: в тексте только то, что их нет в открытом прайсе, а ИНН называют в счёте.

incident_report:
- severity: no_article_failure
- COVER BLOCKER: gpt-image-2 в user-mcp-kv нет. Есть flux2-pro, grok-imagine, nano_banana_pro, z-image. Модель не подменялась. Лица не генерировались. cover.png нет. AURA_BLOG_COVER_PROMPTS.json не менялся.
- volume_gap: нет. 9497 знаков, внутри 8500–9500. Водой не доливалось.
- publish: status=not_published, wordpress_called=false, reason=publish no.
- cannibalization: FAIL. BT01 и BT12 делят primary query «стоимость деда мороза» и H1. Карточка волны это задаёт. BT01 со старым прайсом не редактировался. WARNING BT11/BT10 в отчёте сторожа к BT12 не относится.
- fact_note: четыре живые цены нет в fact-bank от 28 октября. Источник — index.html и kontakty.html на 29 октября 2026. Fact-checker: pass, суммы помечены unverified large_number. Медианы снимка заново не считались.
- fact_holes_kept: сумма 31 декабря, 1 января и ночи; ставка НДС; номер ИНН; ООО; УПД; отзывы; процент на три корпоратива; часы трубки; число гостей.
- link_note: внутренние `/` и `/kontakty/` относительные, домен не куплен. ВК и почта текстом.
- authors-registry.json не использован: dummy-персоны другой тематики.
- skipped: interlinker --apply, llms.txt, index.html, handoff, чужие статьи, WordPress, общий excalibur-run-log.
