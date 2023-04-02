from typing import Dict, List
from tinycss2 import serialize
from tinycss2.ast import FunctionBlock, IdentToken, Node, WhitespaceToken


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

    @property
    def is_fully_init(self):
        return any(
            isinstance(token, FunctionBlock) and token.name != "var"
            for token in self._tokens
        )

    def feed_rules(self, rules: Dict):
        if self.is_fully_init:
            return
        res = []
        for token in self._tokens:
            if isinstance(token, FunctionBlock) and token.name == "var":
                key = token.arguments[0].value
                new_tokens = rules.get(key)
                if new_tokens:
                    res.extend(new_tokens._tokens)
            else:
                res.append(token)
        self._tokens = res

    def get_rule_text(self):
        if self.is_important():
            return serialize(self._sane_tokens()[:-2]).strip()
        return serialize(self._tokens).strip()

    def __eq__(self, __o: object) -> bool:
        return self.get_rule_text() == __o

    def __repr__(self) -> str:
        return f'<Value "{self.get_rule_text()}" {"important" if self.is_important() else ""}>'
