from dotenv import load_dotenv
import os

load_dotenv()

def get_copyright_page(strings, entries):
    total_entries = len(entries)
    authors = {p['author'] for p in entries if p.get('author')}
    sagas = {p['saga'] for p in entries if p.get('saga')}
    books = {p['book'] for p in entries if p.get('book')}

    data = {
        "lang": strings["lang"],
        "title": strings["title"],
        "subtitle": strings["subtitle"],
        "edition": strings["edition"],
        "copyright_desc": strings["copyright_desc"].format(authors=len(authors), entries=total_entries, books=len(books), sagas=len(sagas)),
        "license": strings["license"],
        "project": strings["project"],
        "contact": strings["contact"],
        "copyright": strings["copyright"],
        "version": strings["copyright_version"].format(version=os.getenv("DICT_VERSION")),
        "entries": total_entries,
        "authors": len(authors),
        "sagas": len(sagas),
        "books": len(books),
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
    <div><strong>{title}</strong></div>
    <div>{edition}</div>
    <div>{version}</div>
    <br />
    <div>{copyright_desc}</div>
    <br />
    <div><strong>{license}</strong></div>
    <div>{copyright}</div>
    <br />
    <div>{project}: <a href="https://github.com/cdmoro/literary-dictionary">https://github.com/cdmoro/literary-dictionary</a></div>
    <div>{contact}: carlosbonadeo@gmail.com</div>
</body>
</html>"""

    return template.format(**data)
