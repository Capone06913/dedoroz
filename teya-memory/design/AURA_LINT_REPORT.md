# AURA lint

Файл: `teya-memory/design/AURADESIGN.md`. Проверка вручную по спецификации, 28 октября 2026.

## YAML

Группы на месте: colors, typography, rounded, spacing, borders, shadows, components, motion, assets. Ссылки компонентов ведут на эти токены:

- `{colors.primary}`, `{colors.on-primary}`, `{colors.surface-high}`, `{colors.on-inverse}`, `{colors.surface-lowest}`, `{colors.outline-variant}`, `{colors.outline}`, `{colors.on-background}`
- `{typography.label-md}`, `{typography.body-md}`
- `{rounded.md}`, `{rounded.DEFAULT}`, `{rounded.full}`
- `{spacing.md}`
- `{shadows.card}`, `{shadows.sticky}`

Битых ссылок нет.

## Контраст

| Пара | Отношение | AA 4.5 |
|---|---:|---|
| `#6E1A28` / `#FFF7F2` | 10.77 | да |
| `#54141E` / `#FFF7F2` | 13.26 | да |
| `#1E4F86` / `#F4F7FB` | 7.76 | да |
| `#F7F1E8` / `#1A1210` | 16.44 | да |
| `#FFFBF6` / `#1A1210` | 17.91 | да |
| `#141218` / `#F6F1EA` | 16.55 | да |
| `#8F1D1D` / `#FFF7F2` | 8.40 | да |
| `#8A6232` / `#F7F1E8` | 4.83 | да, но золото оставлено линии, не абзацу |
| `#8A6232` / `#141218` | 3.43 | нет для мелкого текста. Мелкий золотой текст на ночи запрещён |
| `#8A7564` / `#FFFBF6` | 4.24 | нет. Это только обводка поля, не цвет текста |

Обязательные пары primary/on-primary и background/on-background проходят.

## Углы

sm 4, default 8, md 12, lg 16, xl 20. Кнопки и карточки оба md 12. Разрыва «2 против 40» нет. `full` только у переключателя, это отдельная роль, не карточка.

## Deliverables

Todo, source analysis, decomposition, budget, blueprints, scorecard, inventory, transitions, brand-kit prompt, color psychology, font match, shape map, visual diff, reviewer, QA, lint, page plan, blog concept — создаются этим проходом.

## Точность источника

Чужого макета не было. Точность считается по брифу: переключатель, одна строка, три цены, телефон, живые кадры.

## Статус

Lint контракта: pass. Блокер генерации вынесен в registry и не является ошибкой YAML.
