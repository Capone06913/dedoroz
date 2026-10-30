#!/usr/bin/env python3
"""Extra municipal kindergartens from mdoy.pro card pages (sad=ID)."""

from __future__ import annotations

import json
import re
import time

import requests
from bs4 import BeautifulSoup

from nn_common import (
    RAW_DIR,
    dump_json,
    extract_district,
    is_generic_email,
    kindergarten_priority,
    make_record,
    pick_org_phone,
    upsert,
)


def collect() -> list[dict]:
    s = requests.Session()
    s.headers["User-Agent"] = "DedMoroz52Leads/1.0 (open-data research)"
    index: dict[str, dict] = {}
    existing = RAW_DIR / "mdoy-kindergartens.json"
    if existing.exists():
        for rec in json.loads(existing.read_text(encoding="utf-8")):
            upsert(index, rec)
    print("[mdoy-ids] seed", len(index))

    ids: set[int] = set()
    for ra in range(1, 9):
        try:
            r = s.get(f"https://mdoy.pro/index_gor.php?gor=2&ra={ra}", timeout=20)
            ids.update(int(x) for x in re.findall(r"sad=(\d+)", r.text))
        except requests.RequestException:
            pass
        time.sleep(0.2)
    ids.update(range(70, 220))
    ids.update(range(800, 980))
    print("[mdoy-ids] fetching", len(ids), "ids")

    n_new = 0
    for i, sid in enumerate(sorted(ids), 1):
        try:
            r = s.get(f"https://mdoy.pro/index_ds.php?sad={sid}", timeout=15)
        except requests.RequestException:
            continue
        if r.status_code != 200 or len(r.text) < 2000:
            continue
        soup = BeautifulSoup(r.text, "lxml")
        title = soup.find(["h1", "h2", "h3"])
        name = title.get_text(" ", strip=True) if title else ""
        if not name or not re.search(r"(детск|доу|ясли|сад)", name, re.I):
            continue
        text = soup.get_text("\n", strip=True)
        text_nolead = re.sub(r"Руководитель:\s*.+", " ", text)
        addr_m = re.search(r"Адрес:\s*(.+)", text_nolead)
        address = addr_m.group(1).strip() if addr_m else ""
        if "нижний новгород" not in (address + text_nolead).lower():
            continue
        phones = re.findall(r"(?:\+7|8|\()[\d\s\-()]{10,}", text_nolead)
        emails = re.findall(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", text_nolead)
        email = next((e for e in emails if is_generic_email(e)), "")
        before = len(index)
        rec = make_record(
            name=name,
            address=address or "г. Нижний Новгород",
            district=extract_district(address, text_nolead),
            phone=pick_org_phone([(p, "сад") for p in phones]),
            website=f"https://mdoy.pro/index_ds.php?sad={sid}",
            email=email,
            vk="",
            segment="детские сады и центры",
            subsegment="частный детский сад" if "частн" in name.lower() else "детский сад",
            priority=kindergarten_priority(name, "детский сад", email, "x"),
            source="mdoy.pro",
            source_url=f"https://mdoy.pro/index_ds.php?sad={sid}",
        )
        upsert(index, rec)
        if len(index) > before:
            n_new += 1
        if i % 40 == 0:
            print(f"  {i}/{len(ids)} unique={len(index)} new={n_new}")
        time.sleep(0.12)

    rows = list(index.values())
    dump_json(existing, rows)
    print("[mdoy-ids] unique", len(rows), "new", n_new)
    return rows


if __name__ == "__main__":
    collect()
