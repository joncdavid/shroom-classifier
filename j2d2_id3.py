#!/usr/bin/env python
#
# filename: j2d2_id3.py
# authors:  Jon David and Jarett Decker
# date:     Wednesday, February 3, 2016
#

import math
from j2d2_datadef import ShroomDefs
from j2d2_database import ShroomDatabase


class ID3Node:
    def __init__(self, db, defs):
        self.isleaf = False
        self.leafvalue = None
        self.db = db
        self.defs = defs
        self.children = set()
        self.initialize()

    def initialize(self):
        if self.is_homogeneous(self.db):
            self.isleaf = True
            self.leafvalue = mode(self.db)[0]
            return
        gain_table = calc_all_gain(self.db, self.defs)
        recmd_attr = recommend_next_attr(gain_table)
        self.split(recmd_attr)
        
    def is_homogeneous(self, db):
        """Checks if, at this node, all class/labels are homogeneous."""
        unique_labels = set()
        for r in db.records:
            unique_labels.add(r)
        return len(unique_labels) == 1
    
    def split(self, attr):
        """Partitions the dataset about this attribute."""
        #TODO edge case: handling ?-missing values.
        for valid_value in self.defs.attr_values[attr]:
            #get subset of db where attr=valid_value
            subset_records = []
            for r in self.db.records:
                if r.attr_values[attr] == valid_value:
                    subset_db.append(r)
            sub_db = ShroomDatabase(subset_records)
            self.children.add(sub_db, defs)

# End of class ID3Node
#--------------------------------------------------------------------

def mode(db, attr=None):
    """Finds the most common value for a particular attribute.
    If attr=None, find the mode of the class/label"""
    v = []
    if attr: v = db.fetch_attr_vector(attr)
    elif attr is None: v = db.fetch_class_vector(attr)
    
    disttable = calc_disttable(v)
    highest_freq = max(disttable.values())
    mode = []  #because some might be tied 
    for x in disttable:
        if disttable[x] == highest_freq:
            mode.append(x)
    return mode
    
def calc_disttable(vector):
    """Calculates distribution table for some vector."""
    disttable = {}
    for x in vector:
        if x not in disttable:
            disttable[x] = 0
        disttable[x] += 1
    return disttable
    
def recommend_next_attr(gain_table):
    """Recommends the attribute with the highest gain as
    the next decision node."""
    recommended_attr = None
    highest_gain = 0.0
    for attr in gain_table:
        gain = gain_table[attr]
        if gain > highest_gain:
            highest_gain = gain
            recommended_attr = attr
    return recommended_attr, highest_gain
    
def calc_all_gain(db, defs):
    """Calculates the information gain for all attributes."""
    gain_table = {}
    for a in defs.attr_set:
        gain_table[a] = calc_gain(a, db, defs)
    return gain_table
        
def calc_gain(attr, db, defs):
    """Calculates information gain on this attribute."""
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

def calc_entropy(vector):
    """Calculates entropy for some vector."""
    num_elements = len(vector)
    disttable = calc_disttable(vector)
    acc_entropy = 0.0000
    for x in disttable:
        p = 1.0*disttable[x]/num_elements
        entropy = -1.0*p*math.log(p,2)
        acc_entropy += entropy
    return acc_entropy
        
