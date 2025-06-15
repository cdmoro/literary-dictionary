import html

from src.modules.cross_reference_module import (
    cross_reference_markup,
    get_author_cr_link,
    get_saga_cr_link,
)
from src.modules.entries_module import get_entry_markup
from src.constants import encoding


def get_books_page(lang, title, books, strings, cross_reference):
    template = f"""<?xml version="1.0" encoding="{encoding}"?>
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

    for entry in books:
        id = entry["id"]
        title = entry["name"]
        saga = entry["saga"]
        saga_id = entry["saga_id"]
        author = entry["author"]
        author_id = entry["author_id"]
        additional_info = {}

        if saga_id:
            additional_info[strings["saga"]] = (
                f'<a href="{get_saga_cr_link(saga, saga_id)}"><em>{html.escape(saga)}</em></a>'
            )

        additional_info[strings["author"]] = (
            f'<a href="{get_author_cr_link(author, author_id)}">{html.escape(author)}</a>'
        )

        if cross_reference[id]:
            additional_info[strings["see_also"]] = cross_reference_markup(
                cross_reference[id]
            )

        template += get_entry_markup(
            id=f"B_{id}",
            name=title,
            display_name=f"{title} ({entry['publication_year']})",
            abbr=entry["abbr"],
            description=entry["description"],
            additional_info=additional_info,
        )

    template += """  </mbp:frameset>
</body>
</html>"""

    return template
