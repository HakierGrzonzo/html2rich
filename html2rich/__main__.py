from sys import argv
from os.path import dirname
from rich import print

from html2rich.resolvers import get_directory_resolver

from .document import Document

file = argv[1]
file_directory = dirname(file)

resolver = get_directory_resolver(file_directory)

document = Document(open(file).read(), resolver)
tree = document.get_displayable_node_tree()
print(tree)
