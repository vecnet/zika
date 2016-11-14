# Copyright (C) 2016, University of Notre Dame
# All rights reserved
from html.parser import HTMLParser


class FindHTMLElementById(HTMLParser):
    """
    Primitive class for finding HTML element with specified id. Used in unit tests mostly.
    If element found, self.tag (string) and self.attributes (dict) are extracted from html
    Based on HTMLParse: https://docs.python.org/2/library/htmlparser.html
    Usage example:
        parser = FindHTMLElementById(id="gender_id")
        parser.feed("<html>...</html>"
        print(parser.is_found)
        print(parser.is_duplicated_id)
        print(parser.tag)
        print(parser.attributes)
    """
    def __init__(self, element_id):
        # HTMLParser is old-style class and doesn't support "super" method
        HTMLParser.__init__(self)
        self.element_id = element_id
        self.tag = None
        self.is_found = False
        self.is_duplicated_id = False
        self.attributes = None

    def handle_starttag(self, tag, attrs):
        """
        This method is called to handle the start of a tag (e.g. <div id="main">).
        https://docs.python.org/2/library/htmlparser.html#HTMLParser.HTMLParser.handle_starttag
        :param tag: the name of the tag converted to lower case
        :param attrs: is a list of (name, value) pairs containing the attributes found inside the tag's <> brackets.
        """
        for attribute, value in attrs:
            if attribute == "id" and value == self.element_id:
                if not self.is_found:
                    self.tag = tag
                    self.is_found = True
                    self.attributes = dict(attrs)
                else:
                    self.is_duplicated_id = True