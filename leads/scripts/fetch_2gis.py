#!/usr/bin/env python3
"""2ГИС source notes.

The public 2GIS website blocks datacenter IPs (captcha /museum),
and the Catalog API key used by the website is restricted for /3.0/items.

This project stores 2GIS rows in leads/raw/2gis-*.json collected from the
public 2GIS catalogue (via a 2GIS places scraper: dami_studio/2gis-places-scraper,
city = «Нижний Новгород»). Re-run that scraper and save the dataset as:

  leads/raw/2gis-restaurants.json
  leads/raw/2gis-kindergartens.json
  leads/raw/2gis-companies.json

Then: python3 ingest_2gis.py && python3 build_leads.py

Queries used:

  restaurants: ресторан, кафе, банкетный зал, лофт, караоке, бар
  kindergartens: детский сад, частный детский сад, детский центр,
                 центр развития, детский клуб
  companies: IT компания, завод, офис компании, банк,
             строительная компания, логистика
"""

from ingest_2gis import ingest
from nn_common import RAW_DIR


def main() -> None:
    ingest(sorted(RAW_DIR.glob("2gis-*.json")))


if __name__ == "__main__":
    main()
