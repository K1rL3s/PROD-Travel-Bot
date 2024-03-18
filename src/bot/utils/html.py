import html


def html_quote(value: str) -> str:
    if not isinstance(value, str):
        return value
    return html.escape(value, quote=False)
