from typing import Dict, Literal
from math import ceil


def separateUnit(string):
    """
    Separates the unit and number in given string
    e.g. '1 em' will return (float(1), 'em')
    """
    # create an array of valid numbers (and '.')
    nums = ["."] + [str(x) for x in range(10)]
    num_str = str()
    unit_str = str()
    # find first char in string that is not a number or '.', split the string on it
    for i in range(len(string)):
        if string[i] not in nums:
            num_str = string[: i - 1]
            unit_str = string[i - 1 :]
    if num_str == str():
        num_str = string
    return float(num_str), unit_str


def unitConverter(entry):
    """
    converts absolute and some relative css units (cm, mm, em etc.) to
    number of newlines or spaces
    If the unit is not supported or the argument is not valid → returns 0
    """
    entry = str(entry)
    try:
        if entry.strip() in ["0", "auto", None, str()]:
            return 0
        # declare the dict - conversion table
        unit_to_char_dict = {
            "em": 1,
            "ex": 1,
            "ch": 1,
            "rem": 2,
            "cm": 5,
            "mm": 0.5,
            "in": 12.7,
            "px": 0.13,
            "pt": 0.18,
            "pc": 0.014,
        }
        num, unit = separateUnit(entry.strip())
        try:
            return ceil(num * unit_to_char_dict[unit])
        except KeyError:
            return 0
    except ValueError:
        return 0


def parse_spacings(
    rules: Dict, spacing_prefix: Literal["margin"] | Literal["padding"]
):
    def prefix(suffix):
        return f"{spacing_prefix}-{suffix}"

    spacings = {
        "top": None,
        "right": None,
        "bottom": None,
        "left": None,
    }
    if base_rule := rules.get(spacing_prefix):
        base_rule = base_rule.split(" ")
        spacings["top"] = base_rule[0]
        spacings["right"] = (
            base_rule[1] if len(base_rule) > 1 else spacings["top"]
        )
        spacings["bottom"] = (
            base_rule[2] if len(base_rule) > 2 else spacings["top"]
        )
        spacings["left"] = (
            base_rule[3] if len(base_rule) > 3 else spacings["right"]
        )

    for direction in spacings.keys():
        if value := rules.get(prefix(direction)):
            spacings[direction] = value

    fancy_spacings = {
        "block-start": "top",
        "block-end": "bottom",
        "inline-start": "left",
        "inline-end": "right",
    }

    for direction in fancy_spacings.keys():
        if value := rules.get(prefix(direction)):
            spacings[fancy_spacings[direction]] = value

    return tuple(
        map(
            unitConverter,
            [
                spacings["top"],
                spacings["right"],
                spacings["bottom"],
                spacings["left"],
            ],
        )
    )
