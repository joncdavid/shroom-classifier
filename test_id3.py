#!/usr/bin/env python
#
# filename: test_id3.py
# authors:  Jon David and Jarett Decker
# date:     Thursday, February 4, 2016
#

from j2d2_datadef import ShroomDefs
from j2d2_database import ShroomDatabase
from j2d2_id3 import *

deffilename = "_shroom.data.definition"
trainfilename = "./data/training.dat"
#trainfilename = "./data/training.10.dat"

print "\n"
print "definition file: ", deffilename
print "training set: ", trainfilename

mydefs = ShroomDefs(deffilename)
mydb = ShroomDatabase([], trainfilename)

root = id3(mydb, 'class', mydefs.attr_set, mydefs)
print root.label
set_depth(root, 0)
root.print_tree()
