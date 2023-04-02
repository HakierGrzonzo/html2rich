from rich import print

from html2rich import Document

# Simple document
document = Document('<p style="color: red">Hello world!</p>')
print(document.get_displayable_node_tree())

# document with external assets
html = """
<html>
<head>
    <link rel="stylesheet" href="myStyles.css"/>
</head>
<body>
    <p>I am blue</p>
</body>
</html>
"""


def resolver(file_name: str):
    if file_name == "myStyles.css":
        return "p { color: blue }"


document = Document(html, resolver)
print(document.get_displayable_node_tree())
