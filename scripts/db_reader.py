"""Database reader for Story Atlas – reads books, sagas, and entries from SQLite databases."""

import glob
import os
import sqlite3
from typing import List, Optional


def get_connection(db_path: str):
    """Create a SQLite connection with row factory."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_databases(lang: Optional[str] = None) -> List[str]:
    """Return list of database paths, optionally filtered by language."""
    pattern = "dictionary/dictionary.*.db"
    dbs = glob.glob(pattern)
    if lang:
        dbs = [db for db in dbs if f".{lang}." in db]
    return sorted(dbs)


def get_lang_from_db_path(db_path: str) -> str:
    """Extract language code from database filename."""
    base = os.path.basename(db_path)
    return base.split(".")[1]


def get_all_books(conn) -> List[dict]:
    """Fetch all books with author and saga info, including cover image paths.

    ``book_cover`` is the book-specific override (may be NULL).
    ``saga_cover`` is the saga-level cover inherited by all books in the saga
    (may be NULL).  The orchestrator resolves the effective cover from these
    two values.
    """
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            b.id,
            b.global_id,
            b.name,
            b.description,
            b.publication_year,
            b.saga_id,
            b.cover AS book_cover,
            a.id AS author_id,
            a.name AS author_name,
            s.name AS saga_name,
            s.global_id AS saga_global_id,
            s.cover AS saga_cover
        FROM books b
        JOIN authors a ON b.author_id = a.id
        LEFT JOIN sagas s ON b.saga_id = s.id
        ORDER BY b.name
        """
    )
    return [dict(row) for row in cur.fetchall()]


def get_all_sagas(conn) -> List[dict]:
    """Fetch all sagas that have no associated books, with author info.

    Sagas that already have book entries are excluded because each book gets
    its own companion; a top-level saga companion is only useful when the saga
    has no individual book records.

    ``cover`` holds the optional cover image path stored in the database.
    """
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            s.id,
            s.global_id,
            s.name,
            s.description,
            s.cover,
            a.id AS author_id,
            a.name AS author_name
        FROM sagas s
        JOIN authors a ON s.author_id = a.id
        WHERE NOT EXISTS (
            SELECT 1 FROM books b WHERE b.saga_id = s.id
        )
        ORDER BY s.name
        """
    )
    return [dict(row) for row in cur.fetchall()]


_ENTRIES_COLUMNS = """
        SELECT
            e.id,
            e.global_id,
            e.name,
            e.display_name,
            e.alias,
            e.description,
            e.category_id,
            e.draft,
            e.book_id,
            e.saga_id,
            e.author_id,
            c.name AS category_name,
            c.abbr AS category_abbr
        FROM entries e
        LEFT JOIN categories c ON e.category_id = c.id
"""


def get_entries_for_book(
    conn, book_id: int, include_drafts: bool = False
) -> List[dict]:
    """Fetch all entries for a specific book, ordered by name.

    Uses ``draft = 0`` as the default spoiler filter. When the schema is
    extended with a ``spoiler_level`` column, this function can be updated to
    filter on that column instead.
    """
    cur = conn.cursor()
    if include_drafts:
        cur.execute(
            _ENTRIES_COLUMNS + "WHERE e.book_id = ? ORDER BY e.name",
            (book_id,),
        )
    else:
        cur.execute(
            _ENTRIES_COLUMNS + "WHERE e.book_id = ? AND e.draft = 0 ORDER BY e.name",
            (book_id,),
        )
    return [dict(row) for row in cur.fetchall()]


def get_entries_for_saga(
    conn, saga_id: int, include_drafts: bool = False
) -> List[dict]:
    """Fetch all entries for a specific saga, ordered by name.

    Uses ``draft = 0`` as the default spoiler filter.
    """
    cur = conn.cursor()
    if include_drafts:
        cur.execute(
            _ENTRIES_COLUMNS + "WHERE e.saga_id = ? ORDER BY e.name",
            (saga_id,),
        )
    else:
        cur.execute(
            _ENTRIES_COLUMNS + "WHERE e.saga_id = ? AND e.draft = 0 ORDER BY e.name",
            (saga_id,),
        )
    return [dict(row) for row in cur.fetchall()]
