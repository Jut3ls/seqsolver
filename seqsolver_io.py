# -*- coding: utf-8 -*-
"""
Main interface for reading and converting input data from schrodinger.inp
"""

import sys
import numpy as np

# DIR = input("Please enter the directory of your schrodinger.inp file:")
DIR = r"."
try:
    FP = open(DIR + r"\schrodinger.inp", "r")
except FileNotFoundError:
    print("Can not open file {}".format("schrodinger.inp"))
    print("Exiting...")
    sys.exit(1)
else:  # it seems we have to read data line by line due to formating issues
    mass = np.genfromtxt("schrodinger.inp", max_rows=1)
    boundries = np.genfromtxt("schrodinger.inp", skip_header=1, max_rows=1)
    eigenvalues = np.genfromtxt("schrodinger.inp", skip_header=2, max_rows=1)
    points = np.genfromtxt("schrodinger.inp", skip_header=4, max_rows=1)
    xdata = np.genfromtxt("schrodinger.inp", skip_header=5, usecols=0)
    ydata = np.genfromtxt("schrodinger.inp", skip_header=5, usecols=1)
