# Дед Мороз и Снегурочка — Нижний Новгород (dedoroz)

Рабочая копия проекта: статический макет сайта, SEO-память (Teya), HTML-письмо КП.

## Что где лежит

| Путь | Назначение |
|------|------------|
| `teya-memory/design/` | **Текущий сайт** — HTML, `site.css`, `site.js`, медиа |
| `teya-memory/` | Бриф, семантика, статьи блога, карты под будущую тему WordPress |
| `email-kp/` | Отдельное HTML-письмо для рассылки |
| `ded/` | Исходные живые фото |

WordPress-тема (`teya-memory/wp/theme/dedmoroz-nn/`) пока только с ассетами; прод на `dedmoroz52.ru` — следующий этап.

## Локальный просмотр

```powershell
cd teya-memory\design
if (-not (Test-Path ded)) { Copy-Item -Recurse ..\..\ded .\ded }
python -m http.server 8080
```

Открыть: http://127.0.0.1:8080/index.html

## Превью на GitHub Pages

При push в `main` деплоится папка `teya-memory/design/` (Actions → **Deploy static site**).

URL: https://capone06913.github.io/dedoroz/ (после первого успешного деплоя).

## Снимок версии

- **2026-10-29** — зафиксирована текущая вёрстка (главная, контакты, форматы 14 920–34 920 ₽, FAQ, новогодняя музыка, блог-страницы в design).
