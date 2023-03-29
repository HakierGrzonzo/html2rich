from tinycss2 import parse_stylesheet
from tinycss2.ast import QualifiedRule, WhitespaceToken
from html2rich.css_parser.rule import Rule

from html2rich.css_parser.utils import split_array


def parse_qualified_rule(rule: QualifiedRule):
    selectors = split_array(
        [
            rule
            for rule in rule.prelude
            if not isinstance(rule, WhitespaceToken)
        ],
        lambda a: a == ",",
    )
    for selector in selectors:
        yield Rule(selector, rule.content)


def parse_file_into_rules(stylesheet: str):
    style = parse_stylesheet(
        stylesheet, skip_comments=True, skip_whitespace=True
    )
    for rule in style:
        if not isinstance(rule, QualifiedRule):
            continue
        yield from parse_qualified_rule(rule)
