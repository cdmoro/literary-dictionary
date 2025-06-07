from collections import defaultdict
from src.utils import normalize_character


def get_entries(conn):
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            e.id,
            e.name,
            e.display_name,
            e.alias,
            e.description,
            a.id           AS author_id,
            a.name         AS author,
            s.id           AS saga_id,
            s.name         AS saga,
            b.id           AS book_id,
            b.name         AS book,
            c.abbr         AS category,
            c.id           AS category_id
        FROM entries e
        LEFT JOIN authors a ON e.author_id = a.id
        LEFT JOIN sagas s   ON e.saga_id = s.id
        LEFT JOIN books b   ON e.book_id = b.id
        LEFT JOIN categories c ON e.category_id = c.id
        WHERE e.draft = 0
        ORDER BY e.name COLLATE NOCASE
    """
    )

    entries = []
    for row in cur.fetchall():
        entries.append(dict(row))

    return entries


def get_entries_by_letter(entries):
    entries_by_letter = defaultdict(list)

    for entry in entries:
        name = entry["name"]
        firstLetter = normalize_character(name[0])
        if firstLetter.isalpha():
            entries_by_letter[firstLetter].append(entry)
        else:
            entries_by_letter["D_Other"].append(entry)

    return entries_by_letter


def get_entry_markup(
    id, name, abbr, description, additional_info, display_name=None, aliases=None
):
    display_name = display_name or name

    template = f"""    <idx:entry name="default" scriptable="yes" spell="yes" id="{id}">
      <a id="{id}"></a>

      <dt>
        <idx:orth value="{name}">{display_name}</idx:orth>\n"""

    # Alias
    if aliases:
        for alias in aliases.split(";"):
            template += f'        <idx:orth value="{alias}" />\n'

    template += "      </dt>\n\n"

    # Definition
    template += "      <dd>\n"
    template += f"""        <div><em>{abbr}.</em> {description}</div>"""

    for title, desc in additional_info.items():
        if len(desc) > 0:
            template += f"""\n        <div>
          <strong>{title}:</strong> {desc}
        </div>"""

    template += """\n      </dd>
    </idx:entry>
        
    <hr/>\n\n"""

    return template
