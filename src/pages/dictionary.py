import html

from src.modules.cross_reference_module import (
    cross_reference_markup,
    get_author_cr_link,
    get_book_cr_link,
    get_saga_cr_link,
)
from src.modules.entries_module import get_entry_markup
from src.constants import encoding
from src.utils import normalize_character
from src.config import ARGS
import re


def get_dictionary_page(lang, letter, group, strings, cross_reference):
    title = letter if letter != "Other" else strings["other_title"]

    template = f"""<?xml version="1.0" encoding="{encoding}"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html
    xml:lang="{lang}"
    xmlns="http://www.w3.org/1999/xhtml"
    """

    if not ARGS.epub:
        template += """xmlns:math="http://exslt.org/math"
        xmlns:svg="http://www.w3.org/2000/svg"
        xmlns:tl="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
        xmlns:saxon="http://saxon.sf.net/"
        xmlns:xs="http://www.w3.org/2001/XMLSchema"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:cx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:mbp="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
        xmlns:mmc="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
        xmlns:idx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
        """

    template += f""">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="../Styles/style.css"/>
    <title>{title}</title>
</head>

<body>
  <dl>\n"""

    if not ARGS.epub:
        template += "<mbp:frameset>\n"

    for entry in group:
        id = entry["id"]
        author = entry.get("author")
        author_id = entry.get("author_id")
        book = entry.get("book")
        book_id = entry.get("book_id")
        saga = entry.get("saga")
        saga_id = entry.get("saga_id")

        additional_info = {}

        if author:
            origin_placeholders = {
                "book": f'<a href="{get_book_cr_link(book, book_id)}">{html.escape(book or "")}</a>',
                "saga": f'<a href="{get_saga_cr_link(saga, saga_id)}">{html.escape(saga or "")}</a>',
                "author": f'<a href="{get_author_cr_link(author, author_id)}">{html.escape(author)}</a>',
            }

            origin = strings["origin_author"]

            if book and saga:
                origin = strings["origin_book_saga"]
            elif book:
                origin = strings["origin_book"]
            elif saga:
                origin = strings["origin_saga"]

            additional_info[strings["origin"]] = origin.format(**origin_placeholders)

        if cross_reference[id]:
            additional_info[strings["see_also"]] = cross_reference_markup(
                cross_reference[id]
            )

        template += get_entry_markup(
            id=f"D_{id}",
            name=entry["name"],
            display_name=entry.get("display_name"),
            aliases=entry["alias"],
            abbr=entry["category"],
            description=entry["description"],
            additional_info=additional_info,
            dict_markup=not ARGS.epub,
        )

    if not ARGS.epub:
        template += "  </mbp:frameset>"

    template += """  </dl>
</body>
</html>"""

    return template


def get_dictionary_by_book_page(lang, entries_by_book, book_data, strings):
    template = f"""<?xml version="1.0" encoding="{encoding}"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="../Styles/style.css"/>
    <title>{strings["dictionary"]}: {strings["section_toc_subtitle"]}</title>
</head>
<body>
    <h1 class="toc-title">{strings["dictionary"]}:</h1>
    <h2 class="toc-subtitle">{strings["section_toc_subtitle_by_book"]}</h2>\n"""

    for book, entries in sorted(entries_by_book.items()):
        book_file_letter = normalize_character(book[0])
        author_file_letter = normalize_character(book_data[book]["author"][0])

        template += '<div class="entries-by-book">'
        template += f'  <h3 class="entries-by-book-title"><a href="../Books/B_{book_file_letter}.xhtml#B_{book_data[book]["id"]}">{html.escape(book)}</a></h3>\n'
        template += f'  <div class="entries-by-book-author"><a href="../Authors/A_{author_file_letter}.xhtml#A_{book_data[book]["author_id"]}">{book_data[book]["author"]}</a></div>'
        template += '  <div class="entries-by-book-entries">'

        entries_link = []
        for entry in entries:
            entry_file_letter = normalize_character(entry["name"][0])
            # description = re.sub("<[^<]+?>", "", entry["description"][0:30])
            # template += f'  <p class="p-spacing"><a href="D_{entry_file_letter}.xhtml#D_{entry["id"]}">{html.escape(entry["name"])}</a>: <em>{html.escape(description)}...</em></p>\n'
            entries_link.append(
                f'<a href="D_{entry_file_letter}.xhtml#D_{entry["id"]}">{html.escape(entry["name"])}</a>'
            )
        template += ", ".join(entries_link)
        template += "  </div>"
        template += "</div>"

    template += """\n</body>
</html>"""

    return template


def get_dictionary_by_alias_page(lang, entries_by_alias, strings):
    template = f"""<?xml version="1.0" encoding="{encoding}"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="../Styles/style.css"/>
    <title>{strings["dictionary"]}: {strings["section_toc_subtitle"]}</title>
</head>
<body>
    <h1 class="toc-title">{strings["dictionary"]}:</h1>
    <h2 class="toc-subtitle">{strings["section_toc_subtitle_by_book"]}</h2>\n"""

    for alias, entries in sorted(entries_by_alias.items()):

        template += "<div>"
        template += f'  <strong>{html.escape(alias)}</strong>: {strings["see"]} '

        aliases = []
        for entry in entries:
            entry_file_letter = normalize_character(entry["name"][0])
            aliases.append(
                f'<a href="D_{entry_file_letter}.xhtml#D_{entry["id"]}">{html.escape(entry["name"])}</a>'
            )

        template += ", ".join(aliases)
        template += ".</div>"

    template += """\n</body>
</html>"""

    return template
