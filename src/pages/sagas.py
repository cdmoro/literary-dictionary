def get_sagas_page(cur, strings):
    cur.execute('''
        SELECT s.id, s.name, s.description, c.abbr, a.name as author
        FROM sagas s, authors a
        CROSS JOIN categories c
        WHERE c.id = 15 AND s.author_id == a.id
        ORDER BY s.name
    ''')

    sagas = []
    for row in cur.fetchall():
        sagas.append(dict(row))
        
    title = strings["sagas"]

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
    <title>{title}</title>
</head>

<body>
  <h1>{title}</h1>
  <mbp:frameset>\n'''

    for entry in sagas:
        id = entry["id"]
        name = entry['name']
        description = entry['description']
        abbr = entry['abbr']
        author = entry['author']

        # Headword
        template += f'''    <idx:entry name="default" scriptable="yes" spell="yes" id="s-{id}">
      <a id="s-{id}"></a>

      <dt>
        <idx:orth>{name}</idx:orth>\n'''
        
        template += '      </dt>\n\n'
        
        # Definition
        template += '''      <dd>
        <div>'''

        template += f'<em>{abbr}.</em> '
        template += f'{description}</div>\n'
        
        template += f'        <div><strong>{strings["author"]}:</strong> {author}</div>\n'

        template += '''      </dd>
    </idx:entry>

    <hr/>\n\n'''

    template += '''  </mbp:frameset>
</body>
</html>'''

    return template