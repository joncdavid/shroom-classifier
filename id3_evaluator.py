#!/usr/bin/env python
#
# filename: id3_evaluator.py
# authors:  Jon David and Jarrett Decker
# date:     Thursday, February 10, 2016
#

import pdb
import abc
import math

from datadef import ShroomDefs
from database import *
from id3_tree import *
from id3 import *

class ID3ShroomReport(object):
    """This class summarizes the performance of an ID3 algorithm
    on a training set and evaluation set."""
    def __init__(self, predicted_v, actual_v):
        self.total = 0
        self.predicted_v = predicted_v
        self.actual_v = actual_v
        self.false_p = 0
        self.true_p = 0
        self.false_e = 0
        self.true_e = 0
        self._initialize()

    def _initialize(self):
        self.total = len(self.actual_v)
        # construct pair-wise list.
        create_pair = lambda x,y: (x, y)
        pair_list = map(create_pair, self.predicted_v, self.actual_v)
        
        self.true_p = 0
        self.true_e = 0
        self.false_e = 0
        self.false_p = 0
        for pair in pair_list:
            if pair[1]=='p' and pair[0]=='p':
                self.true_p += 1
            elif pair[1]=='e' and pair[0]=='e':
                self.true_e += 1
            elif pair[1]=='p' and pair[0]=='e':
                self.false_e += 1
            elif pair[1]=='e' and pair[0]=='p':
                self.false_p += 1

    def calc_accuracy(self):
        return float(self.true_p + self.true_e) / self.total

    def calc_misclassification_rate(self):
        return 1.0 - self.calc_accuracy()

    def print_confusion_matrix(self):
        print("\nConfusion Matrix:")
        print("-----------------------------------------")
        print("\t\tPred:{}\tPred:{}".format('p','e'))
        print("actual {}:\t{}\t{}".format('p', self.true_p, self.false_e))
        print("actual {}:\t{}\t{}".format('e', self.false_p, self.true_e))

    def print_summary(self):
        print("\nReport Summary")
        print("-----------------------------------------")
        print("Total records: ", self.total)
        print("Correct classification: ", self.true_p + self.true_e)
        print("Incorrect classification: ", self.false_p + self.false_e)
        print("Accuracy: ", self.calc_accuracy())
        print("Misclassification rate: ", self.calc_misclassification_rate())

        
class ID3ShroomEvaluator(object):
    """This class is responsible for evaluating classification
    performance"""
    
    def __init__(self):
        return
    
    def generate_id3_tree(self, selection_criteria,
                          datadef_filename, training_filename):
        """Generates an ID3 classification tree."""
        criteria = None
        if selection_criteria == "gain":
            criteria = InformationGainCriteria()
        elif selection_criteria == "misclassification":
            criteria = ClassificationErrorCriteria()
        data_defs = ShroomDefs(datadef_filename)
        training_db = ShroomDatabase([], training_filename)
        classification_tree = id3(criteria, training_db, 'class',
                                  data_defs.attr_set, data_defs)
        return classification_tree
        
    def generate_predicted_db(self, id3_tree, actual_db):
        """Generates predictions on data."""
        predicted_records = []
        for r in actual_db.records:
            predicted_label = id3_tree.classify(r)
            predicted_record = ShroomRecord(predicted_label)
            predicted_record.attributes = r.attributes
            predicted_records.append(predicted_record)
        return ShroomDatabase(predicted_records)
        
    def evaluate(self, predicted_db, actual_db):
        """Compares predictions against actual data."""
        predicted_v = predicted_db.fetch_class_vector()
        actual_v = actual_db.fetch_class_vector()

        return ID3ShroomReport(predicted_v, actual_v)
