from src.modules.cross_reference_module import get_author_cr_link, get_saga_cr_link, get_book_cr_link

def get_dictionary_page(lang, letter, group, strings, cross_reference):
    title = letter if letter != "Other" else strings["other_title"]

    template = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html
    xmlns="http://www.w3.org/1999/xhtml"
    xml:lang="{lang}"
    xmlns:math="http://exslt.org/math"
    xmlns:svg="http://www.w3.org/2000/svg"
    xmlns:tl="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
    xmlns:saxon="http://saxon.sf.net/"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:cx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:mbp="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
    xmlns:mmc="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
    xmlns:idx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="../Styles/style.css"/>
    <title>{title}</title>
</head>

<body>
  <mbp:frameset>\n'''

    for entry in group:
        id = entry["id"]
        headword = entry['headword']
        aliases = entry.get('alias', '')
        displayValue = entry.get('display_value') or headword
        description = entry['description']
        category = entry.get('category')
        author = entry.get('author')
        author_id = entry.get('author_id')
        book = entry.get('book')
        book_id = entry.get('book_id')
        saga = entry.get('saga')
        saga_id = entry.get('saga_id')
        
        origin_placeholders = {
            'book': entry.get('book'),
            'saga': entry.get('saga'),
            'author':  entry.get('author'),
            'author_href': get_author_cr_link(author, author_id),
            'saga_href': get_saga_cr_link(saga, saga_id),
            'book_href': get_book_cr_link(book, book_id)
        }

        # Headword
        template += f'''    <idx:entry name="default" scriptable="yes" spell="yes" id="D_{id}">
      <a id="D_{id}"></a>

      <idx:orth value="{headword}"><dt>{displayValue}</dt></idx:orth>\n'''

        # Alias
        if aliases:
            for alias in aliases.split(';'):
                template += f'        <idx:orth value="{alias}" />\n'
        
        template += '\n'
        
        # Definition
        template += '''      <dd>
        <div>'''

        if (category):
            template += f'<em>{category}.</em> '
        template += f'{description}</div>\n'
        
        template += '        <div>'
        
        # Origin
        template += f'<strong>{strings["origin"]}:</strong> '

        if book and saga:
            template += strings["origin_book_saga"].format(**origin_placeholders)
        elif book:
            template += strings["origin_book"].format(**origin_placeholders)
        elif saga:
            template += strings["origin_saga"].format(**origin_placeholders)
        else:
            template += strings["origin_author"].format(**origin_placeholders)

        template += '</div>\n'

        # See also
        if cross_reference[id]:
            template += f'''        <div>
          <strong>{strings["see_also"]}:</strong> \n'''
            
            seeAlsoLinks = []

            for ref in cross_reference[id]:
                seeAlsoLinks.append(f'          <a href="{ref["link"]}">{ref["headword"]}</a>')

            template += ', \n'.join(seeAlsoLinks)
            template += '\n        </div>\n'
        
        template += '''      </dd>
    </idx:entry>

    <hr/>\n\n'''

    template += '''  </mbp:frameset>
</body>
</html>'''

    return template