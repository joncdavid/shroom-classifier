#!/usr/bin/env python
#
# filename: j2d2_id3.py
# authors:  Jon David and Jarett Decker
# date:     Wednesday, February 3, 2016
#

import math
from j2d2_datadef import ShroomDefs
from j2d2_database import ShroomDatabase

class ID3Tree:
    LEAF_STR="{}is-leaf:{}, leaf-value:{}, depth:{}"
    DECISION_STR="{}attr:{}={}, gain:{}, depth:{}"
    
    def __init__(self, root):
        self.root = root
        set_depth(root, 0)

    def print_tree(self):
        """Recursively prints this tree."""
        self._print_tree(self.root)
        
    def _print_tree(self, root):
        """Recursively prints the tree represented by root."""
        if not root:
            return
        
        offset = "\t"*root.depth
        if root.isleaf:
            print ID3Tree.LEAF_STR.format(offset,
                                          root.isleaf,
                                          root.label,
                                          root.depth)
            return
        print ID3Tree.DECISION_STR.format(offset,
                                          root.parent_attr,
                                          root.parent_attr_val,
                                          root.gain,
                                          root.depth)
#        print "num childrens: ", len(root.children)
        for child in root.children:
            self._print_tree(child)

def set_depth(node, depth):
    if not node:
        return
    
    node.depth = depth
    for child in node.children:
        set_depth(child, depth+1)
    
def id3(db, target_attr, attributes, defs):
#   print "\n========"
    root = ID3Node()
    v = db.fetch_class_vector()
    is_homogeneous, label = root.is_homogeneous(v)
    if(is_homogeneous):
        root.label = label
        root.isleaf = True
#        print "homogeneous. mode:{}".format(label)
        return root
    if len(attributes) == 0:
        root.label = mode2(examples, target_attr)[0]
        root.isleaf = True
#        print "empty attributes. mode:{}".format(root.label)
        return root

    gain_table = calc_all_gain(db, defs)
    A, gain = recommend_next_attr(gain_table)
#    print "Recommended A:{}, gain:{}.".format(A,gain)
    
    root.decision_attr = A
    for v in defs.attr_values[A]:
#        print "A:{} == ai:{}".format(A,v)
        node = ID3Node()
        node.parent_attr = A
        node.parent_attr_val = v
        node.gain = gain
        root.children.append(node)
        subset_records = []
        for x in db.records:
            if x.attributes[A] == v:
                subset_records.append(x)

#        print "|S|={}, |Sv|={}.".format(len(db.records),
#                                        len(subset_records))
        if len(subset_records) == 0:
            leafnode = ID3Node()
            leafnode.isleaf = True
            leafnode.label = mode2(db.records, 'class')[0]
#            print "leafnode. label:{}".format(leafnode.label)
            root.add_child(node)
        else:
            subattributes = filter(lambda x: x != A, attributes)
#            print "|A|={}, |A-a|={}.".format(len(attributes),
#                                             len(subattributes))
            subset_db = ShroomDatabase(subset_records)
            subtree = id3(subset_db, target_attr, attributes, defs)
            root.add_child(subtree)
    return root
            

class ID3Node:
    def __init__(self, depth=0):
        self.isleaf = False
        self.label = None
        self.decision_attr = None
        self.parent_attr = None
        self.parent_attr_val = None
        self.gain = 0.0
        self.depth = depth
        self.children = []

    def add_child(self, node):
        self.children.append(node)
        
    def is_homogeneous(self, vector):
        """Checks if, at this node, all class/labels are homogeneous."""
        unique_labels = set()
        for v in vector:
            unique_labels.add(v)
        if len(unique_labels) == 1:
            return True, list(unique_labels)[0]
        return False, None

    
    

# End of class ID3Node
#--------------------------------------------------------------------

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
        
