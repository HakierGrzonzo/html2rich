from typing import List, Tuple

from rich.text import Text

from html2rich.colors import colors


def debug_gen(gen):
    for g in gen:
        print(g)
        yield g


def format_color(r, g, b):
    return f"rgb({r},{g},{b})"


DECORATION_MAP = {"underline": "u", "line-through": "s"}


def rules_as_markup(rules) -> Tuple[str, str]:
    tokens = []
    if "bold" in rules.get("font-weight", ""):
        tokens.append("bold")
    if (color := rules.get("color")) is not None:
        converted_color = colors.get(color)
        if converted_color:
            tokens.append(format_color(*converted_color))
        else:
            tokens.append(color)
    if (decoration := rules.get("text-decoration")) is not None:
        decoration = DECORATION_MAP.get(decoration)
        if decoration:
            tokens.append(decoration)

    if rules.get("font-style") == "italic":
        tokens.append("i")

    if len(tokens) > 0:
        return f"[{' '.join(tokens)}]", "[/]"
    return "", ""


def wrap_strings_into_text(elements: List):
    last_string = ""
    for element in elements:
        if not isinstance(element, str):
            if len(last_string):
                yield Text.from_markup(last_string, end="")
                last_string = ""
            yield element
        else:
            last_string += element
    yield Text.from_markup(last_string, end="")
