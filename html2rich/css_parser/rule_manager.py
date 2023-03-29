from bs4 import Tag
from tinycss2 import parse_declaration_list
from html2rich.css_parser.default_stylesheet import (
    default as default_stylesheet,
)
from html2rich.css_parser.parse_file import (
    parse_file_into_rules,
    parse_qualified_rule,
)
from html2rich.css_parser.rule import Rule


class RuleManager:
    def __init__(self, add_default_stylesheet=True, rules=None) -> None:
        self.rules = [] if rules is None else rules
        if add_default_stylesheet:
            self.add_stylesheet(default_stylesheet)

    def add_stylesheet(self, stylesheet_string: str):
        self.rules.extend(parse_file_into_rules(stylesheet_string))

    def add_tag_rule(self, tag: Tag):
        style = tag.get("style")
        if style is None:
            return
        declarations = parse_declaration_list(
            style, skip_comments=True, skip_whitespace=True
        )
        rule = Rule(declarations=declarations)
        self.rules.append(rule)

    def resolve_rules(self, tag: Tag):
        rules = list(
            filter(
                lambda a: a[0] > 0,
                [(rule.matches(tag), rule) for rule in self.rules],
            )
        )
        rules.sort(key=lambda a: a[0])
        res = {}
        for _, rule in rules:
            for key, value in rule.get_dict().items():
                # handle important
                res[key] = value.get_rule_text()
        return res

    def get_nestable_copy(self):
        return RuleManager(
            add_default_stylesheet=False, rules=self.rules.copy()
        )
