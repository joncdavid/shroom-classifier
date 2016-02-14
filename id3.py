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
from id3_util import *
from id3_tree import *

    
def id3(criteria, db, target_attr, attributes, defs,
        chi_table, CI="0%", ignore=None):
    v = db.fetch_class_vector()
    homogeneous, label = is_homogeneous(v)
    if(homogeneous):
        return ID3Tree( ID3LeafNode(label) )
    if len(attributes) == 0:
        label = mode2(db.records, target_attr)[0]
        return ID3Tree( ID3LeafNode(label) )

    A, stat = criteria.recommend_next_attr(attributes, db, defs)
    decision_node = None
    if isinstance(criteria, InformationGainCriteria):
        decision_node = ID3DecisionNode(A, stat, 0.0)
    else:
        decision_node = ID3DecisionNode(A, 0.0, stat)
         
    tree = ID3Tree(decision_node)
    for v in defs.attr_values[A]:
        #if(v == "?"):
        #    continue
        
        chi_squared = calc_chi_squared(A, defs, db)
        dof = len(defs.attr_values[A])
        if CI != "0%" and should_prune(chi_squared, dof, CI, chi_table):
            label = mode2(db.records, target_attr)[0]
            return ID3Tree( ID3LeafNode(label))

        edge = ID3Edge(A, v)
        subset_db = filter_subset(db, A, v) #"?") #removed guard to improve acc.
        subset_records = subset_db.records
        if len(subset_records) == 0:
            label = mode2(db.records, 'class')[0]
            leaf_node = ID3LeafNode(label)
            tree.add_node(decision_node, edge, leaf_node)
        else:
            subattributes = attributes - set([A])
            subset_db = ShroomDatabase(subset_records)
            subtree = id3(criteria, subset_db, target_attr,
                          subattributes, defs, chi_table, CI)
            tree.add_tree(decision_node, edge, subtree)
    return tree
