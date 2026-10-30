# Что прописать на хостинге

Сайт статический. Корень сайта — эта папка: страницы, `robots.txt`, `sitemap.xml`, `.htaccess`.

Канонический адрес: `https://dedmoroz52.ru` (без www, только https).

## Домены и DNS

1. Основной домен — `dedmoroz52.ru`.
2. `www.dedmoroz52.ru` — тот же сайт (алиас), не отдельная копия.
3. `new-yaer.ru` и `www.new-yaer.ru` — алиасы того же каталога. Редирект постраничный: `https://new-yaer.ru/kafe.html` открывает `https://dedmoroz52.ru/kafe.html`, а не главную.
4. У регистратора: A-запись (или AAAA) на IP хостинга для `dedmoroz52.ru`, `www`, `new-yaer.ru` и `www.new-yaer.ru`.

## Панель (Timeweb, Beget, Reg.ru и похожие)

1. Привязать все четыре имени к одному сайту. `dedmoroz52.ru` — главный.
2. Выпустить SSL на `dedmoroz52.ru`, `www.dedmoroz52.ru`, `new-yaer.ru`, `www.new-yaer.ru` (один сертификат с несколькими именами или отдельный на каждый).
3. Включить в панели «перенаправлять HTTP на HTTPS» и «с www на без www», если такие галки есть. Они делают то же, что `.htaccess`.
4. Залить файлы в корень сайта (`public_html`, `www` или `docs` — как называется у хостера). `index.html` должен открываться по `/`.
5. Если после галки «на HTTPS» браузер пишет «слишком много перенаправлений», выключите http-правило в `.htaccess` (последний блок) и оставьте редирект панели. На Beget и части тарифов Apache не видит HTTPS и зацикливается.
6. Пример для VPS с nginx — `nginx.dedmoroz52.conf.example`. На shared-хостинге его некуда вставлять, достаточно панели и `.htaccess`.

## Проверка

- `http://dedmoroz52.ru/kafe.html` → `https://dedmoroz52.ru/kafe.html`
- `https://www.dedmoroz52.ru/shou.html` → `https://dedmoroz52.ru/shou.html`
- `http://www.new-yaer.ru/blog.html` → `https://dedmoroz52.ru/blog.html`
- `https://dedmoroz52.ru/index.html` → `https://dedmoroz52.ru/`
- `https://dedmoroz52.ru/robots.txt` и `https://dedmoroz52.ru/sitemap.xml` открываются и отдают 200.

`kp.html` и `kp-pdf.html` в sitemap нет: это макеты письма и PDF, не страницы для поиска. В `robots.txt` они закрыты.
