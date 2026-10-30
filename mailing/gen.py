C=dict(dark="#3C0008",deep="#8E0610",cream="#FFF6EA",white="#FFFBF6",gold="#E8B84A",gt="#9A7028",ink="#1A0507",mut="#5c4a42")
IMG="{{IMG_BASE}}"  # заменить на публичный URL папки images/
def btn(t,h): return f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center"><tr><td bgcolor="{C["deep"]}" style="border-radius:999px;"><a href="{h}" style="display:inline-block;padding:14px 28px;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:700;color:{C["cream"]};text-decoration:none;border-radius:999px;">{t}</a></td></tr></table>'
def p(t): return f'<p style="margin:0 0 14px;font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.55;color:{C["ink"]};">{t}</p>'
def h(t,s=26): return f'<h1 style="margin:0 0 14px;font-family:Georgia,\'Times New Roman\',serif;font-size:{s}px;line-height:1.15;color:{C["ink"]};">{t}</h1>'
def kick(t): return f'<div style="font-family:Arial,sans-serif;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:{C["gt"]};margin:0 0 8px;">{t}</div>'
def im(f,a): return f'<img src="{IMG}{f}" width="600" alt="{a}" style="display:block;width:100%;max-width:600px;height:auto;border:0;">'
PRICES=[("Выход","20–25 мин","14 370 ₽"),("Шоу","30 мин","19 640 ₽"),("Welcome","60 мин","26 480 ₽"),("По столикам","60 мин","37 900 ₽")]
def prices():
    r="".join(f'<tr><td style="padding:10px 12px;border-bottom:1px solid #eadccb;font-family:Arial,sans-serif;font-size:14px;color:{C["ink"]};"><b>{a}</b> · {b}</td><td align="right" style="padding:10px 12px;border-bottom:1px solid #eadccb;font-family:Georgia,serif;font-size:16px;font-weight:700;color:{C["deep"]};white-space:nowrap;">{c}</td></tr>' for a,b,c in PRICES)
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{C["white"]};border:1px solid #eadccb;">{r}</table><p style="margin:8px 0 0;font-family:Arial,sans-serif;font-size:12px;color:{C["mut"]};">Цены действуют до 01.12.2026. Оплата — чек самозанятого или безнал, без НДС.</p>'
def wrap(title,pre,body):
    return f'''<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="X-UA-Compatible" content="IE=edge"><title>{title}</title></head>
<body style="margin:0;padding:0;background:{C["dark"]};">
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:{C["dark"]};">{pre}&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{C["dark"]}"><tr><td align="center" style="padding:20px 8px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:{C["cream"]};">
<tr><td bgcolor="{C["deep"]}" style="padding:18px 28px;font-family:Georgia,serif;font-size:20px;font-weight:700;color:{C["cream"]};">Дед Мороз и Снегурочка <span style="font-family:Arial,sans-serif;font-size:12px;font-weight:400;color:{C["gold"]};">· Нижний Новгород</span></td></tr>
{body}
<tr><td bgcolor="{C["dark"]}" style="padding:22px 28px;font-family:Arial,sans-serif;font-size:13px;line-height:1.6;color:{C["cream"]};">
<b>Надежда</b> · <a href="tel:+79524516579" style="color:{C["gold"]};text-decoration:none;">8 (952) 451-65-79</a> · <a href="mailto:ded.moroz.nnovgorod@yandex.ru" style="color:{C["gold"]};">ded.moroz.nnovgorod@yandex.ru</a><br>
<a href="https://dedmoroz52.ru" style="color:{C["gold"]};">dedmoroz52.ru</a> · <a href="https://vk.ru/newyearmagic52" style="color:{C["gold"]};">ВКонтакте</a><br><br>
<span style="font-size:11px;color:#cdb9a8;">Вы получили это письмо как деловое предложение на корпоративный адрес заведения, опубликованный в открытых источниках. {{{{SENDER_LEGAL}}}} (ФИО/статус самозанятого, ИНН).<br>
Не хотите получать письма? <a href="{{{{UNSUBSCRIBE_URL}}}}" style="color:{C["gold"]};">Отписаться в один клик</a> — больше не напишем.</span>
</td></tr></table></td></tr></table></body></html>'''
def sec(x,pad="28px"): return f'<tr><td style="padding:{pad} 28px 4px;">{x}</td></tr>'
CTA_MAIL="mailto:ded.moroz.nnovgorod@yandex.ru?subject=%D0%9F%D0%B0%D1%80%D1%82%D0%BD%D1%91%D1%80%D1%81%D1%82%D0%B2%D0%BE"
CTA_TEL="tel:+79524516579"
# Письмо 1
e1=wrap("Новогодний номер, который продаёт ваши банкеты","Партнёрство для {{COMPANY}}: 10–15% ресторану, цена гостю не меняется",
 f'<tr><td>{im("hero-live.jpg","Дед Мороз и Снегурочка на банкете")}</td></tr>'+
 sec(kick("Для ресторанов и кафе")+h("Новогодний номер, который продаёт ваши банкеты")+
 p("Здравствуйте, {{NAME|коллеги}}!")+
 p("Мы — Дед Мороз и Снегурочка в Нижнем Новгороде, работаем только с юрлицами: рестораны, кафе, корпоративные праздники. Предлагаем {{COMPANY}} партнёрство на сезон 2026.")+
 p("<b>Как это работает:</b> вы предлагаете наш номер гостям, которые бронируют новогодний банкет. Цена для гостя не меняется, а ресторан получает <b>10–15% агентских</b> с каждого заказа.")+
 p("Для площадки: приезжаем за 30 минут, подачу горячего не ломаем."))+
 sec(kick("Форматы и цены")+prices())+
 sec(btn("Обсудить партнёрство",CTA_MAIL)+'<div style="height:8px"></div>'+p('<span style="font-size:13px;color:#5c4a42;">Или просто ответьте на это письмо — пришлём условия и материалы для ваших менеджеров.</span>'),"22px"))
# Письмо 2
e2=wrap("Чем удобен номер для площадки","Приезжаем за 30 минут, подачу горячего не ломаем — что получает {{COMPANY}}",
 f'<tr><td>{im("with-guests.jpg","Номер среди гостей")}</td></tr>'+
 sec(kick("Для менеджера площадки")+h("Приезжаем за 30 минут, подачу горячего не ломаем",24)+
 p("Здравствуйте, {{NAME|коллеги}}! Неделю назад писали о партнёрстве — коротко о том, почему номер не создаёт хлопот залу:")+
 p("• <b>Приходим заранее</b> — согласуем тайминг с администратором до начала программы.<br>• <b>Не в гостевом туалете</b> — переодеваемся в выделенной зоне.<br>• <b>Посадку не ломаем</b> — формат «По столикам» идёт между гостями, без перестановок.<br>• <b>Профессиональный тон</b> — без «утренника», для взрослой аудитории.")+
 p("<b>Ваша выгода:</b> 10–15% агентских с каждого заказа, цена для гостя та же. Дополнительный аргумент для менеджера, когда гость выбирает, где бронировать банкет."))+
 f'<tr><td style="padding:14px 28px 0;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td width="50%" style="padding-right:4px;">{im("fmt-welcome.jpg","Формат Welcome")}</td><td width="50%" style="padding-left:4px;">{im("fmt-stoliki.jpg","Формат По столикам")}</td></tr></table></td></tr>'+
 sec(prices())+sec(btn("Получить условия партнёрства",CTA_MAIL),"22px"))
# Письмо 3
e3=wrap("Последнее письмо о партнёрстве","Даты на декабрь разбирают — закрепить условия для {{COMPANY}}?",
 sec(kick("Сезон до 31 декабря")+h("Последнее письмо — и не будем отвлекать",24)+
 p("Здравствуйте, {{NAME|коллеги}}!")+
 p("Сезон короткий: новогодние банкеты бронируют сейчас, а свободные даты на декабрь ограничены. Если идея партнёрства интересна — достаточно ответить «да», и мы пришлём условия: 10–15% ресторану, цена для гостя без изменений.")+
 p("Цены текущего прайса действуют до 01.12.2026 — от 14 370 ₽ за выход 20–25 минут.")+
 p("Если не актуально — тоже ответьте, мы уберём ваш адрес из списка."))+
 f'<tr><td style="padding:10px 28px 0;">{im("team-stage.jpg","Дед Мороз и Снегурочка")}</td></tr>'+
 sec(btn("Да, пришлите условия",CTA_MAIL)+'<div style="height:10px"></div>'+f'<p style="margin:0 0 14px;text-align:center;font-family:Arial,sans-serif;font-size:14px;"><a href="{CTA_TEL}" style="color:{C["deep"]};font-weight:700;">Или позвонить Надежде: 8 (952) 451-65-79</a></p>',"22px"))
for n,e in [(1,e1),(2,e2),(3,e3)]: open(f"email-{n}.html","w").write(e)
