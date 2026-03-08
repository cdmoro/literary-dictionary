#!/usr/bin/env python3
"""CLI entry point for the Literary Dictionary static site generator.

Usage
-----
Generate all languages::

    python3 generate_site.py

Generate a single language::

    python3 generate_site.py --lang en

Use a custom output directory::

    python3 generate_site.py --output site
"""

import argparse
import os
import sys

# Allow running from the project root without installing the package.
sys.path.insert(0, os.path.dirname(__file__))

from scripts.site_generator import generate_site  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a static HTML site from the Literary Dictionary databases."
    )
    parser.add_argument(
        "--lang",
        metavar="LANG",
        help="Language code to generate (e.g. en, es).  Defaults to all languages.",
    )
    parser.add_argument(
        "--output",
        metavar="DIR",
        default="docs",
        help="Output directory (default: docs).",
    )
    args = parser.parse_args()

    print(f"\n📚 Generating Literary Dictionary static site → {args.output}/\n")
    generate_site(output_dir=args.output, lang_filter=args.lang)
    print("\n🎉 Done!")


if __name__ == "__main__":
    main()
