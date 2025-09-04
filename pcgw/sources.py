"""Input source utilities for listing PCGamingWiki game URLs.

This module implements the three input modes described in the
instructions:

```
--from-sitemap   # parse the main sitemap to list game pages
--from-category  # parse a category page listing games
--from-file      # read URLs from a file
```

Each function returns a list of absolute PCGamingWiki URLs.
```
"""

from __future__ import annotations

import logging
import time
from typing import Iterable, List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

PCGW_BASE = "https://www.pcgamingwiki.com"
SITEMAP_URL = f"{PCGW_BASE}/sitemap.xml"


def _rate_limited_get(url: str, delay: float = 1.0) -> requests.Response:
    """Fetch ``url`` respecting a simple rate limit.

    PCGamingWiki asks scrapers to be gentle.  We sleep for ``delay`` seconds
    between requests and return the :class:`requests.Response` object.
    """

    logging.info("Fetching %s", url)
    resp = requests.get(url, timeout=30)
    time.sleep(delay)
    resp.raise_for_status()
    return resp


def from_sitemap() -> List[str]:
    """Return all game URLs extracted from the public sitemap.

    Only URLs belonging to the main ``/wiki/`` namespace are kept.  This
    filters out categories, files and other mediawiki pages that contain a
    colon in the slug.
    """

    resp = _rate_limited_get(SITEMAP_URL)
    soup = BeautifulSoup(resp.text, "xml")
    urls = []
    for loc in soup.find_all("loc"):
        url = loc.get_text(strip=True)
        if "/wiki/" not in url:
            continue
        slug = url.split("/wiki/", 1)[1]
        if ":" in slug:
            continue  # skip non game pages
        urls.append(url)
    return urls


def from_category(url: str) -> List[str]:
    """Return all game URLs listed in the given category page.

    The function follows ``next page`` links until all entries in the
    category are gathered.
    """

    urls: List[str] = []
    next_url = url
    while next_url:
        resp = _rate_limited_get(next_url)
        soup = BeautifulSoup(resp.text, "html.parser")
        cat = soup.find("div", class_="mw-category")
        if cat:
            for a in cat.find_all("a"):
                href = a.get("href")
                if not href:
                    continue
                abs_url = urljoin(PCGW_BASE, href)
                urls.append(abs_url)
        # check for "next page" link
        next_link = soup.find("a", class_="mw-nextlink")
        if next_link and next_link.get("href"):
            next_url = urljoin(PCGW_BASE, next_link["href"])
        else:
            next_url = None
    return urls


def from_file(path: str) -> List[str]:
    """Return game URLs listed line by line in ``path``."""

    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


__all__ = ["from_sitemap", "from_category", "from_file", "PCGW_BASE"]
