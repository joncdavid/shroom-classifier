#!/usr/bin/env python
#
# filename: id3_rules.py
# authors:  Jon David and Jarrett Decker
# date:     Saturday, February 13, 2016
#

import abc
import pdb

from id3_tree import *


class ID3Condition(object):
    COND_STR = "({}={})"

    def __init__(self, attr, attr_val):
        self.attr = attr
        self.attr_val = attr_val
        
    def __str__(self):
        """Gets the string representation of a condition."""
        return self.COND_STR.format(self.attr, self.attr_val)

    def __repr__(self):
        return str(self)

    
class ID3Rule(object):
    """A classification rule in IF antecedent, THEN consequent form."""
    RULE_STR = "IF ({}), THEN {}."

    def __init__(self, consequence=None):
        self.antecedent = []
        self.consequence = consequence

    def __str__(self):
        """Returns the if-then string representation of this rule."""
        cond_str_list = []
        for condition in self.antecedent:
            cond_str_list.append( str(condition) )
        all_cond_str = " AND ".join(cond_str_list)
        rule_str = self.RULE_STR.format(all_cond_str, self.consequence)
        return rule_str

    def __repr__(self):
        return str(self)

    def add_condition(self, id3_condition):
        """Adds condition c to the antecedent."""
        self.antecedent.append(id3_condition)
        
    def print_rule(self):
        """Prints the if-then string representation of this rule."""
        print( str(self) )
