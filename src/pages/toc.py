def get_toc_page(lang, strings):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="Styles/style.css"/>
    <title>{strings["contents"]}</title>
</head>
<body class="contents">
    <h1>{strings["contents"]}</h1>
    <div><a href="Cover.xhtml">{strings["cover"]}</a></div>
    <div><a href="Copyright.xhtml">{strings["about"]}</a></div>
    <div><a href="TOC.xhtml">{strings["contents"]}</a></div>
    <div><a href="Abbreviations.xhtml">{strings["abbr_guide"]}</a></div>
    <div><a href="Dictionary.xhtml">{strings["dictionary"]}</a></div>
    <div><a href="Books.xhtml">{strings["books"]}</a></div>
    <div><a href="Sagas.xhtml">{strings["sagas"]}</a></div>
    <div><a href="Authors.xhtml">{strings["authors"]}</a></div>
</body>
</html>
"""
