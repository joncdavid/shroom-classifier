#!/usr/bin/env python
#
# filename: id3.py
# authors:  Jon David and Jarrett Decker
# date:     Wednesday, February 10, 2016
#

import pdb
import abc
import math

from datadef import ShroomDefs
from database import ShroomDatabase
from id3_tree import *

    
def id3(criteria, db, target_attr, attributes, defs):
    v = db.fetch_class_vector()
    homogeneous, label = is_homogeneous(v)
    if(homogeneous):
        return ID3Tree( ID3LeafNode(label) )
    if len(attributes) == 0:
        label = mode2(examples, target_attr)[0]
        return ID3Tree( ID3LeafNode(label) )

    A, stat = criteria.recommend_next_attr(attributes, db, defs)
    decision_node = None
    if isinstance(criteria, InformationGainCriteria):
        decision_node = ID3DecisionNode(A, stat, 0.0)
    else:
        decision_node = ID3DecisionNode(A, 0.0, stat)
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
            subtree = id3(criteria, subset_db, target_attr,
                          subattributes, defs)
            tree.add_tree(decision_node, edge, subtree)
    return tree


class SelectionCriteria(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        return

    @abc.abstractmethod
    def recommend_next_attr(self, attributes, db, defs):
        """Returns the recommended attribute, and criteria."""
        return

class InformationGainCriteria(SelectionCriteria):
    def __init__(self):
        super(self.__class__, self).__init__()

    def recommend_next_attr(self, attributes, db, defs):
        """Recommends the attribute with the highest gain as
        the next decision node."""
        gain_table = calc_all_gain(attributes, db, defs)
        best_attr = None
        highest_gain = 0.0
        for attr in gain_table:
            gain = gain_table[attr]
            if(gain > highest_gain):
                best_attr, highest_gain = attr, gain
        return best_attr, highest_gain
        

class ClassificationErrorCriteria(SelectionCriteria):
    def __init__(self):
        super(self.__class__, self).__init__()

    def recommend_next_attr(self, attributes, db, defs):
        """Recommends the attribute with the minimum
        classification error as the next decision node."""
        misclass_table = calc_all_class_error(attributes, db, defs)        
        best_attr = None
        #min_classify_error = 1.0  #wait, are we minimizing
        min_classify_error = 0.0   #or maximizing?  Right now it
                                   #looks like maximizes works...
                                   #but I think we're supposed to
                                   #be minimizing. Maybe there's
                                   #a logic inversion somewhere.
        # gain and misclass produce different trees.
        # is that expected?
        for attr in misclass_table:
            classify_error = misclass_table[attr]
            #if(classify_error < min_classify_error):
            if(classify_error > min_classify_error):    
                best_attr = attr
                min_classify_error = classify_error
        return best_attr, min_classify_error

        
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
        
def calc_all_class_error(attributes, db, defs):
    """Calculates the classification error for all attributes of a ShroomDatabase."""
    tot_len = len(db.fetch_class_vector())
    class_error_table = dict()
    class_error_before = calc_class_error(db.fetch_class_vector())
    for attr in attributes:
        interim_db_list = []
        for symbol in defs.attr_values[attr]:
            interim_list = []
            for r in db.records:
                if r.attributes[attr] == symbol:
                    interim_list.append(r)
            interim_db_list.append(ShroomDatabase(interim_list))
        interim_class_error = 0
        for idb in interim_db_list:
            vec = idb.fetch_class_vector()
            interim_class_error += (len(vec) / tot_len * calc_class_error(vec))
        class_error_after = class_error_before - interim_class_error
        class_error_table[attr] = class_error_after
    return class_error_table

def calc_class_error(vector):
    """Calculates the classification error for some vector."""
    n = len(vector)
    if n == 0:
        return 1
    table = dict()
    for v in vector:
        if (v in table.keys()) == False:
            table[v] = 0
        table[v] += 1
    for k in table.keys():
        table[k] /= (1.0)*n
    error = 1.0 - max(table.values())
    return error

