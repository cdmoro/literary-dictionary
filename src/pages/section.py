from src.utils import normalize_character
from src.constants import encoding
import html


def get_section_page(lang, title, subtitle=None):
    return f"""<?xml version="1.0" encoding="{encoding}"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="../Styles/style.css"/>
    <title>{title}{ f": {subtitle}" if subtitle else ''}</title>
</head>
<body>
    <h1 class="section-title">{title.upper()}</h1>
    { f'<h2 class="section-subtitle">{subtitle.upper()}</h2>' if subtitle else ''}
</body>
</html>"""


def get_section_toc(lang, title, entries_by_letter, strings, prefix):
    template = f"""<?xml version="1.0" encoding="{encoding}"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="../Styles/style.css"/>
    <title>{strings["ncx_dictionary_toc"]}</title>
</head>
<body>
    <h1>{strings["ncx_dictionary_toc"]}</h1>\n"""

    for letter, group in sorted(
        entries_by_letter.items(), key=lambda x: (x[0] == "Other", x[0])
    ):
        letter = letter if letter != "Other" else strings["other_title"]
        template += f'\n    <h2 class="letter-toc-title">{letter}</h2>\n\n'

        for entry in group:
            name = entry["name"]
            template += f'    <div><a href="{prefix}_{normalize_character(name[0])}.xhtml#{prefix}_{entry["id"]}">{html.escape(name)}</a></div>\n'

    template += """\n</body>
</html>"""

    return template
