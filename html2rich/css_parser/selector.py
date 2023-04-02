from bs4 import Tag
from tinycss2.ast import HashToken, IdentToken, Node
from rich import print
from typing import List


def strip_whitespace(tokens: List[Node]) -> List[Node]:
    start = 0
    while tokens[start].type == "whitespace":
        start += 1
    end = -1
    while tokens[end].type == "whitespace":
        end -= 1
    end = end + 1 if end < -1 else None
    return tokens[start:end]


class SimpleSelector:
    def __init__(self, tag_id, classes, tag_name) -> None:
        self.tag_id = tag_id
        self.classes = classes
        self.tag_name = tag_name

    def raw(self) -> str:
        if self.tag_id:
            return f"#{self.tag_id}"
        tmp_list = [
            self.tag_name if self.tag_name is not None else "",
            *self.classes,
        ]
        return ".".join(tmp_list)

    def __repr__(self) -> str:
        return f"<SimpleSelector {self.raw()}/>"

    def strength(self):
        return sum(
            [
                self.tag_id is not None,
                len(self.classes),
                self.tag_name is not None,
            ]
        )

    def match(self, tag: Tag):
        if self.tag_id is not None:
            return tag.get("id") == self.tag_id
        if any(c not in tag.get("class", []) for c in self.classes):
            return False
        if self.tag_name is not None:
            return self.tag_name == tag.name
        return True


class ComplexSelector:
    op = None

    def __init__(self, left: SimpleSelector, right: SimpleSelector) -> None:
        self._left = left
        self._right = right

    def __repr__(self) -> str:
        return f"<ComplexSelector {self._left.raw()} {self.op} {self._right.raw()} />"

    def strength(self):
        return self._left.strength() + self._right.strength()

    def raw(self):
        return self.__repr__()

    def match(self, tag: Tag):
        raise NotImplementedError("Abstract")


class ContainedSelector(ComplexSelector):
    op = " "

    def match(self, tag: Tag):
        root_parent = tag.parent
        while root_parent is not None:
            if self._left.match(root_parent):
                break
            else:
                root_parent = root_parent.parent
        return root_parent is not None and self._right.match(tag)


class ParentSelector(ComplexSelector):
    op = ">"

    def match(self, tag: Tag):
        return self._left.match(tag.parent) and self._right.match(tag)


class FirstAfterSelector(ComplexSelector):
    op = "+"

    def match(self, tag: Tag):
        sibiling = tag.previousSibling
        while not isinstance(sibiling, Tag) and sibiling is not None:
            sibiling = sibiling.previousSibling
        if sibiling is None:
            return False
        return self._left.match(sibiling) and self._right.match(tag)


class AfterSelector(ComplexSelector):
    op = "~"

    def match(self, tag: Tag):
        sibiling = tag.previousSibling
        while sibiling is not None:
            if not isinstance(sibiling, Tag):
                sibiling = sibiling.previousSibling
                continue
            if self._left.match(sibiling):
                break

        return sibiling is not None and self._right.match(tag)


SEPARATORS = {
    " ": lambda a, b: ContainedSelector(a, b),
    ">": lambda a, b: ParentSelector(a, b),
    "+": lambda a, b: FirstAfterSelector(a, b),
    "~": lambda a, b: AfterSelector(a, b),
}


class EverythingSelector:
    def raw(self):
        return "*"

    def strength(self):
        return 1

    def match(self, _):
        return True


def parse_simple_selector(tokens: List[Node]):
    token_gen = iter(tokens)
    classes = []
    tag_id = None
    tag_name = None
    while True:
        try:
            symbol = next(token_gen)
            if symbol == ".":
                className = next(token_gen)
                assert isinstance(className, IdentToken)
                classes.append(className.value)
            elif symbol == ":":
                pseudo_selector = next(token_gen)
                if pseudo_selector.value == "root":
                    return EverythingSelector()
                else:
                    # Ignore traits for now
                    break
            elif symbol == "*":
                return EverythingSelector()
            elif isinstance(symbol, HashToken):
                tag_id = next(token_gen).value
            elif isinstance(symbol, IdentToken):
                tag_name = symbol.value
            else:
                print(symbol)
                raise Exception("Failed to parse token")
        except StopIteration:
            break
    return SimpleSelector(tag_id, classes, tag_name)


def wrap_selectors(tokens: List[Node]):
    accumulator = []
    for token in tokens:
        if (
            token.type in ["whitespace", "literal"]
            and token.value in SEPARATORS
        ):
            yield parse_simple_selector(accumulator)
            yield SEPARATORS[token.value]
            accumulator = []
        else:
            accumulator.append(token)
    if len(accumulator):
        yield parse_simple_selector(accumulator)


def parse_selector(tokens: List[Node]):
    stripped_tokens = strip_whitespace(tokens)
    selectors = wrap_selectors(stripped_tokens)
    selector = None
    while True:
        try:
            selector_or_op = next(selectors)
            if isinstance(selector_or_op, SimpleSelector) or isinstance(
                selector_or_op, EverythingSelector
            ):
                selector = selector_or_op
            else:
                selector = selector_or_op(selector, next(selectors))
        except StopIteration:
            break
    if selector is None:
        raise Exception("failed to parse selector")
    return selector
