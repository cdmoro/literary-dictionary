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

_GITHUB_REPO = "https://github.com/cdmoro/literary-dictionary"

# Full language names + flag emoji for each supported locale
_LANG_META: dict = {
    "en": {"name": "English",    "emoji": "\U0001f1ec\U0001f1e7"},
    "es": {"name": "Espa\u00f1ol",  "emoji": "\U0001f1ea\U0001f1f8"},
    "fr": {"name": "Fran\u00e7ais", "emoji": "\U0001f1eb\U0001f1f7"},
    "it": {"name": "Italiano",   "emoji": "\U0001f1ee\U0001f1f9"},
    "pt": {"name": "Portugu\u00eas", "emoji": "\U0001f1f5\U0001f1f9"},
}

# ---------------------------------------------------------------------------
# CSS – embedded in every page (uses CSS custom properties for theming)
# ---------------------------------------------------------------------------

_CSS = """\
/* === Reset =============================================================== */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; font-size: 16px; }

/* === CSS custom properties (light theme defaults) ======================== */
:root {
    --bg: #f7f3ee;
    --surface: #fff;
    --surface-border: #d5c9b0;
    --text: #2c2c2c;
    --text-muted: #7a6a55;
    --text-subtle: #9a8a75;
    --link: #2c5282;
    --header-bg: #1d2d44;
    --header-text: #e8dcc8;
    --header-link: #a8b8cc;
    --header-link-border: #344e6a;
    --header-link-active-bg: #e8dcc8;
    --header-link-active-text: #1d2d44;
    --search-bg: #263a55;
    --search-text: #e8dcc8;
    --search-focus-bg: #fff;
    --search-focus-text: #2c2c2c;
    --accent: #a08060;
    --letter-nav-border: #c8b99a;
    --letter-nav-text: #5c4a35;
    --entry-border: #e8ddd0;
    --badge-bg: #e8f0df;
    --badge-text: #3a5a28;
    --badge-border: #c5d9b8;
    --stat-num: #1d2d44;
    --card-title: #1d2d44;
    --card-author: #5c4a35;
    --breadcrumb-link: #5c7ab0;
    --h1: #1d2d44;
    --h2: #2c3e50;
    --footer-text: #9a8a75;
}
/* === Dark theme (auto via media query) =================================== */
@media (prefers-color-scheme: dark) {
    html:not([data-theme="light"]) {
        --bg: #12192a; --surface: #1a2540; --surface-border: #273b56;
        --text: #ddd6c8; --text-muted: #a8987a; --text-subtle: #7a6a55;
        --link: #7caaee; --header-bg: #0c1624; --header-text: #e8dcc8;
        --header-link: #7a90a8; --header-link-border: #1e3250;
        --header-link-active-bg: #e8dcc8; --header-link-active-text: #0c1624;
        --search-bg: #162030; --search-text: #c8d8e8;
        --search-focus-bg: #1a2540; --search-focus-text: #ddd6c8;
        --accent: #c09870; --letter-nav-border: #3a5070; --letter-nav-text: #a08060;
        --entry-border: #273b56; --badge-bg: #1a3020; --badge-text: #88c870;
        --badge-border: #2a5038; --stat-num: #8ab4e8;
        --card-title: #a8c8f0; --card-author: #a08060;
        --breadcrumb-link: #7caaee; --h1: #c8d8f0; --h2: #a0b8d8;
        --footer-text: #6a5a48;
    }
}
/* === Dark theme (explicit) =============================================== */
html[data-theme="dark"] {
    --bg: #12192a; --surface: #1a2540; --surface-border: #273b56;
    --text: #ddd6c8; --text-muted: #a8987a; --text-subtle: #7a6a55;
    --link: #7caaee; --header-bg: #0c1624; --header-text: #e8dcc8;
    --header-link: #7a90a8; --header-link-border: #1e3250;
    --header-link-active-bg: #e8dcc8; --header-link-active-text: #0c1624;
    --search-bg: #162030; --search-text: #c8d8e8;
    --search-focus-bg: #1a2540; --search-focus-text: #ddd6c8;
    --accent: #c09870; --letter-nav-border: #3a5070; --letter-nav-text: #a08060;
    --entry-border: #273b56; --badge-bg: #1a3020; --badge-text: #88c870;
    --badge-border: #2a5038; --stat-num: #8ab4e8;
    --card-title: #a8c8f0; --card-author: #a08060;
    --breadcrumb-link: #7caaee; --h1: #c8d8f0; --h2: #a0b8d8;
    --footer-text: #6a5a48;
}
body {
    font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.7;
    color: var(--text);
    background: var(--bg);
    min-height: 100vh;
    transition: background 0.25s, color 0.25s;
}
a { color: var(--link); text-decoration: none; }
a:hover { text-decoration: underline; }
/* === Site Header =========================================================== */
.site-header {
    background: var(--header-bg);
    color: var(--header-text);
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 8px rgba(0,0,0,0.35);
    transition: background 0.25s;
}
.header-inner {
    max-width: 1100px;
    margin: 0 auto;
    padding: 0.65rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
}
.site-logo {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 1.1rem;
    font-weight: bold;
    color: var(--header-text);
    text-decoration: none;
    white-space: nowrap;
    flex-shrink: 0;
}
.site-logo:hover { color: #fff; text-decoration: none; }
/* Language pills */
.header-langs { display: flex; gap: 0.28rem; flex-wrap: wrap; }
.header-langs a {
    padding: 0.15rem 0.55rem;
    border-radius: 20px;
    font-size: 0.76rem;
    font-weight: 700;
    color: var(--header-link);
    border: 1px solid var(--header-link-border);
    text-decoration: none;
    letter-spacing: 0.04em;
    transition: all 0.15s;
}
.header-langs a:hover, .header-langs a.active {
    background: var(--header-link-active-bg);
    color: var(--header-link-active-text);
    border-color: var(--header-link-active-bg);
    text-decoration: none;
}
/* Theme toggle */
.theme-toggle {
    display: flex;
    gap: 0.15rem;
    background: rgba(0,0,0,0.2);
    border-radius: 20px;
    padding: 0.15rem 0.3rem;
    border: 1px solid var(--header-link-border);
}
.theme-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.08rem 0.38rem;
    border-radius: 14px;
    font-size: 0.72rem;
    color: var(--header-link);
    transition: all 0.15s;
    font-family: inherit;
    font-weight: 600;
    letter-spacing: 0.03em;
}
.theme-btn:hover { color: var(--header-text); }
.theme-btn.active {
    background: var(--header-link-active-bg);
    color: var(--header-link-active-text);
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
    width: 200px;
    padding: 0.32rem 0.7rem 0.32rem 2rem;
    border-radius: 20px;
    border: 1px solid var(--header-link-border);
    background: var(--search-bg);
    color: var(--search-text);
    font-size: 0.86rem;
    outline: none;
    transition: background 0.2s, width 0.2s, color 0.2s;
}
.search-input::placeholder { color: #7a90a8; }
.search-input:focus {
    background: var(--search-focus-bg);
    color: var(--search-focus-text);
    border-color: var(--accent);
    width: 260px;
}
.search-drop {
    position: absolute;
    top: calc(100% + 6px);
    right: 0;
    width: 360px;
    background: var(--surface);
    border: 1px solid var(--surface-border);
    border-radius: 10px;
    box-shadow: 0 8px 28px rgba(0,0,0,0.22);
    overflow: hidden;
    z-index: 200;
}
.sr-item {
    display: flex;
    align-items: baseline;
    gap: 0.45rem;
    padding: 0.52rem 1rem;
    border-bottom: 1px solid var(--surface-border);
    cursor: pointer;
    text-decoration: none;
    color: var(--text);
    transition: background 0.1s;
}
.sr-item:last-child { border-bottom: none; }
.sr-item:hover, .sr-item.focused { background: var(--bg); text-decoration: none; color: var(--text); }
.sr-name { font-weight: 700; font-size: 0.9rem; }
.sr-abbr { font-size: 0.7rem; color: var(--text-muted); font-style: italic; }
.sr-lang { font-size: 0.7rem; color: var(--text-subtle); opacity: 0.7; }
.sr-origin { font-size: 0.76rem; color: var(--text-subtle); margin-left: auto; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 130px; }
.sr-none { padding: 0.8rem 1rem; color: var(--text-subtle); font-size: 0.88rem; }
/* === Page Wrapper ========================================================= */
.page-wrap { max-width: 1100px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }
/* === Hero ================================================================= */
.hero {
    text-align: center;
    padding: 3.2rem 1rem 2.2rem;
    margin-bottom: 0.5rem;
}
.hero h1 {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 2.8rem;
    color: var(--h1);
    line-height: 1.15;
    margin-bottom: 0.5rem;
}
.hero .tagline {
    font-size: 1.05rem;
    color: var(--text-muted);
    font-style: italic;
    max-width: 520px;
    margin: 0 auto;
}
/* === Headings ============================================================= */
h1 {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 2rem;
    color: var(--h1);
    line-height: 1.2;
    margin-bottom: 0.25rem;
}
h2 {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 1.3rem;
    color: var(--h2);
    margin: 2.2rem 0 0.75rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--surface-border);
}
.page-subtitle { color: var(--text-muted); font-style: italic; font-size: 0.95rem; margin-bottom: 1.5rem; }
/* === Breadcrumb =========================================================== */
.breadcrumb {
    font-size: 0.83rem;
    color: var(--text-subtle);
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.3rem;
}
.breadcrumb a { color: var(--breadcrumb-link); }
.breadcrumb a:hover { text-decoration: underline; }
.breadcrumb-sep { color: #bbb; }
/* === Stats ================================================================ */
.stats { display: flex; flex-wrap: wrap; gap: 0.75rem; margin: 1.5rem 0 2rem; }
.stat-box {
    background: var(--surface);
    border: 1px solid var(--surface-border);
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
    color: var(--stat-num);
    line-height: 1;
}
.stat-lbl { font-size: 0.75rem; color: var(--text-muted); margin-top: 0.2rem; text-transform: uppercase; letter-spacing: 0.05em; }
/* === Letter Nav =========================================================== */
.letter-nav { display: flex; flex-wrap: wrap; gap: 0.3rem; margin: 1rem 0 1.5rem; }
.letter-nav a {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2.2rem;
    height: 2.2rem;
    border-radius: 6px;
    border: 1px solid var(--letter-nav-border);
    font-family: Georgia, serif;
    font-size: 1rem;
    font-weight: bold;
    color: var(--letter-nav-text);
    background: var(--surface);
    text-decoration: none;
    transition: all 0.15s;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}
.letter-nav a:hover, .letter-nav a.active {
    background: var(--header-bg);
    color: var(--header-text);
    border-color: var(--header-bg);
    text-decoration: none;
}
/* === Cards Grid =========================================================== */
.cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 0.9rem;
    margin-top: 0.5rem;
}
.card {
    background: var(--surface);
    border: 1px solid var(--surface-border);
    border-radius: 10px;
    padding: 1rem 1.1rem 0.9rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    transition: box-shadow 0.2s, transform 0.15s, background 0.25s;
    text-decoration: none;
    color: inherit;
    display: block;
}
.card:hover { box-shadow: 0 5px 16px rgba(0,0,0,0.15); transform: translateY(-2px); text-decoration: none; }
.card-emoji { font-size: 1.6rem; margin-bottom: 0.4rem; }
.card-title { font-family: Georgia, serif; font-size: 1rem; font-weight: bold; color: var(--card-title); margin-bottom: 0.2rem; line-height: 1.3; }
.card-author { font-size: 0.84rem; color: var(--card-author); }
.card-year { color: var(--text-subtle); font-size: 0.8rem; }
.card-saga { font-size: 0.8rem; color: var(--text-muted); font-style: italic; margin-top: 0.2rem; }
/* === Entry Cards ========================================================== */
.entry {
    background: var(--surface);
    border: 1px solid var(--entry-border);
    border-radius: 8px;
    padding: 0.9rem 1.1rem 0.75rem;
    margin-bottom: 0.55rem;
    transition: box-shadow 0.15s, border-color 0.15s, background 0.25s;
}
.entry:target { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(160,128,96,0.2); }
.entry:hover { box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.entry-head { display: flex; align-items: baseline; flex-wrap: wrap; gap: 0.45rem; margin-bottom: 0.35rem; }
.entry-name { font-family: Georgia, serif; font-size: 1.06rem; font-weight: bold; color: var(--h1); }
.entry-badge {
    display: inline-block;
    padding: 0.08rem 0.42rem;
    border-radius: 4px;
    background: var(--badge-bg);
    color: var(--badge-text);
    font-size: 0.7rem;
    font-style: italic;
    font-weight: 700;
    letter-spacing: 0.03em;
    border: 1px solid var(--badge-border);
    vertical-align: middle;
}
.entry-alias { font-size: 0.84rem; color: var(--text-muted); font-style: italic; }
.entry-body { font-size: 0.94rem; line-height: 1.65; color: var(--text); margin-bottom: 0.45rem; }
.entry-meta { display: flex; flex-wrap: wrap; gap: 0.6rem 1.5rem; font-size: 0.84rem; }
.entry-origin { color: var(--card-author); }
.entry-origin a { color: var(--breadcrumb-link); }
.entry-origin a:hover { text-decoration: underline; }
.entry-see-also { color: var(--card-author); }
.entry-see-also a { color: var(--breadcrumb-link); }
.entry-see-also a:hover { text-decoration: underline; }
/* === Feedback bar ========================================================= */
.feedback-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem 1.2rem;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px dashed var(--surface-border);
    font-size: 0.82rem;
}
.feedback-bar a { color: var(--text-subtle); }
.feedback-bar a:hover { color: var(--link); text-decoration: underline; }
/* === Back to top ========================================================= */
.back-top {
    display: inline-block;
    margin-top: 1.5rem;
    padding: 0.4rem 1rem;
    border: 1px solid var(--letter-nav-border);
    border-radius: 20px;
    font-size: 0.84rem;
    color: var(--letter-nav-text);
    text-decoration: none;
    transition: all 0.15s;
}
.back-top:hover { background: var(--header-bg); color: var(--header-text); border-color: var(--header-bg); text-decoration: none; }
/* === Footer =============================================================== */
footer {
    margin-top: 4rem;
    padding: 1.5rem;
    border-top: 1px solid var(--surface-border);
    text-align: center;
    font-size: 0.8rem;
    color: var(--footer-text);
    transition: color 0.25s;
}
footer a { color: var(--breadcrumb-link); }
footer .footer-sep { margin: 0 0.4rem; opacity: 0.4; }
/* === Responsive =========================================================== */
@media (max-width: 640px) {
    .header-inner { padding: 0.55rem 1rem; gap: 0.5rem; }
    .search-input { width: 130px; }
    .search-input:focus { width: 175px; }
    .search-drop { width: min(320px, 90vw); right: -0.5rem; }
    .page-wrap { padding: 1.5rem 1rem 3rem; }
    h1 { font-size: 1.6rem; }
    .hero h1 { font-size: 2rem; }
}
"""


# ---------------------------------------------------------------------------
# Theme init script – placed in <head> to prevent flash of wrong colour
# ---------------------------------------------------------------------------

_THEME_INIT_JS = (
    "<script>(function(){"
    "var t=localStorage.getItem('ld-theme');"
    "if(t==='dark')document.documentElement.setAttribute('data-theme','dark');"
    "else if(t==='light')document.documentElement.setAttribute('data-theme','light');"
    "})();</script>"
)


# ---------------------------------------------------------------------------
# Search JS – inline in every page (no external deps)
# ---------------------------------------------------------------------------


def _search_js(entries: list, letter_prefix: str) -> str:
    """Build the inline search script for a page.

    ``entries``       – entry list (may span multiple languages when each entry
                        has a ``_search_href`` key with a pre-built full path
                        and a ``_search_lang`` key with the language code).
    ``letter_prefix`` – path prefix to letter pages from the current page.
                        Use ``""`` for lang-index/letter pages; ``"../"`` for
                        nested book/saga pages.  Ignored when an entry already
                        has a ``_search_href`` key.
    """
    data = []
    for e in entries:
        name = e.get("display_name") or e["name"]
        letter = _entry_letter(e)
        alias = e.get("alias") or ""
        abbr = e.get("category_abbr") or ""
        origin = e.get("book_name") or e.get("saga_name") or ""
        # Pre-built href wins (used for global home-page search)
        href = e.get("_search_href") or f"{letter_prefix}{letter}.html#entry-{e['id']}"
        lang_tag = e.get("_search_lang", "")
        # Pre-lowercase search fields to avoid repeated toLowerCase() calls in JS.
        data.append({
            "n": name,
            "nl": name.lower(),
            "a": alias,
            "al": alias.lower(),
            "ab": abbr,
            "o": origin,
            "lg": lang_tag,
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
        "||(e.al&&e.al.indexOf(q)>=0);}}).slice(0,10);"
        "if(!res.length){{drop.innerHTML='<div class=\"sr-none\">No results found</div>';}}"
        "else{{drop.innerHTML=res.map(function(e){{"
        "return '<a href=\"'+e.h+'\" class=\"sr-item\">'+"
        "'<span class=\"sr-name\">'+esc(e.n)+'</span>'+"
        "(e.ab?'<span class=\"sr-abbr\">'+esc(e.ab)+'</span>':'')+"
        "(e.lg?'<span class=\"sr-lang\">'+esc(e.lg.toUpperCase())+'</span>':'')+"
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

    theme_toggle = (
        '<div class="theme-toggle">'
        '<button class="theme-btn" data-t="auto" title="Auto theme">Auto</button>'
        '<button class="theme-btn" data-t="light" title="Light theme">\u2600\ufe0f</button>'
        '<button class="theme-btn" data-t="dark" title="Dark theme">\U0001f319</button>'
        "</div>"
    )

    return (
        '<header class="site-header">\n'
        '  <div class="header-inner">\n'
        f'    <a class="site-logo" href="{root_prefix}index.html">&#128218; Literary Dictionary</a>\n'
        f"    {lang_nav}\n"
        f"    {theme_toggle}\n"
        '    <div class="search-wrap">\n'
        '      <span class="search-icon">&#128269;</span>\n'
        '      <input id="site-search" class="search-input" type="search"\n'
        '             placeholder="Search entries\u2026" autocomplete="off" aria-label="Search entries"/>\n'
        '      <div id="search-drop" class="search-drop" hidden></div>\n'
        "    </div>\n"
        "  </div>\n"
        "</header>"
    )


def _footer(root_prefix: str) -> str:
    """Render the site footer with repo link, author credit, and feedback links."""
    report_url = (
        f"{_GITHUB_REPO}/issues/new?title=Error+report&labels=bug"
        "&body=Describe+the+error+here%3A%0A%0APage%3A+"
    )
    suggest_book_url = (
        f"{_GITHUB_REPO}/issues/new?title=Book+suggestion%3A+&labels=suggestion"
    )
    suggest_saga_url = (
        f"{_GITHUB_REPO}/issues/new?title=Saga+suggestion%3A+&labels=suggestion"
    )
    sep = '<span class="footer-sep">&middot;</span>'
    return (
        "<footer>\n"
        "  <p>\n"
        f'    <a href="{root_prefix}index.html">Home</a>{sep}'
        f'<a href="{_GITHUB_REPO}" target="_blank" rel="noopener">GitHub</a>{sep}'
        f'<a href="{report_url}" target="_blank" rel="noopener">Report an error</a>{sep}'
        f'<a href="{suggest_book_url}" target="_blank" rel="noopener">Suggest a book</a>{sep}'
        f'<a href="{suggest_saga_url}" target="_blank" rel="noopener">Suggest a saga</a>\n'
        "  </p>\n"
        '  <p style="margin-top:0.4rem;">Made by '
        f'<a href="https://github.com/cdmoro" target="_blank" rel="noopener">Carlos Bonadeo</a>'
        "</p>\n"
        "</footer>"
    )


def _ui_js(active_lang: Optional[str]) -> str:
    """Return the theme-toggle initialisation and language-preference script."""
    lang_pref = (
        f"localStorage.setItem('ld-lang','{active_lang}');"
        if active_lang else ""
    )
    return (
        "<script>(function(){{"
        "var cur=localStorage.getItem('ld-theme')||'auto';"
        "function applyTheme(t){{"
        "if(t==='dark')document.documentElement.setAttribute('data-theme','dark');"
        "else if(t==='light')document.documentElement.setAttribute('data-theme','light');"
        "else document.documentElement.removeAttribute('data-theme');"
        "document.querySelectorAll('.theme-btn').forEach(function(b){{"
        "b.classList.toggle('active',b.dataset.t===t);}});"
        "localStorage.setItem('ld-theme',t);cur=t;"
        "}}"
        "document.querySelectorAll('.theme-btn').forEach(function(b){{"
        "b.addEventListener('click',function(){{applyTheme(b.dataset.t);}});"
        "}});"
        f"applyTheme(cur);{lang_pref}"
        "}})();</script>"
    )


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

    return (
        "<!DOCTYPE html>\n"
        f'<html lang="{active_lang or "en"}">\n'
        "<head>\n"
        '    <meta charset="utf-8"/>\n'
        '    <meta name="viewport" content="width=device-width, initial-scale=1"/>\n'
        f'    <title>{html.escape(title)} \u2013 Literary Dictionary</title>\n'
        f"    {_THEME_INIT_JS}\n"
        f"    <style>{_CSS}</style>\n"
        "</head>\n"
        "<body>\n"
        f"{_header(root_prefix, available_langs, active_lang)}\n"
        '<div class="page-wrap">\n'
        f"{body}\n"
        "</div>\n"
        f"{_footer(root_prefix)}\n"
        f"{_ui_js(active_lang)}\n"
        f"{search_script}\n"
        "</body>\n"
        "</html>"
    )


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
    """entry_id -> list of (related_entry, target_letter).

    Cross-references are scoped to the same book (or same saga for
    saga-level entries) so that characters from different books do not
    cross-reference each other.  The scope key is namespaced to avoid
    collisions between book IDs and saga IDs that happen to share the
    same integer value.
    """
    by_scope_cat: dict = defaultdict(list)
    letters: dict = {}
    for e in entries:
        letters[e["id"]] = _entry_letter(e)
        cat = e.get("category_id")
        if cat is None:
            continue
        # Namespace scope to avoid collisions between book_id and saga_id
        # integer values from different tables.
        if e.get("book_id"):
            scope = ("book", e["book_id"])
        elif e.get("saga_id"):
            scope = ("saga", e["saga_id"])
        else:
            scope = None
        by_scope_cat[(scope, cat)].append(e)

    result = {}
    for e in entries:
        cat = e.get("category_id")
        if e.get("book_id"):
            scope = ("book", e["book_id"])
        elif e.get("saga_id"):
            scope = ("saga", e["saga_id"])
        else:
            scope = None
        peers = [
            p for p in by_scope_cat.get((scope, cat), [])
            if p["id"] != e["id"]
        ]
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


def _feedback_bar(context: str = "", book_name: str = "") -> str:
    """Render a small feedback / issue-report bar."""
    ctx_enc = html.escape(context, quote=True).replace(" ", "+")
    report_url = (
        f"{_GITHUB_REPO}/issues/new"
        f"?title=Error+report%3A+{ctx_enc}"
        "&labels=bug&body=Describe+the+issue%3A%0A%0APage%3A+"
        + ctx_enc
    )
    parts = [
        f'<a href="{report_url}" target="_blank" rel="noopener">'
        f'<span aria-hidden="true">&#9888;&#65039;</span> Report an error</a>',
    ]
    if book_name:
        book_enc = html.escape(book_name, quote=True).replace(" ", "+")
        entry_url = (
            f"{_GITHUB_REPO}/issues/new"
            f"?title=Entry+suggestion%3A+{book_enc}"
            f"&labels=suggestion&body=Book%2FSaga%3A+{book_enc}"
            "%0AEntry+name%3A+%0ADescription%3A+"
        )
        parts.append(
            f'<a href="{entry_url}" target="_blank" rel="noopener">&#43; Suggest a new entry</a>'
        )
    return '<div class="feedback-bar">' + "".join(parts) + "</div>"


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

    body = (
        f"{breadcrumb}\n"
        f"<h1>{html.escape(display)}</h1>\n"
        f'<p class="page-subtitle">{lang.upper()} edition</p>\n'
        f"{_letter_nav_html(all_letters, active=letter)}\n"
        "<section>\n"
        f"{entries_html}"
        "</section>\n"
        f"{_feedback_bar(display)}\n"
        '<a class="back-top" href="#">&#8593; Back to top</a>'
    )

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

    body = (
        f"{breadcrumb}\n"
        f"<h1>{html.escape(title)}</h1>\n"
        f'<p class="page-subtitle">{html.escape(author)}{html.escape(year)}</p>\n'
        f"{saga_note}\n"
        "<section>\n"
        f"{entries_html}"
        "</section>\n"
        f"{_feedback_bar(title, book_name=title)}\n"
        '<a class="back-top" href="#">&#8593; Back to top</a>'
    )

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

    body = (
        f"{breadcrumb}\n"
        f"<h1>{html.escape(title)}</h1>\n"
        f'<p class="page-subtitle">{html.escape(author)}</p>\n'
        "<section>\n"
        f"{entries_html}"
        "</section>\n"
        f"{_feedback_bar(title, book_name=title)}\n"
        '<a class="back-top" href="#">&#8593; Back to top</a>'
    )

    return _page(
        f"{title} \u2013 {lang.upper()}",
        body,
        root_prefix="../../",
        available_langs=available_langs,
        active_lang=lang,
        entries_for_search=all_lang_entries,
        search_letter_prefix="../",
    )


def _index_page(
    lang_data: dict,
    available_langs: list,
    all_lang_search_entries: Optional[list] = None,
) -> str:
    """Global landing page.

    ``all_lang_search_entries`` is a combined list of entries from every
    language, each augmented with a ``_search_href`` and ``_search_lang`` key
    so that home-page search works across all locales.
    """
    lang_cards = ""
    for lc in available_langs:
        meta = _LANG_META.get(lc, {"name": lc.upper(), "emoji": ""})
        emoji = meta["emoji"]
        lang_name = meta["name"]
        lang_cards += (
            f'<a class="card" href="{lc}/index.html" aria-label="{html.escape(lang_name)}">'
            f'<div class="card-emoji" aria-hidden="true">{emoji}</div>'
            f'<div class="card-title">{html.escape(lang_name)}</div>'
            f"</a>"
        )

    # If a language preference is stored redirect to that edition on load.
    lang_list = "','".join(available_langs)
    lang_redirect_js = (
        f"<script>(function(){{"
        f"var lp=localStorage.getItem('ld-lang');"
        f"if(lp&&['{lang_list}'].indexOf(lp)>=0){{"
        f"window.location.replace(lp+'/index.html');}}"
        f"}})();</script>"
    )

    body = (
        '<div class="hero">\n'
        "    <h1>Literary Dictionary</h1>\n"
        '    <p class="tagline">Characters, places, and concepts from world literature</p>\n'
        "</div>\n"
        "<h2>Available editions</h2>\n"
        f'<div class="cards-grid">{lang_cards}</div>\n'
        f"{lang_redirect_js}\n"
    )

    return _page(
        "Literary Dictionary",
        body,
        root_prefix="",
        available_langs=available_langs,
        active_lang=None,
        entries_for_search=all_lang_search_entries,
        search_letter_prefix="",
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
    # Accumulated search entries from every language for the global index page
    all_lang_search_entries: list = []

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
            "lang_name": _LANG_META.get(lang, {}).get("name", lang.upper()),
        }

        # Augment a copy of each entry with pre-built search hrefs for the
        # global index page (home-page search across all languages).
        for e in entries:
            letter = _entry_letter(e)
            e_copy = dict(e)
            e_copy["_search_href"] = f"{lang}/{letter}.html#entry-{e['id']}"
            e_copy["_search_lang"] = lang
            all_lang_search_entries.append(e_copy)

        # Group entries by letter
        by_letter: dict = defaultdict(list)
        for e in entries:
            by_letter[_entry_letter(e)].append(e)
        all_letters = sorted(by_letter.keys(), key=lambda x: (x == "Other", x))

        # Build see-also scoped per book/saga (not across books)
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

    # --- global index (search spans all languages) ---
    _write(
        os.path.join(output_dir, "index.html"),
        _index_page(lang_data, available_langs, all_lang_search_entries),
    )

    print(f"  \u2705 Site written to: {output_dir}/")
