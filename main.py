"""Command line interface for the PCGamingWiki scraper.

The scraper can obtain the list of game pages from three different input
sources:

* ``--from-sitemap``   – Parse the PCGamingWiki sitemap to list all games.
* ``--from-category``  – Parse a specific category URL.
* ``--from-file``      – Read a file containing one game URL per line.

For each game the scraper extracts save and configuration file locations and
writes the combined dataset to JSON, CSV and SQLite files.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
from pathlib import Path
from typing import List

from playwright.async_api import async_playwright

from pcgw import sources
from pcgw.exporter import to_csv, to_json, to_sqlite
from pcgw.scraper import RateLimiter, scrape_game

DEFAULT_JSON = "dataset.json"
DEFAULT_CSV = "dataset.csv"
DEFAULT_SQLITE = "dataset.sqlite"


async def scrape_all(urls: List[str]) -> List:
    """Scrape all ``urls`` sequentially with rate limiting."""

    limiter = RateLimiter(rate=1.0)  # 1 request/second
    results = []
    async with async_playwright() as pw:
        browser = await pw.firefox.launch(headless=True)
        for url in urls:
            try:
                logging.info("Scraping %s", url)
                game = await scrape_game(url, browser, limiter)
                results.append(game)
            except Exception as exc:  # pragma: no cover - network errors
                logging.error("Failed to scrape %s: %s", url, exc)
        await browser.close()
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="PCGamingWiki multi-game scraper")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--from-sitemap", action="store_true", help="Parse URLs from the sitemap")
    group.add_argument("--from-category", metavar="URL", help="Parse URLs from a category page")
    group.add_argument("--from-file", metavar="FILE", help="Read URLs from a file")
    parser.add_argument("--output-json", default=DEFAULT_JSON)
    parser.add_argument("--output-csv", default=DEFAULT_CSV)
    parser.add_argument("--output-sqlite", default=DEFAULT_SQLITE)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    if args.from_sitemap:
        urls = sources.from_sitemap()
    elif args.from_category:
        urls = sources.from_category(args.from_category)
    else:
        urls = sources.from_file(args.from_file)

    if not urls:
        logging.error("No URLs to process")
        return

    games = asyncio.run(scrape_all(urls))

    # export
    to_json(games, args.output_json)
    to_csv(games, args.output_csv)
    to_sqlite(games, args.output_sqlite)
    logging.info("Exported %d games", len(games))


if __name__ == "__main__":
    main()
