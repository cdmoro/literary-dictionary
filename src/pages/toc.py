import re
from src.constants import encoding


def get_toc_page(lang, strings, dictionary, appendixes):
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
  <div><a href="Copyright.xhtml">{strings["about"]}</a></div>
  <div><a href="TOC.xhtml">{strings["contents"]}</a></div>
  <div><a href="Abbreviations.xhtml">{strings["abbr_guide"]}</a></div>\n"""

    template += f'  <div><a href="Dictionary/Dictionary.xhtml">{strings["dictionary"]}</a></div>\n'

    dictionary_toc_files = [
        file for file in dictionary if not re.fullmatch(r"[A-Z]_[A-Z]", file)
    ]
    dictionary_letters = [
        file for file in dictionary if re.fullmatch(r"[A-Z]_[A-Z]", file)
    ]

    for toc_file in dictionary_toc_files:
        if toc_file == "Dictionary":
            continue
        template += f'<div class="toc-subsection"><a href="Dictionary/{toc_file}.xhtml">{strings[f'ncx_{toc_file.lower()}']}</a></div>'

    template += '  <div class="toc-letters">'

    for index, file in enumerate(dictionary_letters):
        if index % 13 == 0 and index != 0:
            template += "<br/>"

        template += f'<a class="toc-letter" href="Dictionary/{file}.xhtml">{file.split("_")[1]}</a>&nbsp;&nbsp;&nbsp;'

    template += "</div>\n"

    for section, file in appendixes.items():
        if len(file) == 0:
            continue

        template += f'  <div><a href="{section}/{section}.xhtml">{strings["appendix"]}: {strings[section.lower()]}</a></div>\n'

    template += """</body>
</html>
"""

    return template
