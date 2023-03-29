from bs4 import Tag
from rich.console import Group
from rich.padding import Padding
from rich.text import Text

from html2rich.css_parser.rule_manager import RuleManager
from html2rich.utils import rules_as_markup, wrap_strings_into_text


class Node:
    def __init__(self, tag: Tag, css_resolver: RuleManager) -> None:
        self._css_resolver = css_resolver
        self._css_resolver.add_tag_rule(tag)
        self._tag = tag

    def get_children(self, css_rules):
        markup_start, markup_end = rules_as_markup(css_rules)
        for child in self._tag.children:
            if isinstance(child, Tag):
                yield from Node(
                    child, self._css_resolver.get_nestable_copy()
                ).as_rich()
            else:
                yield markup_start + child.get_text() + markup_end

    def as_rich(self):
        # TODO: handle inline
        rules = self._css_resolver.resolve_rules(self._tag)
        display = rules.get("display", "inline")
        if display == "none":
            return
        if display == "block":
            margin = Padding(
                Group(*wrap_strings_into_text(self.get_children(rules)))
            )
            yield Padding(margin)
        elif display == "inline":
            if self._tag.name == "a":
                yield f"[link={self._tag.get('href')}]"
                yield from self.get_children(rules)
                yield "[/]"
            else:
                yield from self.get_children(rules)
