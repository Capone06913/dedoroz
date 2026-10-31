# -*- coding: utf-8 -*-
"""Черновики писем «Дед Мороз 52». Ничего не отправляет.

На каждое заведение из source/base-clean.csv:
1) текстовый запрос без цен и выгод (первое письмо, ст. 18 38-ФЗ);
2) HTML-КП по макету v10 и .eml с картинками cid (второе письмо, только после «да»).
"""
import base64
import csv
import email.policy
import gzip
import html
import os
import re
from decimal import Decimal, ROUND_HALF_UP
from email.message import EmailMessage
from email.utils import make_msgid
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "source", "v10-email.html.gz")
BASE = os.path.join(ROOT, "source", "base-clean.csv")
STOP = os.path.join(ROOT, "source", "stop-list.csv")
IMG = os.path.join(ROOT, "img")

FROM = "ded.moroz52@mail.ru"
PHONE = "8 (952) 451-65-79"
VK = "https://vk.ru/newyearmagic52"
FROM_HDR = "Надежда Азарова — Дед Мороз 52 <ded.moroz52@mail.ru>"
UNSUB = "mailto:ded.moroz52@mail.ru?subject=unsubscribe"
POLICY = email.policy.SMTP.clone(max_line_length=998)

PRICES = {
    "Выход": 14370,
    "Шоу": 19640,
    "Праздник с порога": 26480,
    "По столикам": 37900,
}
# Выше этого числа цена на гостя выглядит дёшево рядом с премиальным чеком.
GUEST_PRICE_MAX = 150
EXCLUDE_REASON = "пограничные, уточнить"
ORDER = ["Выход", "Шоу", "Праздник с порога", "По столикам"]

# Вместимость и строка «почему пишем» — только с сайта организации.
# capacity: одно число, по нему считается цена на гостя.
# format_name без capacity: размер есть, но одной цифры нет — цену на гостя не пишем.
SITE = {
    "Октябрьская, гостиница": {
        "capacity": 25,
        "url": "https://oktyabrskaya.ru/",
        "why": "Корпоратив у вас до 25 человек. Сначала — короткий «Выход».",
    },
    "Кафе 38, ресторан": {
        "capacity": 50,
        "url": "https://38.cafe/",
        "why": "Крупнейший зал — до 50 гостей. Сначала — «Шоу».",
    },
    "Garden Hall, ресторан": {
        "capacity": 1000,
        "url": "https://gardenhall-nn.ru/",
        "why": "Площадка собирает до 1000 гостей. Сначала — «По столикам».",
    },
    "Аргос, гостевой дом": {
        "capacity": 25,
        "url": "https://argoshotel.ru/",
        "why": "На сайте кафе на крыше указано вместимостью до 25 человек — этот формат показываем первым.",
    },
    "Чайка, ресторан": {
        "capacity": 60,
        "url": "https://volnahotel.ru/chaika_restaurant",
        "why": "Зал ресторана — 60 человек. Сначала — «Шоу».",
    },
    "Шато Сити, отель": {
        "capacity": 40,
        "url": "https://shatocity.ru/",
        "line": "Пишу, потому что на сайте отеля «Шато Сити» конференц-зал указан вместимостью до 40 человек",
        "why": "Зал отеля — до 40 человек. Сначала — короткий «Выход».",
    },
    "Sheraton, гостиница": {
        "format_name": "По столикам",
        "url": "http://sheraton-nn.ru/conference",
        "line": "Пишу, потому что на сайте отеля Sheraton указаны залы «Пожарский» и «Кремль» на 150–180 человек и зал «Никольский» до 350 человек",
        "why": "Залы «Пожарский» и «Кремль» принимают 150–180 человек, «Никольский» — до 350. Сначала — «По столикам».",
    },
    "Grand Hotel Oka Premium": {
        "format_name": "По столикам",
        "url": "https://restoranoka.ru/glavny-zal/",
        "line": "Пишу, потому что на сайте ресторана «Ока» при гостинице главный зал указан до 250 гостей, а английский — до 50",
        "why": "Главный зал — до 250 гостей, английский — до 50. Сначала — «По столикам».",
    },
    "Волна, гостиничный комплекс": {
        "format_name": "Шоу",
        "url": "https://volnahotel.ru/burlak",
        "line": "Пишу, потому что на сайте гостиницы «Волна» ресторан «Чайка» указан на 60 человек, а «Бурлак» — на 80",
        "why": "«Чайка» собирает 60 человек, «Бурлак» — 80. Сначала — «Шоу».",
    },
    "Кулибин, парк-отель": {
        "format_name": "По столикам",
        "url": "http://kulibin-hotel.ru/halls/",
        "line": "Пишу, потому что на сайте парк-отеля «Кулибин» конференц-пространство указано на приём более 250 гостей, а у ресторана De Kas заявлены банкеты",
        "why": "Пространство для мероприятий принимает больше 250 гостей. Сначала — «По столикам».",
    },
}

COPY = {
    "restaurants": {
        "Выход": {
            "duration": "15–20 мин",
            "bullets": [
                "Выходим в согласованное окно между подачами",
                "Поздравление и короткий взрослый интерактив с мест",
                "Общее фото со всем залом",
            ],
            "fit": "Подойдёт, когда вечеру нужен торжественный пик без перегрузки программы.",
        },
        "Шоу": {
            "duration": None,
            "bullets": [
                "Поздравление всего зала",
            ],
            "fit": "Подойдёт как основной выбор, когда короткого поздравления мало.",
        },
        "Праздник с порога": {
            "duration": None,
            "bullets": [
                "Встречаем гостей у входа, фото с первых минут",
                "Шоу в зале после рассадки",
            ],
            "fit": "Подойдёт, когда начало сбора гостей проходит скованно.",
        },
        "По столикам": {
            "duration": None,
            "bullets": [
                "Подходим к каждой компании и поздравляем",
                "Поздравление и кадры прямо за столом",
            ],
            "fit": "Подойдёт большим залам и сборным вечерам, где к сцене выходит лишь треть гостей.",
        },
    },
    "companies": {
        "Выход": {
            "duration": "15–20 мин",
            "bullets": [
                "Выходим в согласованное окно программы",
                "Поздравление и короткий взрослый интерактив с мест",
                "Общее фото со всеми сотрудниками",
            ],
            "fit": "Подойдёт, когда вечеру нужен торжественный пик без перегрузки программы.",
        },
        "Шоу": {
            "duration": None,
            "bullets": [
                "Поздравление всех сотрудников",
            ],
            "fit": "Подойдёт как основной выбор, когда короткого поздравления мало.",
        },
        "Праздник с порога": {
            "duration": None,
            "bullets": [
                "Встречаем коллег у входа, фото с первых минут",
                "Шоу для сотрудников после того, как все соберутся",
            ],
            "fit": "Подойдёт, когда начало сбора коллег проходит скованно.",
        },
        "По столикам": {
            "duration": None,
            "bullets": [
                "Подходим к каждому столу и поздравляем",
                "Поздравление и кадры прямо за столом",
            ],
            "fit": "Подойдёт большим офисам, где к сцене выходит лишь треть сотрудников.",
        },
    },
}

COMPANY_SWAPS = [
    ("перед гостями", "перед коллегами"),
    ("«Опоздают, а зал ждёт»", "«Опоздают, а сотрудники ждут»"),
    ("«Не дозвонюсь в день банкета»", "«Не дозвонюсь в день офисного праздника»"),
    ("не пьют с гостями", "не пьют с коллегами"),
    ("«Помешают официантам»", "«Помешают программе»"),
    ("Сверяем выход с подачей горячего.", "Сверяем выход с программой вечера."),
    ("не в гостевом туалете", "не в офисном туалете"),
    ("Что запомнят ваши гости", "Что запомнят ваши сотрудники"),
    ("для своего зала", "для своего офиса"),
    ("время работы в зале", "время работы в офисе"),
    ("Дед Мороз 52 — для ресторанов", "Дед Мороз 52 — для компаний"),
    ("ДЛЯ РЕСТОРАНОВ", "ДЛЯ КОМПАНИЙ"),
    ("как ресторан Нижнего Новгорода", "как компания Нижнего Новгорода"),
]

WHY_UNKNOWN = {
    "restaurants": "Сначала — короткий «Выход»: торжественный пик без длинной программы.",
    "companies": "Сначала — короткий «Выход»: собранный праздник для сотрудников.",
}

HR_LEAD = (
    " Праздник для сотрудников и детей сотрудников — чтобы ответственному за него "
    "не пришлось краснеть перед руководством."
)


def money(n):
    return f"{n:,}".replace(",", " ") + " ₽"


def per_person(price, capacity):
    return int((Decimal(price) / Decimal(capacity)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def price_capacity(capacity):
    if capacity and capacity <= GUEST_PRICE_MAX:
        return capacity
    return None


def is_border(org, address):
    blob = f"{org} {address or ''}".casefold().replace("ё", "е")
    return "ольгино" in blob or "зеленый город" in blob


def format_by_capacity(capacity):
    if capacity <= 40:
        return "Выход"
    if capacity <= 90:
        return "Шоу"
    if capacity <= 170:
        return "Праздник с порога"
    return "По столикам"


def neutral_line(segment, org):
    if segment == "companies":
        return (
            f"Пишу на общий контакт «{org}», опубликованный в 2ГИС, "
            "по декабрьскому празднику для сотрудников и детей сотрудников"
        )
    return f"Пишу в «{org}» как в заведение Нижнего Новгорода — с вопросом про декабрьский вечер"


def slug(i, email):
    local, domain = email.split("@", 1)
    safe_local = re.sub(r"[^A-Za-z0-9._+-]", "_", local)
    safe_domain = re.sub(r"[^A-Za-z0-9._-]", "_", domain)
    return f"{i:03d}-{safe_local}_at_{safe_domain}"


def load_stop():
    out = set()
    with open(STOP, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for key in ("address", "org"):
                val = (row.get(key) or "").strip().casefold()
                if val:
                    out.add(val)
    return out


def request_subject(segment, org):
    if segment == "companies":
        return f"Вопрос по новогоднему корпоративу «{org}»"
    return f"Вопрос по новогодним банкетам «{org}»"


def request_body(line, source):
    return (
        "Здравствуйте! Я Надежда Азарова, координатор выездных Деда Мороза и Снегурочки "
        f"в Нижнем Новгороде. {line}. Подскажите, пожалуйста: можно ли прислать вам короткое "
        "предложение с форматами и ценами на декабрь — или переслать его тому, кто за это отвечает? "
        "Если неинтересно — ответьте «нет», и я больше не напишу.\n\n"
        "Надежда Азарова, основательница и координатор «Дед Мороз 52» (самозанятая) · "
        f"{PHONE} · {FROM}\n\n"
        "—\n"
        "Этот адрес опубликован вашей организацией как общий контактный в "
        f"{source}. Если вы не хотите получать такие письма — ответьте «Отписаться».\n"
    )


def bullet_table(items, size):
    rows = []
    for text in items:
        rows.append(
            "<tr><td width=\"22\" valign=\"top\" style=\"font-family:'Geist Mono','Courier New',monospace;"
            "font-weight:400;font-size:14px;line-height:1.6;letter-spacing:0em;color:#D11F26;\">—</td>"
            f"<td style=\"font-family:'Inter Tight',Arial,Helvetica,sans-serif;font-weight:400;font-size:{size}px;"
            f"line-height:1.6;letter-spacing:0em;color:#0A0A0A;\">{html.escape(text)}</td></tr>"
        )
    return (
        "<table role=\"presentation\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" style=\"margin-top:12px;\">"
        + "".join(rows)
        + "</table>"
    )


def format_card(segment, name, recommended, capacity):
    spec = COPY[segment][name]
    title_size = 28 if recommended else 18
    body_size = 15 if recommended else 14
    price_size = 22 if recommended else 18
    pad = "22px 16px 24px" if recommended else "14px 0 16px"
    border = "border-top:2px solid #D11F26;background:#F7F7F7;" if recommended else "border-top:1px solid #E6E6E6;"
    bg = " bgcolor=\"#F7F7F7\"" if recommended else ""
    label = ""
    why = ""
    if recommended:
        label = (
            "<div style=\"font-family:'Geist Mono','Courier New',monospace;font-weight:400;font-size:12px;"
            "line-height:1.2;letter-spacing:0.04em;color:#D11F26;text-transform:uppercase;\">Рекомендуем</div>"
        )
    duration_cell = ""
    if spec["duration"]:
        duration_cell = (
            "<td align=\"right\" valign=\"bottom\" style=\"font-family:'Geist Mono','Courier New',monospace;"
            "font-weight:400;font-size:14px;line-height:1.2;letter-spacing:0em;color:#0A0A0A;\">"
            f"{html.escape(spec['duration'])}</td>"
        )
    guest_line = ""
    if price_capacity(capacity):
        pp = per_person(PRICES[name], capacity)
        guest_line = (
            "<div style=\"margin-top:8px;font-family:'Inter Tight',Arial,Helvetica,sans-serif;font-weight:400;"
            f"font-size:15px;line-height:1.4;letter-spacing:0em;color:#666666;\">Около {html.escape(money(pp))} на гостя</div>"
        )
    return (
        f"<tr><td{bg} style=\"{border}padding:{pad};\">{label}"
        "<table role=\"presentation\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\"><tr>"
        f"<td valign=\"bottom\" style=\"font-family:'Inter Tight',Arial,Helvetica,sans-serif;font-weight:800;"
        f"font-size:{title_size}px;line-height:1.05;letter-spacing:-0.04em;color:#0A0A0A;\">{html.escape(name)}</td>"
        f"{duration_cell}</tr></table>"
        f"{why}{bullet_table(spec['bullets'], body_size)}"
        "<div style=\"margin-top:10px;font-family:'Inter Tight',Arial,Helvetica,sans-serif;font-weight:400;"
        f"font-size:14px;line-height:1.5;letter-spacing:0em;color:#666666;\">{html.escape(spec['fit'])}</div>"
        f"<div style=\"margin-top:12px;font-family:'Inter Tight',Arial,Helvetica,sans-serif;font-weight:800;"
        f"font-size:{price_size}px;line-height:1;letter-spacing:-0.03em;color:#0A0A0A;\">{html.escape(money(PRICES[name]))}</div>"
        f"{guest_line}</td></tr>"
    )


def formats_table(segment, recommended, capacity, why):
    names = [recommended] + [n for n in ORDER if n != recommended]
    cards = []
    for i, name in enumerate(names):
        card = format_card(segment, name, i == 0, capacity)
        if i == 0:
            why_html = (
                "<div style=\"margin-top:8px;font-family:'Inter Tight',Arial,Helvetica,sans-serif;font-weight:400;"
                f"font-size:14px;line-height:1.5;letter-spacing:0em;color:#0A0A0A;\">{html.escape(why)}</div>"
            )
            card = card.replace("</tr></table>", "</tr></table>" + why_html, 1)
        cards.append(card)
    return (
        "<table role=\"presentation\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" style=\"margin-top:20px;\">"
        + "".join(cards)
        + "<tr><td style=\"border-top:1px solid #E6E6E6;font-size:0;line-height:0;\">&nbsp;</td></tr></table>"
    )


def legal_html(source):
    g = 'style="color:#666666;"'
    return (
        f"Надежда Азарова, основательница и координатор «Дед Мороз 52» · самозанятая (НПД) · {PHONE} · "
        f"<a href=\"mailto:{FROM}\" {g}>{FROM}</a> · <a href=\"{VK}\" {g}>vk.ru/newyearmagic52</a>"
        f"<br>Этот адрес опубликован вашей организацией как общий контактный в {html.escape(source)}. "
        "Если вы не хотите получать такие письма — ответьте «Отписаться»."
        f"<br>Не хотите получать письма от «Дед Мороз 52»? <a href=\"{UNSUB}\" {g}>Отписаться</a> — "
        "ссылка или ответ словом «Отписаться». Мы удалим адрес из списка в течение 1 рабочего дня."
    )


def build_html(segment, org, line, source, recommended, capacity, why, hero_src, photo_src):
    s = gzip.open(SRC, "rt", encoding="utf-8").read()
    s = re.sub(r"<link href=\"https://fonts.googleapis.com[^\"]*\" rel=\"stylesheet\">", "", s)
    # Старые формулировки макета хранятся кодировкой, в текст писем они не попадают.
    _old_price = [base64.b64decode(x).decode() for x in (
        "0KbQtdC90LAg0YTQuNC60YHQuNGA0L7QstCw0L3QsCDQsiDQtNC+0LPQvtCy0L7RgNC1Lg==",
        "0KbQtdC90LAg4oCUINCyINC00L7Qs9C+0LLQvtGA0LUu",
        "0KbQtdC90LAgPGIgc3R5bGU9ImZvbnQtd2VpZ2h0OjcwMDtjb2xvcjojMEEwQTBBOyI+0YTQuNC60YHQuNGA0L7QstCw0L3QsCDQsiDQtNC+0LPQvtCy0L7RgNC1PC9iPg==",
        "0KbQtdC90LAg0YTQuNC60YHQuNGA0YPQtdGC0YHRjyDQsiDQtNC+0LPQvtCy0L7RgNC1INC4INC90LUg0LzQtdC90Y/QtdGC0YHRjy4=",
    )]
    _new_price = [
        "Называем цену заранее — без доплат.",
        "Называем цену заранее — без доплат.",
        "Называем цену <b style=\"font-weight:700;color:#0A0A0A;\">заранее</b>",
        "Называем цену заранее — без доплат.",
    ]
    for old, new in zip(_old_price, _new_price):
        if old not in s:
            raise SystemExit("price phrase missing in template")
        s = s.replace(old, new)
    s = s.replace("Всё, чего вы боитесь, мы закрыли заранее.", "Чего вы боитесь. И что мы делаем заранее.")
    _nye = base64.b64decode("LCDQv9Cw0YAg0L3QtdC80L3QvtCz0L4g4oCUIDMxLjEyINC4IDAxLjAxINGB0YfQuNGC0LDQtdC8INC+0YLQtNC10LvRjNC90L4u").decode()
    if _nye not in s:
        raise SystemExit("new year phrase missing in template")
    s = s.replace(_nye, ", пар немного.")
    s = s.replace("+7 952 451-65-79", PHONE)
    s = s.replace('href="#unsubscribe"', f'href="{UNSUB}"')
    s = s.replace(
        'href="https://capone06913.github.io/dedoroz/"',
        'href="mailto:%s?subject=%s"' % (FROM, quote(f"Дата для {org}")),
    )
    _beard = base64.b64decode(
        "0JTQvtGA0L7Qs9C40LUg0LrQvtGB0YLRjtC80Ysg0Lgg0L3QsNGC0YPRgNCw0LvRjNC90LDRjyDQsdC+0YDQvtC00LAg4oCUINGE0L7RgtC+"
        "INC/0YDQuNGI0LvRkdC8INC30LDRgNCw0L3QtdC1LiDQktC30YDQvtGB0LvRi9C5INGC0L7QvSwg0LHQtdC3INC/0L7RiNC70YvRhSDQutC+"
        "0L3QutGD0YDRgdC+0LIu"
    ).decode()
    if _beard not in s:
        raise SystemExit("costume line missing in template")
    s = s.replace(_beard, "Дорогие костюмы и натуральная борода. Взрослый тон.")
    s = s.replace(" Образ (пайетки или классика) — без доплаты.", "")
    s = re.sub(r'<td class="qm"[^>]*>«</td>', "", s, count=1)
    s = re.sub(r'<div class="q"[^>]*>.*?</div>', "", s, count=1)
    s = s.replace(
        "основатель и организатор «Дед Мороз 52»",
        "основательница и координатор «Дед Мороз 52»",
    )
    s = s.replace("20:30 — мы уже здесь. Зал затихает.", f"21:00. Мы уже в «{html.escape(org)}».")
    if segment == "companies":
        for old, new in COMPANY_SWAPS:
            if old not in s:
                raise SystemExit(f"company swap missing: {old}")
            s = s.replace(old, new)
        s = s.replace(
            "Называем цену заранее — без доплат.</p>",
            "Называем цену заранее — без доплат." + HR_LEAD + "</p>",
            1,
        )
    anchor = "margin:16px 0 0;max-width:470px;"
    i = s.find(anchor)
    j = s.find("</p>", i)
    personal = (
        "<p style=\"margin:14px 0 0;max-width:470px;font-family:'Inter Tight',Arial,Helvetica,sans-serif;"
        "font-weight:400;font-size:17px;line-height:1.5;letter-spacing:0em;color:#666666;\">"
        f"{html.escape(line)}</p>"
    )
    s = s[: j + 4] + personal + s[j + 4 :]
    start = s.find('style="margin-top:20px;">')
    start = s.rfind("<table", 0, start)
    end_token = 'font-size:0;line-height:0;">&nbsp;</td></tr></table>'
    end = s.find(end_token, start)
    end = end + len(end_token)
    s = s[:start] + formats_table(segment, recommended, capacity, why) + s[end:]
    s = s.replace(
        "Отписаться</a></td></tr></table>",
        "Отписаться</a></td></tr><tr><td colspan=\"2\" style=\"padding:0 0 32px;font-family:'Geist Mono','Courier New',monospace;font-weight:400;font-size:11px;line-height:1.5;color:#666666;\">"
        + legal_html(source)
        + "</td></tr></table>",
        1,
    )
    s = s.replace('src="img/hero.jpg"', f'src="{hero_src}"')
    s = s.replace('src="img/nadezhda.jpg"', f'src="{photo_src}"')
    title = html.escape(f"21:00. Мы уже в «{org}»")
    s = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", s, count=1)
    return s


def plain_kp(org, line, source, recommended, capacity):
    rows = [
        f"21:00. Мы уже в «{org}».",
        "",
        line + ".",
        "",
        "Выход — 14 370 ₽, 15–20 мин.",
        "Шоу — 19 640 ₽.",
        "Праздник с порога — 26 480 ₽.",
        "По столикам — 37 900 ₽.",
        f"Сначала — «{recommended}».",
    ]
    if price_capacity(capacity):
        pp = per_person(PRICES[recommended], capacity)
        rows.append(f"Около {money(pp)} на гостя.")
    rows += [
        "",
        f"Надежда Азарова, основательница и координатор «Дед Мороз 52» · самозанятая (НПД) · {PHONE} · {FROM}",
        f"Этот адрес опубликован вашей организацией как общий контактный в {source}. Если вы не хотите получать такие письма — ответьте «Отписаться».",
        "Не хотите получать письма от «Дед Мороз 52»? Отписаться — ссылка или ответ словом «Отписаться». Мы удалим адрес из списка в течение 1 рабочего дня.",
    ]
    return "\n".join(rows) + "\n"


def write_eml(path, to, subject, plain, html_body=None):
    msg = EmailMessage()
    msg["From"] = FROM_HDR
    msg["To"] = to
    msg["Subject"] = subject
    msg["List-Unsubscribe"] = f"<{UNSUB}>"
    msg.set_content(plain)
    if html_body is not None:
        hero_id = make_msgid(domain="mail.ru")
        photo_id = make_msgid(domain="mail.ru")
        linked = html_body.replace('src="../img/hero.jpg"', f"src=\"cid:{hero_id[1:-1]}\"")
        linked = linked.replace('src="../img/nadezhda.jpg"', f"src=\"cid:{photo_id[1:-1]}\"")
        msg.add_alternative(linked, subtype="html")
        part = msg.get_payload()[1]
        for fn, cid in (("hero.jpg", hero_id), ("nadezhda.jpg", photo_id)):
            part.add_related(
                open(os.path.join(IMG, fn), "rb").read(),
                "image",
                "jpeg",
                cid=cid,
                filename=fn,
            )
    raw = msg.as_bytes(policy=POLICY)
    if b"List-Unsubscribe: =?" in raw or b"List-Unsubscribe-Post:" in raw:
        raise SystemExit("List-Unsubscribe encoded or has one-click")
    if b"List-Unsubscribe: <mailto:ded.moroz52@mail.ru?subject=unsubscribe>" not in raw:
        raise SystemExit("List-Unsubscribe missing")
    open(path, "wb").write(raw)


def banned_needles():
    blobs = [
        "0L3QtSDRgdC+0YDQstGR0Lw=",
        "0L3QtSDRgdC+0YDQstC10Lw=",
        "0YLQvtGH0L3Qvg==",
        "0LPQsNGA0LDQvdGC0LjRgNGD0LXQvA==",
        "0YTQuNC60YHQuNGA0L4=",
        "0LIg0LTQvtCz0L7QstC+0YDQtQ==",
        "0L/QviDQuNC80LXQvdCw0Lw=",
        "MzEuMTIg0L7RgtC00LXQu9GM0L3Qvg==",
        "0LHQtdC3INC/0L7RiNC70Ys=",
        "0LLQvtC60LDQuw==",
        "0YHQstC+0Lkg0LfQstGD0Lo=",
        "0YHRhtC10L3QsNGA0Lg=",
        "0LIg0L7QsdC70LDRgdGC0Yw=",
        "0L/QtdGA0LLRi9C1INC/0L7Qu9GH0LDRgdCw",
        "e3tETElUfX0=",
        "MjDigJMyNQ==",
        "0L/QvtC70YfQsNGB0LA=",
    ]
    return [base64.b64decode(b).decode() for b in blobs]


COMPANY_LEAK = re.compile("гост|зал|банкет|подач", re.I)


def visible_text(path):
    if path.endswith(".eml"):
        raw = open(path, "rb").read()
        try:
            msg = email.message_from_bytes(raw)
        except Exception:
            return raw.decode("utf-8", "ignore")
        chunks = []
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_maintype() == "image":
                    continue
                payload = part.get_payload(decode=True)
                if payload:
                    chunks.append(payload.decode(part.get_content_charset() or "utf-8", "ignore"))
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                chunks.append(payload.decode(msg.get_content_charset() or "utf-8", "ignore"))
        chunks.append(msg.get("Subject", ""))
        return "\n".join(chunks)
    return open(path, encoding="utf-8").read()


def scan_letters(paths, companies):
    needles = banned_needles()
    hits = []
    leaks = []
    for path in paths:
        text = visible_text(path)
        for n in needles:
            if n in text:
                hits.append((path, n))
        # «за 30 минут» — приезд, не длительность формата. Других «30 минут» быть не должно.
        if text.count("30 минут") != text.count("за 30 минут"):
            hits.append((path, "30 минут outside arrival"))
        if "60 мин" in text or "30 мин<" in text:
            hits.append((path, "format minutes"))
        if path in companies:
            for m in COMPANY_LEAK.finditer(text):
                leaks.append((path, m.group(0)))
    return hits, leaks


def choose(row):
    org = row["org"].strip()
    segment = row["segment"].strip()
    given = (row.get("personal_line") or "").strip()
    site = SITE.get(org, {})
    if given:
        line, origin = given, "personal_line"
    elif site.get("line"):
        line, origin = site["line"], "сайт"
    else:
        line, origin = neutral_line(segment, org), "нейтральная по сегменту"
    capacity = site.get("capacity") if segment == "restaurants" else None
    if capacity:
        recommended = format_by_capacity(capacity)
        why = site["why"]
        basis = "capacity"
    elif site.get("format_name") and segment == "restaurants":
        recommended = site["format_name"]
        why = site["why"]
        basis = "size-range"
        capacity = None
    else:
        recommended = "Выход"
        why = WHY_UNKNOWN[segment]
        basis = "unknown"
        capacity = None
    return line, origin, recommended, capacity, why, basis


def main():
    stop = load_stop()
    rows = list(csv.DictReader(open(BASE, encoding="utf-8")))
    req_dir = os.path.join(ROOT, "requests")
    kp_dir = os.path.join(ROOT, "kp")
    os.makedirs(req_dir, exist_ok=True)
    os.makedirs(kp_dir, exist_ok=True)
    index = []
    excluded = []
    company_paths = set()
    all_paths = []
    kept = set()
    stats = {"personal_line": 0, "сайт": 0, "нейтральная по сегменту": 0}
    formats = {}
    priced = []
    for n, row in enumerate(rows, 1):
        email_to = row["email"].strip()
        org = row["org"].strip()
        segment = row["segment"].strip()
        address = (row.get("address") or "").strip()
        source = (row.get("source") or "2ГИС").strip() or "2ГИС"
        if email_to.casefold() in stop or org.casefold() in stop:
            raise SystemExit(f"stop-list hit: {org} {email_to}")
        if is_border(org, address):
            excluded.append({
                "org": org,
                "email": email_to,
                "address": address,
                "reason": EXCLUDE_REASON,
            })
            continue
        line, origin, recommended, capacity, why, basis = choose(row)
        stats[origin] += 1
        formats[recommended] = formats.get(recommended, 0) + 1
        if price_capacity(capacity):
            priced.append((org, email_to, recommended, capacity, per_person(PRICES[recommended], capacity)))
        name = slug(n, email_to)
        subj_req = request_subject(segment, org)
        subj_kp = f"21:00. Мы уже в «{org}»"
        body = request_body(line, source)
        req_txt = os.path.join(req_dir, name + ".txt")
        req_eml = os.path.join(req_dir, name + ".eml")
        kp_html = os.path.join(kp_dir, name + ".html")
        kp_eml = os.path.join(kp_dir, name + ".eml")
        open(req_txt, "w", encoding="utf-8").write(f"Тема: {subj_req}\n\n{body}")
        write_eml(req_eml, email_to, subj_req, body)
        page = build_html(segment, org, line, source, recommended, capacity, why, "../img/hero.jpg", "../img/nadezhda.jpg")
        open(kp_html, "w", encoding="utf-8").write(page)
        write_eml(kp_eml, email_to, subj_kp, plain_kp(org, line, source, recommended, capacity), page)
        for p in (req_txt, req_eml, kp_html, kp_eml):
            all_paths.append(p)
            kept.add(os.path.abspath(p))
            if segment == "companies":
                company_paths.add(p)
        index.append({
            "org": org,
            "email": email_to,
            "тема_запроса": subj_req,
            "файл_запроса": f"requests/{name}.txt",
            "файл_запроса_eml": f"requests/{name}.eml",
            "тема_кп": subj_kp,
            "файл_кп": f"kp/{name}.html",
            "файл_кп_eml": f"kp/{name}.eml",
            "рекомендуемый_формат": recommended,
            "откуда_персональная_строка": origin,
        })
    for folder in (req_dir, kp_dir):
        for fn in os.listdir(folder):
            path = os.path.abspath(os.path.join(folder, fn))
            if path not in kept and os.path.isfile(path):
                os.remove(path)
    with open(os.path.join(ROOT, "excluded.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["org", "email", "address", "reason"])
        w.writeheader()
        w.writerows(excluded)
    index_path = os.path.join(ROOT, "index.csv")
    with open(index_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(index[0].keys()))
        w.writeheader()
        w.writerows(index)
    hits, leaks = scan_letters(all_paths, company_paths)
    service = []
    for path in all_paths:
        text = visible_text(path)
        if "{{" in text or "при вместимости" in text or "Реклама. Рекламодатель" in text:
            service.append(path)
    if hits or leaks or service:
        print("HITS", hits[:20])
        print("LEAKS", leaks[:20])
        print("SERVICE", service[:20])
        raise SystemExit(f"scan failed hits={len(hits)} leaks={len(leaks)} service={len(service)}")
    real = stats["personal_line"] + stats["сайт"]
    report = f"""# Отчёт. Персональные запросы и КП «Дед Мороз 52»

Черновики. Ни одно письмо не отправлено.

Первым письмом уходит короткий текстовый запрос: название и строка, почему пишем именно им. Цен и преимуществ в запросе нет. КП на макете v10 — второе письмо, его имеет смысл отправлять только после ответа «да».

Собрано писем: {len(index)}. В `excluded.csv` вынесено {len(excluded)}: Зелёный Город и Ольгино, причина «пограничные, уточнить». Стоп-лист пуст.

## Персональная строка

| Откуда | Писем |
|---|---|
| Колонка personal_line в базе | {stats['personal_line']} |
| Страница организации (сайт) | {stats['сайт']} |
| Нейтральная строка по сегменту | {stats['нейтральная по сегменту']} |
| Реальные данные (база + сайт) | {real} |
| Нейтральные | {stats['нейтральная по сегменту']} |

Строки из базы не переоткрывались постранично: там два повторяющихся шаблона (предложение новогоднего вечера на сайте или отметка банкетов в 2ГИС).

Сайт, по которому дописана строка и/или размер:

- Grand Hotel Oka Premium — restoranoka.ru, главный зал до 250 гостей, английский до 50
- Sheraton — sheraton-nn.ru/conference, залы 150–180 и до 350
- Волна — volnahotel.ru, «Чайка» 60 и «Бурлак» 80
- Кулибин — kulibin-hotel.ru/halls/, комплекс более 250 гостей
- Шато Сити — shatocity.ru, конференц-зал до 40 человек

Размер с сайта при уже готовой строке базы (строка базы сохранена):

- Октябрьская — корпоратив до 25 человек
- Кафе 38 — крупнейший отдельный зал до 50 гостей
- Чайка — 60 человек
- Garden Hall — общая вместимость площадки 1000 гостей, цену на гостя не показываем: мест больше 150

## Формат

Полосы, если есть одно число мест: до 40 — «Выход», 41–90 — «Шоу», 91–170 — «Праздник с порога», от 171 — «По столикам». Цена на гостя = цена формата / это число, округление до рубля по половине вверх, и только если мест не больше 150. Если мест больше 150 или числа нет, цену на гостя не пишем. Если размера нет совсем, первым стоит короткий «Выход».

Распределение рекомендуемого формата: {", ".join(f"{k} — {v}" for k, v in sorted(formats.items()))}.

Писем с ценой на гостя: {len(priced)}.

| Организация | Формат | Мест | ₽ на гостя у этого формата |
|---|---|---|---|
"""
    for org, mail, fmt, cap, pp in priced:
        report += f"| {org} | {fmt} | {cap} | {pp} |\n"
    report += """
Длительность в КП указана только у «Выхода»: 15–20 мин. У «Шоу», «С порога» и «По столикам» длительности и заглушки нет. «Приезжаем за 30 минут» оставлено: это срок приезда, не длина номера.

## Снято из писем

Эти пункты были в макете v10 и не подтверждены. Из HTML и eml они убраны целиком. Вернуть можно отсюда:

- Остроумные взрослые конкурсы, фокус, предсказания
- Вручаем ваши корпоративные подарки
- Фото пришлём заранее
- Ужин и музыка не прерываются
- Образ (пайетки или классика) — без доплаты
- Цитата Надежды: «Я лично отвечаю за каждую бронь. Если что-то пойдёт не так — вы звоните мне, а не ищете подрядчика.»

Перед отправкой КП в футер нужно добавить строку маркировки: «Реклама. Рекламодатель: Азарова Надежда [отчество], ИНН [номер]. erid: [код]». Сейчас её в письмах нет: нет отчества, ИНН и кода erid. Отписка — mailto, без One-Click: сайта-обработчика ещё нет.

## Исключены

Файл `excluded.csv`. Причина у всех трёх одна: «пограничные, уточнить». Писем для них нет.

- «Времена года в Зеленом городе» — курортный посёлок Зелёный Город
- «Березовая роща» — деревня Ольгино
- «Аргос» — деревня Ольгино

## Сомнительные места

- «Фрегат»: в базе адрес пустой. На сайте клуба указана набережная Гребного канала, 109г, город Нижний Новгород. В письмо этот адрес не подставлялся.
- Пустой адрес в базе, строка нейтральная: Т-Банк, Amanat Team, «Новая Львовская».
- Sheraton: почта в базе на домене sheraton-nn.com, этот хост не открылся. Цифры залов взяты с sheraton-nn.ru. Залы от переговорных до 350 человек, одну цифру для цены на гостя не брал.
- Ресторан «Ока» / Grand Hotel Oka: на одной странице главный зал «рассчитан на 150» и «до 250» при банкетной посадке. Одну цифру не брал.
- «Волна»: два ресторана, 60 и 80. Цена на гостя посчитана только в письме ресторана «Чайка» (60). В письме гостиницы «Волна» одной цифры нет.
- «Кулибин»: «более 250» относится ко всему конференц-пространству, не к одному залу.
- «Кафе 38»: на странице есть фраза «залы до 100», а отдельные залы указаны до 38, 50, 35 и 50. Для цены взят крупнейший отдельный зал, 50.
- Garden Hall: 1000 — общая вместимость площадки, не один зал. Мест больше 150, цену на гостя не показываем. Формат по размеру остаётся «По столикам».
- «Шато Сити»: 40 человек — конференц-зал, не банкетный зал.
- «Профсоюзная»: на сайте конференц-залы от 6 до 110 мест. Диапазон шире одной полосы, цену на гостя не считал, первым стоит «Выход».
- Granat: на сайте четыре зала от 15 до 150 человек. По той же причине одной цифры нет, первым стоит «Выход».
- Gold шнур: на сайте есть комната до 10 гостей. Это VIP-комната, не вся площадка. Цифру не брал.
- «Переодеваемся не в гостевом / офисном туалете» и «не пьют с гостями / коллегами» в FACTS отдельной строкой не расписаны. Оставлены из макета v10, потому что рядом с пунктом про трезвых артистов.
- Одинаковый текст у одной организации на разные ящики (Октябрьская, Sheraton, Кулибин и другие пары в базе).
- Строку маркировки нужно вписать перед отправкой КП: отчество, ИНН и erid ещё не заполнены.

## Проверка

Тексты запроса, HTML КП и расшифрованные .eml проверены скриптом: запрещённые формулировки — 0, заглушка длительности — 0, в письмах компаний слова про гостей, зал, банкет и подачу — 0.

## Превью 600 px

- `previews/restaurant-oktyabrskaya-600.png` — «Октябрьская», формат «Выход», 25 мест
- `previews/restaurant-cafe38-600.png` — «Кафе 38», формат «Шоу», 50 мест
- `previews/restaurant-gardenhall-600.png` — Garden Hall, формат «По столикам», 1000 мест, цены на гостя нет
- `previews/company-hydromash-600.png` — Гидромаш, нейтральная строка
- `previews/company-databank-600.png` — Датабанк, нейтральная строка
- `previews/company-yarmarka-600.png` — Нижегородская ярмарка, нейтральная строка
"""
    open(os.path.join(ROOT, "REPORT.md"), "w", encoding="utf-8").write(report)
    print(f"rows {len(index)} excluded {len(excluded)} real {real} neutral {stats['нейтральная по сегменту']} priced {len(priced)}")
    print("formats", formats)


if __name__ == "__main__":
    main()
