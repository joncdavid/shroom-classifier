#!/usr/bin/env python
#
# filename: j2d2_database.py
# authors:  Jon David and Jarett Decker
# date:     Wednesday, February 3, 2016
#

import re
from j2d2_datadef import ShroomDefs

class ShroomRecord:
    """Definition of a mushroom record"""
    def __init__(self, label):
        self.label = label
        self.attributes = {}

    def add_attr(self, attr, symbol):
        self.attributes[attr] = symbol
        

class ShroomDatabase:
    """Definition of mushroom database"""

    def __init__(self, filename, records=[]):
        self.records = records
        if len(self.records) == 0:
            self.load_data(filename)

    def clone(self):
        """Creates a deep copy of this instance."""
        new_record = []
        for r in self.records:
            new_record.append(r)
        return ShroomDatabase("", new_record)

    def load_data(self, filename):
        """Populates mushroom database from filename."""
        with open(filename, 'r') as f:
            for line in f:
                t = line.strip().split(',')
                classname = t[0]
                r = ShroomRecord(classname)
                r.add_attr('cap-shape',t[1])
                r.add_attr('cap-surface',t[2])
                r.add_attr('cap-color',t[3])
                r.add_attr('bruises',t[4])
                r.add_attr('odor',t[5])
                r.add_attr('gill-attachment',t[6])
                r.add_attr('gill-spacing',t[7])
                r.add_attr('gill-size',t[8])
                r.add_attr('gill-color',t[9])
                r.add_attr('stalk-shape',t[10])
                r.add_attr('stalk-root',t[11])
                r.add_attr('stalk-surface-above-ring',t[12])
                r.add_attr('stalk-surface-below-ring',t[13])
                r.add_attr('stalk-color-above-ring',t[14])
                r.add_attr('stalk-color-below-ring',t[15])
                r.add_attr('veil-type',t[16])
                r.add_attr('veil-color',t[17])
                r.add_attr('ring-number',t[18])
                r.add_attr('ring-type',t[19])
                r.add_attr('spore-print-color',t[20])
                r.add_attr('population',t[21])
                r.add_attr('habitat',t[22])
                self.records.append(r)
                
    def validate_data(self, deffilename):
        """
        Validates class and attribute names and attribute values.
        Returns the number invalid attributes and symbols.
        """
        num_invalid = 0
        definitions = ShroomDefs(deffilename)
        for r in self.records:
            if r.label not in definitions.class_set:
                num_invalid = num_invalid + 1
            for attr_name in r.attributes:
                if attr_name not in definitions.attr_set:
                    num_invalid = num_invalid + 1
                symbol = r.attributes[attr_name]
                if symbol not in definitions.attr_values[attr_name]:
                    print "Invalid symbol ", symbol, " for ", attr_name
                    num_invalid = num_invalid + 1
        return num_invalid

    def fetch_class_vector(self):
        """Fetches a vector of class/label values."""
        v = []
        for r in self.records:
            v.append(r.label)
        return v
    
    def fetch_attr_vector(self, attr):
        """Fetches a vector of values of a certain attribute."""
        v = []
        for r in self.records:
            v.append(r.attributes[attr])
        return v
