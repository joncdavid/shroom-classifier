#!/usr/bin/env python
#
# filename: id3_v2.py
# authors:  Jon David and Jarrett Decker
# date:     Wednesday, February 10, 2016
#

import pdb
import math

from datadef import ShroomDefs
from database import ShroomDatabase
from id3_tree import *

    
def id3(db, target_attr, attributes, defs):
    v = db.fetch_class_vector()
    homogeneous, label = is_homogeneous(v)
    if(homogeneous):
        return ID3Tree( ID3LeafNode(label) )
    if len(attributes) == 0:
        label = mode2(examples, target_attr)[0]
        return ID3Tree( ID3LeafNode(label) )

    gain_table = calc_all_gain(attributes, db, defs)
    A, gain = recommend_next_attr(gain_table)
    
    decision_node = ID3DecisionNode(A, gain, 0.0)
    tree = ID3Tree(decision_node)
    for v in defs.attr_values[A]:
        edge = ID3Edge(A, v)
        subset_records = []
        for x in db.records:
            if ((x.attributes[A] == v) and
                (x.attributes[A] != '?')):
                subset_records.append(x)

        if len(subset_records) == 0:
            label = mode2(db.records, 'class')[0]
            leaf_node = ID3LeafNode(label)
            tree.add_node(decision_node, edge, leaf_node)
        else:
            subattributes = attributes - set([A])
            subset_db = ShroomDatabase(subset_records)
            subtree = id3(subset_db, target_attr, subattributes, defs)
            tree.add_tree(decision_node, edge, subtree)
    return tree
            

#---- Utility Functions ---------------------------------------------

def is_homogeneous(vector):
    """Checks if, at this node, all class/labels are homogeneous."""
    unique_labels = set()
    for v in vector:
        unique_labels.add(v)
    if len(unique_labels) == 1:
        return True, list(unique_labels)[0]
    return False, None

def mode2(examples, target_attr):
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
    best_attr = None
    highest_gain = 0.0
    for attr in gain_table:
        gain = gain_table[attr]
        if(gain > highest_gain):
            best_attr, highest_gain = attr, gain
    return best_attr, highest_gain
            
    
def calc_all_gain(attributes, db, defs):
    """Calculates the information gain for all attributes."""
    gain_table = dict()
    for a in attributes:
        gain_table.update({a : calc_gain(a, db, defs)})
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
    partial_entropy = []
    for item in dist_table.items():
        p = 1.0*item[1]/n  #proportion
        partial_entropy.append((-1*p) * math.log((1.0*p), 2))
    entropy = sum(partial_entropy)
    return entropy
        
