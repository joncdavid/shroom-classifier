#!/usr/bin/env python
#
# filename: j2d2_id3.py
# authors:  Jon David and Jarett Decker
# date:     Wednesday, February 3, 2016
#

import math
from j2d2_datadef import ShroomDefs
from j2d2_database import ShroomDatabase


def calc_entropy(vector):
    """Calculates entropy for some vector."""
    disttable = {}
    for x in vector:
        if x not in disttable:
            disttable[x] = 0
        disttable[x] += 1
    num_elements = len(vector)
    
    acc_entropy = 0.0000
    for x in disttable:
        p = 1.0*disttable[x]/num_elements
        entropy = -1.0*p*math.log(p,2)
        acc_entropy += entropy
    return acc_entropy
        
class J2D2Statistics:
    def __init__(self, deffilename, dbfilename):
        self.definitions = ShroomDefs(deffilename)
        self.db = ShroomDatabase(dbfilename)

    def recommend_next_attr(self, gain_table):
        """Recommends the attribute with the highest gain as
        the next decision node."""
        rmend_attr = None
        highest_gain = 0.0
        for attr in gain_table:
            gain = gain_table[attr]
            if gain > highest_gain:
                highest_gain = gain
                rmend_attr = attr
        return rmend_attr, highest_gain
    
    def calc_all_gain(self, db=None):
        """Calculates the information gain for all attributes."""
        if db is None:
            db = self.db
        gain_table = {}
        for a in self.definitions.attr_set:
            gain_table[a] = self.calc_gain(a, db)
        return gain_table
        
    def calc_gain(self, attr, db=None, defs=None):
        """Calculates information gain on this attribute."""
        if db is None:
            db = self.db
        if defs is None:
            defs = self.definitions
            
        cv = db.fetch_class_vector()
        entropy_before = calc_entropy(cv)

        entropy_after = 0.0000
        for symbol in defs.attr_values[attr]:
            expected_cv = []
            for r in db.records:
                if r.attributes[attr] == symbol:
                    expected_cv.append(r.label)            
            attr_entropy = calc_entropy(expected_cv)
            attr_entropy *= 1.0*len(expected_cv)/len(cv)
            entropy_after += attr_entropy

        gain = entropy_before - entropy_after
        return gain

