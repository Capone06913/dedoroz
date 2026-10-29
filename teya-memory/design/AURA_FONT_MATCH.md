# AURA Font Match

Режима репликации чужого сайта нет. Пара выбрана по характеру кадров и задаче HR, из каталога кириллических Google Fonts.

## Пара

| Роль | Семейство | Веса | Кириллица |
|---|---|---|---|
| Display, заголовки, меняющаяся строка | Cormorant Garamond | 500, 600, 700, italic 500 | да, каталог aura-cyrillic-google-fonts, editorial / luxury |
| UI, цены, тело, кнопки, форма | Manrope | 400, 500, 600, 700 | да, тот же каталог |

Третьего семейства нет.

## Почему эта пара

Кадры — банкет, тост, бархат, пайетки, белый зал. Заголовок должен звучать как строка программы, не как детский плакат и не как интерфейс SaaS. Cormorant Garamond даёт антикву с кириллицей и не требует жирного гротеска.

Цены 8 000 / 10 000 / 15 000 должен быстро читать человек с компьютера. Manrope держит цифры ровно и остаётся нейтральным в таблице состава. Inter сознательно не взят: для этой ниши он ничего не говорит и в скилле запрещён как универсальный ответ.

## Что отклонено

- Unbounded, Russo One, Oswald — слишком громко для зала и бухгалтерии.
- Comfortaa, Nunito, Pangolin — детский и рукописный контур.
- Forum и Oranienbaum — близко по культуре, но хуже держат длинный заголовок главной.
- Poiret One — тонкий, плохо на 375px.
- Playfair Display — в скилле помечен как «проверить кириллицу». Не ставим без этой проверки. Cormorant уже в безопасном списке.

## Трекинг

- Display 56px, weight 600: `letter-spacing: -0.02em`, `line-height: 1.08`.
- Меняющаяся строка italic 500: трекинг 0, не отрицательный, чтобы курсив не слипался.
- Label 12px uppercase: `letter-spacing: 0.08em`.
- Цена 40px weight 700: `letter-spacing: -0.03em`.

## Подключение

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
```

## Проверка

Латинские гарнитуры без кириллицы (Clash Display, Satoshi, Neue Montreal) не используются. Space Grotesk, Syne, Outfit, Plus Jakarta Sans не используются.
