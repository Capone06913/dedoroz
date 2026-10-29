=== AURORA-TEAM-INDEXING (CRAWL/INDEX) ===
## Статус: ❌
Indexing map: teya-memory/wp/indexing-crawl-map.md
Robots: план, без публикации. CSS, JS и изображения не закрывать. Googlebot, YandexBot и Bingbot разрешены. Строк Host и Sitemap нет: pending_public_host.
Sitemap: восемь путей без хоста — пять страниц, /blog/, две политики. Школа, четыре гео, BT01–BT06 и служебные URL исключены. XML не опубликован, HTTP 200 не проверялся.
AI crawlers: политика Allow для GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, PerplexityBot, Google-Extended, CCBot. На хост не выкладывалась.
Redirects: old_url_map_path пуст, старого сайта нет. Редиректы не заданы. Слаги AURA /korporativ/, /na-dom/, /sad-i-shkola/, /zayavka/ не регистрируются.
Blockers: public_site_url missing
incident_report:
- open: нет инцидента по составу индексного набора; robots, llms.txt и AI-политика записаны как план и не опубликованы
- blocker: public_site_url missing
- constraint: деплой local-only; canonical и sitemap host не подставлять; в индекс этой сборки пять страниц и оболочка /blog/; школа и гео вне sitemap; BT03, BT04, BT06 без тела и без URL; BT01, BT02, BT05 вне sitemap до тела и Excalibur PASS
