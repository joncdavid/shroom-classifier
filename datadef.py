#!/usr/bin/env python
#
# filename: datadef.py
# authors:  Jon David and Jarett Decker
# date:     Wednesday, February 3, 2016
#

import re


class ShroomDefs:
    """
    Mushroom's are either edible(e), or poisonous(p), are are
    often described with attributes like cap shape, or cap color.

    This class defines the set of valid labels, attributes, and
    values. It also provides functions to verify attribute values.
    """

    DEFAULT_DEF_FILENAME = "_shroom.data.definition"
    
    def __init__(self, filename=DEFAULT_DEF_FILENAME):
        self.class_set = set()
        self.class_values = dict()
        self.attr_set = set()
        self.attr_values = dict()
        self.load_definition(filename)

    
    def verify_symbol(self, attr, symbol):
        """Verifies if symbol is a valid attribute value"""
        return symbol in self.attr_values[attr]

    def get_pretty_string(self, attr, symbol):
        """
        Returns the printer-friendly string representation of
        a symbol, for some attribute.
        """
        if attr=='class':
            return self.class_values[symbol]
        return self.attr_values[attr][symbol]

    def load_definition(self, filename):
        """Loads data definition from <filename>"""
        with open(filename, 'r') as f:
            for line in f:
                regex = r'(class|attribute)\s*=\s*([\w-]*)\s*{(.*)}'
                matchObj = re.search(regex, line)
                
                if not matchObj:
                    continue

                (ttype, name, pairs) = matchObj.groups()
                ttype = ttype.strip()
                name = name.strip()
                pairs = pairs.strip()
                if ttype == 'class':
                    for pair in pairs.split(','):
                        symbol,text = pair.strip().split(':')
                        self.class_set.add(symbol)
                        self.class_values.update({symbol:text})
                elif ttype == 'attribute':
                    self.attr_set.add(name)
                    for pair in pairs.split(','):
                        symbol,text = pair.strip().split(':')
                        if name not in self.attr_values:
                            self.attr_values[name] = {}
                        self.attr_values[name].update({symbol:text})
