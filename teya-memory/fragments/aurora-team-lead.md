=== AURORA-TEAM-LEAD (СТРУКТУРА) ===
## Статус: ✅
Blueprint: teya-memory/wp/aurora-team-blueprint.md
Pages selected: / ; /ded-moroz-na-dom/ ; /ded-moroz-v-detskij-sad/ ; /ded-moroz-v-restoran/ ; /kontakty/
Slug remap: AURA /korporativ/ → /ded-moroz-v-restoran/ ; /na-dom/ → /ded-moroz-na-dom/ ; /sad-i-shkola/ → только сад ; /zayavka/ → /kontakty/
Отложены: /ded-moroz-v-shkolu/ и все гео. Блог — оболочка home.php + блок на главной, не шестая услуга. Статьи пишет Excalibur: BT01, BT02, BT05. BT03, BT04, BT06 — карточки H1 без тела.
Deploy: local-only, allow_publish=no. Тему не активировать. FTP и WordPress не трогать.
Motion exception: Three.js/WebGL not_used, not_a_gap=true. GSAP только crossfade 700ms на главной.
Parallel agents to run:
- aurora-team-content
- aurora-team-navigation
- aurora-team-schema
- aurora-team-indexing
- aurora-team-local-entity
- aurora-team-performance-a11y
- aurora-team-conversion
- aurora-team-security-release
- aurora-team-asset-packager
- aurora-team-motion
Не в эту волну: aurora-team-qa (после релиза), aurora-team-artifact-auditor и Aurora (после карт этой волны).
Blockers:
- brand-kit и style anchor обложек: в MCP KV нет gpt-image-2. Другой моделью не заменять. Лица не генерировать. Живые jpg из ded/ для пяти страниц достаточны.
- public_site_url пуст, dedmoroz.ru не куплен. Host, canonical и абсолютные @id не подставлять.
- ИНН, адрес, email, часы трубки, процент скидки, цена компании после 1 декабря, отзывы — фактов нет, на сайт не ставить. Это запрет, не дыра сборки.
incident_report:
- open: нет инцидента по составу пяти страниц
- blocker: gpt-image-2 отсутствует, brand-kit и обложки блога не собраны
- constraint: деплой выключен; школа и гео вне тестовой сборки; Three.js запрещён брифом и записан как явное motion exception
