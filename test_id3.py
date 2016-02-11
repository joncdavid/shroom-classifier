#!/usr/bin/env python
#
# filename: test_id3.py
# authors:  Jon David and Jarett Decker
# date:     Thursday, February 4, 2016
#

from datadef import ShroomDefs
from database import ShroomDatabase
from id3 import *

import pdb


deffilename = "_shroom.data.definition"
trainfilename = "./data/training.dat"
#trainfilename = "./data/training.10.dat"

print("\n")
print("definition file: ", deffilename)
print("training set: ", trainfilename)

mydefs = ShroomDefs(deffilename)
mydb = ShroomDatabase([], trainfilename)

#pdb.set_trace()
root = id3(mydb, 'class', mydefs.attr_set, mydefs)

#tree = ID3Tree(root)
#pdb.set_trace()
root.print_node(mydefs, True)
#tree.print_tree()
