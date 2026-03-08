"""EPUB builder for Story Atlas reading companions.

Assembles all XHTML, CSS, OPF, NCX, and cover assets into a valid EPUB 2
archive (.epub) for a single book or saga reading companion.
"""

import html
import os
import shutil
import tempfile
import zipfile
from collections import defaultdict

from src.utils import escape_text_nodes, normalize_character

_ENCODING = "utf-8"

# ---------------------------------------------------------------------------
# Internal page generators
# ---------------------------------------------------------------------------


def _companion_styles() -> str:
    """Return the CSS stylesheet for companion EPUBs."""
    return """\
body {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 1em;
    line-height: 1.6;
    margin: 0;
    padding: 1em;
    color: #1a1a1a;
}
h1 { font-size: 1.8em; margin-bottom: 0.5em; }
h2 { font-size: 1.4em; margin-top: 1.5em; margin-bottom: 0.3em; }
h3.letter-heading {
    font-size: 1.2em;
    margin-top: 1.5em;
    color: #444;
    border-bottom: 1px solid #ccc;
    padding-bottom: 0.2em;
}
.see-also { margin-left: 1em; margin-top: 0.3em; font-size: 0.95em; }
.definition { margin-left: 1em; margin-bottom: 0.5em; }
.entry-abbr { font-style: italic; color: #555; }
.entry-alias { color: #666; font-size: 0.9em; }
.section-title { text-align: center; font-size: 2em; margin: 2em 0; }
hr { border: none; border-top: 1px solid #ddd; margin: 0.8em 0; }
a { color: #2a4a8a; text-decoration: none; }
"""


def _container_xml() -> str:
    return """\
<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="content.opf"
                  media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>"""


def _cover_xhtml(lang: str, cover_filename: str) -> str:
    body = (
        f'<img src="Assets/{html.escape(cover_filename)}"'
        ' alt="Cover" style="max-width:100%;"/>'
    )

    return f"""\
<?xml version="1.0" encoding="{_ENCODING}"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}">
<head>
    <title>Cover</title>
</head>
<body style="margin:0;padding:0;text-align:center;">
    {body}
</body>
</html>"""


def _copyright_xhtml(lang: str, title: str, author_name: str) -> str:
    from dotenv import load_dotenv

    load_dotenv()

    creator = os.getenv("AUTHOR", "Carlos Bonadeo")
    version = os.getenv("DICT_VERSION", "1.0.0")
    email = os.getenv("EMAIL", "")
    project = os.getenv("PROJECT", "")

    return f"""\
<?xml version="1.0" encoding="{_ENCODING}"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="Styles/style.css"/>
    <title>About</title>
</head>
<body>
    <h1>{html.escape(title)}</h1>
    <h2>Reading Companion</h2>
    <p><strong>Author:</strong> {html.escape(author_name)}</p>
    <p><strong>Created by:</strong> {html.escape(creator)}</p>
    <p><strong>Version:</strong> {html.escape(version)}</p>
    <p><strong>Project:</strong>
        <a href="{html.escape(project)}">{html.escape(project)}</a></p>
    <p><strong>Contact:</strong>
        <a href="mailto:{html.escape(email)}">{html.escape(email)}</a></p>
    <p><em>This reading companion is for personal use only.</em></p>
</body>
</html>"""


def _toc_xhtml(lang: str, title: str) -> str:
    return f"""\
<?xml version="1.0" encoding="{_ENCODING}"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="Styles/style.css"/>
    <title>Contents</title>
</head>
<body>
    <h1 class="section-title">Contents</h1>
    <div><a href="Cover.xhtml">Cover</a></div>
    <div><a href="Copyright.xhtml">About</a></div>
    <div><a href="TOC.xhtml">Contents</a></div>
    <div><a href="Entries.xhtml">Dictionary Entries – {html.escape(title)}</a></div>
</body>
</html>"""


def _build_see_also_map(entries: list) -> dict:
    """Return a mapping of entry_id → list of related entries.

    Related entries share the same ``category_id`` within the same
    book/saga companion.  Self-references are excluded.
    """
    by_category: dict = defaultdict(list)
    for entry in entries:
        cat_id = entry.get("category_id")
        if cat_id is not None:
            by_category[cat_id].append(entry)

    see_also: dict = {}
    for entry in entries:
        entry_id = entry["id"]
        cat_id = entry.get("category_id")
        if cat_id is not None:
            see_also[entry_id] = [
                e for e in by_category[cat_id] if e["id"] != entry_id
            ]
        else:
            see_also[entry_id] = []
    return see_also


def _entries_xhtml(lang: str, title: str, entries: list) -> str:
    """Generate the main XHTML page listing all entries for a book/saga."""
    see_also_map = _build_see_also_map(entries)

    entries_by_letter: dict = defaultdict(list)
    for entry in entries:
        first = normalize_character(entry["name"][0])
        if first.isalpha():
            entries_by_letter[first].append(entry)
        else:
            entries_by_letter["Other"].append(entry)

    template = f"""\
<?xml version="1.0" encoding="{_ENCODING}"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="Styles/style.css"/>
    <title>{html.escape(title)} – Entries</title>
</head>
<body>
    <h1>{html.escape(title)}</h1>
    <h2>Reading Companion</h2>\n"""

    for letter, group in sorted(
        entries_by_letter.items(), key=lambda x: (x[0] == "Other", x[0])
    ):
        display_letter = letter if letter != "Other" else "Symbols and Numbers"
        template += (
            f'    <h3 class="letter-heading" id="letter-{letter}">'
            f"{html.escape(display_letter)}</h3>\n"
        )
        for entry in group:
            entry_id = entry["id"]
            name = entry.get("display_name") or entry["name"]
            abbr = entry.get("category_abbr") or ""
            desc = entry.get("description") or ""
            alias = entry.get("alias") or ""

            template += f'    <div id="entry-{entry_id}">\n'
            template += f"      <strong>{html.escape(name)}</strong>\n"
            if alias:
                aliases = [a.strip() for a in alias.split(";") if a.strip()]
                if aliases:
                    template += (
                        f'      <span class="entry-alias">'
                        f" ({html.escape(', '.join(aliases))})</span>\n"
                    )
            template += '      <div class="definition">\n'
            if abbr:
                template += f'        <em class="entry-abbr">{html.escape(abbr)}.</em> '
            template += f"{escape_text_nodes(desc)}\n"
            template += "      </div>\n"
            see_also = see_also_map.get(entry_id, [])
            if see_also:
                links = [
                    f'<a href="#entry-{e["id"]}">{html.escape(e.get("display_name") or e["name"])}</a>'
                    for e in see_also
                ]
                template += '      <div class="see-also">\n'
                template += (
                    f"        <strong>See also:</strong> {', '.join(links)}\n"
                )
                template += "      </div>\n"
            template += "    </div>\n"
            template += "    <hr/>\n\n"

    template += """\
</body>
</html>"""
    return template


def _opf_content(
    lang: str,
    title: str,
    uid: str,
    cover_filename: str,
    cover_media_type: str,
    author_name: str,
) -> str:
    from dotenv import load_dotenv

    load_dotenv()

    creator = os.getenv("AUTHOR", "Carlos Bonadeo")
    cover_id = f"Assets_{cover_filename.replace('.', '_')}"

    return f"""\
<?xml version="1.0" encoding="{_ENCODING}"?>
<package version="2.0" xmlns="http://www.idpf.org/2007/opf"
         unique-identifier="BookId">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/"
            xmlns:opf="http://www.idpf.org/2007/opf">
    <dc:title>{html.escape(title)} – Reading Companion</dc:title>
    <dc:creator opf:role="aut">{html.escape(creator)}</dc:creator>
    <dc:subject>{html.escape(author_name)}</dc:subject>
    <dc:language>{lang}</dc:language>
    <dc:identifier id="BookId" opf:scheme="UUID">urn:uuid:{uid}</dc:identifier>
    <meta name="cover" content="{cover_id}"/>
  </metadata>
  <manifest>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="Styles_style_css" href="Styles/style.css" media-type="text/css"/>
    <item id="{cover_id}" href="Assets/{cover_filename}"
          media-type="{cover_media_type}"/>
    <item id="Cover_xhtml" href="Cover.xhtml"
          media-type="application/xhtml+xml"/>
    <item id="Copyright_xhtml" href="Copyright.xhtml"
          media-type="application/xhtml+xml"/>
    <item id="TOC_xhtml" href="TOC.xhtml"
          media-type="application/xhtml+xml"/>
    <item id="Entries_xhtml" href="Entries.xhtml"
          media-type="application/xhtml+xml"/>
  </manifest>
  <spine toc="ncx">
    <itemref idref="Cover_xhtml"/>
    <itemref idref="Copyright_xhtml"/>
    <itemref idref="TOC_xhtml"/>
    <itemref idref="Entries_xhtml"/>
  </spine>
  <guide>
    <reference type="cover" title="Cover" href="Cover.xhtml"/>
    <reference type="toc" title="Contents" href="TOC.xhtml"/>
    <reference type="text" title="About" href="Copyright.xhtml"/>
  </guide>
</package>"""


def _ncx_content(lang: str, title: str, uid: str) -> str:
    return f"""\
<?xml version="1.0" encoding="{_ENCODING}"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
  "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"
     xml:lang="{lang}">
  <head>
    <meta name="dtb:uid" content="urn:uuid:{uid}"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>{html.escape(title)} – Reading Companion</text>
  </docTitle>
  <navMap>
    <navPoint id="navpoint-cover" playOrder="1">
      <navLabel><text>Cover</text></navLabel>
      <content src="Cover.xhtml"/>
    </navPoint>
    <navPoint id="navpoint-copyright" playOrder="2">
      <navLabel><text>About</text></navLabel>
      <content src="Copyright.xhtml"/>
    </navPoint>
    <navPoint id="navpoint-toc" playOrder="3">
      <navLabel><text>Contents</text></navLabel>
      <content src="TOC.xhtml"/>
    </navPoint>
    <navPoint id="navpoint-entries" playOrder="4">
      <navLabel><text>Dictionary Entries</text></navLabel>
      <content src="Entries.xhtml"/>
    </navPoint>
  </navMap>
</ncx>"""


# ---------------------------------------------------------------------------
# Cover media-type helper
# ---------------------------------------------------------------------------

_COVER_MEDIA_TYPES = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "svg": "image/svg+xml",
}


def _cover_media_type(filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower()
    return _COVER_MEDIA_TYPES.get(ext, "image/jpeg")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_companion_epub(
    output_path: str,
    lang: str,
    title: str,
    author_name: str,
    entries: list,
    cover_filename: str,
    cover_src_path: str,
    uid: str,
) -> None:
    """Build a reading companion EPUB file.

    Args:
        output_path:    Full path for the output ``.epub`` file.
        lang:           Language code (e.g. ``'en'``).
        title:          Book or saga title.
        author_name:    Name of the original author.
        entries:        List of entry dicts returned by :mod:`scripts.db_reader`.
        cover_filename: Filename of the cover asset (e.g. ``'cover.svg'``).
        cover_src_path: Absolute path to the cover file on disk.
        uid:            UUID string used as the EPUB unique identifier.
    """
    media_type = _cover_media_type(cover_filename)

    with tempfile.TemporaryDirectory() as tmp:
        meta_inf = os.path.join(tmp, "META-INF")
        assets = os.path.join(tmp, "Assets")
        styles = os.path.join(tmp, "Styles")
        os.makedirs(meta_inf)
        os.makedirs(assets)
        os.makedirs(styles)

        # --- text files ---
        text_files = {
            os.path.join(meta_inf, "container.xml"): _container_xml(),
            os.path.join(tmp, "content.opf"): _opf_content(
                lang, title, uid, cover_filename, media_type, author_name
            ),
            os.path.join(tmp, "toc.ncx"): _ncx_content(lang, title, uid),
            os.path.join(tmp, "Cover.xhtml"): _cover_xhtml(lang, cover_filename),
            os.path.join(tmp, "Copyright.xhtml"): _copyright_xhtml(
                lang, title, author_name
            ),
            os.path.join(tmp, "TOC.xhtml"): _toc_xhtml(lang, title),
            os.path.join(tmp, "Entries.xhtml"): _entries_xhtml(lang, title, entries),
            os.path.join(styles, "style.css"): _companion_styles(),
        }

        for path, content in text_files.items():
            with open(path, "w", encoding=_ENCODING) as fh:
                fh.write(content)

        # --- cover asset ---
        if os.path.exists(cover_src_path):
            shutil.copy2(cover_src_path, os.path.join(assets, cover_filename))
        else:
            # Regenerate an SVG placeholder so the EPUB is always valid
            from scripts.cover_generator import generate_cover_svg

            svg = generate_cover_svg(title, "Reading Companion", lang.upper())
            fallback_name = "cover.svg"
            with open(os.path.join(assets, fallback_name), "w", encoding=_ENCODING) as fh:
                fh.write(svg)

        # --- mimetype (must be first, uncompressed) ---
        mimetype_path = os.path.join(tmp, "mimetype")
        with open(mimetype_path, "w", encoding=_ENCODING) as fh:
            fh.write("application/epub+zip")

        # --- zip into .epub ---
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as epub:
            epub.write(mimetype_path, "mimetype", compress_type=zipfile.ZIP_STORED)
            for root, _, files in os.walk(tmp):
                for fname in files:
                    if fname == "mimetype":
                        continue
                    full = os.path.join(root, fname)
                    arcname = os.path.relpath(full, tmp)
                    epub.write(full, arcname)
