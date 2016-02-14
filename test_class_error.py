#!/usr/bin/env python

import pdb

from id3 import *


deffilename = "_shroom.data.definition"
trainfilename = "./data/training.dat"

mydefs = ShroomDefs(deffilename)
mydb = ShroomDatabase([], trainfilename)

error = calc_class_error(mydb.fetch_class_vector())

class_error_table = calc_all_class_error(mydefs.attr_set,
                                         mydb, mydefs)
print("\nMisclassification table:")
print("===========================")
for attr in class_error_table:
    error = class_error_table[attr]
    print(attr, ": ", error)


#pdb.set_trace()
print("\nMisclassification2 table:")
class_error2_table = calc2_all_class_error(mydefs.attr_set,
                                           mydb, mydefs)
for attr in class_error2_table:
    error2 = class_error2_table[attr]
    print(attr, ": ", error2)


#rmend_attr, value = recommend_next_attr(class_error_table)
#print("\nRecommend: ", rmend_attr, ", ", value)

