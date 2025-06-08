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
    template += (
        f"""        <div>{f"<em>{abbr}.</em> " if abbr else ""}{description}</div>"""
    )

    for title, desc in additional_info.items():
        if len(desc) > 0:
            template += f"""\n        <div>
          <strong>{title}:</strong> {desc}
        </div>"""

    template += """\n      </dd>
    </idx:entry>
        
    <hr/>\n\n"""

    return template
