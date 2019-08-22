# -*- coding: utf-8 -*-
"""Routines for solving the one dimensional time independent schrodinger
equation for any given potential."""

import numpy as np
from scipy import interpolate, linalg


def discrpot(data):
    """Creates discrete potentials from data provided by input file.
    The interpolation type is specified by the user in the input file.


    Args:
        data: List of data that specifies the problem, sets interpolation
        points and declares the interpolation type.


    Returns:
        Array containing the discrete potential.
    """

    window = np.asarray(data[1].split(" "), dtype=float)

    # Creating empty arrays to fill with data
    xpoint = np.zeros(int(data[4]), dtype=float)
    ypoint = np.zeros(int(data[4]), dtype=float)
    potential = np.zeros(shape=(int(window[2]), 2), dtype=float)
    xval = np.linspace(window[0], window[1], int(window[2]))

    for i in range(5, len(data)):  # Seperating x and y values of interp points
        xpoint[i-5] = np.asarray(data[i].split())[0]
        ypoint[i-5] = np.asarray(data[i].split())[1]

    if data[3] == "linear":
        yval = np.interp(xval, xpoint, ypoint)

    if data[3] == "polynomial":
        deg = input("Please enter the degree of the fitting polynomial: ")
        fit = np.polyfit(xpoint, ypoint, int(deg))
        yval = np.zeros(shape=int(window[2]), dtype=float)
        for j in range(int(window[2])):
            for k in range(int(deg)+1):  # assigning correct xVal to polyfit
                yval[j] += fit[k]*xval[j]**(int(deg)-k)

    if data[3] == "cspline":
        tck = interpolate.splrep(xpoint, ypoint)  # Find the spline repres.
        yval = interpolate.splev(xval, tck)  # Evaluate discrete data at xVal

    for ii in range(int(window[2])):
        potential[ii, 0] = xval[ii]
        potential[ii, 1] = yval[ii]
    return potential


def solve_schrodinger(data, pot):
    """Solves the 1D time independent schrodinger equation by discretizing it.


    Args:
        data: List of data that specifies the problem, sets interpolation
        points and declares the interpolation type.

        pot: Array of shape (nPoint, 2) which contains a discrete potential


    Returns:
        energies: The eigenvalues of the wavefunctions in an array

        wave_new: Array containing the eigenfunctions of the discretized SEQ
    """

    window = np.asarray(data[1].split(" "), dtype=float)
    eigen = np.asarray(data[2].split(" "), dtype=int)
    delta_sq = (abs(pot[1, 0])-abs(pot[0, 0]))**2
    add = 1/(float(data[0])*delta_sq)

    # Filling matrix with data to solve with linalg.eigh_tridiagonal()
    diag = np.zeros(shape=int(window[2]), dtype=float)
    off_diag = np.zeros(shape=int(window[2])-1, dtype=float)
    for jj in range(int(window[2])):
        diag[jj] = add + pot[jj, 1]
    for kk in range(int(window[2]-1)):
        off_diag[kk] = -0.5*add

    energies, wavefuncs = linalg.eigh_tridiagonal(diag, off_diag, select="i",
                                                  select_range=eigen-1)

    wave_new = np.zeros(shape=(int(window[2]), eigen[1]+1), dtype=float)
    for ll in range(int(window[2])):
        wave_new[ll, 0] = pot[ll, 0]
        for mm in range(eigen[1]):
            wave_new[ll, mm+1] = wavefuncs[ll, mm]

    return energies, wave_new


def expected_values(data, wfuncs):
    """String


    Args:
        data: List of data that specifies the problem, sets interpolation
        points and declares the interpolation type.

        wfuncs: Array containing the discrete eigenfunctions of the 1D SEQ


    Returns:
        expvalues: Two-column array that contains the expected uncertainty of
        the position operator in the first, and expected uncertainty when
        measuring the position in the second column.
    """

    window = np.asarray(data[1].split(" "), dtype=float)
    eigenval = np.asarray(data[2].split(" "), dtype=int)

    x_expected = np.zeros(shape=eigenval[1], dtype=float)
    x_squared, x_uncertainty = np.array(x_expected), np.array(x_expected)
    expvalues = np.zeros(shape=(eigenval[1], 2), dtype=float)

    for nn in range(eigenval[1]):
        for i in range(int(window[2])):
            x_expected[nn] += wfuncs[i, nn+1]*wfuncs[i, 0]*wfuncs[i, nn+1]
            x_squared[nn] += wfuncs[i, nn+1]*wfuncs[i, 0]**2*wfuncs[i, nn+1]
        x_uncertainty[nn] = (x_squared[nn] - x_expected[nn]**2)**0.5
        expvalues[nn, 0], expvalues[nn, 1] = x_expected[nn], x_uncertainty[nn]
    return expvalues
