from collections.abc import Callable
from bs4 import BeautifulSoup as Soup, Tag
from logging import getLogger

from rich.console import Group
from html2rich.css_parser.rule_manager import RuleManager

from html2rich.node import Node

logger = getLogger(__name__)


def mock_asset_resolver(filename: str) -> None:
    return None


class Document:
    def __init__(
        self,
        html_str: str | bytes,
        asset_resolver: Callable[[str], str | None] = mock_asset_resolver,
    ) -> None:
        self.css_resolver = RuleManager(asset_resolver=asset_resolver)
        self._soup = Soup(html_str, features="lxml")
        self._resolver = asset_resolver
        head = self.get_head()
        if isinstance(head, Tag):
            styles = head.find_all("link", rel="stylesheet")
            for style in styles:
                href = style.get("href")
                if href is None:
                    continue
                new_style = self._resolver(href)
                if new_style is None:
                    logger.error(f"Failed to fetch {href}")
                    continue
                self.css_resolver.add_stylesheet(new_style)
            for style in self._soup.find_all("style"):
                self.css_resolver.add_stylesheet(style.get_text())

    def get_head(self):
        return self._soup.find("head")

    def get_title(self):
        head = self.get_head()
        if head is None:
            return None
        title_tag = head.find("title")
        if not isinstance(title_tag, Tag):
            return None
        return title_tag.get_text()

    def get_body(self):
        body = self._soup.find("body")
        if not isinstance(body, Tag):
            logger.error("Failed to find the body tag")
            return self._soup
        return body

    def get_displayable_node_tree(self):
        return Group(
            *Node(
                self.get_body(), self.css_resolver.get_nestable_copy()
            ).as_rich()
        )
