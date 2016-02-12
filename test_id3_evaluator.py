#!/usr/bin/env python
#
# filename: test_id3_evaluator.py
# authors:  Jon David and Jarrett Decker
# date:     Thursday, February 10, 2016
#

import pdb

from datadef import ShroomDefs
from database import ShroomDatabase
from id3_evaluator import *
from id3 import *


deffilename = "_shroom.data.definition"
trainfilename = "./data/training.dat"
testfilename = "./data/testing.dat"

# criteria_str can be 'gain' or 'misclassification'.
def test_evaluator_with(criteria):
    print("\n\n==== Test ID3Evaluator functionality ====")
    print("definition file: ", deffilename)
    print("training set: ", trainfilename)
    print("test set: ", testfilename)
    print("selection criteria: ", str(criteria))

    mydefs = ShroomDefs(deffilename)
    mydb = ShroomDatabase([], trainfilename)

    evaluator = ID3ShroomEvaluator()
    tree = evaluator.generate_id3_tree(criteria,
                                       deffilename, trainfilename)

    test_db = ShroomDatabase([],testfilename)
    predicted_db = evaluator.generate_predicted_db(tree, test_db)

    report = evaluator.evaluate(predicted_db, test_db)
    report.print_confusion_matrix()
    report.print_summary()

#---- begin ----
test_evaluator_with(InformationGainCriteria())
test_evaluator_with(ClassificationErrorCriteria())
