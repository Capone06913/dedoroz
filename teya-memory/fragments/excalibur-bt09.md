=== EXCALIBUR (SEO/GEO СТАТЬИ БЛОГА) ===

date: 2026-10-29
topic_id: BT09
article: teya-memory/blog/articles/BT09-skolko-stoit-ded-moroz-31-dekabrya/article.html
h1: Сколько стоит Дед Мороз 31 декабря в Нижнем Новгороде
char_count: 9153
qa_verdict: PASS
qa_score: 90/100
core_eeat_lite: 18/20
cover_status: COVER BLOCKER
publish_status: not_published
volume_gap: no

До 1 декабря 2026 в тексте: 14 920 / 19 920 / 24 920 / 34 920 ₽. 31 декабря и 1 января в этот прайс не входят. Отдельная новогодняя цифра не названа. Старые 8 000 / 10 000 / 15 000 и семейные 6 500 не использованы. На дом не продаётся.

incident_report:
- severity: no_article_failure
- COVER BLOCKER: gpt-image-2 в user-mcp-kv нет; AURA_BLOG_COVER_PROMPTS.json пуст (awaiting_topics, topics []). Модель не подменялась. Лица не генерировались. cover.png нет.
- volume_gap: нет. 9153 знака, внутри 8500–9500.
- publish: status=not_published, wordpress_called=false, reason=publish no.
- fact_note: четыре живые цены нет в fact-bank от 28 октября (там старые 8 000 / 10 000 / 15 000). Источник — прайс index.html и kontakty.html на 29 октября 2026. Fact-checker: pass, суммы помечены unverified large_number.
- price_conflict_not_used: герои vyhod.html / shou.html / welcome.html ещё показывают 15 000 / 20 000 / 25 000. В статью не брались.
- fact_holes_kept: отдельная сумма 31 декабря, 1 января и ночи; НДС, ООО, УПД, ИНН; процент на три корпоратива; часы трубки; число гостей; отзывы.
- link_note: внутренние `/` и `/kontakty/` относительные, домен не куплен. ВК текстом, не ссылкой.
- authors-registry.json не использован: dummy-персоны другой тематики.
- skipped: interlinker --apply, llms.txt, index.html, handoff, чужие статьи, WordPress.
