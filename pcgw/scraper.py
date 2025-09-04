"""Scraper for individual PCGamingWiki game pages.

This module contains utilities to fetch a game page using Playwright and to
parse save and configuration file locations from the resulting HTML.

The parsing is intentionally defensive: PCGamingWiki pages are curated by
volunteers and may use slightly different table layouts.  The goal is to
extract as much information as possible without failing when unexpected
structures are encountered.
"""

from __future__ import annotations

import asyncio
import logging
import re
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

from bs4 import BeautifulSoup
from playwright.async_api import Browser, async_playwright

# ---------------------------------------------------------------------------
# Data structures

@dataclass
class Entry:
    """One save or configuration path for a specific operating system."""

    type: str  # "save" or "config"
    os: str  # "windows", "macos" or "linux"
    variant: str  # distribution/platform variant
    path_raw: str
    notes: str
    source_section: str


@dataclass
class GameData:
    """Structured representation of a game page."""

    title: str
    url: str
    platforms: List[str]
    entries: List[Entry]

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "url": self.url,
            "platforms": self.platforms,
            "entries": [asdict(e) for e in self.entries],
        }


# ---------------------------------------------------------------------------
# Rate limiting helper

class RateLimiter:
    """Simple async rate limiter enforcing ``rate`` requests/second."""

    def __init__(self, rate: float = 1.0) -> None:
        self.delay = 1.0 / rate
        self._last = 0.0

    async def wait(self) -> None:
        now = time.monotonic()
        wait_for = self.delay - (now - self._last)
        if wait_for > 0:
            await asyncio.sleep(wait_for)
        self._last = time.monotonic()


# ---------------------------------------------------------------------------
# Fetching

async def fetch_html(browser: Browser, url: str, limiter: RateLimiter, retries: int = 3) -> str:
    """Fetch ``url`` using Playwright with retries and rate limiting."""

    backoff = 1.0
    for attempt in range(1, retries + 1):
        try:
            await limiter.wait()
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            html = await page.content()
            await page.close()
            return html
        except Exception as exc:  # pragma: no cover - network errors
            logging.warning("Fetch failed (%s/%s) for %s: %s", attempt, retries, url, exc)
            await asyncio.sleep(backoff)
            backoff *= 2
    raise RuntimeError(f"Failed to fetch {url} after {retries} attempts")


# ---------------------------------------------------------------------------
# Parsing utilities

VARIANT_NORMALISATION = {
    "steam": "steam",
    "gog": "gog",
    "gog.com": "gog",
    "epic games store": "epic",
    "epic": "epic",
    "microsoft store": "microsoft-store",
    "windows store": "microsoft-store",
    "origin": "origin",
    "ea app": "origin",
    "uplay": "uplay",
    "ubisoft connect": "uplay",
    "default": "default",
    "launcher": "other",
}


def _normalise_os(os_text: str) -> Optional[str]:
    os_text = os_text.lower()
    if "mac" in os_text:
        return "macos"
    if "linux" in os_text or "steamdeck" in os_text:
        return "linux"
    if "win" in os_text:
        return "windows"
    return None


def _normalise_variant(text: str) -> str:
    t = text.strip().lower()
    return VARIANT_NORMALISATION.get(t, t.replace(" ", "-")) or "other"


def _parse_location_cell(cell: BeautifulSoup, os_name: str, type_name: str, source_section: str) -> List[Entry]:
    entries: List[Entry] = []
    items = cell.find_all("li") or [cell]
    notes = ""
    for item in items:
        # Extract notes within the same item (e.g. <sup> references)
        note_parts = [n.get_text(" ", strip=True) for n in item.find_all("sup")]
        notes = " ".join(note_parts).strip()
        text = item.get_text(" ", strip=True)
        variant = "default"
        path = text
        match = re.match(r"([^:]+):\s*(.+)", text)
        if match:
            variant_text, path = match.groups()
            variant = _normalise_variant(variant_text)
        entries.append(
            Entry(
                type=type_name,
                os=os_name,
                variant=variant,
                path_raw=path,
                notes=notes,
                source_section=source_section,
            )
        )
    return entries


def extract_game_data(html: str, url: str) -> GameData:
    """Parse ``html`` of a game page and return structured :class:`GameData`."""

    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("h1", id="firstHeading")
    title = title_tag.get_text(strip=True) if title_tag else url.split("/wiki/")[-1]

    # Platforms are inferred from categories such as "Windows games".
    platforms: List[str] = []
    catlinks = soup.select("div#mw-normal-catlinks ul li a")
    for link in catlinks:
        text = link.get_text(strip=True)
        if text.endswith("games"):
            os_name = _normalise_os(text)
            if os_name and os_name not in platforms:
                platforms.append(os_name)

    entries: List[Entry] = []
    sections = [
        ("Save_game_data_location", "save"),
        ("Configuration_file_location", "config"),
    ]
    for section_id, type_name in sections:
        headline = soup.find("span", class_="mw-headline", id=section_id)
        if not headline:
            continue
        container = headline.find_parent(["h2", "h3"]).find_next("div", class_="container-pcgwikitable")
        if not container:
            continue
        rows = container.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 2:
                continue
            os_cell = cells[0]
            location_cell = cells[1]
            os_name = _normalise_os(os_cell.get_text(" ", strip=True) or "")
            if not os_name:
                continue
            entries.extend(_parse_location_cell(location_cell, os_name, type_name, headline.get_text(strip=True)))

    return GameData(title=title, url=url, platforms=platforms, entries=entries)


# Convenience helper used by the CLI
async def scrape_game(url: str, browser: Browser, limiter: RateLimiter) -> GameData:
    html = await fetch_html(browser, url, limiter)
    return extract_game_data(html, url)


__all__ = ["GameData", "Entry", "scrape_game", "RateLimiter"]
