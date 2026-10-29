=== AURA (ДИЗАЙН) ===
## Статус: ✅
Design root: teya-memory/design/
AURADESIGN.md: ✓
AURA_PAGE_PLAN.md: ✓
Source-first mode: no
Key tokens: ночь #141218, клюква #6E1A28, слоновая кость #F7F1E8, золотая линия #C4A265, классический синий #1E4F86. Шрифты Cormorant Garamond и Manrope. Первый экран: сцена на весь вьюпорт, шапка с меню поверх кадра, горизонтальный полупрозрачный ряд цен.
Pages for Aurora test build: главная, корпоратив, на дом, сад и школа, заявка
Assets: 0 generated / blocker gpt-image-2. Живые кадры ded/: 7 на главной, все файлы открываются. Лица не генерировались.
Visual inventory: 7 зон главной с фото / 7 готовы / ансамбль и клуб с чужим знаком сняты с витрины
Section transitions: 5 / blockers нет
Visual gates: lint pass, diff pass, reviewer pass, qa pass
Риски: brand-kit и style anchor обложек не собраны, пока в MCP KV нет gpt-image-2. Другой моделью не заменял.

incident_report:
- open: нет инцидента по композиции и живым кадрам
- blocker: user-mcp-kv не содержит gpt-image-2. Графика, свет, фон и brand-kit не сгенерированы. Контракт сдан на реальных jpg из ded/

Макет пересобран после отказа заказчика: первый экран больше не письмо. Сцена на весь вьюпорт, меню в шапке, цены одним рядом по нижнему краю кадра.
