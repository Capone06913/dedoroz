=== AURORA-TEAM-SCHEMA (TECH SEO/GEO) ===
## Статус: ✅
Schema map: teya-memory/wp/schema-technical-seo-map.md
Schema types: Organization, WebSite без SearchAction, WebPage, ContactPage, CollectionPage, Service, Offer, FAQPage только на главной, SpeakableSpecification. BreadcrumbList описан и не печатается, пока нет домена. LocalBusiness нет. Article нет до PASS записей.
Yandex: verification и Метрика пусты, теги не ставить. Host в robots не писать. В организации имя, телефон, город и зона. Адреса, часов, гео и карты нет.
Google: JSON-LD без абсолютных @id и canonical. Крошки только будущим JSON-LD, видимой полосы нет. Рейтингов, отзывов, автора-человека и выдуманных цен нет.
Blockers:
- public_site_url пуст, dedmoroz.ru не куплен. Абсолютные @id, canonical, og:url, Host, Sitemap и BreadcrumbList не подставлять. Токен {{PUBLIC_SITE_URL}} в HTML не печатать.
- page-content-pack.md ещё не было. FAQ дома, ресторана и сада в JSON-LD не заполнен: в брифах нет дословных пар. Главная собрана из dossier §10, пятый ответ без семейных цен.
- ИНН, адрес, email, часы, отзывы и AggregateRating не ставятся. Это запрет, не дыра текста.
incident_report:
- open: нет. Карта записана без правок page-content-pack.md и без правок 01-handoff.md
- blocker: домен не куплен, абсолютные идентификаторы схемы отложены
- constraint: LocalBusiness, карта, часы, ИНН и Article в этой волне не выводятся. FAQ внутренних услуг ждёт видимый текст
