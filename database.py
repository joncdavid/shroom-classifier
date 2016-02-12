#!/usr/bin/env python
#
# filename: database.py
# authors:  Jon David and Jarrett Decker
# date:     Wednesday, February 3, 2016
#

import re
from datadef import ShroomDefs

class ShroomRecord:
    """Definition of a mushroom record"""
    def __init__(self, label):
        self.label = label
        self.attributes = {}

    def add_attr(self, attr, symbol):
        self.attributes[attr] = symbol

    def pretty_print(self):
        print(self.label, self.attributes)

    def get_raw_string(self):
        """Returns a string representations of this record
        equivalent to the format it was read."""
        s = [self.label,
             self.attributes['cap-shape'],
             self.attributes['cap-surface'],
             self.attributes['cap-color'],
             self.attributes['bruises'],
             self.attributes['odor'],
             self.attributes['gill-attachment'],
             self.attributes['gill-spacing'],
             self.attributes['gill-size'],
             self.attributes['gill-color'],
             self.attributes['stalk-shape'],
             self.attributes['stalk-root'],
             self.attributes['stalk-surface-above-ring'],
             self.attributes['stalk-surface-below-ring'],
             self.attributes['stalk-color-above-ring'],
             self.attributes['stalk-color-below-ring'],
             self.attributes['veil-type'],
             self.attributes['veil-color'],
             self.attributes['ring-number'],
             self.attributes['ring-type'],
             self.attributes['spore-print-color'],
             self.attributes['population'],
             self.attributes['habitat']]
        return str.join(',', s)
                      

class ShroomDatabase:
    """Definition of mushroom database"""
    def __init__(self, records, filename=None):
        self.records=records
        if filename and len(self.records) == 0:
            self.load_data(filename)

    def load(self, x):
        """Loads a 22-tuple into record. Adds record to records."""
        record = ShroomRecord(x[0])
        record.add_attr('cap-shape', x[1])
        record.add_attr('cap-surface', x[2])
        record.add_attr('cap-color', x[3])
        record.add_attr('bruises', x[4])
        record.add_attr('odor', x[5])
        record.add_attr('gill-attachment', x[6])
        record.add_attr('gill-spacing', x[7])
        record.add_attr('gill-size', x[8])
        record.add_attr('gill-color', x[9])
        record.add_attr('stalk-shape', x[10])
        record.add_attr('stalk-root', x[11])
        record.add_attr('stalk-surface-above-ring', x[12])
        record.add_attr('stalk-surface-below-ring', x[13])
        record.add_attr('stalk-color-above-ring', x[14])
        record.add_attr('stalk-color-below-ring', x[15])
        record.add_attr('veil-type', x[16])
        record.add_attr('veil-color', x[17])
        record.add_attr('ring-number', x[18])
        record.add_attr('ring-type', x[19])
        record.add_attr('spore-print-color', x[20])
        record.add_attr('population', x[21])
        record.add_attr('habitat', x[22])
        self.records.append(record)

    def load_data(self, filename):
        """Populates mushroom database from filename."""
        with open(filename, 'r') as f:
            for line in f:
                t = line.strip().split(',')
                self.load(t)

    def save_data(self, savefilename):
        """Saves this database into savefilename."""
        with open(savefilename, 'w') as f:
            for record in self.records:
                f.write(record.get_raw_string() + "\n")
            
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
                    print("Invalid symbol ", symbol, " for ", attr_name)
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
        
