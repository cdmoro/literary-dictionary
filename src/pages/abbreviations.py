from src.constants import encoding


def get_abbreviation_page(lang, cur, strings):
    cur.execute(
        """
        SELECT abbr, name, description
        FROM categories
        ORDER BY abbr
    """
    )

    categories = []
    for row in cur.fetchall():
        categories.append(dict(row))

        template = f"""<?xml version="1.0" encoding="{encoding}"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}">
<head>
    <title>{strings['abbr_guide']}</title>
    <link rel="stylesheet" type="text/css" href="Styles/style.css"/>
</head>
<body>
    <h1>{strings['abbr_guide']}</h1>
    <table class="abbr-table">"""

        for category in categories:
            template += f"""
        <tr>
            <td>{category.get('abbr')}.</td>
            <td>{category.get('name')} — {category.get('description')}</td>
        </tr>"""

        template += """\n    </table>
</body>
</html>
"""
    return template
