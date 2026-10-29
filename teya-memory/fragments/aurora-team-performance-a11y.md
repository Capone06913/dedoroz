=== AURORA-TEAM-PERFORMANCE-A11Y (CWV/A11Y) ===
## Статус: ✅
Performance/a11y map: teya-memory/wp/performance-accessibility-map.md
CWV targets: LCP<2.5s INP<200ms CLS<0.1
Accessibility blockers: нет
Performance blockers: нет
LCP: show-hero на главной и ресторане; family-home на доме; classic-studio на саде; на контактах LCP — телефон текстом. У LCP нет lazy. classic-hero не preload.
Картинки: живые jpg из ded/, лица не генерировать. Исходники 308 КБ–2,7 МБ в HTML не отдавать: AVIF/WebP, width/height, srcset 480–1280. brand-kit и обложки blocked, URL пустой, не запрашивать.
Шрифты: Cormorant Garamond и Manrope, кириллица, font-display swap, preload не больше двух woff2.
Motion: Three.js/WebGL not_used, not_a_gap=true. GSAP только crossfade главной около 700ms, reduced-motion 0ms. На внутренних страницах движения нет.
375px: липкая полоса 64px, padding-bottom 80px, кнопку формы не перекрывает. Баннер cookie не закрывает номер.
Семантика: skip link, main#primary, фокус 2px #1E4F86, подписи полей, цели нажатия от 48px.
incident_report:
- open: нет
- blocker: нет
- constraint: исходные jpg героя и дома тяжелее бюджета LCP, в карте обязательны производные, это не остановка сборки. Three.js запрещён брифом и записан как явное исключение, не дыра. gpt-image-2 отсутствует, brand-kit и обложки не входят в запросы пяти страниц. Деплой выключен, медиатека ещё не источник srcset.
