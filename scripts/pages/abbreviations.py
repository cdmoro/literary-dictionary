import os

def get_abbreviation_xhtml(cur, strings):
    cur.execute("""
        SELECT abbr, name, description
        FROM categories
        ORDER BY abbr
    """)

    categories = []
    for row in cur.fetchall():
        categories.append(dict(row))

        abbr_xhtml = f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
    <h1>{strings['abbr_guide']}</h1>
    <table class="abbr-table">'''
        
        for category in categories:
            abbr_xhtml += f'''
        <tr>
            <td>{category.get('abbr')}.</td>
            <td>{category.get('name')} — {category.get('description')}</td>
        </tr>'''
        
        abbr_xhtml += '''\n    </table>
</body>
</html>
'''
    return abbr_xhtml