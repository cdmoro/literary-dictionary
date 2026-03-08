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
import json
import os
import sqlite3
from collections import defaultdict
from typing import Optional

from src.utils import escape_text_nodes, normalize_character

_ENCODING = "utf-8"

# ---------------------------------------------------------------------------
# CSS – embedded in every page
# ---------------------------------------------------------------------------

_CSS = """\
/* === Reset =============================================================== */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; font-size: 16px; }
body {
    font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.7;
    color: #2c2c2c;
    background: #f7f3ee;
    min-height: 100vh;
}
/* === Links ================================================================ */
a { color: #2c5282; text-decoration: none; }
a:hover { text-decoration: underline; }
/* === Site Header =========================================================== */
.site-header {
    background: #1d2d44;
    color: #e8dcc8;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 8px rgba(0,0,0,0.28);
}
.header-inner {
    max-width: 1100px;
    margin: 0 auto;
    padding: 0.7rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
}
.site-logo {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 1.15rem;
    font-weight: bold;
    color: #e8dcc8;
    text-decoration: none;
    white-space: nowrap;
    flex-shrink: 0;
}
.site-logo:hover { color: #fff; text-decoration: none; }
/* Language pills in header */
.header-langs { display: flex; gap: 0.3rem; flex-wrap: wrap; }
.header-langs a {
    padding: 0.18rem 0.65rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
    color: #a8b8cc;
    border: 1px solid #344e6a;
    text-decoration: none;
    letter-spacing: 0.04em;
    transition: all 0.15s;
}
.header-langs a:hover, .header-langs a.active {
    background: #e8dcc8;
    color: #1d2d44;
    border-color: #e8dcc8;
    text-decoration: none;
}
/* Search */
.search-wrap { position: relative; margin-left: auto; }
.search-icon {
    position: absolute;
    left: 0.65rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 0.82rem;
    pointer-events: none;
    opacity: 0.55;
}
.search-input {
    width: 210px;
    padding: 0.34rem 0.75rem 0.34rem 2rem;
    border-radius: 20px;
    border: 1px solid #344e6a;
    background: #263a55;
    color: #e8dcc8;
    font-size: 0.86rem;
    outline: none;
    transition: background 0.2s, width 0.2s, color 0.2s;
}
.search-input::placeholder { color: #7a90a8; }
.search-input:focus {
    background: #fff;
    color: #2c2c2c;
    border-color: #a08060;
    width: 270px;
}
.search-drop {
    position: absolute;
    top: calc(100% + 6px);
    right: 0;
    width: 340px;
    background: #fff;
    border: 1px solid #d5c9b0;
    border-radius: 10px;
    box-shadow: 0 8px 28px rgba(0,0,0,0.15);
    overflow: hidden;
    z-index: 200;
}
.sr-item {
    display: flex;
    align-items: baseline;
    gap: 0.45rem;
    padding: 0.55rem 1rem;
    border-bottom: 1px solid #f0ebe3;
    cursor: pointer;
    text-decoration: none;
    color: #2c2c2c;
    transition: background 0.1s;
}
.sr-item:last-child { border-bottom: none; }
.sr-item:hover, .sr-item.focused { background: #f7f3ee; text-decoration: none; color: #2c2c2c; }
.sr-name { font-weight: 700; font-size: 0.92rem; }
.sr-abbr { font-size: 0.72rem; color: #8a7a68; font-style: italic; }
.sr-origin { font-size: 0.78rem; color: #7a8898; margin-left: auto; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 120px; }
.sr-none { padding: 0.8rem 1rem; color: #888; font-size: 0.88rem; }
/* === Page Wrapper ========================================================= */
.page-wrap { max-width: 1100px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }
/* === Hero ================================================================= */
.hero {
    text-align: center;
    padding: 3.5rem 1rem 2.5rem;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 3rem;
    color: #1d2d44;
    line-height: 1.15;
    margin-bottom: 0.5rem;
}
.hero .tagline {
    font-size: 1.1rem;
    color: #7a6a55;
    font-style: italic;
    max-width: 520px;
    margin: 0 auto;
}
.hero-langs { display: flex; flex-wrap: wrap; justify-content: center; gap: 0.5rem; margin-top: 1.5rem; }
.hero-langs a {
    padding: 0.45rem 1.2rem;
    border-radius: 24px;
    border: 2px solid #1d2d44;
    font-weight: 700;
    font-size: 0.88rem;
    color: #1d2d44;
    letter-spacing: 0.06em;
    transition: all 0.15s;
}
.hero-langs a:hover { background: #1d2d44; color: #e8dcc8; text-decoration: none; }
/* === Headings ============================================================= */
h1 {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 2rem;
    color: #1d2d44;
    line-height: 1.2;
    margin-bottom: 0.25rem;
}
h2 {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 1.35rem;
    color: #2c3e50;
    margin: 2.5rem 0 0.75rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #d5c9b0;
}
.page-subtitle { color: #7a6a55; font-style: italic; font-size: 0.95rem; margin-bottom: 1.5rem; }
/* === Breadcrumb =========================================================== */
.breadcrumb {
    font-size: 0.83rem;
    color: #9a8a75;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.3rem;
}
.breadcrumb a { color: #5c7ab0; }
.breadcrumb a:hover { text-decoration: underline; }
.breadcrumb-sep { color: #bbb; }
/* === Stats ================================================================ */
.stats { display: flex; flex-wrap: wrap; gap: 0.75rem; margin: 1.5rem 0 2rem; }
.stat-box {
    background: #fff;
    border: 1px solid #d5c9b0;
    border-radius: 10px;
    padding: 0.9rem 1.5rem;
    min-width: 110px;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.stat-num {
    font-family: Georgia, serif;
    font-size: 2rem;
    font-weight: bold;
    color: #1d2d44;
    line-height: 1;
}
.stat-lbl { font-size: 0.75rem; color: #7a6a55; margin-top: 0.2rem; text-transform: uppercase; letter-spacing: 0.05em; }
/* === Letter Nav =========================================================== */
.letter-nav { display: flex; flex-wrap: wrap; gap: 0.3rem; margin: 1rem 0 1.5rem; }
.letter-nav a {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2.2rem;
    height: 2.2rem;
    border-radius: 6px;
    border: 1px solid #c8b99a;
    font-family: Georgia, serif;
    font-size: 1rem;
    font-weight: bold;
    color: #5c4a35;
    background: #fff;
    text-decoration: none;
    transition: all 0.15s;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}
.letter-nav a:hover, .letter-nav a.active {
    background: #1d2d44;
    color: #e8dcc8;
    border-color: #1d2d44;
    text-decoration: none;
}
/* === Cards Grid =========================================================== */
.cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 0.9rem;
    margin-top: 0.5rem;
}
.card {
    background: #fff;
    border: 1px solid #d5c9b0;
    border-radius: 10px;
    padding: 1rem 1.1rem 0.9rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    transition: box-shadow 0.2s, transform 0.15s;
    text-decoration: none;
    color: inherit;
    display: block;
}
.card:hover {
    box-shadow: 0 5px 16px rgba(0,0,0,0.13);
    transform: translateY(-2px);
    text-decoration: none;
}
.card-title {
    font-family: Georgia, serif;
    font-size: 1rem;
    font-weight: bold;
    color: #1d2d44;
    margin-bottom: 0.3rem;
    line-height: 1.3;
}
.card-author { font-size: 0.84rem; color: #5c4a35; }
.card-year { color: #9a8a75; font-size: 0.8rem; }
.card-saga { font-size: 0.8rem; color: #7a6a55; font-style: italic; margin-top: 0.2rem; }
/* === Entry Cards ========================================================== */
.letter-section-heading {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 1.5rem;
    font-weight: bold;
    color: #1d2d44;
    margin: 2.2rem 0 0.9rem;
    padding: 0.35rem 0 0.35rem 0.85rem;
    border-left: 4px solid #a08060;
    line-height: 1;
}
.entry {
    background: #fff;
    border: 1px solid #e8ddd0;
    border-radius: 8px;
    padding: 0.9rem 1.1rem 0.75rem;
    margin-bottom: 0.55rem;
    transition: box-shadow 0.15s, border-color 0.15s;
}
.entry:target { border-color: #a08060; box-shadow: 0 0 0 3px rgba(160,128,96,0.18); }
.entry:hover { box-shadow: 0 2px 10px rgba(160,128,96,0.15); }
.entry-head {
    display: flex;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-bottom: 0.35rem;
}
.entry-name {
    font-family: Georgia, serif;
    font-size: 1.06rem;
    font-weight: bold;
    color: #1d2d44;
}
.entry-badge {
    display: inline-block;
    padding: 0.08rem 0.42rem;
    border-radius: 4px;
    background: #e8f0df;
    color: #3a5a28;
    font-size: 0.7rem;
    font-style: italic;
    font-weight: 700;
    letter-spacing: 0.03em;
    border: 1px solid #c5d9b8;
    vertical-align: middle;
}
.entry-alias { font-size: 0.84rem; color: #7a6a55; font-style: italic; }
.entry-body { font-size: 0.94rem; line-height: 1.65; color: #3c3c3c; margin-bottom: 0.45rem; }
.entry-meta { display: flex; flex-wrap: wrap; gap: 0.6rem 1.5rem; font-size: 0.84rem; }
.entry-origin { color: #5c4a35; }
.entry-origin a { color: #5c7ab0; }
.entry-origin a:hover { text-decoration: underline; }
.entry-see-also { color: #5c4a35; }
.entry-see-also a { color: #5c7ab0; }
.entry-see-also a:hover { text-decoration: underline; }
/* === Back to top ========================================================= */
.back-top {
    display: inline-block;
    margin-top: 2rem;
    padding: 0.4rem 1rem;
    border: 1px solid #c8b99a;
    border-radius: 20px;
    font-size: 0.84rem;
    color: #5c4a35;
    text-decoration: none;
    transition: all 0.15s;
}
.back-top:hover { background: #1d2d44; color: #e8dcc8; border-color: #1d2d44; text-decoration: none; }
/* === Footer =============================================================== */
footer {
    margin-top: 4rem;
    padding: 1.5rem;
    border-top: 1px solid #d5c9b0;
    text-align: center;
    font-size: 0.8rem;
    color: #9a8a75;
}
footer a { color: #5c7ab0; }
/* === Responsive =========================================================== */
@media (max-width: 640px) {
    .header-inner { padding: 0.6rem 1rem; gap: 0.6rem; }
    .search-input { width: 150px; }
    .search-input:focus { width: 190px; }
    .search-drop { width: min(300px, 90vw); right: -0.5rem; }
    .page-wrap { padding: 1.5rem 1rem 3rem; }
    h1 { font-size: 1.65rem; }
    .hero h1 { font-size: 2rem; }
    .hero .tagline { font-size: 0.95rem; }
}
"""


# ---------------------------------------------------------------------------
# Search JS – inline in every page (no external deps)
# ---------------------------------------------------------------------------


def _search_js(entries: list, letter_prefix: str) -> str:
    """Build the inline search script for a page.

    ``entries``       – full entry list for the current language.
    ``letter_prefix`` – path prefix to letter pages from the current page.
                        Use ``""`` when the current page is at the language
                        level (lang index or letter pages, which live alongside
                        the letter HTML files).  Use ``"../"`` for nested pages
                        (books/, sagas/) that are one directory deeper.
    """
    data = []
    for e in entries:
        name = e.get("display_name") or e["name"]
        letter = _entry_letter(e)
        alias = e.get("alias") or ""
        abbr = e.get("category_abbr") or ""
        origin = e.get("book_name") or e.get("saga_name") or ""
        href = f"{letter_prefix}{letter}.html#entry-{e['id']}"
        # Pre-lowercase search fields to avoid repeated toLowerCase() calls in JS.
        data.append({
            "n": name,
            "nl": name.lower(),
            "a": alias,
            "al": alias.lower(),
            "ab": abbr,
            "o": origin,
            "h": href,
        })

    data_json = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    # Double braces escape literal braces inside .format()
    return (
        "<script>(function(){{"
        "var D={data};"
        "var inp=document.getElementById('site-search');"
        "var drop=document.getElementById('search-drop');"
        "if(!inp)return;"
        "var t,cur=-1;"
        "function esc(s){{return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}}"
        "function run(){{"
        "var q=inp.value.trim().toLowerCase();"
        "if(q.length<2){{drop.hidden=true;return;}}"
        "var res=D.filter(function(e){{return e.nl.indexOf(q)>=0"
        "||(e.al&&e.al.indexOf(q)>=0);}}).slice(0,8);"
        "if(!res.length){{drop.innerHTML='<div class=\"sr-none\">No results found</div>';}}"
        "else{{drop.innerHTML=res.map(function(e){{"
        "return '<a href=\"'+e.h+'\" class=\"sr-item\">'+"
        "'<span class=\"sr-name\">'+esc(e.n)+'</span>'+"
        "(e.ab?'<span class=\"sr-abbr\">'+esc(e.ab)+'</span>':'')+"
        "(e.o?'<span class=\"sr-origin\">'+esc(e.o)+'</span>':'')+'</a>';"
        "}}).join('');}}"
        "drop.hidden=false;cur=-1;"
        "}}"
        "inp.addEventListener('input',function(){{clearTimeout(t);t=setTimeout(run,120);}});"
        "inp.addEventListener('keydown',function(e){{"
        "var its=drop.querySelectorAll('.sr-item');"
        "if(e.key==='ArrowDown'){{e.preventDefault();cur=Math.min(cur+1,its.length-1);}}"
        "else if(e.key==='ArrowUp'){{e.preventDefault();cur=Math.max(cur-1,0);}}"
        "else if(e.key==='Enter'&&cur>=0&&its[cur]){{window.location.href=its[cur].href;return;}}"
        "else if(e.key==='Escape'){{drop.hidden=true;return;}}"
        "its.forEach(function(el,i){{el.classList.toggle('focused',i===cur);}});"
        "if(cur>=0&&its[cur])its[cur].scrollIntoView({{block:'nearest'}});"
        "}});"
        "document.addEventListener('pointerdown',function(e){{"
        "if(!inp.contains(e.target)&&!drop.contains(e.target))drop.hidden=true;"
        "}});"
        "}})();</script>"
    ).format(data=data_json)


# ---------------------------------------------------------------------------
# HTML page skeleton
# ---------------------------------------------------------------------------


def _header(
    root_prefix: str,
    available_langs: list,
    active_lang: Optional[str],
) -> str:
    lang_links = []
    for lc in available_langs:
        active = ' class="active"' if lc == active_lang else ""
        lang_links.append(
            f'<a href="{root_prefix}{lc}/index.html"{active}>{lc.upper()}</a>'
        )
    lang_nav = '<div class="header-langs">' + "".join(lang_links) + "</div>"

    return f"""\
<header class="site-header">
  <div class="header-inner">
    <a class="site-logo" href="{root_prefix}index.html">&#128218; Literary Dictionary</a>
    {lang_nav}
    <div class="search-wrap">
      <span class="search-icon">&#128269;</span>
      <input id="site-search" class="search-input" type="search"
             placeholder="Search entries\u2026" autocomplete="off" aria-label="Search entries"/>
      <div id="search-drop" class="search-drop" hidden></div>
    </div>
  </div>
</header>"""


def _page(
    title: str,
    body: str,
    root_prefix: str,
    available_langs: list,
    active_lang: Optional[str],
    entries_for_search: Optional[list] = None,
    search_letter_prefix: str = "",
) -> str:
    search_script = ""
    if entries_for_search is not None:
        search_script = _search_js(entries_for_search, search_letter_prefix)

    return f"""\
<!DOCTYPE html>
<html lang="{active_lang or 'en'}">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title>{html.escape(title)} \u2013 Literary Dictionary</title>
    <style>{_CSS}</style>
</head>
<body>
{_header(root_prefix, available_langs, active_lang)}
<div class="page-wrap">
{body}
</div>
<footer>
  <p>Literary Dictionary &mdash; <a href="{root_prefix}index.html">Home</a></p>
</footer>
{search_script}
</body>
</html>"""


def _letter_nav_html(all_letters: list, active: Optional[str] = None) -> str:
    links = []
    for ltr in all_letters:
        disp = ltr if ltr != "Other" else "#"
        active_class = ' class="active"' if ltr == active else ""
        links.append(f'<a href="{ltr}.html"{active_class}>{disp}</a>')
    return '<div class="letter-nav">' + "".join(links) + "</div>"


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
# Entry HTML fragment
# ---------------------------------------------------------------------------


def _entry_html(entry: dict, see_also: list, letter_link_prefix: str = "") -> str:
    """Render a single entry as a styled card HTML fragment."""
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

    # --- head line ---
    out += '  <div class="entry-head">\n'
    out += f'    <span class="entry-name">{html.escape(name)}</span>\n'
    if abbr:
        out += f'    <span class="entry-badge">{html.escape(abbr)}</span>\n'
    if alias:
        aliases = [a.strip() for a in alias.split(";") if a.strip()]
        if aliases:
            out += (
                f'    <span class="entry-alias">'
                f'{html.escape(", ".join(aliases))}</span>\n'
            )
    out += "  </div>\n"

    # --- body ---
    if desc:
        out += f'  <p class="entry-body">{escape_text_nodes(desc)}</p>\n'

    # --- meta (origin + see also) ---
    meta_parts = []

    if author_name:
        if book_name and saga_name:
            origin_text = (
                f'<em><a href="{letter_link_prefix}books/{html.escape(book_gid)}.html">'
                f"{html.escape(book_name)}</a></em>"
                f" (part of <em>{html.escape(saga_name)}</em>),"
                f" {html.escape(author_name)}"
            )
        elif book_name:
            origin_text = (
                f'<em><a href="{letter_link_prefix}books/{html.escape(book_gid)}.html">'
                f"{html.escape(book_name)}</a></em>,"
                f" {html.escape(author_name)}"
            )
        elif saga_name:
            origin_text = (
                f'<em><a href="{letter_link_prefix}sagas/{html.escape(saga_gid)}.html">'
                f"{html.escape(saga_name)}</a></em>,"
                f" {html.escape(author_name)}"
            )
        else:
            origin_text = html.escape(author_name)
        meta_parts.append(
            f'<span class="entry-origin">&#128218; {origin_text}</span>'
        )

    if see_also:
        links = [
            f'<a href="{letter_link_prefix}{tgt_letter}.html#entry-{p["id"]}">'
            f'{html.escape(p.get("display_name") or p["name"])}</a>'
            for p, tgt_letter in see_also
        ]
        meta_parts.append(
            f'<span class="entry-see-also">'
            f"<strong>See also:</strong> {', '.join(links)}</span>"
        )

    if meta_parts:
        out += '  <div class="entry-meta">\n'
        for part in meta_parts:
            out += f"    {part}\n"
        out += "  </div>\n"

    out += "</div>\n"
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
    all_entries: list,
) -> str:
    display = letter if letter != "Other" else "Symbols and Numbers"
    entries_html = "".join(
        _entry_html(e, see_also_map.get(e["id"], []))
        for e in entries
    )

    breadcrumb = (
        f'<nav class="breadcrumb">'
        f'<a href="../index.html">Home</a>'
        f'<span class="breadcrumb-sep">&rsaquo;</span>'
        f'<a href="index.html">{lang.upper()}</a>'
        f'<span class="breadcrumb-sep">&rsaquo;</span>'
        f'<span>{html.escape(display)}</span>'
        f"</nav>"
    )

    body = f"""\
{breadcrumb}
<h1>{html.escape(display)}</h1>
<p class="page-subtitle">{lang.upper()} edition</p>
{_letter_nav_html(all_letters, active=letter)}
<section>
{entries_html}
</section>
<a class="back-top" href="#">&#8593; Back to top</a>"""

    return _page(
        f"{display} \u2013 {lang.upper()}",
        body,
        root_prefix="../",
        available_langs=available_langs,
        active_lang=lang,
        entries_for_search=all_entries,
        search_letter_prefix="",
    )


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

    stats = f"""\
<div class="stats">
  <div class="stat-box"><div class="stat-num">{entry_count}</div><div class="stat-lbl">Entries</div></div>
  <div class="stat-box"><div class="stat-num">{book_count}</div><div class="stat-lbl">Books</div></div>
  <div class="stat-box"><div class="stat-num">{saga_count}</div><div class="stat-lbl">Series</div></div>
</div>"""

    books_html = '<div class="cards-grid">'
    for book in books:
        year = (
            f' <span class="card-year">({book["publication_year"]})</span>'
            if book.get("publication_year") else ""
        )
        saga_tag = (
            f'<div class="card-saga">{html.escape(book["saga_name"])}</div>'
            if book.get("saga_name") else ""
        )
        books_html += (
            f'<a class="card" href="books/{html.escape(book["global_id"])}.html">'
            f'<div class="card-title">{html.escape(book["name"])}</div>'
            f'<div class="card-author">{html.escape(book["author_name"])}{year}</div>'
            f"{saga_tag}"
            f"</a>"
        )
    books_html += "</div>"

    sagas_html = '<div class="cards-grid">'
    for saga in sagas:
        sagas_html += (
            f'<a class="card" href="sagas/{html.escape(saga["global_id"])}.html">'
            f'<div class="card-title">{html.escape(saga["name"])}</div>'
            f'<div class="card-author">{html.escape(saga["author_name"])}</div>'
            f"</a>"
        )
    sagas_html += "</div>"

    breadcrumb = (
        f'<nav class="breadcrumb">'
        f'<a href="../index.html">Home</a>'
        f'<span class="breadcrumb-sep">&rsaquo;</span>'
        f'<span>{lang.upper()}</span>'
        f"</nav>"
    )

    body = f"""\
{breadcrumb}
<h1>Literary Dictionary</h1>
<p class="page-subtitle">{lang.upper()} edition</p>
{stats}
<h2>Browse by letter</h2>
{_letter_nav_html(all_letters)}
<h2>Books</h2>
{books_html}
<h2>Series</h2>
{sagas_html}"""

    return _page(
        f"Literary Dictionary \u2013 {lang.upper()}",
        body,
        root_prefix="../",
        available_langs=available_langs,
        active_lang=lang,
        entries_for_search=entries,
        search_letter_prefix="",
    )


def _book_page(
    lang: str,
    book: dict,
    entries: list,
    see_also_map: dict,
    available_langs: list,
    all_lang_entries: list,
) -> str:
    title = book["name"]
    author = book["author_name"]
    year = f" ({book['publication_year']})" if book.get("publication_year") else ""
    saga_note = ""
    if book.get("saga_name"):
        saga_gid = book.get("saga_gid", "")
        saga_note = (
            f'<p class="page-subtitle">Part of: '
            f'<a href="../sagas/{html.escape(saga_gid)}.html">'
            f"{html.escape(book['saga_name'])}</a></p>"
        )

    entries_html = "".join(
        _entry_html(e, see_also_map.get(e["id"], []), letter_link_prefix="../")
        for e in entries
    )

    breadcrumb = (
        f'<nav class="breadcrumb">'
        f'<a href="../../index.html">Home</a>'
        f'<span class="breadcrumb-sep">&rsaquo;</span>'
        f'<a href="../index.html">{lang.upper()}</a>'
        f'<span class="breadcrumb-sep">&rsaquo;</span>'
        f'<span>{html.escape(title)}</span>'
        f"</nav>"
    )

    body = f"""\
{breadcrumb}
<h1>{html.escape(title)}</h1>
<p class="page-subtitle">{html.escape(author)}{html.escape(year)}</p>
{saga_note}
<section>
{entries_html}
</section>
<a class="back-top" href="#">&#8593; Back to top</a>"""

    return _page(
        f"{title} \u2013 {lang.upper()}",
        body,
        root_prefix="../../",
        available_langs=available_langs,
        active_lang=lang,
        entries_for_search=all_lang_entries,
        search_letter_prefix="../",
    )


def _saga_page(
    lang: str,
    saga: dict,
    entries: list,
    see_also_map: dict,
    available_langs: list,
    all_lang_entries: list,
) -> str:
    title = saga["name"]
    author = saga["author_name"]

    entries_html = "".join(
        _entry_html(e, see_also_map.get(e["id"], []), letter_link_prefix="../")
        for e in entries
    )

    breadcrumb = (
        f'<nav class="breadcrumb">'
        f'<a href="../../index.html">Home</a>'
        f'<span class="breadcrumb-sep">&rsaquo;</span>'
        f'<a href="../index.html">{lang.upper()}</a>'
        f'<span class="breadcrumb-sep">&rsaquo;</span>'
        f'<span>{html.escape(title)}</span>'
        f"</nav>"
    )

    body = f"""\
{breadcrumb}
<h1>{html.escape(title)}</h1>
<p class="page-subtitle">{html.escape(author)}</p>
<section>
{entries_html}
</section>
<a class="back-top" href="#">&#8593; Back to top</a>"""

    return _page(
        f"{title} \u2013 {lang.upper()}",
        body,
        root_prefix="../../",
        available_langs=available_langs,
        active_lang=lang,
        entries_for_search=all_lang_entries,
        search_letter_prefix="../",
    )


def _index_page(lang_data: dict, available_langs: list) -> str:
    """Global landing page with per-language stats."""
    lang_cards = ""
    for lc in available_langs:
        data = lang_data.get(lc, {})
        entry_count = data.get("entry_count", 0)
        book_count = data.get("book_count", 0)
        lang_name = data.get("lang_name", lc.upper())
        lang_cards += (
            f'<a class="card" href="{lc}/index.html">'
            f'<div class="card-title">{html.escape(lang_name)}</div>'
            f'<div class="card-author">{entry_count} entries &middot; {book_count} books</div>'
            f"</a>"
        )

    hero_lang_links = "".join(
        f'<a href="{lc}/index.html">{lc.upper()}</a>' for lc in available_langs
    )

    body = f"""\
<div class="hero">
    <h1>Literary Dictionary</h1>
    <p class="tagline">Characters, places, and concepts from world literature</p>
    <div class="hero-langs">{hero_lang_links}</div>
</div>
<h2>Available editions</h2>
<div class="cards-grid">{lang_cards}</div>"""

    return _page(
        "Literary Dictionary",
        body,
        root_prefix="",
        available_langs=available_langs,
        active_lang=None,
        entries_for_search=None,
    )


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
                    all_entries=entries,
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
                _book_page(lang, book, b_entries, b_see_also, available_langs,
                           all_lang_entries=entries),
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
                _saga_page(lang, saga, s_entries, s_see_also, available_langs,
                           all_lang_entries=entries),
            )

    # --- global index ---
    _write(
        os.path.join(output_dir, "index.html"),
        _index_page(lang_data, available_langs),
    )

    print(f"  ✅ Site written to: {output_dir}/")
