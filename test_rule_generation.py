#!/usr/bin/env python
#
# filename: test_rule_generation.py
# authors:  Jon David and Jarrett Decker
# date:     Saturday, February 13, 2016
#

import pdb

from datadef import ShroomDefs
from database import ShroomDatabase
from id3_evaluator import *
from id3 import *
from id3_tree import *
from id3_rules import *



deffilename = "_shroom.data.definition"
trainfilename = "./data/training.dat"  
testfilename = "./data/testing.dat"
chitable_filename = "./chi_square_table.txt"

mydefs = ShroomDefs(deffilename)
mydb = ShroomDatabase([], trainfilename)
chi_table = ChiSquareDistributionTable(chitable_filename)

evaluator = ID3ShroomEvaluator()
tree = evaluator.generate_id3_tree(InformationGainCriteria(),
                                   deffilename, trainfilename,
                                   chi_table, "99%")
print("Printing entire tree.")
tree.print_entire_tree()

#pdb.set_trace()
print("Printing generated rules.")
rule_list = tree.generate_rules()
tree.print_rules(rule_list)
