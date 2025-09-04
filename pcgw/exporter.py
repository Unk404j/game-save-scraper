"""Utility functions for exporting scraped data to various formats."""

from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path
from typing import Iterable

from .scraper import GameData


def to_json(games: Iterable[GameData], path: str | Path) -> None:
    """Write the full dataset to ``path`` in JSON format."""

    data = [g.to_dict() for g in games]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def to_csv(games: Iterable[GameData], path: str | Path) -> None:
    """Write a flattened CSV file where each row represents an entry."""

    fieldnames = [
        "title",
        "url",
        "platforms",
        "type",
        "os",
        "variant",
        "path_raw",
        "notes",
        "source_section",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for g in games:
            for e in g.entries:
                row = {
                    "title": g.title,
                    "url": g.url,
                    "platforms": ";".join(g.platforms),
                    **e.__dict__,
                }
                writer.writerow(row)


def to_sqlite(games: Iterable[GameData], path: str | Path) -> None:
    """Persist entries into a SQLite database.

    A single table named ``entries`` is created with columns corresponding to
    the fields of the JSON schema. Existing databases are overwritten.
    """

    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS entries (
            title TEXT,
            url TEXT,
            platforms TEXT,
            type TEXT,
            os TEXT,
            variant TEXT,
            path_raw TEXT,
            notes TEXT,
            source_section TEXT
        )
        """
    )
    cur.execute("DELETE FROM entries")
    for g in games:
        for e in g.entries:
            cur.execute(
                "INSERT INTO entries VALUES (?,?,?,?,?,?,?,?,?)",
                (
                    g.title,
                    g.url,
                    ";".join(g.platforms),
                    e.type,
                    e.os,
                    e.variant,
                    e.path_raw,
                    e.notes,
                    e.source_section,
                ),
            )
    conn.commit()
    conn.close()


__all__ = ["to_json", "to_csv", "to_sqlite"]
