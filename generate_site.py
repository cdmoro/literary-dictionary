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

Generate and immediately serve the site locally::

    python3 generate_site.py --serve
    python3 generate_site.py --lang en --serve --port 9000

Without ``--port`` the server tries 9000, then 9001, 9002 … until it
finds an available port.
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
    parser.add_argument(
        "--serve",
        action="store_true",
        help="After generating, start a local HTTP server to preview the site.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        metavar="PORT",
        help=(
            "Port for the local preview server. Only used with --serve. "
            "When omitted, the first available port starting from 9000 is used."
        ),
    )
    args = parser.parse_args()

    print(f"\n📚 Generating Literary Dictionary static site → {args.output}/\n")
    generate_site(output_dir=args.output, lang_filter=args.lang)
    print("\n🎉 Done!")

    if args.serve:
        import http.server
        import socketserver
        import webbrowser

        output_abs = os.path.abspath(args.output)

        # Serve from the output directory
        os.chdir(output_abs)

        class _Handler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, fmt, *a):  # suppress per-request noise
                """Override to suppress HTTP access log lines."""

        # Determine port: explicit value, or auto-scan from 9000 upward.
        auto_select = args.port is None
        port = 9000 if auto_select else args.port
        httpd = None
        while httpd is None:
            try:
                httpd = socketserver.TCPServer(("", port), _Handler)
            except OSError:
                if not auto_select or port >= 65535:
                    raise
                port += 1

        url = f"http://localhost:{port}/"
        print(f"\n🌐  Serving site at {url}")
        print("    Press Ctrl+C to stop.\n")

        try:
            webbrowser.open(url)
        except webbrowser.Error:
            pass  # browser unavailable – user can open the URL manually

        with httpd:
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nServer stopped.")


if __name__ == "__main__":
    main()
