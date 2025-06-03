def get_authors_page(title, authors, strings):
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
  <h1>{title}</h1>
  <mbp:frameset>\n'''

    for entry in authors:
        id = entry["id"]
        name = entry['name']
        description = entry['description']
        birth_year = entry['birth_year']
        death_year = entry['death_year']
        abbr = entry['abbr']

        # Headword
        template += f'''    <idx:entry name="default" scriptable="yes" spell="yes" id="A-{id}">
      <a id="A-{id}"></a>

      <dt>
        <idx:orth value="{name}">{name} '''
        
        if not death_year:
            template += f'({strings["birth_abbr"]}. {birth_year})'
        else:
            template += f'({birth_year}–{death_year})'
        
        template += '''</idx:orth>\n'''
        
        template += '      </dt>\n\n'
        
        # Definition
        template += '''      <dd>
        <div>'''

        template += f'<em>{abbr}.</em> '
        template += f'{description}</div>\n'

        template += '''      </dd>
    </idx:entry>

    <hr/>\n\n'''

    template += '''  </mbp:frameset>
</body>
</html>'''

    return template