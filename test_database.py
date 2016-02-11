#!/usr/bin/env python
#
# filename: test_database.py
# authors:  Jon David and Jarrett Decker
# date:     Thursday, February 10, 2016
#

import pdb

from database import ShroomDatabase


trainfilename = "./data/training.dat"
testfilename = "./data/testing.dat"
outfilename = "./output.dat"

print("\n\n==== Test database ====")
print("training file: ", trainfilename)
print("testing file: ", testfilename)
print("output file: ", outfilename)

training_db = ShroomDatabase([], trainfilename)
test_db = ShroomDatabase([], testfilename)

out_db = ShroomDatabase(test_db.records)
out_db.save_data(outfilename)

print("\nVerify {} and {} are equal.".format(testfilename,
                                               outfilename))
print("Use diff -Z, to ignore whitespace at end of line")
