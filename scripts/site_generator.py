"""Static site generator for the Literary Dictionary.

Reads all SQLite databases and generates a ``docs/`` directory containing a
static HTML site that can be deployed to GitHub Pages or Netlify.

Site structure::

    docs/
    ├── index.html                  # Landing page (all languages + stats)
    ├── en/
    │   ├── index.html              # EN – letter nav + books/sagas list
    │   ├── A.html                  # Entries starting with A
    │   ├── B.html                  # ...
    │   ├── books/
    │   │   └── <book-gid>.html     # Book-specific entries
    │   └── sagas/
    │       └── <saga-gid>.html     # Saga-specific entries
    └── es/, fr/, it/, pt/          # Same structure for each language
"""

import glob as _glob
import html
import os
import sqlite3
from collections import defaultdict
from typing import Optional

from src.utils import escape_text_nodes, normalize_character

_ENCODING = "utf-8"

# ---------------------------------------------------------------------------
# CSS – embedded in every page (no external deps)
# ---------------------------------------------------------------------------

_CSS = """\
*, *::before, *::after { box-sizing: border-box; }
body {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 1rem;
    line-height: 1.7;
    max-width: 860px;
    margin: 0 auto;
    padding: 1rem 1.5rem 3rem;
    color: #1a1a1a;
    background: #fafaf8;
}
a { color: #2a4a8a; text-decoration: none; }
a:hover { text-decoration: underline; }
nav.site-nav {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    padding: 0.6rem 0;
    border-bottom: 2px solid #ddd;
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
}
nav.site-nav a {
    padding: 0.2rem 0.5rem;
    border-radius: 3px;
    background: #eee;
    color: #333;
}
nav.site-nav a:hover { background: #ddd; text-decoration: none; }
nav.lang-nav {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin: 1rem 0;
}
nav.lang-nav a {
    padding: 0.3rem 0.8rem;
    border: 1px solid #aaa;
    border-radius: 4px;
    font-size: 0.9rem;
    background: #fff;
}
nav.lang-nav a:hover, nav.lang-nav a.active {
    background: #2a4a8a;
    color: #fff;
    border-color: #2a4a8a;
    text-decoration: none;
}
h1 { font-size: 2rem; margin-bottom: 0.3rem; }
h2 { font-size: 1.4rem; margin-top: 2rem; margin-bottom: 0.5rem; color: #333; }
h3.letter-heading {
    font-size: 1.3rem;
    margin-top: 2rem;
    color: #444;
    border-bottom: 2px solid #ccc;
    padding-bottom: 0.2rem;
}
.subtitle { color: #666; font-style: italic; margin-bottom: 1.5rem; }
.stats { display: flex; flex-wrap: wrap; gap: 1rem; margin: 1rem 0 2rem; }
.stat-box {
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 6px;
    padding: 0.8rem 1.2rem;
    min-width: 120px;
    text-align: center;
}
.stat-num { font-size: 1.8rem; font-weight: bold; color: #2a4a8a; }
.stat-lbl { font-size: 0.8rem; color: #666; }
.letter-nav {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem;
    margin: 1rem 0;
}
.letter-nav a {
    display: inline-block;
    width: 2rem;
    height: 2rem;
    line-height: 2rem;
    text-align: center;
    border: 1px solid #ccc;
    border-radius: 3px;
    font-size: 0.9rem;
    background: #fff;
}
.letter-nav a:hover { background: #2a4a8a; color: #fff; border-color: #2a4a8a; text-decoration: none; }
.entry { margin-bottom: 0; }
.entry strong { font-size: 1.05rem; }
.entry-alias { color: #666; font-size: 0.9rem; margin-left: 0.3rem; }
.definition { margin: 0.3rem 0 0.3rem 1.2rem; }
.entry-abbr { font-style: italic; color: #555; }
.origin { margin: 0.2rem 0 0.2rem 1.2rem; font-size: 0.95rem; }
.see-also { margin: 0.2rem 0 0.2rem 1.2rem; font-size: 0.95rem; }
hr { border: none; border-top: 1px solid #e0e0e0; margin: 0.8rem 0; }
.books-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}
.book-card {
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 6px;
    padding: 0.8rem 1rem;
}
.book-card h4 { margin: 0 0 0.3rem; font-size: 1rem; }
.book-card .author { color: #555; font-size: 0.85rem; }
.book-card .year { color: #888; font-size: 0.8rem; }
.book-card .count { margin-top: 0.5rem; font-size: 0.85rem; }
footer {
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid #ddd;
    font-size: 0.85rem;
    color: #888;
    text-align: center;
}
"""


# ---------------------------------------------------------------------------
# HTML skeleton helpers
# ---------------------------------------------------------------------------


def _page(title: str, body: str, root_prefix: str = "") -> str:
    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title>{html.escape(title)} – Literary Dictionary</title>
    <style>{_CSS}</style>
</head>
<body>
{body}
<footer>
    <p>Literary Dictionary – <a href="{root_prefix}index.html">Home</a></p>
</footer>
</body>
</html>"""


def _site_nav(lang: Optional[str], root_prefix: str, available_langs: list) -> str:
    links = [f'<a href="{root_prefix}index.html">🏠 Home</a>']
    for lc in available_langs:
        active = ' class="active"' if lc == lang else ""
        links.append(f'<a href="{root_prefix}{lc}/index.html"{active}>{lc.upper()}</a>')
    return '<nav class="site-nav">' + " ".join(links) + "</nav>"


def _lang_nav(current_lang: str, available_langs: list, path_from_lang: str = "") -> str:
    parts = []
    for lc in available_langs:
        active = ' class="active"' if lc == current_lang else ""
        # From a lang subdirectory, link to sibling lang: ../en/ etc.
        parts.append(
            f'<a href="../{lc}/{path_from_lang}"{active}>{lc.upper()}</a>'
        )
    return '<nav class="lang-nav">' + "".join(parts) + "</nav>"


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------


def _get_connection(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def _get_all_entries(conn) -> list:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT e.id, e.name, e.display_name, e.alias, e.description,
               e.book_id, e.saga_id, e.author_id, e.category_id,
               c.abbr AS category_abbr, c.name AS category_name,
               b.name AS book_name, b.global_id AS book_gid,
               s.name AS saga_name, s.global_id AS saga_gid,
               a.name AS author_name
        FROM entries e
        LEFT JOIN categories c ON e.category_id = c.id
        LEFT JOIN books b ON e.book_id = b.id
        LEFT JOIN sagas s ON e.saga_id = s.id
        LEFT JOIN authors a ON e.author_id = a.id
        WHERE e.draft = 0
        ORDER BY e.name COLLATE NOCASE
        """
    )
    return [dict(r) for r in cur.fetchall()]


def _get_books(conn) -> list:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT b.id, b.global_id, b.name, b.publication_year,
               a.name AS author_name,
               s.global_id AS saga_gid, s.name AS saga_name
        FROM books b
        JOIN authors a ON b.author_id = a.id
        LEFT JOIN sagas s ON b.saga_id = s.id
        ORDER BY b.name
        """
    )
    return [dict(r) for r in cur.fetchall()]


def _get_sagas(conn) -> list:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT s.id, s.global_id, s.name, a.name AS author_name
        FROM sagas s
        JOIN authors a ON s.author_id = a.id
        ORDER BY s.name
        """
    )
    return [dict(r) for r in cur.fetchall()]


def _entry_letter(entry: dict) -> str:
    first = normalize_character(entry["name"][0])
    return first if first.isalpha() else "Other"


def _build_see_also(entries: list) -> dict:
    """entry_id → list of (related_entry, target_letter)."""
    by_cat: dict = defaultdict(list)
    letters: dict = {}
    for e in entries:
        cat = e.get("category_id")
        if cat is not None:
            by_cat[cat].append(e)
        letters[e["id"]] = _entry_letter(e)
    result = {}
    for e in entries:
        cat = e.get("category_id")
        peers = [p for p in by_cat.get(cat, []) if p["id"] != e["id"]]
        result[e["id"]] = [(p, letters[p["id"]]) for p in peers]
    return result


# ---------------------------------------------------------------------------
# Entry HTML fragment (shared between letter pages and book/saga pages)
# ---------------------------------------------------------------------------


def _entry_html(entry: dict, see_also: list, letter_link_prefix: str = "") -> str:
    """Render a single entry as an HTML fragment.

    ``see_also`` is a list of (related_entry, target_letter) tuples.
    ``letter_link_prefix`` is prepended to letter-page hrefs (e.g. ``'../'``
    when inside books/ or sagas/).
    """
    eid = entry["id"]
    name = entry.get("display_name") or entry["name"]
    abbr = entry.get("category_abbr") or ""
    desc = entry.get("description") or ""
    alias = entry.get("alias") or ""
    book_name = entry.get("book_name") or ""
    book_gid = entry.get("book_gid") or ""
    saga_name = entry.get("saga_name") or ""
    saga_gid = entry.get("saga_gid") or ""
    author_name = entry.get("author_name") or ""

    out = f'<div class="entry" id="entry-{eid}">\n'
    out += f"  <strong>{html.escape(name)}</strong>"
    if alias:
        aliases = [a.strip() for a in alias.split(";") if a.strip()]
        if aliases:
            out += f'  <span class="entry-alias">({html.escape(", ".join(aliases))})</span>'
    out += "\n"
    out += '  <div class="definition">\n'
    if abbr:
        out += f'    <em class="entry-abbr">{html.escape(abbr)}.</em> '
    out += f"{escape_text_nodes(desc)}\n  </div>\n"

    # Origin
    if author_name:
        if book_name and saga_name:
            origin = (
                f'<em><a href="{letter_link_prefix}books/{html.escape(book_gid)}.html">'
                f"{html.escape(book_name)}</a></em>"
                f" (part of <em>{html.escape(saga_name)}</em>), "
                f"{html.escape(author_name)}"
            )
        elif book_name:
            origin = (
                f'<em><a href="{letter_link_prefix}books/{html.escape(book_gid)}.html">'
                f"{html.escape(book_name)}</a></em>, {html.escape(author_name)}"
            )
        elif saga_name:
            origin = (
                f'<em><a href="{letter_link_prefix}sagas/{html.escape(saga_gid)}.html">'
                f"{html.escape(saga_name)}</a></em>, {html.escape(author_name)}"
            )
        else:
            origin = f"{html.escape(author_name)}"
        out += f'  <div class="origin"><strong>Origin:</strong> {origin}</div>\n'

    # See also
    if see_also:
        links = [
            f'<a href="{letter_link_prefix}{tgt_letter}.html#entry-{p["id"]}">'
            f'{html.escape(p.get("display_name") or p["name"])}</a>'
            for p, tgt_letter in see_also
        ]
        out += (
            f'  <div class="see-also"><strong>See also:</strong>'
            f" {', '.join(links)}</div>\n"
        )

    out += "</div>\n<hr/>\n"
    return out


# ---------------------------------------------------------------------------
# Page generators
# ---------------------------------------------------------------------------


def _letter_page(
    lang: str,
    letter: str,
    entries: list,
    all_letters: list,
    see_also_map: dict,
    available_langs: list,
) -> str:
    display = letter if letter != "Other" else "Symbols and Numbers"
    letter_nav_links = []
    for ltr in all_letters:
        disp = ltr if ltr != "Other" else "#"
        if ltr == letter:
            letter_nav_links.append(
                f'<a href="{ltr}.html" style="background:#2a4a8a;color:#fff">{disp}</a>'
            )
        else:
            letter_nav_links.append(f'<a href="{ltr}.html">{disp}</a>')
    letter_nav = '<div class="letter-nav">' + "".join(letter_nav_links) + "</div>"

    entries_html = "".join(
        _entry_html(e, see_also_map.get(e["id"], []))
        for e in entries
    )

    body = f"""\
{_site_nav(lang, '../', available_langs)}
{_lang_nav(lang, available_langs, f'{letter}.html')}
<h1>Literary Dictionary</h1>
<p class="subtitle">{display} — {lang.upper()} edition</p>
{letter_nav}
<h3 class="letter-heading">{html.escape(display)}</h3>
{entries_html}"""

    return _page(f"{display} – {lang.upper()}", body, root_prefix="../")


def _lang_index_page(
    lang: str,
    entries: list,
    books: list,
    sagas: list,
    all_letters: list,
    available_langs: list,
) -> str:
    entry_count = len(entries)
    book_count = len(books)
    saga_count = len(sagas)

    letter_nav_links = [
        f'<a href="{ltr}.html">{ltr if ltr != "Other" else "#"}</a>'
        for ltr in all_letters
    ]
    letter_nav = '<div class="letter-nav">' + "".join(letter_nav_links) + "</div>"

    stats = f"""\
<div class="stats">
  <div class="stat-box"><div class="stat-num">{entry_count}</div><div class="stat-lbl">Entries</div></div>
  <div class="stat-box"><div class="stat-num">{book_count}</div><div class="stat-lbl">Books</div></div>
  <div class="stat-box"><div class="stat-num">{saga_count}</div><div class="stat-lbl">Series</div></div>
</div>"""

    books_html = '<div class="books-grid">'
    for book in books:
        year = f'<span class="year">{book["publication_year"]}</span>' if book.get("publication_year") else ""
        saga_tag = ""
        if book.get("saga_name"):
            saga_tag = f'<div class="author">{html.escape(book["saga_name"])}</div>'
        books_html += f"""\
<div class="book-card">
  <h4><a href="books/{html.escape(book['global_id'])}.html">{html.escape(book['name'])}</a></h4>
  <div class="author">{html.escape(book['author_name'])} {year}</div>
  {saga_tag}
</div>"""
    books_html += "</div>"

    sagas_html = '<div class="books-grid">'
    for saga in sagas:
        sagas_html += f"""\
<div class="book-card">
  <h4><a href="sagas/{html.escape(saga['global_id'])}.html">{html.escape(saga['name'])}</a></h4>
  <div class="author">{html.escape(saga['author_name'])}</div>
</div>"""
    sagas_html += "</div>"

    body = f"""\
{_site_nav(lang, '../', available_langs)}
{_lang_nav(lang, available_langs)}
<h1>Literary Dictionary</h1>
<p class="subtitle">{lang.upper()} edition</p>
{stats}
<h2>Browse by letter</h2>
{letter_nav}
<h2>Books</h2>
{books_html}
<h2>Series</h2>
{sagas_html}"""

    return _page(f"Literary Dictionary – {lang.upper()}", body, root_prefix="../")


def _book_page(
    lang: str,
    book: dict,
    entries: list,
    see_also_map: dict,
    available_langs: list,
) -> str:
    title = book["name"]
    author = book["author_name"]
    year = f" ({book['publication_year']})" if book.get("publication_year") else ""
    saga_note = ""
    if book.get("saga_name"):
        saga_gid = book.get("saga_gid", "")
        saga_note = (
            f'<p>Part of: <a href="../sagas/{html.escape(saga_gid)}.html">'
            f"{html.escape(book['saga_name'])}</a></p>"
        )

    entries_html = "".join(
        _entry_html(e, see_also_map.get(e["id"], []), letter_link_prefix="../")
        for e in entries
    )

    body = f"""\
{_site_nav(lang, '../../', available_langs)}
{_lang_nav(lang, available_langs, f'books/{html.escape(book["global_id"])}.html')}
<h1>{html.escape(title)}</h1>
<p class="subtitle">{html.escape(author)}{html.escape(year)}</p>
{saga_note}
<p><a href="../index.html">← {lang.upper()} index</a></p>
{entries_html}"""

    return _page(f"{title} – {lang.upper()}", body, root_prefix="../../")


def _saga_page(
    lang: str,
    saga: dict,
    entries: list,
    see_also_map: dict,
    available_langs: list,
) -> str:
    title = saga["name"]
    author = saga["author_name"]

    entries_html = "".join(
        _entry_html(e, see_also_map.get(e["id"], []), letter_link_prefix="../")
        for e in entries
    )

    body = f"""\
{_site_nav(lang, '../../', available_langs)}
{_lang_nav(lang, available_langs, f'sagas/{html.escape(saga["global_id"])}.html')}
<h1>{html.escape(title)}</h1>
<p class="subtitle">{html.escape(author)}</p>
<p><a href="../index.html">← {lang.upper()} index</a></p>
{entries_html}"""

    return _page(f"{title} – {lang.upper()}", body, root_prefix="../../")


def _index_page(lang_data: dict, available_langs: list) -> str:
    """Global landing page with per-language stats."""
    lang_cards = ""
    for lc in available_langs:
        data = lang_data.get(lc, {})
        entries = data.get("entry_count", 0)
        books = data.get("book_count", 0)
        lang_cards += f"""\
<div class="book-card">
  <h4><a href="{lc}/index.html">{lc.upper()} – {html.escape(data.get('lang_name', lc.upper()))}</a></h4>
  <div class="author">{entries} entries · {books} books</div>
</div>"""

    body = f"""\
<h1>Literary Dictionary</h1>
<p class="subtitle">Characters, places, spells and more from world literature</p>
<nav class="lang-nav">
{''.join(f'<a href="{lc}/index.html">{lc.upper()}</a>' for lc in available_langs)}
</nav>
<h2>Available editions</h2>
<div class="books-grid">{lang_cards}</div>"""

    return _page("Literary Dictionary", body, root_prefix="")


# ---------------------------------------------------------------------------
# Writer
# ---------------------------------------------------------------------------


def _write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding=_ENCODING) as fh:
        fh.write(content)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def generate_site(
    output_dir: str = "docs",
    lang_filter: Optional[str] = None,
) -> None:
    """Generate the full static site into *output_dir*.

    Args:
        output_dir:   Root output directory (defaults to ``docs/``).
        lang_filter:  If given, only generate pages for this language code.
    """
    db_files = sorted(_glob.glob("dictionary/dictionary.*.db"))
    available_langs = [os.path.basename(p).split(".")[1] for p in db_files]
    if lang_filter:
        db_files = [p for p in db_files if f".{lang_filter}." in p]

    lang_data: dict = {}

    for db_path in db_files:
        lang = os.path.basename(db_path).split(".")[1]
        print(f"  Generating {lang.upper()} pages …")
        conn = _get_connection(db_path)
        try:
            entries = _get_all_entries(conn)
            books = _get_books(conn)
            sagas = _get_sagas(conn)
        finally:
            conn.close()

        lang_data[lang] = {
            "entry_count": len(entries),
            "book_count": len(books),
            "lang_name": lang.upper(),
        }

        # Group entries by letter
        by_letter: dict = defaultdict(list)
        for e in entries:
            by_letter[_entry_letter(e)].append(e)
        all_letters = sorted(by_letter.keys(), key=lambda x: (x == "Other", x))

        # Build global see-also (across all entries for this language)
        see_also_map = _build_see_also(entries)

        # --- lang index ---
        _write(
            os.path.join(output_dir, lang, "index.html"),
            _lang_index_page(lang, entries, books, sagas, all_letters, available_langs),
        )

        # --- letter pages ---
        for letter in all_letters:
            _write(
                os.path.join(output_dir, lang, f"{letter}.html"),
                _letter_page(
                    lang, letter, by_letter[letter],
                    all_letters, see_also_map, available_langs,
                ),
            )

        # --- book pages ---
        book_entries: dict = defaultdict(list)
        for e in entries:
            if e.get("book_id"):
                book_entries[e["book_id"]].append(e)

        for book in books:
            b_entries = book_entries.get(book["id"], [])
            if not b_entries:
                continue
            b_see_also = _build_see_also(b_entries)
            _write(
                os.path.join(output_dir, lang, "books", f"{book['global_id']}.html"),
                _book_page(lang, book, b_entries, b_see_also, available_langs),
            )

        # --- saga pages ---
        saga_entries: dict = defaultdict(list)
        for e in entries:
            if e.get("saga_id"):
                saga_entries[e["saga_id"]].append(e)

        for saga in sagas:
            s_entries = saga_entries.get(saga["id"], [])
            if not s_entries:
                continue
            s_see_also = _build_see_also(s_entries)
            _write(
                os.path.join(output_dir, lang, "sagas", f"{saga['global_id']}.html"),
                _saga_page(lang, saga, s_entries, s_see_also, available_langs),
            )

    # --- global index ---
    _write(
        os.path.join(output_dir, "index.html"),
        _index_page(lang_data, available_langs),
    )

    print(f"  ✅ Site written to: {output_dir}/")
