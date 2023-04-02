import logging
from tinycss2 import parse_stylesheet
from tinycss2.ast import AtRule, QualifiedRule
from html2rich.css_parser.rule import Rule
from html2rich.css_parser.selector import strip_whitespace

from html2rich.css_parser.utils import split_array

logger = logging.getLogger(__name__)


def parse_qualified_rule(rule: QualifiedRule):
    selectors = split_array(
        rule.prelude,
        lambda a: a == ",",
    )
    for selector in selectors:
        yield Rule(selector, rule.content)


def parse_file_into_rules(stylesheet: str):
    style = parse_stylesheet(
        stylesheet, skip_comments=True, skip_whitespace=True
    )
    for rule in style:
        if isinstance(rule, QualifiedRule):
            yield from parse_qualified_rule(rule)
        elif isinstance(rule, AtRule):
            if rule.lower_at_keyword == "import":
                tokens = strip_whitespace(rule.prelude)
                if len(tokens) != 1:
                    logger.error("Failed to parse import rule")
                    continue
                url = tokens[0].value
                imported = yield url
                if imported is None:
                    logger.warning(f"Failed to resolve {url}")
                    continue
                yield from parse_file_into_rules(imported)
