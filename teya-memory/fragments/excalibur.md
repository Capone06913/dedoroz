=== EXCALIBUR (SEO/GEO СТАТЬИ БЛОГА) ===

date: 2026-10-28
status: articles_ready_local
publish: not_published
reason: allow_publish=no

Готовы три статьи: BT01, BT02, BT05. QA PASS. Обложки не сделаны: COVER BLOCKER, это не провал текстов. BT03, BT04, BT06 отложены следующей волной, не провал.

incident_report:
- severity: no_article_failure
- COVER BLOCKER: в user-mcp-kv нет gpt-image-2; AURA_BLOG_COVER_PROMPTS.json пуст (awaiting_topics). Подмена модели не делалась. Лица не рисовались. cover.png нет.
- volume_gap: BT02 8235 знаков (разрыв 265 до 8500). BT05 6124 знака (разрыв 2376 до 8500; карточка темы просит 3000–4500). Водой не доливалось. BT01 8833, внутри контракта.
- publish: status=not_published, reason=allow_publish=no, deploy_mode=local-only. WordPress не вызывался.
- deferred_next_wave: BT03, BT04, BT06.
- fact_holes_kept: ИНН, НДС, ООО, УПД, адрес, email, часы телефона, процент на 3+ корпоратива, цена юрлица после 1 декабря и ночью, отзывы, диплом, вывески Миража и Джамэла, один ли документ на три выхода.
- link_note: ВК оставлен текстом, не ссылкой. Проверяльщик получал HTTP 418. Домен сайта не куплен, внутренние URL относительные.
- authors-registry.json не использован: dummy-персоны другой тематики.
