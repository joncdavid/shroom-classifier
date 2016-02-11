#!/usr/bin/env python
#
# filename: test_id3_tree.py
# authors:  Jon David and Jarrett Decker
# date:     Wednesday, February 10, 2016
#

import pdb

from id3_tree import *

def test_print():
    d1 = ID3DecisionNode('odor', 0.903, 0.0, 0)
    edge_odor1 = ID3Edge('odor', 'a')
    edge_odor2 = ID3Edge('odor', 'p')
    edge_odor3 = ID3Edge('odor', 'n')
    leaf_odor1 = ID3LeafNode('e', 1)
    leaf_odor2 = ID3LeafNode('p', 1)
    
    d2 = ID3DecisionNode('spore-print-color', 0.1378, 0.0, 1)
    edge_spore1 = ID3Edge('spore-print-color', 'u')
    edge_spore2 = ID3Edge('spore-print-color', 'r')
    leaf_spore1 = ID3LeafNode('e', 2)
    leaf_spore2 = ID3LeafNode('p', 2)
    
    d1.print_node()
    edge_odor1.print_edge(d1.depth)
    edge_odor2.print_edge(d1.depth)
    edge_odor3.print_edge(d1.depth)
    leaf_odor1.print_node()
    leaf_odor2.print_node()
    
    d2.print_node()
    edge_spore1.print_edge(d2.depth)
    edge_spore2.print_edge(d2.depth)
    leaf_spore1.print_node()
    leaf_spore2.print_node()

def test_add_node():
    root = ID3DecisionNode('odor', 0.903, 0.0, 0)
    tree = ID3Tree(root)

    edge_odor_a = ID3Edge('odor', 'a')  #almond
    leaf_odor_a = ID3LeafNode('e')
    tree.add_node(root, edge_odor_a, leaf_odor_a)

    edge_odor_p = ID3Edge('odor', 'p')  #pungent
    leaf_odor_p = ID3LeafNode('p')
    tree.add_node(root, edge_odor_p, leaf_odor_p)

    edge_odor_n = ID3Edge('odor', 'n')  #none
    d2 = ID3DecisionNode('spore-print-color', 0.1378, 0.0, 1)
    tree.add_node(root, edge_odor_n, d2)

    edge_spore_u = ID3Edge('spore', 'u')  #purple
    leaf_spore_u = ID3LeafNode('e')
    tree.add_node(d2, edge_spore_u, leaf_spore_u)
    
    edge_spore_r = ID3Edge('spore', 'r')  #green
    leaf_spore_r = ID3LeafNode('p')
    tree.add_node(d2, edge_spore_r, leaf_spore_r)

    edge_spore_w = ID3Edge('spore', 'w')  #white
    d3 = ID3DecisionNode('habitat', 0.2965, 0.0, 2)
    tree.add_node(d2, edge_spore_w, d3)

    edge_habitat_p = ID3Edge('habitat', 'p') #paths
    leaf_habitat_p = ID3LeafNode('e')
    tree.add_node(d3, edge_habitat_p, leaf_habitat_p)

    edge_habitat_u = ID3Edge('habitat', 'u') #urban
    leaf_habitat_u = ID3LeafNode('e')
    tree.add_node(d3, edge_habitat_u, leaf_habitat_u)

    edge_habitat_w = ID3Edge('habitat', 'w') #waste
    leaf_habitat_w = ID3LeafNode('e')
    tree.add_node(d3, edge_habitat_w, leaf_habitat_w)

    tree.update_all_depths()
    tree.print_entire_tree()

def test_add_tree():
    root = ID3DecisionNode('odor', 0.903, 0.0, 0)
    tree = ID3Tree(root)

    edge_odor_a = ID3Edge('odor', 'a')  #almond
    leaf_odor_a = ID3LeafNode('e')
    tree.add_node(root, edge_odor_a, leaf_odor_a)

    edge_odor_p = ID3Edge('odor', 'p')  #pungent
    leaf_odor_p = ID3LeafNode('p')
    tree.add_node(root, edge_odor_p, leaf_odor_p)

    
    edge_odor_n = ID3Edge('odor', 'n')  #none
    d2 = ID3DecisionNode('spore-print-color', 0.1378, 0.0, 1)
    tree2 = ID3Tree(d2)

    edge_spore_u = ID3Edge('spore', 'u')  #purple
    leaf_spore_u = ID3LeafNode('e')
    tree2.add_node(d2, edge_spore_u, leaf_spore_u)

    #pdb.set_trace()
    edge_spore_r = ID3Edge('spore', 'r')  #green
    leaf_spore_r = ID3LeafNode('p')
    tree2.add_node(d2, edge_spore_r, leaf_spore_r)

    edge_spore_w = ID3Edge('spore', 'w')  #white
    d3 = ID3DecisionNode('habitat', 0.2965, 0.0, 2)
    tree2.add_node(d2, edge_spore_w, d3)

    edge_habitat_p = ID3Edge('habitat', 'p') #paths
    leaf_habitat_p = ID3LeafNode('e')
    tree2.add_node(d3, edge_habitat_p, leaf_habitat_p)

    edge_habitat_u = ID3Edge('habitat', 'u') #urban
    leaf_habitat_u = ID3LeafNode('e')
    tree2.add_node(d3, edge_habitat_u, leaf_habitat_u)

    edge_habitat_w = ID3Edge('habitat', 'w') #waste
    leaf_habitat_w = ID3LeafNode('e')
    tree2.add_node(d3, edge_habitat_w, leaf_habitat_w)

#    #pdb.set_trace()

    tree.add_tree(root, edge_odor_n, tree2)
    tree.update_all_depths()
    tree.print_entire_tree()

    
#test_print()
#test_add_node()
#pdb.set_trace()
test_add_tree()

