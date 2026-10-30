#!/usr/bin/env python3
"""Run public-source collectors, then build CSV/XLSX."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fetch_firmoteka import collect as collect_firmoteka
from fetch_mdoy import collect as collect_mdoy
from fetch_mdoy_ids import collect as collect_mdoy_ids
from fetch_yandex import collect as collect_yandex
from build_leads import main as build_main


def main() -> None:
    print("== mdoy.pro ==")
    collect_mdoy()
    collect_mdoy_ids()
    print("== firmoteka ==")
    try:
        collect_firmoteka()
    except Exception as exc:
        print("[firmoteka] skip:", exc)
    print("== yandex maps ==")
    for segment in ("рестораны", "детские сады и центры", "компании"):
        collect_yandex(segment)
    print("== build ==")
    build_main()


if __name__ == "__main__":
    main()
