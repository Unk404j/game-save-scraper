# PCGamingWiki multi-game scraper

This project scrapes [PCGamingWiki](https://www.pcgamingwiki.com/) to build a
structured dataset of save game and configuration file locations for many
games.  The scraper uses [Playwright](https://playwright.dev/) to retrieve
pages and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) to
parse them.

The dataset is exported to JSON, CSV and SQLite for use by future tools such
as save-game managers.

## Installation

```bash
pip install playwright beautifulsoup4 html5lib requests
python -m playwright install
```

## Usage

Three input modes are available:

```bash
# Parse all games referenced in the sitemap
python main.py --from-sitemap

# Parse games listed inside a category
python main.py --from-category "https://www.pcgamingwiki.com/wiki/Category:Windows_games"

# Read game URLs from a text file
python main.py --from-file games.txt
```

The scraper respects PCGamingWiki's robots.txt and performs requests with a
rate limit of roughly one request per second.  Results are written to
``dataset.json``, ``dataset.csv`` and ``dataset.sqlite``.

## JSON schema

Each game entry follows the schema below:

```json
{
  "title": "Game Title",
  "url": "https://www.pcgamingwiki.com/wiki/Game_Title",
  "platforms": ["windows", "macos", "linux"],
  "entries": [
    {
      "type": "save",                    // "save" or "config"
      "os": "windows|macos|linux",
      "variant": "steam|gog|epic|microsoft-store|origin|uplay|portable|default|other",
      "path_raw": "%USERPROFILE%\\Saved Games\\Game\\...",
      "notes": "Any notes from the table cell",
      "source_section": "Save game data location"
    }
  ]
}
```

Notes:
* Environment variables and placeholders are kept as-is.
* The scraper stores the section name from which each entry originates for
  traceability.

## Limitations

The scraper is designed for educational purposes and makes a best effort to be
polite: it implements retries with exponential backoff and logs all
operations. Please avoid running it with high concurrency.
