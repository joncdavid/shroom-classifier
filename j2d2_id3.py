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
    def __init__(self, db, defs, gain=0, depth=0):
        self.isleaf = False
        self.leafvalue = None
        self.db = db
        self.defs = defs
        self.gain = gain
        self.depth = depth
        self.children = set()
        self.initialize()

    def initialize(self):
        if self.is_homogeneous(self.db):
            self.isleaf = True
            self.leafvalue = mode(self.db)[0]
            return
        gain_table = calc_all_gain(self.db, self.defs)
        recmd_attr, gain = recommend_next_attr(gain_table)
        self.split(recmd_attr, gain)
        
    def is_homogeneous(self, db):
        """Checks if, at this node, all class/labels are homogeneous."""
        unique_labels = set()
        for r in db.records:
            unique_labels.add(r)
        return len(unique_labels) == 1
    
    def split(self, attr, gain):
        """Partitions the dataset about this attribute."""
        #TODO edge case: handling ?-missing values.
        for valid_value in self.defs.attr_values[attr]:
            #get subset of db where attr=valid_value
            subset_records = []
            for r in self.db.records:
                if r.attr_values[attr] == valid_value:
                    subset_db.append(r)
            sub_db = ShroomDatabase(subset_records)
            child_node = ID3Node(sub_db, defs, gain, self.depth+1)
            self.children.add(child_node)

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
    
def calc_distribution_table(vector):
    """Calculates distribution table for some vector."""
    dist_table = {}
    for x in vector:
        if x not in dist_table:
            dist_table[x] = 0
        dist_table[x] += 1
    return dist_table
    
def recommend_next_attr(gain_table):
    """Recommends the attribute with the highest gain as
    the next decision node."""
    highest_gain = max(gain_table.values())
    f_maxtuple = lambda x,y: x if(x[1] >= y[1]) else y
    (attr,gain) = reduce(f_maxtuple, gain_table.items())
    return attr, gain
    
def calc_all_gain(db, defs):
    """Calculates the information gain for all attributes."""
    f = lambda a: (a, calc_gain(a, db, defs))
    gain_table = dict( map(f, defs.attr_set) )
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
    n = len(vector)
    dist_table = calc_distribution_table(vector)
    f_pentropy = lambda x: (-1.0*x[1]/n)*math.log((1.0*x[1]/n),2)
    entropy = sum( map(f_pentropy, dist_table.items()) )
    return entropy
        
