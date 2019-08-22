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

doublewell_cspline = ['4.0', '-20.0 20.0 1999', '1 10', 'cspline', '5',
                      '-20.0 35.0', '-10.0  0.0', '  0.0  2.0', ' 10.0  0.0',
                      ' 20.0 35.0']


def schrodinger(arg):
    """Creates discrete potentials from data provided by input and then solves
    the one dimensional time independent schrodinger equation.


    Args:
        arg: A list of data provided by seqsolver_io.py from schrodinger.inp
        which specifies the problem.


    Returns:
        Discrete 1D wavefunctions, the discrete potential,
        all desired eigenvalues, expected values of the position operator <x>,
        expected uncertainty when measuring position, all in .dat format
    """

    window = np.asarray(arg[1].split(" "), dtype=float)

    # Creating empty arrays to fill with data
    xpoint = np.zeros(int(arg[4]), dtype=float)
    ypoint = np.zeros(int(arg[4]), dtype=float)
    potential = np.zeros(shape=(int(window[2]), 2), dtype=float)
    xval = np.linspace(window[0], window[1], int(window[2]))

    # Extracting data from input
    eigen = np.asarray(arg[2].split(" "), dtype=int)
    delta_sq = (abs(xval[1])-abs(xval[0]))**2
    add = 1/(float(arg[0])*delta_sq)

    for i in range(5, len(arg)):  # Seperating x and y values of interp points
        xpoint[i-5] = np.asarray(arg[i].split())[0]
        ypoint[i-5] = np.asarray(arg[i].split())[1]

    if arg[3] == "linear":
        yval = np.interp(xval, xpoint, ypoint)

    elif arg[3] == "polynomial":
        deg = input("Please enter the degree of the fitting polynomial: ")
        fit = np.polyfit(xpoint, ypoint, int(deg))
        yval = np.zeros(shape=int(window[2]), dtype=float)
        for j in range(int(window[2])):
            for k in range(int(deg)+1):  # assigning correct xVal to polyfit
                yval[j] += fit[k]*xval[j]**(int(deg)-k)

    elif arg[3] == "cspline":
        tck = interpolate.splrep(xpoint, ypoint)  # Calc interp coefficients
        yval = interpolate.splev(xval, tck)  # Evaluate discrete data at xVal

    else:
        print("Error: Interpolation type not correctly specified.")

    for ii in range(int(window[2])):  # Saving discrpot in desired format
        potential[ii, 0] = xval[ii]
        potential[ii, 1] = yval[ii]
    np.savetxt("potential.dat", potential)

    # Filling matrix with data to solve with linalg.eigh_tridiagonal()
    diag = np.zeros(shape=int(window[2]), dtype=float)
    off_diag = np.zeros(shape=int(window[2])-1, dtype=float)
    for jj in range(int(window[2])):
        diag[jj] = add + potential[jj, 1]
    for kk in range(int(window[2]-1)):
        off_diag[kk] = -0.5*add

    energies, wavefuncs = linalg.eigh_tridiagonal(diag, off_diag, select="i",
                                                  select_range=eigen-1)
    np.savetxt("energies.dat", energies)
    wave_new = np.zeros(shape=(int(window[2]), eigen[1]+1), dtype=float)
    for ll in range(int(window[2])):
        wave_new[ll, 0] = xval[ll]
        for mm in range(eigen[1]):
            wave_new[ll, mm+1] = wavefuncs[ll, mm]
    np.savetxt("wavefuncs.dat", wave_new)

    x_expected = np.zeros(shape=eigen[1], dtype=float)
    x_squared, x_uncertainty = np.array(x_expected), np.array(x_expected)
    expvalues = np.zeros(shape=(eigen[1], 2), dtype=float)

    for nn in range(eigen[1]):
        for oo in range(int(window[2])):
            x_expected[nn] += wave_new[oo, nn+1]*xval[oo]*wave_new[oo, nn+1]
            x_squared[nn] += wave_new[oo, nn+1]*xval[oo]**2*wave_new[oo, nn+1]
        x_uncertainty[nn] = (x_squared[nn] - x_expected[nn]**2)**0.5
        expvalues[nn, 0], expvalues[nn, 1] = x_expected[nn], x_uncertainty[nn]
    np.savetxt("expvalues.dat", expvalues)


if __name__ == '__main__':
    schrodinger(harm_poly)
