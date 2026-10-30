#!/usr/bin/env python3
"""Collect organisation cards from public Yandex Maps HTML (city geo_id=47)."""

from __future__ import annotations

import json
import random
import re
import time
from typing import Iterable
from urllib.parse import quote

import requests

from nn_common import (
    RAW_DIR,
    dump_json,
    extract_district,
    make_record,
    pick_org_phone,
    restaurant_priority,
    kindergarten_priority,
    company_priority,
    upsert,
)

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
BASE = "https://yandex.ru/maps/47/nizhny-novgorod"
JSON_RE = re.compile(r'<script type="application/json"[^>]*>(.*?)</script>', re.S)

DISTRICTS = [
    "Автозаводский",
    "Канавинский",
    "Ленинский",
    "Московский",
    "Нижегородский",
    "Приокский",
    "Советский",
    "Сормовский",
]

# Downtown → Avtozavod / Sormovo coverage, z=14 keeps the viewport in the city.
GRID = [
    (lon, lat)
    for lat in (56.24, 56.28, 56.32, 56.36, 56.395)
    for lon in (43.80, 43.88, 43.96, 44.04)
]

SEGMENT_QUERIES = {
    "рестораны": [
        "ресторан",
        "кафе",
        "банкетный зал",
        "лофт для праздника",
        "площадка для мероприятий",
        "ресторан банкет",
    ],
    "детские сады и центры": [
        "детский сад",
        "частный детский сад",
        "детский центр",
        "центр развития детей",
        "детский клуб",
    ],
    "компании": [
        "IT компания",
        "завод",
        "офис компании",
        "банк",
        "строительная компания",
        "логистическая компания",
    ],
}

CATEGORIES = {
    "рестораны": [
        ("restaurant", "184106394"),
        ("cafe", "184106390"),
        ("banquet_hall", "184106402"),
        ("bar", "184107743"),
    ],
    "детские сады и центры": [
        ("kindergarten", "184105890"),
        ("children_developmental_center", "184106084"),
        ("childrens_club", "184106086"),
    ],
    "компании": [
        ("it_company", "184105750"),
        ("bank", "184105746"),
        ("industrial_enterprise", "184105398"),
        ("construction_company", "184105414"),
    ],
}


def session() -> requests.Session:
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": UA,
            "Accept-Language": "ru-RU,ru;q=0.9",
            "Accept": "text/html,application/xhtml+xml",
        }
    )
    return s


def parse_state(html: str) -> dict | None:
    blobs = JSON_RE.findall(html)
    if not blobs:
        return None
    blobs.sort(key=len, reverse=True)
    try:
        return json.loads(blobs[0])
    except json.JSONDecodeError:
        return None


def iter_items(state: dict) -> Iterable[dict]:
    stack = state.get("stack") or []
    if not stack:
        return
    items = ((stack[0].get("results") or {}).get("items") or [])
    for item in items:
        if item.get("type") != "business":
            continue
        yield item


def subsegment_from_item(item: dict, segment: str) -> str:
    cats = " ".join(c.get("name", "") for c in (item.get("categories") or []))
    blob = cats.lower()
    if segment == "рестораны":
        if "банкет" in blob or "лофт" in blob:
            return "банкетный зал"
        if "ресторан" in blob:
            return "ресторан"
        if "кафе" in blob:
            return "кафе"
        if "бар" in blob:
            return "бар"
        return "площадка"
    if segment == "детские сады и центры":
        if "частн" in blob or "центр" in blob or "клуб" in blob:
            if "сад" in blob:
                return "частный детский сад"
            return "детский центр"
        return "детский сад"
    return cats.split(",")[0].strip() if cats else "компания"


def record_from_item(item: dict, segment: str, source_url: str) -> dict | None:
    name = item.get("title") or item.get("shortTitle") or ""
    address = item.get("fullAddress") or item.get("address") or ""
    oid = item.get("id") or ""
    org_url = f"https://yandex.ru/maps/org/{item.get('seoname') or 'org'}/{oid}/" if oid else source_url
    phones = []
    for ph in item.get("phones") or []:
        phones.append((ph.get("number") or ph.get("value") or "", ph.get("info") or ""))
    website = ""
    for u in item.get("urls") or []:
        if "vk.com" in u:
            continue
        website = u
        break
    features = []
    for feat in item.get("features") or []:
        features.append(str(feat.get("name") or ""))
        val = feat.get("value")
        if isinstance(val, list):
            features.extend(str(x.get("name") if isinstance(x, dict) else x) for x in val)
        elif val not in (None, True, False):
            features.append(str(val))
    cats = ", ".join(c.get("name", "") for c in (item.get("categories") or []))
    rating = float((item.get("ratingData") or {}).get("ratingValue") or 0)
    reviews = int((item.get("ratingData") or {}).get("reviewCount") or 0)
    sub = subsegment_from_item(item, segment)
    if segment == "рестораны":
        prio = restaurant_priority(name, cats, " ".join(features), rating, reviews, website)
    elif segment == "детские сады и центры":
        prio = kindergarten_priority(name, sub, "", website)
    else:
        prio = company_priority(name, cats, reviews, website)
    vk = ""
    rec = make_record(
        name=name,
        address=address,
        district=extract_district(address, f"{cats} {item.get('description') or ''}"),
        phone=pick_org_phone(phones),
        website=website,
        email="",
        vk=vk,
        segment=segment,
        subsegment=sub,
        priority=prio,
        source="Яндекс Карты",
        source_url=org_url,
    )
    return rec


def fetch_url(s: requests.Session, url: str, retries: int = 3) -> dict | None:
    for attempt in range(retries):
        try:
            r = s.get(url, timeout=35)
            if r.status_code in {429, 503}:
                time.sleep(2 + attempt * 2)
                continue
            if r.status_code >= 400:
                return None
            return parse_state(r.text)
        except requests.RequestException:
            time.sleep(1.5 + attempt)
    return None


def collect(segment: str) -> list[dict]:
    s = session()
    index: dict[str, dict] = {}
    seen_urls: set[str] = set()
    urls: list[str] = []

    for slug, cid in CATEGORIES.get(segment, []):
        for page in range(1, 9):
            urls.append(f"{BASE}/category/{slug}/{cid}/?page={page}")

    for query in SEGMENT_QUERIES[segment]:
        q = quote(query)
        for page in range(1, 5):
            urls.append(f"{BASE}/search/{q}/?page={page}")
        for dist in DISTRICTS:
            urls.append(f"{BASE}/search/{quote(query + ' ' + dist + ' район')}/")
        if segment == "рестораны" and query in {"ресторан", "кафе", "банкетный зал"}:
            for lon, lat in GRID:
                urls.append(f"{BASE}/search/{q}/?ll={lon},{lat}&z=14")
        if segment == "детские сады и центры" and query in {"детский сад", "детский центр"}:
            for lon, lat in GRID:
                urls.append(f"{BASE}/search/{q}/?ll={lon},{lat}&z=14")
        if segment == "компании" and query in {"IT компания", "завод", "офис компании"}:
            for lon, lat in GRID[::2]:
                urls.append(f"{BASE}/search/{q}/?ll={lon},{lat}&z=13")

    print(f"[yandex] {segment}: {len(urls)} urls")
    for i, url in enumerate(urls, 1):
        if url in seen_urls:
            continue
        seen_urls.add(url)
        state = fetch_url(s, url)
        if not state:
            continue
        n = 0
        for item in iter_items(state):
            rec = record_from_item(item, segment, url)
            if rec:
                upsert(index, rec)
                n += 1
        if i % 15 == 0:
            print(f"  {i}/{len(urls)} unique={len(index)} last+{n}")
        time.sleep(0.45 + random.random() * 0.35)
    dump_json(RAW_DIR / f"yandex-{segment.replace(' ', '_')}.json", list(index.values()))
    print(f"[yandex] {segment}: {len(index)} unique")
    return list(index.values())


def main() -> None:
    all_rows = []
    for segment in SEGMENT_QUERIES:
        all_rows.extend(collect(segment))
    dump_json(RAW_DIR / "yandex-all.json", all_rows)
    print("[yandex] total", len(all_rows))


if __name__ == "__main__":
    main()
