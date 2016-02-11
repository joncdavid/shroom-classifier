#!/usr/bin/env python
#
# filename: id3_util.py
# authors:  Jon David and Jarett Decker
# date:     Wednesday, February 9, 2016
#
# description:
#   Contains utility functions necessary for building ID3 tree.
#   

import math
from datadef import ShroomDefs
from database import ShroomDatabase

import pdb


def mode2(examples, target_attr):
    """Given a set of examples, finds the most common value
    for a particular attribute."""
    v = []
    db = ShroomDatabase(examples)
    if target_attr=='class':
        v = db.fetch_class_vector()
    else:
        v = db.fetch_class_vector(target_attr)
    return mode(v)
    
def mode(vector):
    """Finds the most common value for a particular attribute.
    If attr=None, find the mode of the class/label"""
    disttable = calc_distribution_table(vector)
    highest_freq = max(disttable.values())
    mode = []  #return a list because some might be tied 
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
    
def calc_all_gain(attributes, db, defs):
    """Calculates the information gain for all attributes."""
    f = lambda a: (a, calc_gain(a, db, defs))
    gain_table = dict( map(f, attributes) )
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
        
def calc_misclassifcation_error():
    """Calculates misclassification for some error."""
    return 0.0
