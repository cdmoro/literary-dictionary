def get_contents_xhtml(strings):
    return f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
    <h1>{strings["contents"]}</h1>
    <nav epub:type="toc" class="toc">
        <ol>
            <li><a href="Cover.xhtml">{strings["cover"]}</a></li>
            <li><a href="Copyright.xhtml">{strings["about"]}</a></li>
            <li><a href="A.xhtml">{strings["definitions"]}</a></li>
            <li><a href="Abbreviations.xhtml">{strings["abbr_guide"]}</a></li>
        </ol>
    </nav>
</body>
</html>
'''