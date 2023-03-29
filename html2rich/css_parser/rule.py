from typing import List, Optional
from bs4 import Tag
from tinycss2 import serialize

from tinycss2.ast import Declaration, Node, WhitespaceToken
from tinycss2.parser import QualifiedRule

from html2rich.css_parser.utils import split_array
from html2rich.css_parser.value import Value


class Rule:
    def __init__(
        self,
        selector: Optional[List[Node]] = None,
        rule: Optional[List[Node]] = None,
        declarations: Optional[List[Declaration]] = None,
    ) -> None:
        self._selector = selector
        self._declatations = declarations
        self._rule = rule

    def get_dict(self):
        if not self._declatations:
            declarations = [
                list(split_array(declaration, lambda a: a == ":"))
                for declaration in split_array(self._rule, lambda a: a == ";")
            ]
            return {
                serialize(
                    filter(lambda a: not isinstance(a, WhitespaceToken), key)
                ): Value(value)
                for key, value in filter(lambda a: len(a) == 2, declarations)
            }
        else:
            return {d.lower_name: Value(d.value) for d in self._declatations}

    def __repr__(self) -> str:
        return serialize(
            [
                QualifiedRule(
                    content=self._rule, prelude=self._selector, line=1, column=1
                )
            ]
        )

    def matches(self, tag: Tag) -> int:
        if self._selector is None:
            # This is a rule straight from the tag
            return 999999
        if tag.name == serialize(self._selector):
            return 1
        return -1
