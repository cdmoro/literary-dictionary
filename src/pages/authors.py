from src.modules.cross_reference_module import cross_reference_markup
from src.modules.entries_module import get_entry_markup
from src.constants import encoding
from src.config import ARGS


def get_authors_page(
    lang, title, authors, strings, book_cross_reference, saga_cross_reference
):
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

    for entry in authors:
        id = entry["id"]
        name = entry["name"]
        birth_year = entry["birth_year"]
        death_year = entry["death_year"]
        display_name = name + (
            f' ({strings["birth_abbr"]}. {birth_year})'
            if not death_year
            else f" ({birth_year}–{death_year})"
        )
        additional_info = {}

        if saga_cross_reference[id]:
            additional_info[strings["sagas"]] = cross_reference_markup(
                saga_cross_reference[id], "../Sagas/"
            )

        if book_cross_reference[id]:
            additional_info[strings["books"]] = cross_reference_markup(
                book_cross_reference[id], "../Books/"
            )

        template += get_entry_markup(
            id=f"A_{id}",
            name=name,
            display_name=display_name,
            abbr=entry["abbr"],
            description=entry["description"],
            additional_info=additional_info,
        )

    if not ARGS.epub:
        template += "  </mbp:frameset>"

    template += """ </dl>
</body>
</html>"""

    return template
