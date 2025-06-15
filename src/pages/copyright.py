import os

from dotenv import load_dotenv

from src.constants import encoding

from src.config import ARGS

load_dotenv()


def get_copyright_page(strings):
    data = {
        "lang": strings["lang"].lower(),
        "title": strings["about"],
        "book_title": strings["title"],
        "edition": strings["edition"],
        "copyright_desc": strings["copyright_desc"],
        "license": strings["license"],
        "project": strings["project"],
        "contact": strings["contact"],
        "copyright": strings["copyright"].format(ebook_author=os.getenv("AUTHOR")),
        "copyright_commercial": strings["copyright_commercial"].format(
            ebook_author=os.getenv("AUTHOR")
        ),
        "version": strings["copyright_version"].format(
            version=os.getenv("DICT_VERSION")
        ),
        "entries_label": strings["entries"],
        "authors_label": strings["authors"],
        "sagas_label": strings["sagas"],
        "books_label": strings["books"],
        "repo": os.getenv("PROJECT"),
        "email": os.getenv("EMAIL"),
        "cc_link": f'https://creativecommons.org/licenses/by/4.0/deed.{strings["lang"].lower()}',
        "encoding": encoding,
    }

    template = """<?xml version="1.0" encoding="{encoding}"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="Styles/style.css"/>
    <title>{title}</title>
</head>
<body>
    <h1>{book_title}</h1>
    <div>{edition}</div>
    <div>{version}<br/></div>
    <div>{copyright_desc}<br/></div>
    <div><strong>{project}</strong>: <a href="{repo}">{repo}</a></div>
    <div><strong>{contact}</strong>: <a href="mailto:{email}">{email}</a><br/></div>
    <div><strong>{license}</strong><br/></div>"""

    if ARGS.commercial:
        template += "<div>{copyright_commercial}</div>"
    else:
        template += """<div>
        <a href="{cc_link}" target="_blank" rel="noopener noreferrer">
            <img src="Assets/cc_banner.png" alt="Creative Commons Attribution 4.0 International" />
        </a>
        <br/>
    </div>
    <div>{copyright}</div>"""

    template += """</body>
</html>"""

    return template.format(**data)
