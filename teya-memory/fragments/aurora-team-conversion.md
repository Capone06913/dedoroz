=== AURORA-TEAM-CONVERSION (ФОРМЫ И ЦЕЛИ) ===
## Статус: ✅
Conversion map: teya-memory/wp/conversion-tracking-map.md
Forms: пять страниц, поля имя, телефон, дата, тип площадки, сообщение. Обязательны имя, телефон, дата, площадка и согласие. Сообщение необязательно. Предвыбор формата только на ресторане, длины визита на доме, минут на саде. Успех в local-only честный: письмо не уходит, дата не забронирована. На контактах обязателен боковой кадр stage-vocal, его нельзя заменить пустой карточкой. На главной у заявки своего кадра нет.
Analytics goals: план phone_click, vk_click, cta_click, form_submit. form_submit не слать, пока доставка не VK и не MAX. Email, Telegram, WhatsApp и MAX целей нет. Счётчик Метрики и GA4 не вставлять.
Consent: страница «Политика конфиденциальности» /politika-konfidencialnosti/, страница «Политика cookies» /politika-cookies/, баннер с кнопкой «Принять cookies» и ссылками на обе политики, чекбокс «Соглашаюсь на обработку имени и телефона» со ссылкой на политику. Согласие в cookie dedmoroz_cookie_ok и в localStorage.
Missing credentials: metrika_counter_id, ga4_measurement_id, gtm_container_id, crm_webhook_url, telegram, whatsapp, email, SMTP, MAX, ИНН и юридическое имя. Не выдумывать.
Blockers: нет блокера карты. Доставка лида позже во ВК или MAX. Сейчас рабочий канал — +7 (952) 451-65-79 и https://vk.ru/ded.moroz.nnov. Кнопку MAX не ставить.
incident_report:
- open: нет. Карта форм, CTA, согласий и имён целей записана. Счётчик не вставлен.
- blocker: нет блокера спецификации. Почта и CRM пустые, это запрет на выдуманный SMTP, не дыра формы.
- constraint: local-only, wp_mail не вызывать; MAX на сайт не ставить; form_submit не считать лидом, пока нет живой доставки; боковой кадр stage-vocal обязателен только на /kontakty/.
