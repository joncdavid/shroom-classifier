#!/usr/bin/env python
#
# filename: id3_util.py
# authors:  Jon David and Jarrett Decker
# date:     Wednesday, February 10, 2016
#

import abc
import pdb
import math
from datadef import ShroomDefs
from database import ShroomDatabase


class SelectionCriteria(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        return

    @abc.abstractmethod
    def recommend_next_attr(self, attributes, db, defs):
        """Returns the recommended attribute, and criteria."""
        return

class InformationGainCriteria(SelectionCriteria):
    def __init__(self):
        super(self.__class__, self).__init__()
        
    def __str__(self):
        return "gain"

    def recommend_next_attr(self, attributes, db, defs):
        """Recommends the attribute with the highest gain as
        the next decision node."""
        gain_table = calc_all_gain(attributes, db, defs)
        best_attr = None
        highest_gain = 0.0
        for attr in gain_table:
            gain = gain_table[attr]
            if(gain > highest_gain):
                best_attr, highest_gain = attr, gain
        return best_attr, highest_gain
        

class ClassificationErrorCriteria(SelectionCriteria):
    def __init__(self):
        super(self.__class__, self).__init__()

    def __str__(self):
        return "misclassification"

    def recommend_next_attr(self, attributes, db, defs):
        """Recommends the attribute with the minimum
        classification error as the next decision node."""

        #misclass_table = calc2_all_class_error(attributes, db, defs)
        misclass_table = calc_all_class_error(attributes, db, defs)
        #misclass_table = calc_all_class_error(attributes, db, defs)
        #went with calc2_* because max depth is 13, whereas
        #          calc_*'s max depth is 15.
        #Both have the same accuracy over the test dataset.
        best_attr = None
        max_classify_error = 0
        for attr in misclass_table:
            classify_error = misclass_table[attr]
            if(classify_error >= max_classify_error):
                best_attr = attr
                max_classify_error = classify_error
        return best_attr, max_classify_error

#---- Utility Functions ---------------------------------------------

def is_homogeneous(vector):
    """Checks if, at this node, all class/labels are homogeneous."""
    unique_labels = set()
    for v in vector:
        unique_labels.add(v)
    if len(unique_labels) == 1:
        return True, list(unique_labels)[0]
    return False, None

def mode2(examples, target_attr):
    v = []
    db = ShroomDatabase(examples)
    if target_attr=='class':
        v = db.fetch_class_vector()
    else:
        v = db.fetch_class_vector(target_attr)
    return mode(v)
    
def mode(vector):
    """Finds the most common value for a particular attribute.
    If attr=None, find the mode of the class/label"""
    disttable = calc_distribution_table(vector)
    highest_freq = max(disttable.values())
    mode = []  #because some might be tied 
    for x in disttable:
        if disttable[x] == highest_freq:
            mode.append(x)
    return mode
    
def calc_distribution_table(vector):
    """Calculates distribution table for some vector."""
    dist_table = {}
    for x in vector:
        if x not in dist_table:
            dist_table[x] = 0
        dist_table[x] += 1
    return dist_table
    
def calc_all_gain(attributes, db, defs):
    """Calculates the information gain for all attributes."""
    gain_table = dict()
    for a in attributes:
        gain_table.update({a : calc_gain(a, db, defs)})
    return gain_table
        
def calc_gain(attr, db, defs):
    """Calculates information gain on this attribute."""
    cv = db.fetch_class_vector()
    entropy_before = calc_entropy(cv)

    entropy_after = 0.0000
    for symbol in defs.attr_values[attr]:
        subset_db = filter_subset(db, attr, symbol, "?")
        expected_cv = subset_db.fetch_class_vector()
        attr_entropy = calc_entropy(expected_cv)
        attr_entropy *= 1.0*len(expected_cv)/len(cv)
        entropy_after += attr_entropy

    gain = entropy_before - entropy_after
    return gain

def calc_entropy(vector):
    """Calculates entropy for some vector."""
    n = len(vector)
    dist_table = calc_distribution_table(vector)
    partial_entropy = []
    for item in dist_table.items():
        p = 1.0*item[1]/n  #proportion
        partial_entropy.append((-1*p) * math.log((1.0*p), 2))
    entropy = sum(partial_entropy)
    return entropy

def filter_subset(db, attr, filter_value, ignore=None):
    """Produces a subset database by filtering on attr's filter_value"""
    subset_records = []
    for r in db.records:
        v = r.attributes[attr]
        if v == ignore:
            continue
        if v == filter_value:
            subset_records.append(r)
    subset_db = ShroomDatabase(subset_records)
    return subset_db

def calc2_all_class_error(attributes, db, defs):
    """Calculates misclassification error for all attributes."""
    misclass_table = dict()
    for attr in attributes:
        misclass_table.update({attr:calc2_class_error(attr, db, defs)})
    return misclass_table

def calc2_class_error(attribute, db, defs):
    """Calculates misclassification error for this attribute."""
    M = 0.0   # M is misclassification error for this attr.
    n = len(db.fetch_class_vector())
    for symbol in defs.attr_values[attribute]:
        subset_db = filter_subset(db, attribute, symbol) #, "?")rm guard
        sub_vector = subset_db.fetch_class_vector()
        dist_table = calc_distribution_table(sub_vector)
        prob_p_ = 0.0
        prob_e_ = 0.0
        if 'p' in dist_table:
            prob_p_ = float(dist_table['p']) / n
        if 'e' in dist_table:
            prob_e_ = float(dist_table['e']) / n
        n_v = len(sub_vector)
        M = M + (1.0 - max(prob_p_, prob_e_))*(float(n_v)/n)
    return M

def calc_all_class_error(attributes, db, defs):
    """Calculates the classification error for all attributes of a ShroomDatabase."""
    tot_len = len(db.fetch_class_vector())
    class_error_table = dict()
    class_error_before = calc_class_error(db.fetch_class_vector())
    for attr in attributes:
        interim_db_list = []
        for symbol in defs.attr_values[attr]:
            interim_list = []
            for r in db.records:
                if r.attributes[attr] == symbol:
                    interim_list.append(r)
            interim_db_list.append(ShroomDatabase(interim_list))
        interim_class_error = 0
        for idb in interim_db_list:
            vec = idb.fetch_class_vector()
            interim_class_error += (len(vec) / tot_len * calc_class_error(vec))
        class_error_after = class_error_before - interim_class_error
        class_error_table[attr] = class_error_after
    return class_error_table

def calc_class_error(vector):
    """Calculates the classification error for some vector."""
    n = len(vector)
    if n == 0:
        return 1
    table = dict()
    for v in vector:
        if (v in table.keys()) == False:
            table[v] = 0
        table[v] += 1
    for k in table.keys():
        table[k] /= (1.0)*n
    error = 1.0 - max(table.values())
    return error

def calc_all_chi_squared(attributes, defs, db):
    """Calculates Chi-squared value for all attributes."""
    chi2_table = {}
    for a in attributes:
        chi2_table.update({a : calc_chi_squared(a, defs,
                                                predicted_db, actual_db)})
    return chi2_table

def calc_chi_squared(attr, defs, db):
    """Calculates Chi-squared value for this attribute."""
    v = db.fetch_class_vector()
    dist_table = calc_distribution_table(v)
    p = dist_table['p']
    e = dist_table['e']
    n = p + e

    chi_squared = 0.0
    for symbol in defs.attr_values[attr]:
        subset_i = filter_subset(db, attr, symbol) #, "?")#rm guard
        if len(subset_i.records) == 0:
            continue
        subset_v = subset_i.fetch_class_vector()
        dist_table_v = calc_distribution_table(subset_v)
        
        p_i = 0
        e_i = 0
        if 'p' in dist_table_v:
            p_i = dist_table_v['p']
        if 'e' in dist_table_v:
            e_i = dist_table_v['e']
        #pdb.set_trace()
        p_i_prime = (p_i + e_i)*(float(p)/(p+e))
        e_i_prime = (p_i + e_i)*(float(e)/(p+e))
        local_chi2 = ( (math.pow((p_i - p_i_prime),2) / p_i_prime) +
                       (math.pow((e_i - e_i_prime),2) / e_i_prime) )
        chi_squared += local_chi2
    return chi_squared

def should_prune(chi2, dof, CI, chi_table):
    x = chi_table.get_score(dof, CI)
    if not x:
        return False
    if chi2 < x:
        return True
    return False
            

class ChiSquareDistributionTable(object):
    """A class that represents the Chi-Squared distribution table."""
    def __init__(self, filename):
        self.table = {}
        self.ci_alpha_map = {"99%":"0.01",
                             "95%":"0.05",
                             "50%":"0.05",
                             "0%" : None}
        self.load(filename)

    def load(self, filename):
        #pdb.set_trace()
        with open(filename, 'r') as f:
            for line in f:
                dof, p50, p05, p01 = line.strip().split(",")
                if dof not in self.table:
                    self.table[dof] = {}
                self.table[dof]["0.50"] = p50
                self.table[dof]["0.05"] = p05
                self.table[dof]["0.01"] = p01

    def get_score(self, dof, CI):
        alpha = self.ci_alpha_map[CI]
        if not alpha:
            return None
        return float( self._get_score(dof, alpha) )
    
    def _get_score(self, dof, alpha):
        dof_str = str(dof) if isinstance(dof,int) else dof
        return self.table[dof_str][alpha]
