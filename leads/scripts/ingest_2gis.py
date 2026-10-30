#!/usr/bin/env python3
"""Normalize 2GIS place JSON (Apify or catalog export) into lead records."""

from __future__ import annotations

import json
from pathlib import Path

from nn_common import (
    RAW_DIR,
    company_priority,
    extract_district,
    is_generic_email,
    kindergarten_priority,
    make_record,
    pick_org_phone,
    pick_vk,
    restaurant_priority,
    upsert,
)


def _first(obj: dict, *keys):
    for k in keys:
        if obj.get(k) not in (None, "", [], {}):
            return obj[k]
    return ""


def _as_list(val) -> list:
    if val is None:
        return []
    if isinstance(val, list):
        return val
    return [val]


def phones_of(item: dict) -> list[tuple[str, str]]:
    out = []
    for p in _as_list(_first(item, "phones", "phone", "contacts.phones")):
        if isinstance(p, dict):
            out.append((p.get("number") or p.get("value") or p.get("phone") or "", p.get("type") or ""))
        else:
            out.append((str(p), ""))
    contacts = item.get("contacts") or {}
    if isinstance(contacts, dict):
        for p in _as_list(contacts.get("phones") or contacts.get("phone")):
            if isinstance(p, dict):
                out.append((p.get("number") or p.get("value") or "", ""))
            else:
                out.append((str(p), ""))
    return out


def emails_of(item: dict) -> str:
    vals = []
    for e in _as_list(_first(item, "emails", "email")):
        vals.append(e if isinstance(e, str) else (e.get("value") or e.get("email") or ""))
    contacts = item.get("contacts") or {}
    if isinstance(contacts, dict):
        for e in _as_list(contacts.get("emails") or contacts.get("email")):
            vals.append(e if isinstance(e, str) else str(e))
    for e in vals:
        if is_generic_email(e):
            return e.lower()
    return ""


def website_of(item: dict) -> str:
    w = _first(item, "website", "site", "url")
    if isinstance(w, list):
        w = w[0] if w else ""
    if isinstance(w, dict):
        w = w.get("value") or w.get("url") or ""
    return str(w or "")


def social_blob(item: dict) -> str:
    parts = []
    for key in ("social", "socials", "socialLinks", "links", "socialProfiles"):
        val = item.get(key)
        if not val:
            continue
        parts.append(json.dumps(val, ensure_ascii=False) if not isinstance(val, str) else val)
    return " ".join(parts)


def cats_of(item: dict) -> str:
    cats = _first(item, "categories", "category", "rubrics", "rubric")
    if isinstance(cats, list):
        names = []
        for c in cats:
            if isinstance(c, dict):
                names.append(c.get("name") or c.get("title") or "")
            else:
                names.append(str(c))
        return ", ".join(x for x in names if x)
    return str(cats or "")


def classify(cats: str, query_hint: str = "") -> tuple[str, str]:
    blob = f"{cats} {query_hint}".lower()
    if any(w in blob for w in ("детск", "садик", "kindergarten", "развит", "дошколь")):
        sub = "детский центр" if any(w in blob for w in ("центр", "клуб", "развит")) else "детский сад"
        if "частн" in blob:
            sub = "частный детский сад"
        return "детские сады и центры", sub
    if any(w in blob for w in ("ресторан", "кафе", "банкет", "бар", "лофт", "караоке", "общепит")):
        if "банкет" in blob or "лофт" in blob:
            return "рестораны", "банкетный зал"
        if "ресторан" in blob:
            return "рестораны", "ресторан"
        if "кафе" in blob:
            return "рестораны", "кафе"
        return "рестораны", "площадка"
    return "компании", cats.split(",")[0].strip() or "компания"


def record_from_place(item: dict, default_segment: str | None = None) -> dict | None:
    name = str(_first(item, "name", "title", "orgName") or "").strip()
    address = str(
        _first(item, "fullAddress", "address", "full_address", "addressName", "full_address_name") or ""
    ).strip()
    cats = cats_of(item)
    segment, sub = classify(cats, str(item.get("searchQuery") or item.get("query") or ""))
    if default_segment and segment != default_segment:
        # keep the run's intended bucket when the rubric is noisy
        if default_segment == "рестораны" and segment != "детские сады и центры":
            segment, sub = default_segment, sub if sub else "ресторан"
        elif default_segment == "детские сады и центры" and "компани" not in cats.lower():
            segment, sub = default_segment, sub if "детск" in sub else "детский сад"
        elif default_segment == "компании":
            if segment == "рестораны":
                return None
            segment, sub = default_segment, sub if sub else "компания"
    rating = float(_first(item, "rating", "reviewsRating") or 0 or 0)
    try:
        reviews = int(_first(item, "reviewsCount", "reviewCount", "reviews") or 0)
    except (TypeError, ValueError):
        reviews = 0
    website = website_of(item)
    email = emails_of(item)
    vk = pick_vk(social_blob(item) + " " + json.dumps(item.get("vk") or "", ensure_ascii=False))
    source_url = str(_first(item, "url", "placeUrl", "link", "2gisUrl") or "")
    if not source_url:
        pid = _first(item, "id", "placeId", "firmId")
        source_url = f"https://2gis.ru/nizhniy_novgorod/firm/{pid}" if pid else "https://2gis.ru/nizhniy_novgorod"
    district = str(item.get("district") or "")
    if item.get("postcode"):
        address = f"{address}, {item.get('postcode')}" if address else str(item.get("postcode"))
    if segment == "рестораны":
        prio = restaurant_priority(name, cats, cats, rating, reviews, website)
    elif segment == "детские сады и центры":
        prio = kindergarten_priority(name, sub, email, website)
    else:
        prio = company_priority(name, cats, reviews, website)
    return make_record(
        name=name,
        address=address or "г. Нижний Новгород",
        district=extract_district(address, f"{cats} {district}"),
        phone=pick_org_phone(phones_of(item)),
        website=website,
        email=email,
        vk=vk,
        segment=segment,
        subsegment=sub,
        priority=prio,
        source="2ГИС",
        source_url=source_url,
    )


def load_places(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        for key in ("items", "places", "results"):
            if isinstance(data.get(key), list):
                data = data[key]
                break
        else:
            data = [data]
    return [x for x in data if isinstance(x, dict)]


def ingest(paths: list[Path], default_segment: str | None = None) -> list[dict]:
    index: dict[str, dict] = {}
    for path in paths:
        if not path.exists():
            continue
        hint = default_segment
        n = path.name.lower()
        if hint is None:
            if "kindergart" in n or "sad" in n:
                hint = "детские сады и центры"
            elif "company" in n or "compan" in n:
                hint = "компании"
            elif "rest" in n or "cafe" in n:
                hint = "рестораны"
        for item in load_places(path):
            rec = record_from_place(item, default_segment=hint)
            upsert(index, rec)
    rows = list(index.values())
    print(f"[2gis] ingested {len(rows)} from {len(paths)} files")
    return rows


if __name__ == "__main__":
    ingest(sorted((RAW_DIR).glob("2gis-*.json")))
