#!/usr/bin/env python
#
# filename: run_experiments
# authors:  Jon David and Jarrett Decker
# date:     Thursday, February 10, 2016
#

import pdb
import sys

from datadef import ShroomDefs
from database import ShroomDatabase
from id3_evaluator import *
from id3 import *


deffilename = "_shroom.data.definition"
trainfilename = "./data/training.dat"  
testfilename = "./data/testing.dat"
validationfilename = "./data/validation.dat"
chitable_filename = "./chi_square_table.txt"


def test_experiment(criteria, validationfilename, CI, path):
    print("\n\n")
    print("=====================================================")
    print("Run Experiment")
    print("=====================================================")
    print("definition file: ", deffilename)
    print("training set: ", trainfilename)
    print("validation set: ", validationfilename)
    print("selection criteria: ", str(criteria))
    print("confidence interval: ", CI)

    mydefs = ShroomDefs(deffilename)
    mydb = ShroomDatabase([], trainfilename)
    chi_table = ChiSquareDistributionTable(chitable_filename)

    evaluator = ID3ShroomEvaluator()
    tree = evaluator.generate_id3_tree(criteria, deffilename,
                                       trainfilename, chi_table, CI)

    validation_db = ShroomDatabase([], validationfilename)
    predicted_db = evaluator.generate_predicted_db(tree, validation_db)

    savefile = "{}prediction.{}.{}".format(path,
                                           str(criteria),
                                           CI)
    predicted_db.save_class_only(savefile)
    print("\nSaved predicted data to file: {}".format(savefile))

    tree.print_summary()
    report = evaluator.evaluate(predicted_db, validation_db)
    report.print_confusion_matrix()
    report.print_summary()

#---- begin ----
expectedfile = None
path = None
if len(sys.argv) >= 3:
    expectedfile = sys.argv[1]
    path = sys.argv[2]
else:
    expectedfile = testfilename
    path = "./results/test/"
    
print("Using validation file: ", expectedfile)
print("Writing to dir: ", path)

test_experiment(InformationGainCriteria(), expectedfile, "99%", path)
test_experiment(InformationGainCriteria(), expectedfile, "95%", path)
test_experiment(InformationGainCriteria(), expectedfile, "50%", path)
test_experiment(InformationGainCriteria(), expectedfile, "0%", path)

test_experiment(ClassificationErrorCriteria(), expectedfile, "99%", path)
test_experiment(ClassificationErrorCriteria(), expectedfile, "95%", path)
test_experiment(ClassificationErrorCriteria(), expectedfile, "50%", path)
test_experiment(ClassificationErrorCriteria(), expectedfile, "0%", path)

