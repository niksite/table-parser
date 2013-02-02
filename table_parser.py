#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Description:
HTML tables parsing is now as easy as:

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

You may also use data type specifiers:

table = table_parse(html, headers=['Res ID|string|reservation_id', 'Client ID|string|client_id', 'Res Date|date|timestamp', 'Pick-Up Date|date|arrival', 'Pick-Up Location|string|place', 'Status|string|status', 'Email|email|email', 'Net Due|money|revenue', 'Total|money|value'])


History:
   * 2011-08-22 Initial commit to coogle code. Version 0.2 released.
   * 2010-12-14T22:13:21+0300 Initial commit. Version 0.1 released.
"""

__author__ = 'Nikolay Panov (author@niksite.ru)'
__license__ = 'GPLv3'
__version__ = 0.2
__updated__ = '2011-08-22 12:20:54 nik'

from dateutil.parser import parse as date_parse
import lxml.html
import logging
import re


def value_parse(header, value, header_type):
    ascii_filter = re.compile('[^\w\.\,\:\?\!@]+')
    date_filter = re.compile('[^\w \/]')
    float_filter = re.compile('[^\d.]')
    int_filter = re.compile('\D')
    text_value = value.text_content()
    # html_value = lxml.html.tostring(value)
    if header_type == 'date':
        # try to parse it as date
        value = date_filter.sub(' ', text_value).strip()
        value = date_parse(value)
    elif header_type == 'link':
        value = value.cssselect('a')
        value = value[0].attrib['href']
    elif header_type == 'email':
        value = text_value.lower().strip()
    elif header_type == 'float':
        try:
            value = float(float_filter.sub('', text_value).strip())
        except:
            value = 0
    elif header_type == 'int':
        try:
            value = int(int_filter.sub('', text_value).strip())
        except:
            value = 0
    elif header_type == 'money':
        try:
            value = round(float(float_filter.sub('', text_value).strip()), 2)
        except:
            value = 0.00
    else:
        value = ascii_filter.sub(' ', text_value).strip()
    return value


def table_parse(html, headers=[], loglevel=logging.WARNING):
    logger = logging.getLogger('table_parser')
    logger.setLevel(loglevel)
    logger.manager.emittedNoHandlerWarning = True
    doc = lxml.html.document_fromstring(html)
    logger.debug('headers: %s' % headers)
    result = []
    name_converting = {}
    if headers:
        tmp_headers = {}
        for header in headers:
            try:
                name, template, newname = header.split('|')
            except:
                name, template, newname = header, 'string', header
            tmp_headers[name] = template
            name_converting[name] = newname
        headers = tmp_headers
    else:
        return {}
    for table in doc.cssselect('table'):
        if len(table.cssselect('table')) > 1:
            continue  # this table include another tables
        if headers and not all([header in table.text_content() for header in headers]):
            continue  # this table has no required headers
        logger.debug('parsing table %s' % ([header in table.text_content() for header in headers]))
        table_headers = []
        result_dict = {}
        for tr in table.cssselect('tr'):
            if all([header in tr.text_content() for header in headers]):
                # this is header of this table
                table_headers = []
                for td in tr.cssselect('td,th'):
                    if td.attrib.get('colspan'):
                        for i in range(int(td.attrib.get('colspan'))):
                            table_headers.append(td.text_content().strip())
                    else:
                        table_headers.append(td.text_content().strip())
                logger.debug('we have the following headers: %s' % table_headers)
                continue
            if table_headers:
                # this is not a headers line
                table_cols = [td for td in tr.cssselect('td')]
                # logger.debug('table_cols len=%s, table_headers len=%s' % (len(table_cols), len(table_headers)))
                if len(table_cols) == len(table_headers):
                    result_dict = {}
                    for i, table_header in enumerate(table_headers):
                        value = table_cols[i]
                        if table_header in headers:
                            value = value_parse(table_header, value, headers[table_header])
                            result_dict[name_converting[table_header]] = value
                    result.append(result_dict)
            else:
                # it seems like vertical table design
                for header in headers:
                    if header in tr.text_content() and len(tr.cssselect('td')) > 1:
                        table_header = tr.cssselect('td')[0].text_content().strip()
                        logger.debug('we have found header %s (table_header=%s)' % (header, table_header))
                        if table_header == header:
                            value = value_parse(table_header, tr.cssselect('td')[1], headers[table_header])
                            result_dict[name_converting[table_header]] = value
        if result_dict not in result:
            result.append(result_dict)
    return result


if __name__ == '__main__':
    from optparse import OptionParser

    logging.basicConfig()
    parser = OptionParser(usage="%prog [-q] [-t <headers>] <filename or url>", version=str(__version__))
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print debug messages to stdout")
    parser.add_option("-t", "--headers",
                      action="append", type="string", dest="headers",
                      help="list of headers of the table you need to be parsed")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("you have missed url")
    filename_or_url = args[0]
    if filename_or_url.startswith('http:'):
        # download...
        pass
    else:
        html = '\n'.join(open(filename_or_url).readlines())
    if options.verbose:
        print '%s -> %s' % (filename_or_url, table_parse(html, headers=options.headers, loglevel=logging.DEBUG))
    else:
        print table_parse(html, headers=options.headers, loglevel=logging.WARNING)



# Emacs:
# Local variables:
# time-stamp-pattern: "100/^__updated__ = '%%'$"
# End:
