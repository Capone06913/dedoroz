=== AURORA-TEAM-NAVIGATION (МЕНЮ И ПЕРЕЛИНКОВКА) ===
## Статус: ✅
Navigation map: teya-memory/wp/navigation-linking-map.md
Primary menu: Ресторан и кафе → /ded-moroz-v-restoran/ ; На дом → /ded-moroz-na-dom/ ; Детский сад → /ded-moroz-v-detskij-sad/ ; Контакты → /kontakty/. Словомарк ведёт на /. В шапке телефон +7 (952) 451-65-79 и «Позвонить Надежде» (`tel:+79524516579`). Блога, школы и гео в шапке нет.
Липкая полоса до 767px: высота 64px, фон #6E1A28, текст #FFF7F2, тот же номер и «Позвонить Надежде». Баннер cookies выше полосы, не поверх номера.
Footer menu: услуги (ресторан, дом, сад) ; компания (главная) ; блог → /blog/ «Вопросы перед заказом Деда Мороза» ; документы (Политика конфиденциальности, Политика cookies) ; контакты (телефон, ВК https://vk.ru/ded.moroz.nnov, страница контактов, тихий Instagram). Зона выезда строкой без ссылок.
Homepage blog: шесть H1 из 11-blog-topics.md без href на single. Живая ссылка блока — заголовок на /blog/. Permalink BT01, BT02, BT05 только после PASS Excalibur. BT03, BT04, BT06 записью не становятся.
Internal links per page: главная 6, ресторан 4, дом 5, сад 5, контакты 7, архив блога 5, каждая политика 3. Анкоры с названием страницы. Крошки только JSON-LD, видимый HTML не печатать.
Отложены без href: /ded-moroz-v-shkolu/, /dzerzhinsk/, /arzamas/, /kstovo/, /nizhegorodskaya-oblast/.
Blockers: нет
incident_report:
- open: нет инцидента по меню и живым ссылкам пяти страниц
- blocker: нет
- constraint: школа и четыре гео в карте ядра есть, в эту сборку ссылками не входят; шесть тем блога видимы как H1, permalink статей выключен до PASS; видимые верхние крошки запрещены
