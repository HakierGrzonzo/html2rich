from bs4 import Tag
from rich.console import Console, ConsoleOptions, RenderResult, group
from rich.padding import Padding

class Node:
    def __init__(self, tag: Tag) -> None:
        self._tag = tag

    @group()
    def get_children(self):
        for child in self._tag.children:
            if isinstance(child, Tag):
                yield Node(child)
            else:
                yield child.get_text()

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        # TODO: handle inline
        margin = Padding(self.get_children())
        yield Padding(margin)
        





