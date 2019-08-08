#!/usr/bin/python3
"""
Main interface for reading and converting input data from schrodinger.inp
"""

import sys

# DIR = input("Please enter the directory of your schrodinger.inp file:")
DIR = r"."
try:
    FP = open(DIR + r"\schrodinger.inp", "r")
except FileNotFoundError:
    print("Can not open file {}".format("schrodinger.inp"))
    print("Exiting...")
    sys.exit(1)
else:
    line = FP.readlines()
    data = []  # created so that the file lines aren't overwritten
    while line:
        data = line
        line = FP.readlines()
    print(data)
