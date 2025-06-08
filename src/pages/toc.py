import re
from src.constants import encoding


def get_toc_page(lang, strings, pages_by_section):
    template = f"""<?xml version="1.0" encoding="{encoding}"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="Styles/style.css"/>
    <title>{strings["contents"]}</title>
</head>
<body>
  <h1>{strings["contents"]}</h1>
  <div><a href="Cover.xhtml">{strings["cover"]}</a></div>
  <div><a href="Copyright.xhtml">{strings["about"]}</a></div>
  <div><a href="TOC.xhtml">{strings["contents"]}</a></div>
  <div><a href="Abbreviations.xhtml">{strings["abbr_guide"]}</a></div>\n"""

    for section, files in pages_by_section.items():
        if len(files) == 0:
            continue

        template += f'  <div><a href="{section}/{section}.xhtml">{strings[section.lower()]}</a></div>\n'

        template += '  <div class="toc-letters">'

        letter_links = [file for file in files if re.fullmatch(r"[A-Z]_[A-Z]", file)]

        for index, file in enumerate(letter_links):
            if index % 13 == 0 and index != 0:
                template += "<br/>"

            template += f'<a class="toc-letter" href="{section}/{file}.xhtml">{file.split("_")[1]}</a>&nbsp;&nbsp;&nbsp;'

        template += "</div>\n"

    template += """</body>
</html>
"""

    return template
