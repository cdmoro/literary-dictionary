#!/usr/bin/env python3
"""Story Atlas – Reading Companion Generator

Generates reading companion EPUBs from the existing SQLite databases.
One EPUB is created per book and one per saga for every available language
(or a specific language selected with ``--lang``).

Output structure
----------------
::

    output/
        en/
            books/
                mainly-grand-frog.epub
                ...
            sagas/
                vastly-sound-bug.epub
                ...
        es/
            ...

Usage
-----
::

    # Generate companions for all languages
    python generate_companions.py

    # Only English
    python generate_companions.py --lang en

    # Only book companions for Spanish
    python generate_companions.py --lang es --books-only

    # Include draft entries
    python generate_companions.py --include-drafts

    # Custom output directory
    python generate_companions.py --output /path/to/output
"""

import argparse
import os
import sys

# Ensure the repository root is on the Python path so that ``src`` and
# ``scripts`` packages can be imported regardless of where the script is
# invoked from.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.build_orchestrator import run  # noqa: E402


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="generate_companions",
        description=(
            "Story Atlas – generate reading companion EPUBs "
            "from literary dictionary SQLite databases."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--lang",
        default=None,
        metavar="LANG",
        help=(
            "Language code to process (e.g. en, es, fr, it, pt). "
            "Omit to process all available languages."
        ),
    )
    parser.add_argument(
        "--output",
        default="output",
        metavar="DIR",
        help="Root output directory (default: output).",
    )
    parser.add_argument(
        "--include-drafts",
        action="store_true",
        help="Include entries marked as drafts (excluded by default).",
    )
    parser.add_argument(
        "--books-only",
        action="store_true",
        help="Generate book-level companions only.",
    )
    parser.add_argument(
        "--sagas-only",
        action="store_true",
        help="Generate saga-level companions only.",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.books_only and args.sagas_only:
        parser.error("--books-only and --sagas-only are mutually exclusive.")

    run(
        lang=args.lang,
        output_dir=args.output,
        include_drafts=args.include_drafts,
        books_only=args.books_only,
        sagas_only=args.sagas_only,
    )


if __name__ == "__main__":
    main()
