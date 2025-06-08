from src.constants import encoding


def get_cover_page(lang):
    return f"""<?xml version="1.0" encoding="{encoding}"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}">
<head>
    <title>Cover</title>
</head>
<body>
    <svg viewBox="0 0 600 900" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="100%" preserveAspectRatio="xMidYMid meet" height="100%">
        <image xlink:href="Assets/cover.jpg" width="600" height="900"/>
    </svg>
</body>
</html>"""
