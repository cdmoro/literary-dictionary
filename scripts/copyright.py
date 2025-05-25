from dotenv import load_dotenv
import os

load_dotenv()

def get_copyright_html(strings, entries):
    total_registros = len(entries)
    autores = {p['author'] for p in entries if p.get('author')}
    sagas = {p['saga'] for p in entries if p.get('saga')}
    libros = {p['book'] for p in entries if p.get('book')}

    data = {
        "lang": strings["lang"],
        "title": strings["title"],
        "subtitle": strings["subtitle"],
        "copyright": strings["copyright"],
        "version": strings["copyright_version"].format(version=os.getenv("DICT_VERSION")),
        "entries": total_registros,
        "authors": len(autores),
        "sagas": len(sagas),
        "books": len(libros),
        "entries_label": strings["entries"],
        "authors_label": strings["authors"],
        "sagas_label": strings["sagas"],
        "books_label": strings["books"],
    }

    template = """<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
    <div><strong>{title} ({lang})</strong></div>
    <div><em>{subtitle}</em></div>
    <br />
    <div>{copyright}</div>
    <div><strong>{version}</strong></div>
    <br />
    <ul>
        <li>{entries_label}: {entries}</li>
        <li>{authors_label}: {authors}</li>
        <li>{sagas_label}: {sagas}</li>
        <li>{books_label}: {books}</li>
    </ul>
</body>
</html>"""

    return template.format(**data)
