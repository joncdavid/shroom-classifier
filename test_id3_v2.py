#!/usr/bin/env python
#
# filename: test_id3_v2.py
# authors:  Jon David and Jarrett Decker
# date:     Thursday, February 10, 2016
#

from datadef import ShroomDefs
from database import ShroomDatabase
from id3_v2 import *

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
tree = id3(mydb, 'class', mydefs.attr_set, mydefs)
tree.print_entire_tree()
