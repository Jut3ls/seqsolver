# -*- coding: utf-8 -*-
"""Routines for solving the one dimensional time independent schrodinger
equation for any given potential."""

import numpy as np
from scipy import interpolate

fin_linear = ['2.0', '-2.0 2.0 1999', '1 3', 'linear', '6', '-2.0  0.0',
              '-0.5  0.0', '-0.5 -10.0', ' 0.5 -10.0', ' 0.5  0.0',
              ' 2.0  0.0']

inf_linear = ['2.0', '-2.0 2.0 1999', '1 5', 'linear', '2', '-2.0 0.0',
              ' 2.0 0.0']

doublewell_linear = ['2.0', '-20.0 20.0 1999', '1 16', 'linear', '8',
                     '-20.0 100.0', ' -8.0  -1.5', ' -7.0  -1.5',
                     ' -0.5   1.8', '  0.5   1.8', '  7.0  -1.5',
                     '  8.0  -1.5', ' 20.0 100.0']

harm_poly = ['4.0', '-5.0 5.0 1999', '1 5', 'polynomial', '3', '-1.0 0.5',
             ' 0.0 0.0', ' 1.0 0.5']

as_cspline = ['1.0', '0.0 20.0 1999', '1 7', 'cspline', '12', ' 0.0 30.0',
              ' 1.0 11.8', ' 2.0  1.7', ' 3.0  0.0', ' 5.0  0.6', ' 7.0  1.6',
              ' 9.0  2.4', '11.0  3.0', '13.0  3.4', '15.0  3.6', '19.0  3.79',
              '20.0  3.8']


def schrodinger(arg):
    """Trying to realize the algorithm here"""

    window = np.asarray(arg[1].split(" "), dtype=float)
    xVal = np.zeros(int(arg[4]), dtype=float)
    yVal = np.zeros(int(arg[4]), dtype=float)
    potential = np.zeros(shape=(int(window[2]), 2), dtype=float)
    xPot = np.linspace(window[0], window[1], int(window[2]))

    for j in range(5, len(arg)):  # Seperating x and y values of interp points
        xVal[j-5] = np.asarray(arg[j].split())[0]
        yVal[j-5] = np.asarray(arg[j].split())[1]

    if arg[3] == "linear":
        yPot = np.interp(xPot, xVal, yVal)
        for k in range(int(window[2])):  # Saving discrpot in desired format
            potential[k, 0] = xPot[k]
            potential[k, 1] = yPot[k]
        np.savetxt("potential.dat", potential)

    elif arg[3] == "polynomial":
        deg = input("Please enter the degree of the fitting polynomial: ")
        fit = np.polyfit(xVal, yVal, int(deg))
        yPot = np.zeros(shape=int(window[2]), dtype=float)
        for i in range(int(window[2])):
            for l in range(int(deg)+1):  # assigning correct xVal to polyfit
                yPot[i] += fit[l]*xPot[i]**(int(deg)-l)
            potential[i, 0] = xPot[i]
            potential[i, 1] = yPot[i]
        np.savetxt("potential.dat", potential)

    elif arg[3] == "cspline":
        tck = interpolate.splrep(xVal, yVal)  # Calc interp coefficients
        yPot = interpolate.splev(xPot, tck)  # Evaluate discrete data at xPot
        for m in range(int(window[2])):
            potential[m, 0] = xPot[m]
            potential[m, 1] = yPot[m]
        np.savetxt("potential.dat", potential)

    else:
        print("Error: Interpolation type not specified.")


if __name__ == "__main__":
    schrodinger(as_cspline)
