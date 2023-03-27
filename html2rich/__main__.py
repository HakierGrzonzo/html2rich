from sys import stdin
from rich import print

from .document import Document

document = Document(stdin.read())

print(document.get_displayable_node_tree())
