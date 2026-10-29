=== AURORA-TEAM-SECURITY-RELEASE (БЕЗОПАСНЫЙ РЕЛИЗ) ===
## Статус: ✅
Security/release map: teya-memory/wp/security-release-map.md
Required reports:
- teya-memory/wp/site-spec.json
- teya-memory/wp/build-report.json
Эти два JSON в этой волне не создавались. Их соберёт report compiler по контракту карты.
Режим: TEYA_DEPLOY_MODE=local-only, TEYA_ALLOW_PUBLISH=no, TEYA_ALLOW_ACTIVATE_THEME=no.
theme_slug: dedmoroz-nn
site_name: Дед Мороз и Снегурочка. Нижний Новгород
public_site_url: пусто
Форма: delivery=not_configured, писем наружу нет. Cookie-баннер и две политики обязательны до формы.
Rollback required: no
Release blockers: публикация закрыта флагами local-only; публичного URL нет; paint evidence и импорт WP Media ещё not_run и не могут быть pass; brand-kit и style anchor обложек blocked без gpt-image-2 (девять живых jpg для пяти страниц этим не отменяются).
incident_report:
- open: нет инцидента карты. site-spec.json и build-report.json сознательно оставлены report compiler. Деплой, FTP и активация не выполнялись. Секреты из teya.env.local в карту и фрагмент не копировались.
- blocker: публичный релиз этой волны запрещён. Paint-скриншоты и wp-media-map отсутствуют, потому что волн paint и удалённого деплоя ещё не было. Пока их нет, published=true ставить нельзя.
- constraint: локальная тема без активации; форма не вызывает почту, SMTP, CRM и Telegram; cookie-баннер и политики конфиденциальности и cookie обязательны до готовности формы; пакет темы не содержит teya-memory, .env и файлы credentials; dedmoroz.ru в URL отчётов не подставлять.
