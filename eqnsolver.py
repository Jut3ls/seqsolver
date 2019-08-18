# -*- coding: utf-8 -*-
"""Routines for solving the one dimensional time independent schrodinger
equation for any given potential."""

import numpy as np
from scipy import interpolate, linalg


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
    """
    Trying to realize the algorithm here
    """
    # Extracting data from input
    mass = float(arg[0])
    eigen = np.asarray(arg[2].split(" "), dtype=int)
    window = np.asarray(arg[1].split(" "), dtype=float)
    delta = window[1]/int(window[2]-1)
    a = 1/(mass*delta**2)

    # Creating empty arrays to fill with data
    xVal = np.zeros(int(arg[4]), dtype=float)
    yVal = np.zeros(int(arg[4]), dtype=float)
    potential = np.zeros(shape=(int(window[2]), 2), dtype=float)
    xPot = np.linspace(window[0], window[1], int(window[2]))

    for i in range(5, len(arg)):  # Seperating x and y values of interp points
        xVal[i-5] = np.asarray(arg[i].split())[0]
        yVal[i-5] = np.asarray(arg[i].split())[1]

    if arg[3] == "linear":
        yPot = np.interp(xPot, xVal, yVal)
        for j in range(int(window[2])):  # Saving discrpot in desired format
            potential[j, 0] = xPot[j]
            potential[j, 1] = yPot[j]
        np.savetxt("potential.dat", potential)

    elif arg[3] == "polynomial":
        deg = input("Please enter the degree of the fitting polynomial: ")
        fit = np.polyfit(xVal, yVal, int(deg))
        yPot = np.zeros(shape=int(window[2]), dtype=float)
        for k in range(int(window[2])):
            for l in range(int(deg)+1):  # assigning correct xVal to polyfit
                yPot[k] += fit[l]*xPot[k]**(int(deg)-l)
            potential[k, 0] = xPot[k]
            potential[k, 1] = yPot[k]
        np.savetxt("potential.dat", potential)

    elif arg[3] == "cspline":
        tck = interpolate.splrep(xVal, yVal)  # Calc interp coefficients
        yPot = interpolate.splev(xPot, tck)  # Evaluate discrete data at xPot
        for ii in range(int(window[2])):
            potential[ii, 0] = xPot[ii]
            potential[ii, 1] = yPot[ii]
        np.savetxt("potential.dat", potential)

    else:
        print("Error: Interpolation type not specified.")

    diag = np.zeros(shape=int(window[2]), dtype=float)
    off_diag = np.zeros(shape=int(window[2])-1, dtype=float)
    for n in range(int(window[2])):
        diag[n] = a + potential[n, 1]
    for m in range(int(window[2]-1)):
        off_diag[m] = -0.5*a

    energies, wavefuncs = linalg.eigh_tridiagonal(diag, off_diag, select="i",
                                                  select_range=eigen-1)
    np.savetxt("energies.dat", energies)
    wavefuncs_new = np.zeros(shape=(int(window[2]), eigen[1]+1), dtype=float)
    for jj in range(int(window[2])):
        wavefuncs_new[jj, 0] = xPot[jj]
        for kk in range(eigen[1]):
            wavefuncs_new[jj, kk+1] = wavefuncs[jj, kk]
    np.savetxt("wavefuncs.dat", wavefuncs_new)

    x_expected = np.zeros(shape=eigen[1], dtype=float)
    x_squared = np.zeros(shape=eigen[1], dtype=float)
    x_uncertainty = np.zeros(shape=eigen[1], dtype=float)
    expvalues = np.zeros(shape=(eigen[1], 2), dtype=float)
    for mm in range(eigen[1]):
        for nn in range(int(window[2])):
            x_expected[mm] += wavefuncs_new[nn, mm+1]*wavefuncs_new[nn, 0]*wavefuncs_new[nn, mm+1]
            x_squared[mm] += wavefuncs_new[nn, mm+1]*wavefuncs_new[nn, 0]**2*wavefuncs_new[nn, mm+1]
        x_uncertainty[mm] = (x_squared[mm] - x_expected[mm]**2)**0.5
        expvalues[mm, 0], expvalues[mm, 1] = x_expected[mm], x_uncertainty[mm]
    np.savetxt("expvalues.dat", expvalues)
"""----I need to clean redundant variables and arrays----"""


# if __name__ == '__main__':
  # schrodinger(as_cspline)
