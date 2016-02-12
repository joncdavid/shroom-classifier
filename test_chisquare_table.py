#!/usr/bin/env python
#
# filename: test_chisquare_table.py
# authors:  Jon David and Jarrett Decker
# date:     Friday, February 11, 2016
#

import pdb

from id3 import ChiSquareDistributionTable


def print_test(chi_table, dof, alpha):
    test_str = "DoF:{}, alpha:{}, p:{}"
    print(test_str.format(dof, alpha,
                          chi_table.get_probability(dof, alpha)))


#---- begin ----
print("\n==== Testing ChiSquareDistributionTable ====")
chitablefile = "./chi_square_table.txt"
chi_table = ChiSquareDistributionTable(chitablefile)

print_test(chi_table, 1, "0.50")
print_test(chi_table, 2, "0.05")
print_test(chi_table, 3, "0.01")
print_test(chi_table, 4, "0.50")
print_test(chi_table, 5, "0.05")
print_test(chi_table, 6, "0.01")
print_test(chi_table, 7, "0.50")
print_test(chi_table, 8, "0.05")
print_test(chi_table, 9, "0.01")
print_test(chi_table, 10, "0.50")
print_test(chi_table, 11, "0.05")


