#!/usr/bin/env python
#
# filename: test_id3.py
# authors:  Jon David and Jarrett Decker
# date:     Thursday, February 10, 2016
#

import pdb

from datadef import ShroomDefs
from database import ShroomDatabase
from id3 import *


def test_id3_gain_criteria(defs, db, chi_table, CI="0%"):
    print("\n==== Testing id3 using gain criteria =====\n")
    gain_criteria = InformationGainCriteria()
    #pdb.set_trace()
    tree = id3(gain_criteria, mydb, 'class', mydefs.attr_set,
               mydefs, chi_table, CI)
    tree.print_entire_tree()

def test_id3_misclass_criteria(defs, db, chi_table, CI="0%"):
    print("\n==== Testing id3 using classifcation-error criteria =====\n")
    misclass_error_criteria = ClassificationErrorCriteria()
    tree = id3(misclass_error_criteria, mydb, 'class',
               mydefs.attr_set, mydefs, chi_table, CI)
    tree.print_entire_tree()


def test_classify(testfilename, chi_table):
    print("\n\n==== Test classification====")
    testdb = ShroomDatabase([], testfilename)
    record = testdb.records[0]
    
    gain_criteria = InformationGainCriteria()
    gain_tree = id3(gain_criteria, mydb, 'class',
                    mydefs.attr_set, mydefs, chi_table)
    gain_classification = gain_tree.classify(record)

    misclass_error_criteria = ClassificationErrorCriteria()
    misclass_tree = id3(misclass_error_criteria, mydb,
                        'class', mydefs.attr_set, mydefs, chi_table)
    misclass_classification = misclass_tree.classify(record)

    print("\nClassification under gain and misclassification:")
    print("record to classify: " + record.get_raw_string())
    print("(gain) classification: " + gain_classification)
    print("(misclass) classification: " + misclass_classification)


##---- Begin -----------------------------------------------

deffilename = "_shroom.data.definition"
trainfilename = "./data/training.dat"
testfilename = "./data/testing.dat"
chitable_filename = "./chi_square_table.txt"

print("\n\n==== Test id3 functionality ====")
print("definition file: ", deffilename)
print("training set: ", trainfilename)
print("testing set: ", testfilename)
print("Chi table file: ", chitable_filename)

mydefs = ShroomDefs(deffilename)
mydb = ShroomDatabase([], trainfilename)
chi_table = ChiSquareDistributionTable(chitable_filename)

test_id3_gain_criteria(mydefs, mydb, chi_table)
test_id3_misclass_criteria(mydefs, mydb, chi_table)
test_classify(testfilename, chi_table)
