"""Build orchestrator for Story Atlas reading companions.

Scans all SQLite databases and generates book-level and saga-level reading
companion EPUBs.  The orchestrator is designed to be called either directly
from :mod:`generate_companions` (the CLI entry point) or programmatically
from other tools.

Future extensions supported by this design:
* Universe companions – add a ``generate_universe_companions`` function that
  queries all entries for a given author and aggregates them.
* Cross-references – the entry data already carries ``saga_id`` / ``book_id``
  links; a future pass can resolve those into internal hyperlinks.
* Multi-edition publications – pass an edition tag to
  :func:`build_companion_epub` and reflect it in the OPF metadata.
"""

import os
import uuid
from typing import Optional

from scripts.cover_generator import create_cover, pick_cover_colour
from scripts.db_reader import (
    get_all_books,
    get_all_sagas,
    get_connection,
    get_databases,
    get_entries_for_book,
    get_entries_for_saga,
    get_lang_from_db_path,
)
from scripts.epub_builder import build_companion_epub
from src.utils import get_translations


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _base_cover_path(lang: str, saga_global_id: Optional[str] = None) -> Optional[str]:
    """Return the path to the best available base cover image.

    Search order:
    1. A saga-/franchise-specific image  ``assets/cover_<saga_global_id>.<ext>``
    2. A language-default image          ``assets/cover_<lang>.<ext>``
    3. ``None`` when nothing is found (the cover generator falls back to SVG).
    """
    candidates = []
    if saga_global_id:
        for ext in ("jpg", "jpeg", "png"):
            candidates.append(f"assets/cover_{saga_global_id}.{ext}")
    for ext in ("jpg", "jpeg", "png"):
        candidates.append(f"assets/cover_{lang}.{ext}")

    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def _make_uid(namespace: str, key: str) -> str:
    """Return a deterministic UUID-5 for the given *key* within *namespace*."""
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"story-atlas-{namespace}-{key}"))


# ---------------------------------------------------------------------------
# Per-language generators
# ---------------------------------------------------------------------------


def generate_book_companions(
    base_output: str,
    lang: str,
    conn,
    strings: dict,
    include_drafts: bool = False,
) -> None:
    """Generate one reading companion EPUB per book in *conn*.

    Output path: ``<base_output>/<lang>/books/<global_id>.epub``
    """
    books = get_all_books(conn)
    if not books:
        print(f"  No books found for {lang.upper()}")
        return

    companion_label = strings.get("companion_reading", "Reading Companion")
    lang_label = strings.get("lang_name", strings.get("lang", lang.upper()))
    created_by_label = strings.get("companion_created_by", "Created by")

    for book in books:
        book_gid = book["global_id"]
        title = book["name"]
        author_name = book["author_name"]
        entries = get_entries_for_book(conn, book["id"], include_drafts=include_drafts)

        if not entries:
            print(
                f"  ⚠️  No entries for book: {title} ({lang.upper()}) — skipping"
            )
            continue

        print(
            f"  📖 Generating companion for book: {title}"
            f" ({lang.upper()}) [{len(entries)} entries]"
        )

        output_path = os.path.join(base_output, lang, "books", f"{book_gid}.epub")
        cover_dir = os.path.join(base_output, lang, "books", ".covers")

        base_cover = _base_cover_path(lang, book.get("saga_global_id"))
        # Books in a saga share the saga's colour; standalone books use their own.
        # saga_global_id is None (SQL NULL via LEFT JOIN) when the book has no saga.
        saga_gid = book.get("saga_global_id")
        colour_id = saga_gid if saga_gid is not None else book_gid
        cover_file = create_cover(
            output_dir=cover_dir,
            title=title,
            lang=lang,
            companion_label=companion_label,
            lang_label=lang_label,
            created_by_label=created_by_label,
            base_cover_path=base_cover,
            bg_colour=pick_cover_colour(colour_id),
        )
        cover_src = os.path.join(cover_dir, cover_file)
        uid = _make_uid("book", f"{book_gid}-{lang}")

        build_companion_epub(
            output_path=output_path,
            lang=lang,
            title=title,
            author_name=author_name,
            entries=entries,
            cover_filename=cover_file,
            cover_src_path=cover_src,
            uid=uid,
        )
        print(f"  ✅ Created: {output_path}")


def generate_saga_companions(
    base_output: str,
    lang: str,
    conn,
    strings: dict,
    include_drafts: bool = False,
) -> None:
    """Generate one reading companion EPUB per saga in *conn*.

    Output path: ``<base_output>/<lang>/sagas/<global_id>.epub``
    """
    sagas = get_all_sagas(conn)
    if not sagas:
        print(f"  No sagas found for {lang.upper()}")
        return

    companion_label = strings.get("companion_reading", "Reading Companion")
    lang_label = strings.get("lang_name", strings.get("lang", lang.upper()))
    created_by_label = strings.get("companion_created_by", "Created by")

    for saga in sagas:
        saga_gid = saga["global_id"]
        title = saga["name"]
        author_name = saga["author_name"]
        entries = get_entries_for_saga(conn, saga["id"], include_drafts=include_drafts)

        if not entries:
            print(
                f"  ⚠️  No entries for saga: {title} ({lang.upper()}) — skipping"
            )
            continue

        print(
            f"  📚 Generating companion for saga: {title}"
            f" ({lang.upper()}) [{len(entries)} entries]"
        )

        output_path = os.path.join(base_output, lang, "sagas", f"{saga_gid}.epub")
        cover_dir = os.path.join(base_output, lang, "sagas", ".covers")

        base_cover = _base_cover_path(lang, saga_gid)
        cover_file = create_cover(
            output_dir=cover_dir,
            title=title,
            lang=lang,
            companion_label=companion_label,
            lang_label=lang_label,
            created_by_label=created_by_label,
            base_cover_path=base_cover,
            bg_colour=pick_cover_colour(saga_gid),
        )
        cover_src = os.path.join(cover_dir, cover_file)
        uid = _make_uid("saga", f"{saga_gid}-{lang}")

        build_companion_epub(
            output_path=output_path,
            lang=lang,
            title=title,
            author_name=author_name,
            entries=entries,
            cover_filename=cover_file,
            cover_src_path=cover_src,
            uid=uid,
        )
        print(f"  ✅ Created: {output_path}")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def run(
    lang: Optional[str] = None,
    output_dir: str = "output",
    include_drafts: bool = False,
    books_only: bool = False,
    sagas_only: bool = False,
) -> None:
    """Scan databases and generate all reading companion EPUBs.

    Args:
        lang:           Language code to process (e.g. ``'en'``). ``None``
                        means *all* available languages.
        output_dir:     Root of the output tree.  EPUBs are written to
                        ``<output_dir>/<lang>/books/`` and
                        ``<output_dir>/<lang>/sagas/``.
        include_drafts: When ``True``, draft entries are included.
        books_only:     Skip saga companions.
        sagas_only:     Skip book companions.
    """
    db_files = get_databases(lang)
    if not db_files:
        msg = f"No databases found for language: {lang}" if lang else "No databases found."
        print(msg)
        return

    print(f"\n🔍 Found {len(db_files)} database(s) to process\n")

    for db_path in db_files:
        db_lang = get_lang_from_db_path(db_path)
        print(f"Processing language: {db_lang.upper()} ({db_path})")
        conn = get_connection(db_path)
        strings = get_translations(db_lang)
        try:
            if not sagas_only:
                print(f"\n  📖 Book companions:")
                generate_book_companions(
                    output_dir, db_lang, conn, strings, include_drafts
                )

            if not books_only:
                print(f"\n  📚 Saga companions:")
                generate_saga_companions(
                    output_dir, db_lang, conn, strings, include_drafts
                )
        finally:
            conn.close()

    print(f"\n🎉 All companions generated in: {output_dir}/")
