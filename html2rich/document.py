from bs4 import BeautifulSoup as Soup, Tag
from logging import getLogger

from html2rich.node import Node

logger = getLogger(__name__) 

class Document:
    def __init__(self, html_str: str | bytes) -> None:
        self._soup = Soup(html_str, features="lxml")

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
        return Node(self.get_body())


