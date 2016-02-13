#!/usr/bin/env python
#
# filename: test_chisquare_table.py
# authors:  Jon David and Jarrett Decker
# date:     Friday, February 11, 2016
#

import pdb

from id3 import ChiSquareDistributionTable


def print_test(chi_table, dof, CI):
    test_str = "DoF:{}, CI:{}, p:{}"
    print(test_str.format(dof, CI,
                          chi_table.get_score(dof, CI)))


#---- begin ----
print("\n==== Testing ChiSquareDistributionTable ====")
chitablefile = "./chi_square_table.txt"
chi_table = ChiSquareDistributionTable(chitablefile)

print_test(chi_table, 1, "50%")
print_test(chi_table, 2, "95%")
print_test(chi_table, 3, "99%")
print_test(chi_table, 4, "50%")
print_test(chi_table, 5, "95%")
print_test(chi_table, 6, "99%")
print_test(chi_table, 7, "50%")
print_test(chi_table, 8, "95%")
print_test(chi_table, 9, "99%")
print_test(chi_table, 10, "50%")
print_test(chi_table, 11, "95%")


