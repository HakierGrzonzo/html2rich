from sys import argv
from rich import print

from .document import Document

document = Document(open(argv[1]).read())
tree = document.get_displayable_node_tree()
print(tree)
