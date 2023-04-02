from typing import Callable
from bs4 import Tag
from tinycss2 import parse_declaration_list
from html2rich.css_parser.default_stylesheet import (
    default as default_stylesheet,
)
from html2rich.css_parser.parse_file import (
    parse_file_into_rules,
)
from html2rich.css_parser.rule import Rule


def mock_asset_resolver(filename: str) -> None:
    return None


class RuleManager:
    def __init__(
        self,
        add_default_stylesheet=True,
        rules=None,
        asset_resolver: Callable[[str], str | None] = mock_asset_resolver,
    ) -> None:
        self.rules = [] if rules is None else rules
        self._resolver = asset_resolver
        if add_default_stylesheet:
            self.add_stylesheet(default_stylesheet)

    def add_stylesheet(self, stylesheet_string: str):
        gen = parse_file_into_rules(stylesheet_string)
        rule = next(gen)
        try:
            while True:
                if isinstance(rule, Rule):
                    self.rules.append(rule)
                    rule = next(gen)
                else:
                    rule = gen.send(self._resolver(rule))
        except StopIteration:
            pass

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
        rules.sort(key=lambda a: -a[0])
        resolved_rules = {}
        for _, rule in rules:
            for key, value in rule.get_dict().items():
                resolved_rules[key] = value

        for rule in resolved_rules.values():
            rule.feed_rules(resolved_rules)
        return {
            key: value.get_rule_text() for key, value in resolved_rules.items()
        }

    def get_nestable_copy(self):
        return RuleManager(
            add_default_stylesheet=False,
            rules=self.rules.copy(),
            asset_resolver=self._resolver,
        )
