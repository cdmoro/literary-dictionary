from dotenv import load_dotenv
import os

load_dotenv()

def get_copyright_page(strings, entries):
    total_entries = len(entries)
    authors = {p['author'] for p in entries if p.get('author')}
    sagas = {p['saga'] for p in entries if p.get('saga')}
    books = {p['book'] for p in entries if p.get('book')}

    data = {
        "lang": strings["lang"].lower(),
        "title": strings["about"],
        "book_title": strings["title"],
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
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="./Styles/style.css"/>
    <title>{title}</title>
</head>
<body>
    <h1>{book_title}</h1>
    <div>{edition}</div>
    <div>{version}</div>
    <div class="space-10">{copyright_desc}</div>

    <div class="space-10"><strong>{license}</strong></div>
    <div>{copyright}</div>

    <div class="space-10">{project}: <a href="https://github.com/cdmoro/literary-dictionary">https://github.com/cdmoro/literary-dictionary</a></div>
    <div>{contact}: carlosbonadeo@gmail.com</div>
</body>
</html>"""

    return template.format(**data)
