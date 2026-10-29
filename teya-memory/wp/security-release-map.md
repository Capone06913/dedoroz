# Карта безопасной сборки и релиза — dedmoroz-nn

Дата: 28 октября 2026.  
Тема: `dedmoroz-nn`. Язык: `ru-RU`.  
Сайт: «Дед Мороз и Снегурочка. Нижний Новгород».

Эта волна собирает локальную тему. Публичного релиза нет. FTP, SSH, активация темы и запись в WordPress запрещены. `site-spec.json` и `build-report.json` здесь не создаются: их позже собирает report compiler по контракту ниже. `01-handoff.md` этот агент не меняет.

## 1. Режим этой волны

Флаги из `teya-memory/teya.env.local` и `site.inv` совпадают:

| Флаг | Значение |
|---|---|
| `TEYA_DEPLOY_MODE` | `local-only` |
| `TEYA_ALLOW_PUBLISH` | `no` |
| `TEYA_ALLOW_ACTIVATE_THEME` | `no` |
| `TEYA_ALLOW_CREATE_PAGES` | `yes` (только когда появится локальный WordPress; сейчас WP нет) |
| `TEYA_ALLOW_CREATE_POSTS` | `yes` (статьи этой волной не создаются) |
| `TEYA_ALLOW_CLEAR_CACHE` | `no` |
| `WP_CLI_AVAILABLE` | `no` |
| `public_site_url` | пустая строка |
| `existing_theme_slug` | пусто |
| `wp_admin_url` | пусто |

`deploy-log.md` в этой волне не изображает публикацию. Если файл появится раньше удалённого деплоя, единственный честный статус: `local-only`, `published: false`.

Планируемый домен `dedmoroz.ru` не куплен. Его нельзя писать в `public_site_url`, Host `robots.txt`, canonical, Sitemap, видимый HTML и абсолютные `@id`.

Идентичность, которую compiler сверяет во всех отчётах:

- `theme_slug`: `dedmoroz-nn`
- `project` / `site_name`: `Дед Мороз и Снегурочка. Нижний Новгород`
- `public_site_url`: `""`

Расхождение любого из трёх полей — блокер релиза (`report identity mismatch`).

## 2. Кто пишет JSON

| Файл | Кто пишет | Когда |
|---|---|---|
| `teya-memory/wp/security-release-map.md` | этот агент, уже записан | сейчас |
| `teya-memory/wp/site-spec.json` | report compiler | после сборки темы, до заявления о готовности |
| `teya-memory/wp/build-report.json` | report compiler | после сборки, с фактами файлов и проверок |

До появления темы compiler ставит визуальные и paint-статусы `not_run`. Слово `pass` до реальных файлов темы, скриншотов и локального просмотра запрещено.

Допустимые статусы полей: `not_run`, `pass`, `fail`, `blocked`, `not_applicable`.

## 3. Контракт `site-spec.json`

Корень — детерминированная спецификация сборки, не рекламный отчёт.

Обязательные поля идентичности и визуала (оба JSON, одни и те же имена):

```text
theme_slug
project
site_name
public_site_url
visual_inventory_status
required_visual_zones_count
ready_visual_zones_count
meaningful_image_count
minimum_meaningful_image_assets_homepage
meaningful_image_gap
section_transitions_status
asset_registry_status
paint_evidence_status
visual_budget_status
section_blueprints_status
style_match_scorecard_status
per_page_visual_budget_status
per_page_section_blueprints_status
per_page_meaningful_image_counts
per_page_visual_gaps
local_asset_files_status
missing_local_asset_files
browser_subresources_status
unstyled_live_paint_status
wp_media_map_status
wp_media_import_status
missing_wp_media_attachments
animation_motion_status
animation_dependency_status
reduced_motion_status
threejs_scene_status
```

`project` и `site_name` оба равны строке из `site.inv`: «Дед Мороз и Снегурочка. Нижний Новгород».

Дополнительные поля этой сборки:

```text
deploy_mode = local-only
allow_publish = no
allow_activate_theme = no
published = false
language = ru-RU
permalink_structure = /%postname%/
aura_slug_source          объект итоговый URL → слаг AURA
pages[]                   пять URL плюс оболочка
legal
forms
secrets_packaged = false
file_allowlist_enforced = true
```

### Пороги, которые compiler копирует как есть

`minimum_meaningful_image_assets_homepage` = **6**. Это порог AURA и `AURA_VISUAL_INVENTORY.json`. В `site.inv` рядом лежит пол 4; в отчёт его записать отдельным полем `site_inv_meaningful_floor: 4`, сдавать страницу по 6. CSS-карточки, градиенты и плашки в `meaningful_image_count` не входят.

`required_visual_zones_count` для главной = **7**. Это обязательные смысловые кадры инвентаря: `hero-show`, `hero-classic`, `boundary-dance`, `welcome-guest`, `hall-banquet`, `stage-vocal`, `documents-pair`. Именованные зоны `site.inv` (`hero`, `formats`, `cases`, `documents`, `booking`) записать отдельно, не подменяя семёрку. `price-cards` — CSS, в семёрку не входит. `ensemble-held` на витрину не ставится.

`ready_visual_zones_count` растёт только когда файл кадра лежит в теме и выведен в шаблоне. До копирования jpg значение 0, статус инвентаря `not_run`.

`meaningful_image_gap` = сколько кадров не хватает до порога страницы. До сборки gap главной не объявлять нулём.

### Ключи `per_page_*` — итоговые слаги

Рядом в каждой записи: `aura_slug_source`.

| Итоговый URL | `aura_slug_source` | Meaningful min | Цветные секции | Карточки | Overlap | Непрямоугольный стык |
|---|---|---:|---:|---:|---:|---:|
| `/` | `/` | 6 | 4 | 3 | 1 | 1 |
| `/ded-moroz-v-restoran/` | `/korporativ/` | 3 | 3 | 3 | 1 | 1 |
| `/ded-moroz-na-dom/` | `/na-dom/` | 2 | 3 | 2 | 1 | 1 |
| `/ded-moroz-v-detskij-sad/` | `/sad-i-shkola/` | 1 | 3 | 1 | 1 | 1 |
| `/kontakty/` | `/zayavka/` | 1 | 2 | 1 | 1 | 1 |

`/blog/`, `/politika-konfidencialnosti/` и `/politika-cookies/` в бюджет пяти страниц не входят. У архива карточки H1 без обложек. У политик нет кадров людей.

`per_page_visual_budget_status` и `per_page_section_blueprints_status` — объект по этим пяти URL. `pass` только если секции blueprint реализованы на итоговом слаге, а не на старом пути AURA (`/korporativ/`, `/na-dom/`, `/sad-i-shkola/`, `/zayavka/` в теме не регистрировать).

Стыки, которые должны быть `pass` в `section_transitions_status` (все `must_replicate`):

- `transition-hero-to-boundary` — overlap 40 / 32 / 24 px, нижний градиент кадра, без волны
- `transition-boundary-to-flow` — hairline
- `transition-flow-to-halls`
- `transition-halls-to-documents`
- `transition-documents-to-booking` — hard-cut в ночь

Стык ночной заявки главной к FAQ — прямой, без диагонали и без волны. Это правило blueprint, не новый переход из JSON.

`style_match_scorecard_status`: `pass`, если ни один критерий ниже своего minimum (цвет 80, плотность 75, композиция 85, ассеты 70, типографика 80, переходы 70, формы 75, запреты 90). Planned-сводка дизайна 87 — ориентир, не замена проверки готовой темы. Copy-in-copy к чужому сайту не считается.

`asset_registry_status`: живые jpg ниже — обязательные. `brand-kit` и `blog-cover-style-anchor` остаются `blocked` (`mcp-gpt-image-2-missing`). Другой моделью их не закрывать. Этот блокер не понижает порог семи живых кадров.

Обязательные id в теме (копия из `ded/`, лица не перерисовывать):

`show-hero`, `classic-hero`, `show-dance`, `welcome-guest`, `hall-banquet`, `stage-vocal`, `classic-studio`, `family-home`, `family-visit`.

В пакет страниц не класть: `ensemble-group`, `ensemble-dance`, `club-clock`, `club-clock-2`. Резервы `show-sg-mic` и `stage-moon` слот не занимают.

`local_asset_files_status`: `pass`, когда эти девять файлов лежат в `teya-memory/wp/theme/dedmoroz-nn/assets/images/`. `missing_local_asset_files` — список id, которых там нет. Пока темы нет, статус `not_run`, а не `fail` и не `pass`.

`animation_motion_status`: один crossfade 700 ms на главной, кадр и одна строка. `animation_dependency_status`: GSAP только на главной. `reduced_motion_status`: при `prefers-reduced-motion` длительность 0. `threejs_scene_status`: `not_used`. Рядом `motion_exception.not_a_gap: true`. Отсутствие Three.js — не дыра.

`source_decomposition` в spec (must-match / must-not) compiler переносит из blueprint §9. Семейные 6 500 ₽ на главную не попадают. ИНН, ООО, НДС, УПД, адрес, email, часы трубки, отзывы и процент скидки в spec не выдумывать.

### Страницы spec

Пять коммерческих:

1. `/` — `front-page.php`
2. `/ded-moroz-na-dom/` — `page-ded-moroz-na-dom.php`
3. `/ded-moroz-v-detskij-sad/` — `page-ded-moroz-v-detskij-sad.php`
4. `/ded-moroz-v-restoran/` — `page-ded-moroz-v-restoran.php`
5. `/kontakty/` — `page-kontakty.php`

Оболочка, не шестая услуга:

- `/blog/` — `home.php` (записи). `page-blog.php` не дублировать.
- `single.php` — тела статей этой волной нет.
- `/politika-konfidencialnosti/` — `page-politika-konfidencialnosti.php`
- `/politika-cookies/` — `page-politika-cookies.php`
- `page.php`, `404.php`, `search.php`, `header.php`, `footer.php`, `index.php`

На собранных страницах нет ссылок на `/ded-moroz-v-shkolu/`, `/dzerzhinsk/`, `/arzamas/`, `/kstovo/`, `/nizhegorodskaya-oblast/`, `/korporativ/`, `/na-dom/`, `/sad-i-shkola/`, `/zayavka/`.

Блог: шесть карточек H1 (BT01–BT06), `article_body: false` до Excalibur PASS. Обложки не подставлять.

## 4. Контракт `build-report.json`

Те же визуальные поля и та же идентичность, что в §3. Плюс факты сборки:

```text
generated_files[]
templates[]
menus
forms.delivery = not_configured
forms.outbound_mail = false
legal.privacy = true|false
legal.cookies = true|false
legal.cookie_banner = true|false
checks.php_lint
checks.theme_structure
checks.theme_check
checks.escaping
package_path
deploy_status = local-only
published = false
activation = not_run
rollback.required = false
rollback.previous_theme_slug = ""
rollback.backup_zip = ""
skipped_checks[]
blockers[]
```

`package_path` пустой, пока zip для удалённой передачи не собирался. Локальная папка темы — `teya-memory/wp/theme/dedmoroz-nn/`. Её наличие не равно публикации.

`paint_evidence_status`, `browser_subresources_status`, `unstyled_live_paint_status` до paint-волны: `not_run`.

`wp_media_map_status`, `wp_media_import_status` до удалённого деплоя: `not_run`. `missing_wp_media_attachments`: пустой список с пометкой, что импорт не запускался. Ставить `pass` при пустом `public_site_url` нельзя.

## 5. Контракт WP Media

Пока сайт локальный и URL пуст, кадры живут в файлах темы. Это staging. Горячие ссылки MCP и tempfile в HTML запрещены уже сейчас.

После будущего деплоя, отдельной волной и только если флаги публикации сменятся, Aurora создаёт:

```text
teya-memory/wp/wp-media-map.json
teya-memory/wp/wp-media-import-log.md
teya-memory/wp/theme/dedmoroz-nn/media-map.json
```

В карте у каждого кадра одновременно `id` и `registry_id`, `attachment_id`, `attachment_url` на хосте сайта, `alt_text` из реестра, `local_source_path`. Пустой alt и alt уровня «фото» / «image» не проходят.

Публичный HTML тогда берёт картинку через вложение WordPress. URL `tempfile.aiquickdraw.com`, MCP и любой чужой временный хост — блокер, даже если карта импорта написана.

В этой волне bootstrap загрузки в медиатеку не оставлять доступным снаружи. Произвольной загрузки файлов у формы нет.

## 6. Контракт paint QA

Design Guardian после локальной сборки кладёт доказательства в `teya-memory/wp/paint-qa/`. JSON со словом `pass` без файлов на диске недействителен.

Обязательные файлы пяти страниц:

```text
paint-evidence.json
paint-qa-report.md
home-1440-fullpage.png
home-375-fullpage.png
page-ded-moroz-na-dom-1440-fullpage.png
page-ded-moroz-na-dom-375-fullpage.png
page-ded-moroz-v-detskij-sad-1440-fullpage.png
page-ded-moroz-v-detskij-sad-375-fullpage.png
page-ded-moroz-v-restoran-1440-fullpage.png
page-ded-moroz-v-restoran-375-fullpage.png
page-kontakty-1440-fullpage.png
page-kontakty-375-fullpage.png
```

Оболочка, без которой форма не открывается:

```text
page-blog-1440-fullpage.png
page-blog-375-fullpage.png
page-politika-konfidencialnosti-1440-fullpage.png
page-politika-konfidencialnosti-375-fullpage.png
page-politika-cookies-1440-fullpage.png
page-politika-cookies-375-fullpage.png
```

Просмотр локальный: публичного URL нет, live-хост не подменять доменом `dedmoroz.ru`. В `paint-evidence.json` поле `public_site_url` пустое, `theme_slug` = `dedmoroz-nn`.

`pass` требует одновременно:

- все перечисленные PNG лежат на диске и совпадают с путями в JSON;
- браузер запросил CSS темы, JS темы и обязательные изображения (не один голый HTML-документ);
- `unstyled_html_detected: false` — нет белого шаблона, голых ссылок и дефолтных кнопок вместо ночи, клюквы и слоновой кости;
- число смысловых кадров на странице не ниже её minimum;
- внутренняя страница несёт визуальный язык AURA, а не generic `page.php`.

Иначе `paint_evidence_status` и `browser_subresources_status` = `fail`, `unstyled_live_paint_status` = `fail`, если на скриншоте голый HTML.

## 7. Форма, политики, cookie

Форма стоит на главной, ресторане, доме, саду и контактах. Поля: имя, телефон, дата, тип площадки, сообщение. Плюс обязательное согласие на обработку ПДн со ссылкой на политику конфиденциальности, скрытый honeypot и nonce. Honeypot не подписывать как обычное поле.

До того как форма считается готовой к сборке, в теме уже есть:

- страница `/politika-konfidencialnosti/`;
- страница `/politika-cookies/`;
- видимый cookie-баннер с принятием и ссылками на обе политики;
- обе ссылки в подвале.

Публичная оферта не нужна (`offer_required = no`). Баннер на 375px стоит выше липкой полосы 64px или в потоке и не закрывает номер.

Согласие на cookie хранится в first-party cookie или `localStorage`. Счётчиков нет: идентификаторы Метрики, GA4 и GTM пустые, пиксели не вставлять. Аналитика до согласия не грузится, потому что её нет.

Доставка: `delivery: not_configured`. Форма не шлёт письма наружу.

Запрещённый исходящий канал в обработчике:

- `wp_mail` и любой SMTP;
- вебхук CRM;
- Telegram;
- запись в `smtp.credentials.local` (файла нет и создавать его не нужно).

Текст успеха не подтверждает бронь и не говорит, что письмо дошло до Надежды или в CRM. Честная формулировка локальной темы: заявка письмом не отправляется, дату подтверждает звонок Надежде, `tel:+79524516579`. Первое действие на странице — звонок, второе — ВК `https://vk.ru/ded.moroz.nnov`.

На ресторане предвыбор формата: 15–20 минут, 30 минут, Welcome. На доме и в саду предвыбор — минуты этой страницы.

## 8. Проверки безопасности кода темы

Каждый PHP-файл темы начинается с `ABSPATH`-guard.

Вывод:

- текст: `esc_html`
- атрибуты: `esc_attr`
- URL: `esc_url`
- HTML редактора, если появится: `wp_kses_post`
- JSON-LD: `wp_json_encode` с флагами, без склейки сырого ввода

Ввод формы:

- текст: `sanitize_text_field`
- сообщение: `sanitize_textarea_field`
- телефон и дата: та же санитизация плюс проверка формата, без исполнения
- nonce: `wp_nonce_field` / `wp_verify_nonce`
- honeypot: непустое поле отклоняет отправку
- сырой `$_POST` в HTML не печатать
- поля файла у формы нет; `media_handle_upload` с публичного запроса не вызывать

Customizer, если появится: URL через `esc_url_raw`, текст через `sanitize_text_field`. Произвольный PHP и JS из настройки не исполнять.

Фильтры безопасности не блокируют YandexBot, Googlebot, Bingbot и объявленных AI-краулеров. До публичного хоста robots лежит в теме и не утверждает, что сайт уже открыт.

Поиск и 404: `noindex`. Коммерческие пять, архив блога и обе политики готовятся как index, follow на будущее, без живого Host.

## 9. Allowlist файлов и ignore

В пакет темы входят только расширения:

`.php`, `.css`, `.js`, `.json`, `.svg`, `.png`, `.jpg`, `.jpeg`, `.webp`, `.txt`, `.md`

`screenshot.png` или `screenshot.jpg` обязателен для структуры темы. Исходный `.scss` может лежать в рабочей копии, в zip уходит скомпилированный `.css`. Бинарные шрифты в allowlist не входят: кириллица Cormorant Garamond и Manrope подключается как описано в карте производительности, `font-display: swap`.

Когда появится упаковка, Aurora создаёт `.deployignore` и `.distignore` в корне пакета. Сейчас zip не собирать. Правила ignore уже такие:

```text
teya-memory/
teya-memory/teya.env.local
teya-memory/hosting.credentials.local
teya-memory/smtp.credentials.local
.env
.env.*
*.credentials.local
*.local
node_modules/
*.log
ded/
.git/
.cursor/
```

Папка `ded/` — источник кадров. В тему копируются только девять назначенных jpg. Весь каталог `ded/` и вся `teya-memory/` в zip темы не входят. Корень zip, если его когда-нибудь соберут: одна папка `dedmoroz-nn/`. Права на будущее: файлы 644, каталоги 755.

## 10. Секреты

`teya-memory/teya.env.local` прочитан только для флагов режима. Значения паролей в эту карту не копируются. Файл содержит пустые поля доступа к WordPress и флаги `local-only` / `no`. Хоста FTP и SSH в `site.inv` нет.

`hosting.credentials.local` и `smtp.credentials.local` в проекте нет. Создавать их и заполнять выдуманными доступами нельзя.

В репозиторий, в тему, в zip, в `site-spec.json`, в `build-report.json` и в handoff не класть:

- `teya.env.local`
- `.env` и любые `*.local` с доступами
- пароли WP, FTP, SSH, SMTP, токены, cookie админки

Если позже появится git, эти пути держатся в `.gitignore`. Секрет, случайно попавший в отчёт, считается инцидентом: отчёт переписать без значения, исходный файл секрета снаружи пакета.

## 11. Структура темы и проверки

Минимум из playbook плюс шаблоны blueprint §4: `style.css` с шапкой WordPress, `Text Domain` = `dedmoroz-nn`, `index.php`, `functions.php`, `header.php`, `footer.php`, `front-page.php`, страницы пяти URL, `home.php`, `single.php`, обе политики, `page.php`, `archive.php`, `search.php`, `searchform.php`, `404.php`, `comments.php`, `screenshot`, `theme.json`, `inc/setup.php`, `inc/enqueues.php`, `inc/seo.php`, `inc/customizer.php`, `inc/breadcrumbs.php`, `inc/security.php`, `inc/media.php` (хелпер карты; до деплоя отдаёт локальный файл темы), `template-parts/content/content.php`, `template-parts/content/content-none.php`, `assets/dist/style.css`, `assets/dist/main.js`.

Видимые крошки выключены. JSON-LD крошек описывает schema-карта, не эта.

Проверки, которые Aurora или compiler фиксируют в `build-report.json`:

1. `php -l` по каждому `.php`, когда PHP доступен в PATH. Нет PHP — статус `skipped`, причина в `skipped_checks`, это не `pass`.
2. Сверка дерева с списком выше. Чужой page builder не подключать.
3. Theme Check — только если есть локальный WordPress и плагин. Сейчас `WP_CLI_AVAILABLE=no` и админки нет: проверка `skipped`, причина `wp_cli_available=no`. Пропуск не равен прохождению.
4. Ручной проход escaping / nonce / sanitize по форме и customizer.

## 12. Превью

Превью этой волны — файлы темы на диске и, когда paint-волна дойдёт, локальный просмотр без активации на удалённом сайте. WordPress Playground или Studio допустимы позже как песочница на машине, без FTP и без смены флагов `TEYA_ALLOW_*`.

Активировать `dedmoroz-nn` на каком-либо WordPress этой волной нельзя.

## 13. Backup и rollback

Сейчас откат не требуется: удалённая тема не загружалась, предыдущий `existing_theme_slug` пуст, активировать нечего. `rollback.required` в отчёте этой волны: `false`. `rollback.previous_theme_slug` и `rollback.backup_zip`: пустые строки.

План на будущий удалённый деплой, если Директор отдельно снимет запрет:

1. Остановиться, если `TEYA_ALLOW_PUBLISH` или `TEYA_ALLOW_ACTIVATE_THEME` всё ещё `no`.
2. Записать активный stylesheet до любых файловых изменений.
3. Снять zip текущего каталога темы на сервере в backup вне пакета темы. В zip не класть `teya.env.local` и пароли.
4. Залить `dedmoroz-nn` отдельным каталогом и не активировать, пока release gates §14 не закрыты и флаг активации не стал явным `yes`.
5. Откат файлов: удалить залитый каталог `dedmoroz-nn`, если активации не было.
6. Откат активации, если она всё же случилась вопреки плану: вернуть записанный прежний stylesheet, затем убрать каталог `dedmoroz-nn`, восстановив backup zip прежней темы, если менялись её файлы.

Пока шаг 2 не выполнен, активация запрещена ещё и потому, что прежний slug не зафиксирован.

## 14. Что блокирует публикацию

Публикация этой волны закрыта флагами. Это режим, а не дыра карты. Пока режим `local-only`, ставить `published: true` нельзя.

Блокеры, которые запрещают будущий publish даже после смены флагов:

- визуальный инвентарь отсутствует или семь зон главной не реализованы;
- visual budget или section blueprints отсутствуют либо не собраны на любом из пяти итоговых URL;
- смысловых кадров меньше порога страницы (главная меньше 6);
- одна герой-картинка вместо набора зон, где источник разложил несколько кадров;
- внутренняя страница выглядит как generic/default текст;
- нет per-page paint evidence или PNG из §6 отсутствует на диске;
- `paint-evidence.json` говорит `pass` без файлов скриншотов;
- живой или локальный просмотр без CSS/JS/изображений темы, либо unstyled HTML;
- обязательный локальный jpg из девяти id отсутствует в теме;
- в публичном HTML есть MCP/tempfile URL;
- после реального деплоя нет `wp-media-map.json`, журнала импорта или `media-map.json`, либо у обязательного кадра нет attachment;
- идентичность отчёта не совпала с `dedmoroz-nn` / именем сайта / пустым URL (или с реальным URL, когда он появится и будет один и тот же во всех отчётах);
- `brand-kit` или style anchor обложки объявлены готовыми без `gpt-image-2` (для пяти страниц живых jpg достаточно, подмена модели остаётся блокером именно этих двух id);
- в пакете секрет, `.env` или `teya-memory`;
- форма вызывает почту, SMTP, CRM или Telegram;
- нет cookie-баннера или любой из двух политик;
- успех формы обещает бронь или доставку в CRM при `delivery: not_configured`.

`not_run` у paint и WP Media в этой локальной волне — честный статус. Он блокирует публикацию и не блокирует запись локальной темы.
