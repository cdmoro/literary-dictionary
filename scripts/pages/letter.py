def get_letter_page(letter, group, strings, cross_reference_data):
    template = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html 
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
    <link rel="stylesheet" type="text/css" href="style.css"/>
    <title>{letter}</title>
</head>

<body>
  <h1>{letter}</h1>
  <mbp:frameset>\n'''

    for entry in group:
        id = entry["id"]
        headword = entry['headword']
        aliases = entry.get('alias', '')
        displayValue = entry.get('display_value') or headword
        description = entry['description']
        abbrev = entry.get('abbrev')
        author = entry.get('author')
        book = entry.get('book')
        saga = entry.get('saga')
        seeAlso = entry.get('seeAlso')

        # Headword
        template += f'''    <idx:entry name="default" scriptable="yes" spell="yes" id="e-{id}">
      <a id="e-{id}"></a>

      <dt>
        <idx:orth value="{headword}">{displayValue}</idx:orth>\n'''

        # Alias
        if aliases:
            for alias in aliases.split(';'):
                template += f'        <idx:orth value="{alias}" />\n'
        
        template += '      </dt>\n\n'
        
        # Definition
        template += '''      <dd>
        <div>'''

        if (abbrev):
            template += f'<em>{abbrev}</em> '
        template += f'{description}</div>\n'
        
        template += '        <div>'
        
        # Origin
        template += f'<strong>{strings["origin"]}:</strong> '

        if book and saga:
            template += strings["origin_book_saga"].format(book=book, saga=saga, author=author)
        elif book:
            template += strings["origin_book"].format(book=book, author=author)
        elif saga:
            template += strings["origin_saga"].format(saga=saga, author=author)
        else:
            template += strings["origin_author"].format(author=author)

        template += '</div>\n'

        # See also
        if seeAlso:
            template += f'''        <div>
                      <strong>{strings["see_also"]}:</strong> \n'''
            
            seeAlso = list(dict.fromkeys(seeAlso))
            seeAlso = sorted(seeAlso, key=lambda id: cross_reference_data[id][0].lower() if id in cross_reference_data else '')
            seeAlsoLinks = []
            for idr in seeAlso:
                if not idr in cross_reference_data:
                    print(f'  - ⏭️  ID {id}: Cross Reference not found ({idr}), skipped')
                    continue
                seeAlsoLinks.append(f'          <a href="{cross_reference_data[idr][1]}#{idr}">{cross_reference_data[idr][0]}</a>')
            template += ', \n'.join(seeAlsoLinks)
            template += '\n        </div>\n'
        
        template += '''      </dd>
    </idx:entry>

    <hr/>\n\n'''

    template += '''  </mbp:frameset>
</body>
</html>'''

    return template