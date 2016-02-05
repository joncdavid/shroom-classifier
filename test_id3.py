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

print "\n"
print "definition file: ", deffilename
print "training set: ", trainfilename

mydefs = ShroomDefs(deffilename)
mydb = ShroomDatabase(trainfilename)

## TODO... sleepy now ~.~
##root_node = ID3Node(mydb, mydefs)


