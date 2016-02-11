#!/usr/bin/env python
#
# filename: id3.py
# authors:  Jon David and Jarett Decker
# date:     Wednesday, February 3, 2016
#

import math
from datadef import ShroomDefs
from database import ShroomDatabase

import pdb

class ID3Tree:
    LEAF_STR="{}is-leaf:{}, leaf-value:{}, depth:{}"
    DECISION_STR="{}attr:{}={}, gain:{}, depth:{}"
    
    def __init__(self, root):
        self.root = root
        self.root.set_depth(0)

    def print_tree(self):
        """Recursively prints this tree."""
        print_tree(self.root)
        
def print_tree(root):
    """Recursively prints the tree represented by root."""
    root.print_node()
    for child in root.children:
        child.print_node()

    
def id3(db, target_attr, attributes, defs):
    #   print "\n======== ID3 ========================="
#    pdb.set_trace()
    root = ID3Node()
    v = db.fetch_class_vector()
    is_homogeneous, label = root.is_homogeneous(v)
    if(is_homogeneous):
        root.label = label
        root.node_type = 'leaf'
        #print "homogeneous. mode:{}".format(label)
        return root
    if len(attributes) == 0:
        root.label = mode2(examples, target_attr)[0]
        root.node_type = 'leaf'
        #print "empty attributes. mode:{}".format(root.label)
        return root

    gain_table = calc_all_gain(attributes, db, defs)
    A, gain = recommend_next_attr(gain_table)
    #print "Recommended A:{}, gain:{}.".format(A,gain)
    
    root.decision_attr = A
    root.label = A
    root.gain = gain
    for v in defs.attr_values[A]:
        #print "A:{} == ai:{}".format(A,v)
        node = ID3Node()
        node.node_type = 'edge'
        node.parent_attr = A
        node.parent_attr_val = v
        node.gain = gain
        subset_records = []
        for x in db.records:
            if ((x.attributes[A] == v) and
                (x.attributes[A] != '?')):
                subset_records.append(x)

        #print "|S|={}, |Sv|={}.".format(len(db.records),
        #                                len(subset_records))
        if len(subset_records) == 0:
            leaf_node = ID3Node()
            leaf_node.node_type = 'leaf'
            leaf_node.label = mode2(db.records, 'class')[0]
            node.add_child(leaf_node)
        else:
            subattributes = attributes - set([A])
            subset_db = ShroomDatabase(subset_records)
            subtree = id3(subset_db, target_attr, subattributes, defs)
            node.add_child(subtree)
        root.add_child(node)
    return root
            

class ID3Node:
    def __init__(self, depth=0):
        self.node_type = 'node'
        self.label = None
        self.decision_attr = None
        self.parent_attr = None
        self.parent_attr_val = None
        self.gain = 0.0
        self.depth = depth
        self.children = []

    def add_child(self, node):
        self.children.append(node)
        node.set_depth(self.depth+1)

    def set_depth(self, depth):
        self.depth = depth
        for child in self.children:
            child.set_depth(depth+1)
        
    def is_homogeneous(self, vector):
        """Checks if, at this node, all class/labels are homogeneous."""
        unique_labels = set()
        for v in vector:
            unique_labels.add(v)
        if len(unique_labels) == 1:
            return True, list(unique_labels)[0]
        return False, None

    NODE_STR = "{}(decision-node (split (attr {}) (gain {}) (depth {})))"
    EDGE_STR = "{}(edge (= {} ({} {})))"
    LEAF_STR = "{}(leaf-node (classify ({} {})) (depth {}))"
    def print_node(self, defs, recursive=False):
        str = None
        #pdb.set_trace()
        offset = "\t" * self.depth
        if self.node_type == 'node':
            str = ID3Node.NODE_STR.format(offset,
                                          self.decision_attr,
                                          self.gain,
                                          self.depth/2)
        elif self.node_type == 'edge':
            pretty_attr_val = defs.get_pretty_string(self.parent_attr,
                                                     self.parent_attr_val)
            str = ID3Node.EDGE_STR.format(offset,
                                          self.parent_attr,
                                          self.parent_attr_val,
                                          pretty_attr_val)
        elif self.node_type == 'leaf':
            pretty_label = defs.get_pretty_string('class',
                                                  self.label)
            str = ID3Node.LEAF_STR.format(offset,
                                          self.label,
                                          pretty_label,
                                          self.depth/2)
        else:
            str = "WARNING: invalid node type: ", self.node_type
        print(str)

        if recursive:
            for child in self.children:
                child.print_node(defs, recursive)
            
    

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
    #highest_gain = max(gain_table.values())
    #f_maxtuple = lambda x,y: x if(x[1] >= y[1]) else y
    #(attr,gain) = reduce(f_maxtuple, gain_table.items())
    #return attr, gain

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
    #f = lambda a: (a, calc_gain(a, db, defs))
    #gain_table = dict( map(f, attributes) )
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
        table[k] /= n
    error = 1 - max(table.values())
    return error