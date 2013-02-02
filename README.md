table-parser
============

HTML tables parsing helper.

```python
>>> from table_parser import table_parse
>>> from pprint import pprint
>>> html = fetch_html('http://www.w3schools.com/tags/tag_table.asp')
>>> pprint(table_parse(html, headers=['Attribute', 'Description']))
[{'Attribute': 'align',
  'Description': 'Deprecated. Use styles instead. Specifies the alignment of a table according to surrounding text'},
 {'Attribute': 'bgcolor',
  'Description': 'Deprecated. Use styles instead. Specifies the background color for a table'},
 {'Attribute': 'border',
  'Description': 'Specifies the width of the borders around a table'},
 {'Attribute': 'cellpadding',
  'Description': 'Specifies the space between the cell wall and the cell content'},
 {'Attribute': 'cellspacing',
  'Description': 'Specifies the space between cells'},
 {'Attribute': 'frame',
  'Description': 'Specifies which parts of the outside borders that should be visible'},
 {'Attribute': 'rules',
  'Description': 'Specifies which parts of the inside borders that should be visible'},
 {'Attribute': 'summary',
  'Description': 'Specifies a summary of the content of a table'},
 {'Attribute': 'width', 'Description': 'Specifies the width of a table'},
 {'Attribute': 'class', 'Description': 'Specifies a classname for an element'},
 {'Attribute': 'dir',
  'Description': 'Specifies the text direction for the content in an element'},
 {'Attribute': 'id', 'Description': 'Specifies a unique id for an element'},
 {'Attribute': 'lang',
  'Description': 'Specifies a language code for the content in an element'},
 {'Attribute': 'style',
  'Description': 'Specifies an inline style for an element'},
 {'Attribute': 'title',
  'Description': 'Specifies extra information about an element'},
 {'Attribute': 'xml:lang',
  'Description': 'Specifies a language code for the content in an element, in XHTML documents'},
 {'Attribute': 'onclick', 'Description': 'Script to be run on a mouse click'},
 {'Attribute': 'ondblclick',
  'Description': 'Script to be run on a mouse double click'},
 {'Attribute': 'onmousedown',
  'Description': 'Script to be run when mouse button is pressed'},
 {'Attribute': 'onmousemove',
  'Description': 'Script to be run when mouse pointer moves'},
 {'Attribute': 'onmouseout',
  'Description': 'Script to be run when mouse pointer moves out of an element'},
 {'Attribute': 'onmouseover',
  'Description': 'Script to be run when mouse pointer moves over an element'},
 {'Attribute': 'onmouseup',
  'Description': 'Script to be run when mouse button is released'},
 {'Attribute': 'onkeydown',
  'Description': 'Script to be run when a key is pressed'},
 {'Attribute': 'onkeypress',
  'Description': 'Script to be run when a key is pressed and released'},
 {'Attribute': 'onkeyup',
  'Description': 'Script to be run when a key is released'}]
```

You may also use data type specifiers:

```python
table = table_parse(html, headers=['Res ID|string|reservation_id', 'Client ID|string|client_id', 'Res Date|date|timestamp', 'Pick-Up Date|date|arrival', 'Pick-Up Location|string|place', 'Status|string|status', 'Email|email|email', 'Net Due|money|revenue', 'Total|money|value'])
```
