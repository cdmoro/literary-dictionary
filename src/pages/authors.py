from src.modules.cross_reference_module import cross_reference_markup
from src.modules.entries_module import get_entry_markup

def get_authors_page(lang, title, authors, strings, cross_reference):
    template = f'''<?xml version="1.0" encoding="utf-8"?>
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
  <mbp:frameset>\n'''

    for entry in authors:
        id = entry["id"]
        name = entry['name']
        birth_year = entry['birth_year']
        death_year = entry['death_year']
        display_name = name + (f' ({strings["birth_abbr"]}. {birth_year})' if not death_year else f' ({birth_year}–{death_year})')
        additional_info = {}

        if cross_reference[id]:
          additional_info[strings['see_also']] = cross_reference_markup(cross_reference[id], "../Books/")

        template += get_entry_markup(
            id=f'A_{id}',
            headword=name,
            display_name=display_name,
            abbr=entry["abbr"],
            description=entry["description"],
            additional_info=additional_info
        )

    template += '''  </mbp:frameset>
</body>
</html>'''

    return template