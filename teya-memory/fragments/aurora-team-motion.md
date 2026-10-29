=== AURORA-TEAM-MOTION (GSAP/THREE ANIMATION) ===
## Статус: ✅ MOTION PLAN READY
Mode: MOTION PLAN
Motion map: teya-memory/wp/animation-motion-map.md
Implementation report: нет, внедрение не в этой волне
Libraries: GSAP core + CustomEase, только главная, crossfade 700ms, ease cubic-bezier(0.22, 1, 0.36, 1). Three.js не подключается.
threejs_scene_status: not_used
not_a_gap: true
Reduced motion: planned, 0ms, смена мгновенная
Performance blockers: нет. performance-accessibility-map.md ещё не был на диске, бюджет взят из блюпринта §22 и AURADESIGN. Чанк GSAP только на `/`, классический кадр героя в DOM без lazy, LCP — show-hero без ожидания JS.
Aurora handoff: сохранить `[data-hero]`, `[data-hero-frame]`, `[data-hero-photo="show|classic"]`, `[data-mode-toggle]`, `[data-mode="show|classic"]`, `[data-hero-line="show|classic"]`, `[data-price-column]`, `[data-price="8000|10000|15000"]`. Цены и H1 вне timeline. Стыки секций — статический CSS, не GSAP.
incident_report:
- open: нет инцидента по единственному жесту. Crossfade кадра и одной строки на главной описан, цены при переключении не меняются.
- blocker: нет блокера движения. Three.js не дыра: запрет заказчика явный, not_a_gap true, это не MOTION THREEJS BLOCKER.
- constraint: тяжёлый WebGL и вау-сцена запрещены; живые фото и заявка с телефона важнее. GSAP не ставить на ресторан, дом, сад, контакты, блог и политики. Код темы в этом запуске не писался.
