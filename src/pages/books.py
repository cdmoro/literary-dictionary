def get_books_page(title, books, strings):
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
    <link rel="stylesheet" type="text/css" href="Styles/style.css"/>
    <title>{title}</title>
</head>

<body>
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
        template += f'''    <idx:entry name="default" scriptable="yes" spell="yes">
      <a id="B-{id}"></a>

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