#!/usr/bin/env python
#
# filename: run_experiments
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
validationfilename = "./data/validation.dat"


def run_experiment(criteria, confidence_interval):
    print("\n\n==== Run Experiment====")
    print("definition file: ", deffilename)
    print("training set: ", trainfilename)
    #print("test set: ", testfilename)
    print("validation set: ", validationfilename)
    print("selection criteria: ", str(criteria))
    print("confidence interval: ", confidence_interval)

    mydefs = ShroomDefs(deffilename)
    mydb = ShroomDatabase([], trainfilename)

    evaluator = ID3ShroomEvaluator()
    tree = evaluator.generate_id3_tree(criteria,
                                       deffilename, trainfilename)

    validation_db = ShroomDatabase([], validationfilename)
    predicted_db = evaluator.generate_predicted_db(tree, validation_db)

    savefile = "prediction.{}.{}".format(str(criteria),
                                         confidence_interval)
    predicted_db.save_data(savefile)
    print("\nSaved predicted data to file: {}".format(savefile))
#    report = evaluator.evaluate(predicted_db, validation_db)
#    report.print_confusion_matrix()
#    report.print_summary()

#---- begin ----
run_experiment(InformationGainCriteria(), '99')
run_experiment(ClassificationErrorCriteria(), '99')
