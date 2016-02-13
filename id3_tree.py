#!/usr/bin/env python
#
# filename: id3_tree.py
# authors:  Jon David and Jarrett Decker
# date:     Wednesday, February 10, 2016
#

import abc
import pdb
import math
from datadef import ShroomDefs
from database import ShroomDatabase


class ID3Node(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self, depth=0):
        self.depth = depth

    def __eq__(self, other):
        return self == other
    
    def __ne__(self, other):
        return not self == other
       
    @abc.abstractmethod
    def print_node(self):
        """Prints this node in tab format."""
        return
        

class ID3LeafNode(ID3Node):
    def __init__(self, classification, depth=0):
        super(self.__class__, self).__init__(depth)
        self.classification = classification

    def __eq__(self, other):
        return self.classification == other.classification

    def __ne__(self, other):
        return not self == other

    LEAF_STR = "{}(leaf-node (classify {}) (depth {}))"
    def print_node(self):
        offset = "\t" * (self.depth*2)
        str = self.LEAF_STR.format(offset,
                                   self.classification,
                                   self.depth)
        print(str)


class ID3DecisionNode(ID3Node):
    def __init__(self, decision_attr, gain, misclass_error,
                 chi_squared=0.0, depth=0):
        super(self.__class__, self).__init__(depth)
        self.decision_attribute = decision_attr
        self.information_gain = gain
        self.misclassification_error = misclass_error
        self.chi_squared = chi_squared

    def __eq__(self, other):
        me = (self.decision_attribute,
              self.information_gain,
              self.misclassification_error, self.depth)
        them = (other.decision_attribute,
                other.information_gain,
                other.misclassification_error, self.depth)
        return me == them

    def __ne__(self, other):
        return not self == other

    NODE_STR = "{}(decision-node (split (attr {}) (gain {}) (misclassification {}) (chi^2 {}) (depth {})))"
    def print_node(self):
        offset = "\t" * (self.depth*2)
        str = self.NODE_STR.format(offset,
                                   self.decision_attribute,
                                   self.information_gain,
                                   self.misclassification_error,
                                   self.chi_squared,
                                   self.depth)
        print(str)

        
class ID3Edge:
    def __init__(self, branch_attribute, branch_value,
                 source_node=None, destination_node=None):
        self.branch_attribute = branch_attribute
        self.branch_value = branch_value
        self.source_node = source_node
        self.destination_node = destination_node

    def __eq__(self, other):
        me = (self.branch_attribute, self.branch_value,
              self.source_node, self.destination_node)
        them = (other.branch_attribute, other.branch_value,
              other.source_node, other.destination_node)
        return me == them

    def __ne__(self, other):
        return not self == other

    EDGE_STR = "{}(edge (= {} {}))"
    def print_edge(self, depth):
        offset = "\t" * (2*depth+1)
        str = self.EDGE_STR.format(offset,
                                   self.branch_attribute,
                                   self.branch_value)
        print(str)
        
        
class ID3Tree:
    def __init__(self, root):
        self.root = root
        self.Nodes = []  #a list of ID3Nodes
        self.Edges = []  #a list of ID3Edges
        self.adjacency = dict({self.root : []})
        self.Nodes.append(root)
        # adjacency a dictionary where:
        #   * it's key is an ID3Node and
        #   * it's value is a list of ID3Edges

    def add_node(self, existing_node, new_edge, new_node):
        """Adds a new edge from existing_node to new_node."""
        new_edge.source_node = existing_node
        new_edge.destination_node = new_node
        new_node.depth = existing_node.depth + 1
        self.Nodes.append(new_node)
        self.Edges.append(new_edge)
        if existing_node not in self.adjacency:
            self.adjacency[existing_node] = []
        self.adjacency[existing_node].append(new_edge)        

    def add_tree(self, existing_node, new_edge, new_tree):
        """Merges a tree into this tree at existing_node."""
        self.Nodes.extend(new_tree.Nodes)
        self.Edges.extend(new_tree.Edges)
        new_edge.source_node = existing_node
        new_edge.destination_node = new_tree.root
        self.Edges.append(new_edge)
        self.adjacency[existing_node].append(new_edge)
        self.adjacency.update(new_tree.adjacency)
        self.update_all_depths()

    def classify(self, shroom_record):
        """Classifies this shroom_record."""
        return self._classify(self.root, shroom_record)

    def _classify(self, node, shroom_record):
        """Classifies this shroom_record."""
        if not node:
            return None
        if isinstance(node, ID3LeafNode):
            return node.classification

        next_node = None
        for edge in self.adjacency[node]:
            val = shroom_record.attributes[edge.branch_attribute]
            if val == "?":
                return None
            if edge.branch_value == val:
                next_node = edge.destination_node
                break
        return self._classify(next_node, shroom_record)

    def get_children(self, node):
        """Gets a list of node's children."""
        children = []
        if node in self.adjacency:
            for edge in self.adjacency[node]:
                children.append(edge.destination_node)
        return children

    def update_all_depths(self):
        """Updates the depth of the root node."""
        self.update_depth(self.root, 0)
        
    def update_depth(self, node, depth):
        """Recursively updates the depth of nodes."""
        node.depth = depth
        for child in self.get_children(node):
            self.update_depth(child, depth+1)

    def max_depth(self):
        """Finds the max depth of this tree."""
        max_depth = 0
        for node in self.Nodes:
            if isinstance(node, ID3LeafNode):
                if node.depth > max_depth:
                    max_depth = node.depth
        return max_depth
    
    def print_summary(self):
        """Prints tree summary."""
        print("\n==== Tree summary ====")
        print("|Nodes|: ", len(self.Nodes))
        print("|Edges|: ", len(self.Edges))
        print("Max depth: ", self.max_depth())
        
    def print_entire_tree(self):
        """Prints entire tree in tab format."""
        self.print_tree_at(self.root)
        self.print_summary()
        return

    def print_tree_at(self, node):
        """Recursively prints this tree in tab format."""
        node.print_node()
        
        if node not in self.adjacency:
            return
        for edge in self.adjacency[node]:
            edge.print_edge(node.depth)
            self.print_tree_at(edge.destination_node)
