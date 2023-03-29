from typing import List
from tinycss2 import serialize
from tinycss2.ast import IdentToken, Node, WhitespaceToken


class Value:
    def __init__(self, tokens: List[Node]) -> None:
        self._tokens = tokens

    def _sane_tokens(self):
        return list(
            filter(lambda a: not isinstance(a, WhitespaceToken), self._tokens)
        )

    def is_important(self):
        sane_tokens = self._sane_tokens()
        if len(sane_tokens) > 2:
            mark, text = sane_tokens[-2:]
            if (
                mark == "!"
                and isinstance(text, IdentToken)
                and text.lower_value == "important"
            ):
                return True
        return False

    def get_rule_text(self):
        if self.is_important():
            return serialize(self._sane_tokens()[:-2]).strip()
        return serialize(self._tokens).strip()

    def __eq__(self, __o: object) -> bool:
        return self.get_rule_text() == __o

    def __repr__(self) -> str:
        return f'<Rule "{self.get_rule_text()}" {"important" if self.is_important() else ""}>'
