#!/usr/bin/env python
#
# filename: test_id3.py
# authors:  Jon David and Jarett Decker
# date:     Thursday, February 4, 2016
#

from j2d2_datadef import ShroomDefs
from j2d2_database import ShroomDatabase
from j2d2_id3 import *

import pdb


deffilename = "_shroom.data.definition"
trainfilename = "./data/training.dat"
#trainfilename = "./data/training.10.dat"

print "\n"
print "definition file: ", deffilename
print "training set: ", trainfilename

mydefs = ShroomDefs(deffilename)
mydb = ShroomDatabase([], trainfilename)

#pdb.set_trace()
root = id3(mydb, 'class', mydefs.attr_set, mydefs)

#tree = ID3Tree(root)
#pdb.set_trace()
root.print_node(mydefs, True)
#tree.print_tree()
