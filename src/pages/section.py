from src.utils import normalize_character

def get_section_page(lang, title):
    return f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="./Styles/style.css"/>
    <title>{title.upper()}</title>
</head>
<body class="section">
    <h1>{title.upper()}</h1>
</body>
</html>'''

def get_section_toc(lang, title, entries_by_letter, strings, prefix, folder):
    template = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="./Styles/style.css"/>
    <title>{title}</title>
</head>
<body class="section-toc">
    <h1>{title}</h1>\n'''

    for letter, group in sorted(entries_by_letter.items(), key=lambda x: (x[0] == "Other", x[0])):
        letter = letter if letter != "Other" else strings["other_title"]
        template += f'\n    <h2>{letter}</h2>\n\n'

        for entry in group:
            name = entry.get("name") or entry.get("headword") or entry.get("title")
            template += f'    <div><a href="./{folder}/{prefix}_{normalize_character(name[0])}.xhtml#{prefix}_{entry["id"]}">{name}</a></div>\n'

    template += '''\n</body>
</html>'''

    return template