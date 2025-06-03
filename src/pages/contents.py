def get_contents_page(strings):
    return f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="Styles/style.css"/>
    <title>{strings["contents"]}</title>
</head>
<body>
    <h1>{strings["contents"]}</h1>
    <nav epub:type="toc" class="toc">
        <ol>
            <li><a href="Cover.xhtml">{strings["cover"]}</a></li>
            <li><a href="Copyright.xhtml">{strings["about"]}</a></li>
            <li><a href="Contents.xhtml">{strings["contents"]}</a></li>
            <li><a href="Abbreviations.xhtml">{strings["abbr_guide"]}</a></li>
            <li><a href="Dictionary.xhtml">{strings["definitions"]}</a></li>
            <li><a href="Books.xhtml">{strings["books"]}</a></li>
            <li><a href="Sagas.xhtml">{strings["sagas"]}</a></li>
            <li><a href="Authors.xhtml">{strings["authors"]}</a></li>
        </ol>
    </nav>
</body>
</html>
'''