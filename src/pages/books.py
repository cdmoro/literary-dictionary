def get_books_page(cur, strings):
    cur.execute('''
        SELECT 
            b.id, 
            b.title, 
            b.description, 
            b.publication_year,
            c.abbr, 
            a.name AS author, 
            s.name AS saga
        FROM books b
        JOIN authors a ON b.author_id = a.id
        CROSS JOIN categories c
        LEFT JOIN sagas s ON b.saga_id = s.id
        WHERE c.id = 14
        ORDER BY b.title;
    ''')

    books = []
    for row in cur.fetchall():
        books.append(dict(row))
        
    title = strings["books"]

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

    for entry in books:
        id = entry["id"]
        title = entry['title']
        description = entry['description']
        publication_year = entry['publication_year']
        abbr = entry['abbr']
        saga = entry['saga']
        author = entry['author']

        # Headword
        template += f'''    <idx:entry name="default" scriptable="yes" spell="yes" id="b-{id}">
      <a id="b-{id}"></a>

      <dt>
        <idx:orth value="{title}">{title} ({publication_year})</idx:orth>\n'''
        
        template += '      </dt>\n\n'
        
        # Definition
        template += '''      <dd>
        <div>'''

        template += f'<em>{abbr}.</em> '
        template += f'{description}</div>\n'
        
        if saga:
            template += f'        <div><strong>{strings["saga"]}:</strong> <em>{saga}</em></div>\n'

        template += f'        <div><strong>{strings["author"]}:</strong> {author}</div>\n'

        template += '''      </dd>
    </idx:entry>

    <hr/>\n\n'''

    template += '''  </mbp:frameset>
</body>
</html>'''

    return template