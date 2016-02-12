#!/usr/bin/env python
#
# filename: test_gain.py
# authors:  Jon David and Jarrett Decker
# date:     Thursday, February 4, 2016
#

from datadef import ShroomDefs
from database import ShroomDatabase
from id3 import *

deffilename = "_shroom.data.definition"
trainfilename = "./data/training.dat"

print("\n")
print("definition file: ", deffilename)
print("training set: ", trainfilename)

mydefs = ShroomDefs(deffilename)
mydb = ShroomDatabase([], trainfilename)
        
gain_table = calc_all_gain(mydefs.attr_set, mydb, mydefs)
print("\nGain table:")
print("===========================")
for attr in gain_table:
    gain = gain_table[attr]
    print(attr, ": ", gain)

# rmend_attr, gain = recommend_next_attr(gain_table)
# print("\nRecommend: ", rmend_attr, ", ", gain)

