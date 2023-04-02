# html2rich

A simple library to convert html to rich objects, with css support


![image](https://user-images.githubusercontent.com/36668331/229368470-e714a1b1-ecdd-4012-baaa-2227a8437f73.png)


## Features:

- CSS property support
  - margins
  - padding
  - `inline`, `block` and basic `flex` support
  - colors
  - text-alingments
  - `@import` support
  - `var(--css-variables)`
  - clickable links
- HTML:
  - use of external stylesheets, embeded ones and the `style` prop on tags.

## How to use:

```python
from rich import print

from html2rich import Document

document = Document('<p style="color: red">Hello world!</p>')
print(document.get_displayable_node_tree())
```

And you should get:

![image](https://user-images.githubusercontent.com/36668331/229368496-aa35aa63-e9e0-4250-854c-5b069887eb17.png)

### Advanced:

#### Resolvers:

To allow the renderer to access external files, you can supply optional `resolver` function to the `Document` class.
The function should take one argument, which is the path to the file and should return `None` or the string content for the file.

```python
from rich import print

from html2rich import Document

# document with external assets
html = '''
<html>
<head>
    <link rel="stylesheet" href="myStyles.css"/>
</head>
<body>
    <p>I am blue</p>
</body>
</html>
'''

def resolver(file_name: str):
    if file_name == "myStyles.css":
        return "p { color: blue }"

document = Document(html, resolver)
print(document.get_displayable_node_tree())
```
