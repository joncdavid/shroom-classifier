#!/usr/bin/env python
#
# filename: test_id3_v2.py
# authors:  Jon David and Jarrett Decker
# date:     Thursday, February 10, 2016
#

import pdb

from datadef import ShroomDefs
from database import ShroomDatabase
from id3_v2 import *


deffilename = "_shroom.data.definition"
trainfilename = "./data/training.dat"
testfilename = "./data/testing.dat"

print("\n\n==== Test id3_v2 ====")
print("definition file: ", deffilename)
print("training set: ", trainfilename)

mydefs = ShroomDefs(deffilename)
mydb = ShroomDatabase([], trainfilename)

#pdb.set_trace()
gain_criteria = InformationGainCriteria()
tree = id3(gain_criteria, mydb, 'class', mydefs.attr_set, mydefs)
tree.print_entire_tree()


print("\n\n==== Test classification====")
testdb = ShroomDatabase([], testfilename)
record = testdb.records[0]
classification = tree.classify(record)

print("record to classify: " + record.get_raw_string())
print("classification: " + classification)

