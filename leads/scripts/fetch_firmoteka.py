#!/usr/bin/env python3
"""Large/medium companies from the open Firmoteka revenue ranking (region 52),
kept only when the legal address is in Nizhny Novgorod city.
"""

from __future__ import annotations

import re
import time

import requests
from bs4 import BeautifulSoup

from nn_common import (
    RAW_DIR,
    company_priority,
    dump_json,
    extract_district,
    make_record,
    upsert,
)

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
URL = "https://firmoteka.ru/rating-by-revenue-reg52"


def collect() -> list[dict]:
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept-Language": "ru"})
    r = s.get(URL, timeout=40)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    index: dict[str, dict] = {}
    # table rows or ranked cards
    for a in soup.select("a"):
        name = a.get_text(" ", strip=True)
        href = a.get("href") or ""
        if not name or len(name) < 4:
            continue
        if not re.search(r"\b(ООО|АО|ПАО|ЗАО|НАО|ГП)\b", name):
            continue
        parent = a.find_parent(["tr", "li", "div", "article"])
        blob = parent.get_text(" ", strip=True) if parent else name
        rec = make_record(
            name=name,
            address=blob if "нижний новгород" in blob.lower() else "г. Нижний Новгород",
            district=extract_district(blob, name),
            phone="",
            website="",
            email="",
            vk="",
            segment="компании",
            subsegment="средний и крупный бизнес",
            priority=company_priority(name, blob, 50, ""),
            source="Firmoteka / открытый рейтинг ФНС",
            source_url=href if href.startswith("http") else URL,
        )
        if rec:
            upsert(index, rec)
    # also parse markdown-like tables dumped as <td>
    for tr in soup.find_all("tr"):
        cells = [c.get_text(" ", strip=True) for c in tr.find_all(["td", "th"])]
        if len(cells) < 2:
            continue
        name = cells[1] if cells[0].isdigit() or cells[0] == "" else cells[0]
        if not re.search(r"\b(ООО|АО|ПАО|ЗАО|НАО|ГП)\b", name):
            continue
        rec = make_record(
            name=name,
            address="г. Нижний Новгород",
            district="",
            phone="",
            website="",
            email="",
            vk="",
            segment="компании",
            subsegment="средний и крупный бизнес",
            priority=company_priority(name, name, 40, ""),
            source="Firmoteka / открытый рейтинг ФНС",
            source_url=URL,
        )
        if rec:
            upsert(index, rec)
    rows = list(index.values())
    dump_json(RAW_DIR / "firmoteka-companies.json", rows)
    print("[firmoteka] unique", len(rows))
    return rows


if __name__ == "__main__":
    collect()
    time.sleep(0)
