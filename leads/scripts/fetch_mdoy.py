#!/usr/bin/env python3
"""Municipal and listed kindergartens from mdoy.pro (open city portal)."""

from __future__ import annotations

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

UA = "DedMoroz52Leads/1.0 (open-data research; Nizhny Novgorod; github.com/Capone06913/dedoroz)"
BASE = "https://mdoy.pro"


def parse_cards(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    rows = []
    for h in soup.find_all("h3"):
        name = h.get_text(" ", strip=True)
        if not name or "детск" not in name.lower() and "доу" not in name.lower() and "ясли" not in name.lower():
            if not re.search(r"(МБДОУ|МАДОУ|МДОУ|ДОУ)", name, re.I):
                continue
        block_bits = [name]
        node = h.parent
        # capture following paragraphs of this card
        for sib in list(h.next_siblings)[:12]:
            if getattr(sib, "name", None) == "h3":
                break
            text = getattr(sib, "get_text", lambda *a, **k: str(sib))(" ", strip=True)
            if text:
                block_bits.append(text)
        blob = "\n".join(block_bits)
        if "спортивн" in blob.lower() and "детский сад" not in blob.lower():
            continue
        addr_m = re.search(r"Адрес:\s*(.+)", blob)
        address = addr_m.group(1).strip() if addr_m else ""
        # drop "Руководитель: FIO" entirely — 152-FZ
        blob_nolead = re.sub(r"Руководитель:\s*.+", " ", blob)
        phones = re.findall(r"(?:\+7|8|\()[\d\s\-()]{10,}", blob_nolead)
        emails = re.findall(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", blob_nolead)
        email = next((e for e in emails if is_generic_email(e)), "")
        site = ""
        a = h.find("a", href=True) or h.parent.find("a", href=True)
        href = a["href"] if a else ""
        if href.startswith("index_ds.php"):
            site = f"{BASE}/{href}"
            source_url = site
        else:
            source_url = f"{BASE}/index_gor.php?gor=2"
        sub = "детский сад"
        if re.search(r"частн", name, re.I):
            sub = "частный детский сад"
        rec = make_record(
            name=name,
            address=address or "Нижний Новгород",
            district=extract_district(address, blob_nolead),
            phone=pick_org_phone([(p, "сад") for p in phones]),
            website=site,
            email=email,
            vk="",
            segment="детские сады и центры",
            subsegment=sub,
            priority=kindergarten_priority(name, sub, email, site),
            source="mdoy.pro",
            source_url=source_url,
        )
        if rec:
            rows.append(rec)
    return rows


def collect() -> list[dict]:
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept-Language": "ru"})
    index: dict[str, dict] = {}
    for ra in range(1, 10):
        url = f"{BASE}/index_gor.php?gor=2&ra={ra}"
        try:
            r = s.get(url, timeout=25)
        except requests.RequestException:
            continue
        if r.status_code != 200 or len(r.text) < 6000:
            continue
        for rec in parse_cards(r.text):
            upsert(index, rec)
        time.sleep(0.4)
    for page in range(1, 18):
        url = f"{BASE}/index_gor.php?gor=2&str={page}"
        try:
            r = s.get(url, timeout=25)
        except requests.RequestException:
            continue
        if r.status_code != 200 or len(r.text) < 6000:
            continue
        n_before = len(index)
        for rec in parse_cards(r.text):
            upsert(index, rec)
        print(f"[mdoy] page {page}: +{len(index) - n_before} total={len(index)}")
        time.sleep(0.35)
    rows = list(index.values())
    dump_json(RAW_DIR / "mdoy-kindergartens.json", rows)
    print("[mdoy] unique", len(rows))
    return rows


if __name__ == "__main__":
    collect()
