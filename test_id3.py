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


def test_id3_gain_criteria(defs, db):
    print("\n==== Testing id3 using gain criteria =====\n")
    gain_criteria = InformationGainCriteria()
    #pdb.set_trace()
    tree = id3(gain_criteria, mydb, 'class', mydefs.attr_set, mydefs)
    tree.print_entire_tree()

def test_id3_misclass_criteria(defs, db):
    print("\n==== Testing id3 using classifcation-error criteria =====\n")
    misclass_error_criteria = ClassificationErrorCriteria()
    tree = id3(misclass_error_criteria, mydb, 'class',
               mydefs.attr_set, mydefs)
    tree.print_entire_tree()


def test_classify(testfilename):
    print("\n\n==== Test classification====")
    testdb = ShroomDatabase([], testfilename)
    record = testdb.records[0]
    
    gain_criteria = InformationGainCriteria()
    gain_tree = id3(gain_criteria, mydb, 'class',
                    mydefs.attr_set, mydefs)
    gain_classification = gain_tree.classify(record)

    misclass_error_criteria = ClassificationErrorCriteria()
    misclass_tree = id3(misclass_error_criteria, mydb,
                        'class', mydefs.attr_set, mydefs)
    misclass_classification = misclass_tree.classify(record)

    print("\nClassification under gain and misclassification:")
    print("record to classify: " + record.get_raw_string())
    print("(gain) classification: " + gain_classification)
    print("(misclass) classification: " + misclass_classification)


##---- Begin -----------------------------------------------

deffilename = "_shroom.data.definition"
trainfilename = "./data/training.dat"
testfilename = "./data/testing.dat"

print("\n\n==== Test id3 functionality ====")
print("definition file: ", deffilename)
print("training set: ", trainfilename)
testfilename = "./data/testing.dat"

mydefs = ShroomDefs(deffilename)
mydb = ShroomDatabase([], trainfilename)

test_id3_gain_criteria(mydefs, mydb)
test_id3_misclass_criteria(mydefs, mydb)
test_classify(testfilename)
