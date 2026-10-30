#!/usr/bin/env python3
"""Visit public organisation websites and keep only generic emails / VK groups."""

from __future__ import annotations

import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

from nn_common import is_generic_email, pick_generic_emails, pick_vk

UA = "DedMoroz52Leads/1.0 (contact harvest for public org mailboxes only)"
CONTACT_PATHS = ("", "/contacts", "/kontakty")
SKIP_HOST_BITS = (
    "vk.com",
    "instagram.com",
    "facebook.com",
    "t.me",
    "whatsapp",
    "yandex.ru",
    "google.",
    "2gis.",
    "mdoy.pro",
)


def _host_ok(url: str) -> bool:
    u = (url or "").lower()
    if not u.startswith("http"):
        return False
    return not any(b in u for b in SKIP_HOST_BITS)


def extract_from_html(html: str, base_url: str) -> tuple[str, str]:
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ", strip=True)
    hrefs = " ".join(a.get("href") or "" for a in soup.find_all("a", href=True))
    blob = f"{html} {text} {hrefs} {base_url}"
    email = pick_generic_emails(blob)
    if not email:
        for a in soup.select("a[href^=mailto]"):
            cand = (a.get("href") or "").split(":", 1)[-1].split("?", 1)[0].strip()
            if is_generic_email(cand):
                email = cand.lower()
                break
    vk = pick_vk(blob)
    return email, vk


def enrich_one(url: str, timeout: int = 8) -> tuple[str, str]:
    if not _host_ok(url):
        return "", ""
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept-Language": "ru"})
    email = vk = ""
    parsed_base = url.rstrip("/")
    # stay on the same origin; try homepage then contact pages
    origin = re.match(r"https?://[^/]+", parsed_base)
    if not origin:
        return "", ""
    origin = origin.group(0)
    for path in CONTACT_PATHS:
        target = parsed_base if path == "" else origin + path
        try:
            r = s.get(target, timeout=timeout, allow_redirects=True)
        except requests.RequestException:
            continue
        if r.status_code >= 400 or "text/html" not in (r.headers.get("content-type") or "text/html"):
            continue
        e, v = extract_from_html(r.text[:400000], r.url)
        email = email or e
        vk = vk or v
        if email and vk:
            break
        time.sleep(0.15)
    return email, vk


def enrich_rows(rows: list[dict], max_workers: int = 8, limit: int | None = None) -> list[dict]:
    jobs = []
    for i, row in enumerate(rows):
        if row.get("email") and row.get("vk"):
            continue
        url = row.get("сайт") or ""
        if not _host_ok(url):
            continue
        jobs.append((i, url))
        if limit and len(jobs) >= limit:
            break
    print(f"[enrich] fetching {len(jobs)} sites")
    results: dict[int, tuple[str, str]] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futs = {pool.submit(enrich_one, url): i for i, url in jobs}
        done = 0
        for fut in as_completed(futs):
            i = futs[fut]
            try:
                results[i] = fut.result()
            except Exception:
                results[i] = ("", "")
            done += 1
            if done % 40 == 0:
                print(f"  enrich {done}/{len(jobs)}")
    got_email = got_vk = 0
    for i, (email, vk) in results.items():
        if email and not rows[i].get("email"):
            rows[i]["email"] = email
            got_email += 1
        if vk and not rows[i].get("vk"):
            rows[i]["vk"] = vk
            got_vk += 1
    print(f"[enrich] new emails={got_email} vk={got_vk}")
    return rows


if __name__ == "__main__":
    raise SystemExit("import enrich_rows from build_leads.py")
