import html
from src.utils import escape_text_nodes


def get_entry_markup(
    id,
    name,
    abbr,
    description,
    additional_info,
    additional_info_extended=None,
    display_name=None,
    aliases=None,
    dict_markup=False,
):
    display_name = display_name or name
    template = ""

    if dict_markup:
        template += f"""    <idx:entry name="default" scriptable="yes" spell="yes" id="{id}">
      <idx:short>\n"""
    else:
        template += "    <div>\n"

    template += f'      <a id="{id}"></a>\n'

    if dict_markup:
        template += f"""<idx:orth value="{html.escape(name)}"><strong>{escape_text_nodes(display_name)}</strong></idx:orth>\n"""

        if aliases:
            for alias in aliases.split(";"):
                template += f'        <idx:orth value="{html.escape(alias)}" />\n'
        template += "\n"
    else:
        template += f"      <strong>{html.escape(display_name)}</strong>\n"
        template += "    </div>\n\n"

    # Definition
    template += '    <div class="definition">\n'

    template += f"""      <div>{f"<em>{html.escape(abbr)}.</em> " if abbr else ""}{escape_text_nodes(description)}</div>"""

    for title, desc in additional_info.items():
        if len(desc) > 0:
            template += f"""\n      <div>
          <strong>{title}:</strong> {desc}
      </div>\n"""

    template += "    </div>\n"

    if dict_markup:
        template += "</idx:short>\n"

    if additional_info_extended:
        template += '    <div class="extended-definition">'

        for title, desc in additional_info_extended.items():
            if len(desc) > 0:
                template += f"""\n          <div>
            <strong>{title}:</strong> {desc}
            </div>"""

        template += "</div>\n"

    if dict_markup:
        template += "  </idx:entry>\n\n"
        template += "  <hr/>\n\n"
    else:
        template += "  <hr/>\n\n"

    return template
