from src.modules.cross_reference_module import (cross_reference_markup,
                                                get_author_cr_link,
                                                get_book_cr_link,
                                                get_saga_cr_link)
from src.modules.entries_module import get_entry_markup


def get_dictionary_page(lang, letter, group, strings, cross_reference):
    title = letter if letter != "Other" else strings["other_title"]

    template = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html
    xml:lang="{lang}"
    xmlns="http://www.w3.org/1999/xhtml"
    xmlns:math="http://exslt.org/math"
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
>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="../Styles/style.css"/>
    <title>{title}</title>
</head>

<body>
  <mbp:frameset>\n"""

    for entry in group:
        id = entry["id"]
        author = entry.get("author")
        author_id = entry.get("author_id")
        book = entry.get("book")
        book_id = entry.get("book_id")
        saga = entry.get("saga")
        saga_id = entry.get("saga_id")

        origin_placeholders = {
            "book": f'<a href="{get_book_cr_link(book, book_id)}">{entry.get('book')}</a>',
            "saga": f'<a href="{get_saga_cr_link(saga, saga_id)}">{entry.get('saga')}</a>',
            "author": f'<a href="{get_author_cr_link(author, author_id)}">{entry.get('author')}</a>',
        }

        origin = strings["origin_author"]

        if book and saga:
            origin = strings["origin_book_saga"]
        elif book:
            origin = strings["origin_book"]
        elif saga:
            origin = strings["origin_saga"]

        additional_info = {strings["origin"]: origin.format(**origin_placeholders)}

        if cross_reference[id]:
            additional_info[strings["see_also"]] = cross_reference_markup(
                cross_reference[id]
            )

        template += get_entry_markup(
            id=f"D_{id}",
            headword=entry["name"],
            display_name=entry.get('display_value'),
            aliases=entry["alias"],
            abbr=entry["category"],
            description=entry["description"],
            additional_info=additional_info,
        )

    template += """  </mbp:frameset>
</body>
</html>"""

    return template
