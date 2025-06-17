import html
from src.utils import escape_text_nodes


def get_entry_markup(
    id, name, abbr, description, additional_info, display_name=None, aliases=None, dict_markup=False
):
    display_name = display_name or name
    template = ""

    if dict_markup:
        template += (
            f'    <idx:entry name="default" scriptable="yes" spell="yes" id="{id}">\n'
        )

    template += f'    <dt><a id="{id}"></a>'

    if dict_markup:
        template += f"""<idx:orth value="{html.escape(name)}">{escape_text_nodes(display_name)}</idx:orth>\n"""

        if aliases:
            for alias in aliases.split(";"):
                template += f'        <idx:orth value="{html.escape(alias)}" />\n'
        template += "      </dt>\n"
    else:
        template += html.escape(display_name)
        template += "</dt>\n"

    # Definition
    template += "      <dd>\n"

    if aliases:
        template += f'        <div>&#11049; {", ".join([html.escape(a.strip()) for a in aliases.split(';')])}</div>\n'

    template += f"""        <div>{f"<em>{html.escape(abbr)}.</em> " if abbr else ""}{escape_text_nodes(description)}</div>"""

    for title, desc in additional_info.items():
        if len(desc) > 0:
            template += f"""\n        <div>
          <strong>{title}:</strong> {desc}
        </div>"""

    template += """\n      <hr/>
    </dd>\n"""

    if dict_markup:
        template += "</idx:entry>\n"

    return template
