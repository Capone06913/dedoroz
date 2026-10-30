=== EXCALIBUR (SEO/GEO СТАТЬИ БЛОГА) ===

date: 2026-10-29
topic_id: BT14
status: article_ready_local
publish: not_published

Путь: teya-memory/blog/articles/BT14-ded-moroz-v-detskij-sad/
H1: Дед Мороз в детский сад: что спросить до утренника
char_count: 9405
QA verdict: PASS 92/100
core_eeat_lite: 19/20
volume_gap: no
cover status: COVER BLOCKER
publish status: not_published

incident_report:
- severity: no_article_failure
- COVER BLOCKER: в user-mcp-kv нет gpt-image-2. AURA_BLOG_COVER_PROMPTS.json пуст (topics: [], awaiting_topics). Сцена BT14 не собрана. Подмена модели не делалась. Лица не рисовались. cover.png нет.
- volume_gap: no. 9405 знаков, внутри 8500–9500. Сетку по минутам, медиану сада и воду не дописывали.
- publish: status=not_published, reason=allow_publish=no, deploy_mode=local-only. WordPress не вызывался.
- fact_holes_kept: сумма по каждой метке минут, цена подарка, текст «Волшебства стихий», садовая надбавка за город, домашний прайс, банкетные 14 370 ₽, свежая медиана сада, часы трубки, email, ИНН, НДС, ООО, УПД.
- forbidden_not_written: старые 8 000 / 10 000 / 15 000, домашний прайс 6 500 ₽, сравнение с банкетом «мы дороже».
- links: /ded-moroz-v-detskij-sad/, /kontakty/, /politika-konfidencialnosti/. Чужие статьи, llms.txt, index.html, handoff и run log не менялись.
- authors-registry.json не использован: dummy-персоны другой тематики.
- interlinker --apply не запускался, чтобы не править чужие article.html.
