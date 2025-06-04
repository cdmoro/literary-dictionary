from src.modules.cross_reference_module import get_author_cr_link, get_saga_cr_link

def get_books_page(lang, title, books, strings, cross_reference):
    template = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html
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

    for entry in books:
        id = entry["id"]
        title = entry['title']
        description = entry['description']
        publication_year = entry['publication_year']
        abbr = entry['abbr']
        saga = entry['saga']
        saga_id = entry['saga_id']
        author = entry['author']
        author_id = entry['author_id']

        # Headword
        template += f'''    <idx:entry name="default" scriptable="yes" spell="yes" id="B_{id}">
      <a id="B_{id}"></a>

      <idx:orth value="{title}"><dt>{title} ({publication_year})</dt></idx:orth>\n\n'''
        
        # Definition
        template += '''      <dd>
        <div>'''

        template += f'<em>{abbr}.</em> '
        template += f'{description}</div>\n'
        
        if saga:
            template += f'        <div><strong>{strings["saga"]}:</strong> <a href="{get_saga_cr_link(saga, saga_id)}"><em>{saga}</em></a></div>\n'

        template += f'        <div><strong>{strings["author"]}:</strong> <a href="{get_author_cr_link(author, author_id)}">{author}</a></div>\n'
        
        if cross_reference[id]:
            template += f'''        <div>
          <strong>{strings["see_also"]}:</strong> \n'''
            
            seeAlsoLinks = []

            for ref in cross_reference[id]:
                seeAlsoLinks.append(f'          <a href="./{ref["link"]}">{ref["title"]}</a>')

            template += ', \n'.join(seeAlsoLinks)
            template += '\n        </div>\n'

        template += '''      </dd>
    </idx:entry>

    <hr/>\n\n'''

    template += '''  </mbp:frameset>
</body>
</html>'''

    return template