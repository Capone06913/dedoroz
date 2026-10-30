#!/usr/bin/env python3
"""Shared helpers for Nizhny Novgorod B2B lead collection.

152-FZ: keep only general organisation contacts. Never store employee names,
personal emails or phones labelled as a manager/director's private number.
"""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "raw"
CSV_FIELDS = [
    "название",
    "адрес",
    "район",
    "телефон",
    "сайт",
    "email",
    "vk",
    "сегмент",
    "подсегмент",
    "приоритет",
    "источник",
    "источник_url",
]

CITY_DISTRICTS = [
    "Автозаводский",
    "Канавинский",
    "Ленинский",
    "Московский",
    "Нижегородский",
    "Приокский",
    "Советский",
    "Сормовский",
]

OBLAST_MARKERS = (
    "дзержинск",
    "кстово",
    "г. бор",
    "город бор",
    "г бор",
    "г. богородск",
    "город богородск",
    "богородский район",
    "балахна",
    "г. городец",
    "город городец",
    "городецкий район",
    "павлово",
    "арзамас",
    "саров",
    "выкса",
    "кулебаки",
    "заволжье",
    "семёнов",
    "семенов",
    "лысково",
    "первомайск",
    "шахунья",
    "навашино",
    "лукоянов",
    "сергач",
    "володарск",
    "чистое бор",
    "п. бор",
    "кстовск",
    "боровск",
    "дальних константиново",
    "дальнее константиново",
    "шатки",
    "вача",
    "сосновское",
    "перевоз",
    "городецк",
)

GENERIC_EMAIL_LOCAL = {
    "info",
    "mail",
    "office",
    "contact",
    "contacts",
    "hello",
    "zakaz",
    "order",
    "orders",
    "booking",
    "book",
    "banquet",
    "banket",
    "event",
    "events",
    "corp",
    "corporate",
    "pr",
    "press",
    "reklama",
    "admin",
    "reception",
    "welcome",
    "org",
    "feedback",
    "sale",
    "sales",
    "trade",
    "marketing",
    "post",
    "posta",
    "inbox",
    "support",
    "help",
    "service",
    "reserv",
    "reserve",
    "reservation",
    "resto",
    "restaurant",
    "cafe",
    "hotel",
    "hr",
    "job",
    "rabota",
    "kadry",
    "dou",
    "mdou",
    "mbdou",
    "madou",
    "detsad",
    "sadik",
    "sad",
    "kindergarten",
    "detcentr",
    "kids",
    "child",
    "deti",
    "secretar",
    "secretary",
    "kantora",
    "referent",
    "buh",
    "buhg",
    "account",
    "accounts",
    "open",
    "partner",
    "partners",
    "opt",
    "optov",
    "franchise",
    "franshiza",
    "comm",
    "commercial",
    "kommercia",
    "kommers",
    "noc",
    "webmaster",
    "www",
    "root",
    "box",
    "e-mail",
    "email",
    "noreply",
    "no-reply",
}

PERSONAL_PHONE_HINTS = (
    "менеджер",
    "директор",
    "заведующ",
    "личный",
    "владел",
    "фио",
    "мобильн",
    "личный кабинет",
)

PLATFORM_EMAIL_DOMAINS = (
    "yandex-team.ru",
    "maps.yandex.ru",
    "yandex.ru",
    "2gis.ru",
    "2gis.com",
    "vk.com",
    "mail.ru",  # only reject bare platform; org@mail.ru may be generic local
)

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\+7|8)[\s\-(]?\d{3}[\s\-)]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}")
VK_RE = re.compile(
    r"https?://(?:m\.)?(?:vk\.com|vkontakte\.ru)/([A-Za-z0-9_.\-]+)",
    re.I,
)
INST_LOCAL_RE = re.compile(
    r"^(ds|mdou|mbdou|madou|dou|sad|detsad|sadik|det)\d",
    re.I,
)

STREET_DISTRICT = {
    "рождественск": "Нижегородский",
    "большая покровск": "Нижегородский",
    "покровская": "Нижегородский",
    "минина": "Нижегородский",
    "варварск": "Нижегородский",
    "ижская": "Нижегородский",
    "зеленск": "Нижегородский",
    "ковалихин": "Нижегородский",
    "малая покровск": "Нижегородский",
    "ошарск": "Нижегородский",
    "плеханова": "Нижегородский",
    "студёная": "Нижегородский",
    "студеная": "Нижегородский",
    "родионова": "Нижегородский",
    "богдановича": "Нижегородский",
    "нижне-печерск": "Нижегородский",
    "семашко": "Нижегородский",
    "малая ямск": "Нижегородский",
    "грузинск": "Нижегородский",
    "белинского": "Нижегородский",
    "максима горького": "Нижегородский",
    "площадь свободы": "Нижегородский",
    "площадь минина": "Нижегородский",
    "гагарина": "Советский",
    "бекетова": "Советский",
    "культурная": "Советский",
    "нартова": "Советский",
    "ванеева": "Советский",
    "оптиков": "Советский",
    "тургаева": "Советский",
    "южное шоссе": "Автозаводский",
    "молодёжный": "Автозаводский",
    "молодежный": "Автозаводский",
    "лескова": "Автозаводский",
    "дьяконова": "Автозаводский",
    "мончегорск": "Автозаводский",
    "янки купалы": "Автозаводский",
    "героя васильева": "Автозаводский",
    "раевского": "Автозаводский",
    "политбойцов": "Автозаводский",
    "ватутина": "Автозаводский",
    "комсомольская": "Ленинский",
    "перекопская": "Ленинский",
    "голубева": "Ленинский",
    "самохвалова": "Московский",
    "березовская": "Московский",
    "московское шоссе": "Московский",
    "страхova": "Московский",
    "сортмовск": "Сормовский",
    "сормовское": "Сормовский",
    "коминтерна": "Сормовский",
    "бурнаковск": "Сормовский",
    "коновалова": "Сормовский",
    "есенина": "Канавинский",
    "канавино": "Канавинский",
    "ленинградск": "Канавинский",
    "советских космонавтов": "Канавинский",
    "тихорецк": "Канавинский",
    "мещерск": "Канавинский",
    "героя попова": "Канавинский",
    "канавиinsk": "Канавинский",
    "ларина": "Приокский",
    "щербинки": "Приокский",
    "академика сахарова": "Приокский",
    "проспект гагарина": "Советский",
}


def fold(text: str) -> str:
    text = (text or "").replace("ё", "е").replace("Ё", "Е")
    text = unicodedata.normalize("NFKC", text)
    return text.lower().strip()


def norm_name(name: str) -> str:
    name = fold(name)
    name = re.sub(r"[«»\"'“”„]", "", name)
    name = re.sub(r"\b(ооо|зао|пао|ао|ип|мбдоу|мадоу|мдоу|ано|нко)\b", " ", name)
    name = re.sub(r"\b(детский сад|д/с|дс)\b", "детский сад", name)
    name = re.sub(r"[^0-9a-zа-я]+", " ", name)
    return re.sub(r"\s+", " ", name).strip()


def norm_addr(address: str) -> str:
    address = fold(address)
    address = re.sub(r"\b(россия|нижегородская область|г\.?о\.?|город)\b", " ", address)
    address = re.sub(r"\b(ул\.|улица|пр-кт|проспект|пр\.|д\.|дом|к\.|корп\.|корпус)\b", " ", address)
    address = re.sub(r"[^0-9a-zа-я]+", " ", address)
    return re.sub(r"\s+", " ", address).strip()


def dedup_key(name: str, address: str) -> str:
    return f"{norm_name(name)}|{norm_addr(address)[:80]}"


def extract_district(address: str, extra: str = "") -> str:
    blob = f"{address} {extra}"
    folded = fold(blob)
    for dist in CITY_DISTRICTS:
        if fold(dist) in folded:
            return dist
    for needle, dist in STREET_DISTRICT.items():
        if needle in folded:
            return dist
    return ""


def is_nizhny_city(address: str, extra: str = "") -> bool:
    blob = fold(f"{address} {extra}")
    if not blob:
        return False
    postal = re.search(r"\b(60[0-9]{4})\b", blob)
    if postal:
        code = postal.group(1)
        if code.startswith("603"):
            return True
        if code.startswith("606") or code.startswith("607"):
            return False
    if any(marker in blob for marker in OBLAST_MARKERS):
        # "бор" as substring is dangerous; markers are already specific
        if "нижний новгород" in blob and "нижегородский район" in blob:
            return True
        return False
    if "нижний новгород" in blob or "nizhny novgorod" in blob or "nizhnii novgorod" in blob:
        return True
    if any(fold(d) in blob for d in CITY_DISTRICTS):
        return True
    return False


def clean_phone(raw: str, label: str = "") -> str:
    if not raw:
        return ""
    hint = fold(label)
    if any(h in hint for h in PERSONAL_PHONE_HINTS) and "ресторан" not in hint and "офис" not in hint:
        return ""
    digits = re.sub(r"\D", "", raw)
    if digits.startswith("8") and len(digits) == 11:
        digits = "7" + digits[1:]
    if len(digits) == 10:
        digits = "7" + digits
    if not (len(digits) == 11 and digits.startswith("7")):
        return ""
    return f"+{digits[0]} ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"


def pick_org_phone(phones: list[tuple[str, str]]) -> str:
    """phones: list of (number, label). Prefer 831 city numbers."""
    cleaned = []
    for number, label in phones:
        p = clean_phone(number, label)
        if p:
            cleaned.append(p)
    if not cleaned:
        return ""
    city = [p for p in cleaned if p.startswith("+7 (831)")]
    return city[0] if city else cleaned[0]


def is_generic_email(email: str) -> bool:
    email = (email or "").strip().lower()
    if not EMAIL_RE.fullmatch(email):
        return False
    local, _, domain = email.partition("@")
    if domain in ("yandex-team.ru", "maps.yandex.ru", "2gis.ru", "2gis.com"):
        return False
    if domain.endswith("yandex-team.ru"):
        return False
    local_main = local.split("+", 1)[0]
    if local_main in GENERIC_EMAIL_LOCAL:
        return True
    if INST_LOCAL_RE.match(local_main):
        return True
    if local_main.endswith("_nn") or local_main.endswith("-nn"):
        return True
    if re.fullmatch(r"[a-z]{2,12}\d{1,4}", local_main) and not re.search(
        r"(ivan|petr|serge|alex|olga|anna|dmit|elena|natal)", local_main
    ):
        # ds19, mdou5, info1 — institutional, not firstname
        if any(k in local_main for k in ("ds", "sad", "dou", "info", "mail", "office", "cafe", "rest")):
            return True
    # first.last or name.surname
    brand_bits = ("rest", "cafe", "sad", "det", "kids", "club", "hotel", "banket", "loft")
    if "." in local_main and not local_main.startswith("info"):
        parts = local_main.split(".")
        if len(parts) == 2 and all(p.isalpha() and 2 <= len(p) <= 16 for p in parts):
            if not any(b in local_main for b in brand_bits):
                return False
    return False


def pick_generic_emails(text: str) -> str:
    found = []
    seen = set()
    for match in EMAIL_RE.findall(text or ""):
        email = match.lower()
        if email in seen:
            continue
        if is_generic_email(email):
            seen.add(email)
            found.append(email)
    return found[0] if found else ""


def clean_website(url: str) -> str:
    if not url:
        return ""
    url = url.strip()
    if url.startswith("vk.com") or "vk.com/" in url or "vkontakte.ru" in url:
        return ""
    if url.startswith("//"):
        url = "https:" + url
    if not re.match(r"^https?://", url, re.I):
        url = "https://" + url
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if not host or host.endswith("yandex.ru") or host.endswith("yandex.com"):
        return ""
    if host.endswith("2gis.ru") or host.endswith("2gis.com"):
        return ""
    if host.endswith("flamp.ru") or "yell.ru" in host:
        return ""
    if "instagram.com" in host or "facebook.com" in host:
        return ""
    query = [
        (k, v)
        for k, v in parse_qsl(parsed.query, keep_blank_values=True)
        if not k.lower().startswith("utm") and k.lower() not in {"yclid", "ysclid", "fbclid", "gclid"}
    ]
    cleaned = parsed._replace(
        scheme="https" if parsed.scheme in {"http", "https"} else parsed.scheme,
        netloc=host,
        query=urlencode(query),
        fragment="",
    )
    return urlunparse(cleaned).rstrip("/")


def pick_vk(text: str) -> str:
    for match in VK_RE.finditer(text or ""):
        slug = match.group(1)
        if slug.lower() in {"share", "widget", "away", "login", "join", "feed", "im", "yandex.maps"}:
            continue
        if re.fullmatch(r"id\d+", slug, re.I):
            continue  # personal page
        return f"https://vk.com/{slug}"
    return ""


def empty_record() -> dict:
    return {k: "" for k in CSV_FIELDS}


def make_record(
    *,
    name: str,
    address: str,
    district: str = "",
    phone: str = "",
    website: str = "",
    email: str = "",
    vk: str = "",
    segment: str,
    subsegment: str = "",
    priority: int = 3,
    source: str,
    source_url: str,
) -> dict | None:
    name = re.sub(r"\s+", " ", (name or "")).strip(" «»\"'")
    address = re.sub(r"\s+", " ", (address or "")).strip()
    if len(name) < 2:
        return None
    if not is_nizhny_city(address, f"{name} {district}"):
        return None
    rec = empty_record()
    rec["название"] = name
    rec["адрес"] = address
    rec["район"] = district or extract_district(address, name)
    rec["телефон"] = phone
    rec["сайт"] = clean_website(website)
    rec["email"] = email.lower() if email and is_generic_email(email) else ""
    rec["vk"] = vk if vk.startswith("https://vk.com/") and "/id" not in vk else pick_vk(vk)
    rec["сегмент"] = segment
    rec["подсегмент"] = subsegment
    rec["приоритет"] = str(max(1, min(5, int(priority))))
    rec["источник"] = source
    rec["источник_url"] = source_url
    return rec


def merge_records(existing: dict, incoming: dict) -> dict:
    out = dict(existing)
    for key in ("адрес", "район", "телефон", "сайт", "email", "vk", "подсегмент", "источник_url"):
        if not out.get(key) and incoming.get(key):
            out[key] = incoming[key]
    # keep richer address
    if incoming.get("адрес") and len(incoming["адрес"]) > len(out.get("адрес") or ""):
        out["адрес"] = incoming["адрес"]
        if incoming.get("район"):
            out["район"] = incoming["район"]
    try:
        out["приоритет"] = str(min(int(out.get("приоритет") or 5), int(incoming.get("приоритет") or 5)))
    except ValueError:
        pass
    sources = {s.strip() for s in (out.get("источник") or "").split(";") if s.strip()}
    if incoming.get("источник"):
        sources.add(incoming["источник"])
    out["источник"] = "; ".join(sorted(sources))
    return out


def upsert(index: dict[str, dict], rec: dict | None) -> None:
    if not rec:
        return
    key = dedup_key(rec["название"], rec["адрес"])
    if key in index:
        index[key] = merge_records(index[key], rec)
    else:
        index[key] = rec


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in CSV_FIELDS})


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def sort_rows(rows: list[dict]) -> list[dict]:
    def key(row: dict):
        try:
            prio = int(row.get("приоритет") or 5)
        except ValueError:
            prio = 5
        filled = sum(bool(row.get(k)) for k in ("телефон", "сайт", "email", "vk"))
        return (prio, -filled, fold(row.get("район") or "яя"), fold(row.get("название") or ""))

    return sorted(rows, key=key)


def dump_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def restaurant_priority(name: str, cats: str, features: str, rating: float, reviews: int, website: str) -> int:
    blob = fold(f"{name} {cats} {features}")
    score = 3
    if any(w in blob for w in ("банкет", "корпоратив", "свадьб", "лофт", "площадк", "event")):
        score -= 1
    if any(w in blob for w in ("премиум", "fine", "steak", "панорам", "отель", "hilton", "marriott", "кортъярд")):
        score -= 1
    if rating >= 4.6 and reviews >= 150:
        score -= 1
    if reviews >= 800:
        score -= 1
    if not website:
        score += 1
    if any(w in blob for w in ("макдоналдс", "бургер кинг", "kfc", "ростикс", "суши wok", "додо")):
        score = 5
    return max(1, min(5, score))


def kindergarten_priority(name: str, subsegment: str, email: str, website: str) -> int:
    blob = fold(name)
    if "частн" in blob or subsegment in {"частный детский сад", "детский центр"}:
        return 1 if (website or email) else 2
    if email or website:
        return 2
    return 3


RESTAURANT_KEEP = (
    "ресторан",
    "кафе",
    "банкет",
    "бар",
    "лофт",
    "караоке",
    "трактир",
    "паб",
    "столов",
    "пицц",
    "суши",
    "кальян",
    "steak",
    "grill",
    "грил",
    "food",
    "кухн",
    "банкетн",
    "площадк",
    "event",
    "веранд",
    "отель",
    "гостиниц",
)
RESTAURANT_DROP = (
    "клининг",
    "химчист",
    "мастер блеск",
    "аптек",
    "нотариус",
    "стоматолог",
    "барбер",
    "салон красот",
    "автосервис",
    "шиномонтаж",
    "автомойк",
    "ломбард",
    "мфо",
    "микрофинанс",
)
KINDER_KEEP = (
    "детский сад",
    "детский садик",
    "мбдоу",
    "мадоу",
    "мдоу",
    "доу ",
    "ясли",
    "дошкол",
    "монтессори",
    "baby",
    "бэби",
    "беби",
    "детский центр",
    "центр развития",
    "детский клуб",
    "развивающ",
    "частн",
    "сад №",
    "сад n",
    "д/с",
    "дс №",
    "логопед",
    "раннего развития",
)
KINDER_DROP = (
    "мбук",
    "учреждение культуры",
    "электрическ",
    "аптек",
    "магазин",
    "фитнес",
    "стадион",
    "спортивн школа",
    "сшор",
    "автошкол",
)
COMPANY_KEEP = (
    "it",
    "айти",
    "банк",
    "завод",
    "производ",
    "строительн",
    "застройщик",
    "логист",
    "грузоперевоз",
    "бизнес-центр",
    "бизнес центр",
    "страхо",
    "телеком",
    "ростелеком",
    "энергет",
    "фарма",
    "холдинг",
    "торговая сеть",
    "офис",
    "компания",
    "пао",
    "оао",
    "нпз",
    "газ",
    "нефть",
    "автозавод",
    "инжиниринг",
    "разработк",
)
COMPANY_DROP = (
    "оптик",
    "коррекц зрения",
    "канцтовар",
    "строительство дач",
    "коттедж",
    "бань и",
    "обмен валют",
    "ломбард",
    "микрофинанс",
    "салон красот",
    "стоматолог",
    "ветеринар",
    "цветы",
    "ритуал",
    "автомойк",
    "шиномонтаж",
)


def in_scope_restaurant(name: str, sub: str, extra: str = "") -> bool:
    blob = fold(f"{name} {sub} {extra}")
    if any(w in blob for w in RESTAURANT_DROP):
        return False
    if sub in {"ресторан", "кафе", "банкетный зал", "бар"}:
        return True
    if "2гис" in fold(extra) or "2gis" in fold(extra):
        return True
    return any(w in fold(name) for w in RESTAURANT_KEEP)


def in_scope_kindergarten(name: str, sub: str, extra: str = "") -> bool:
    name_b = fold(name)
    extra_b = fold(extra)
    if any(w in name_b for w in KINDER_DROP) and not any(
        w in name_b for w in ("детский сад", "мбдоу", "мадоу", "ясли")
    ):
        return False
    if any(w in name_b for w in KINDER_KEEP):
        return True
    if "mdoy" in extra_b:
        return True
    if ("2гис" in extra_b or "2gis" in extra_b) and sub in {
        "детский сад",
        "частный детский сад",
        "детский центр",
    }:
        return True
    return False


def in_scope_company(name: str, sub: str, extra: str = "") -> bool:
    blob = fold(f"{name} {sub} {extra}")
    if any(w in blob for w in COMPANY_DROP):
        return False
    if "firmoteka" in fold(extra) or "рейтинг" in fold(extra):
        return True
    return any(w in blob for w in COMPANY_KEEP)


def company_priority(name: str, cats: str, reviews: int, website: str) -> int:
    blob = fold(f"{name} {cats}")
    large = (
        "газ",
        "сбер",
        "втб",
        "ростелеком",
        "мтс",
        "мегафон",
        "сибур",
        "лукойл",
        "асе",
        "атомстрой",
        "нмжк",
        "россет",
        "тнс энерго",
        "алиди",
        "спар",
        "сладкая жизнь",
        "газпром",
        "транснефть",
        "ядро",
        "netcracker",
        "mera",
        "инфосистемы",
        "1с",
        "магнит",
        "x5",
        "лента",
    )
    if any(w in blob for w in large) or reviews >= 80:
        return 1
    if website and reviews >= 20:
        return 2
    if website or reviews >= 5:
        return 3
    return 4
