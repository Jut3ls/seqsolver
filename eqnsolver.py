# -*- coding: utf-8 -*-
"""Routines for solving the one dimensional time independent schrodinger
equation for any given potential specified by input data.
"""

import numpy as np
from scipy import interpolate, linalg


def solve(inp):
    """Creates discrete potentials from data provided by input file, then
    solves the discretized 1D SEQ and calculates derived units from discrete
    eigenfunctions.


    :param inp: List of data created from schrodinger.inp by\
    seqsolver_io.main() that specifies the potential, sets interpolation\
    points and declares the interpolation type.


    :return: **pot:** Array containing the discrete potential.

        **energies:** The desired eigenvalues of each wavefunction

        **wavefuncs:** Array containing the eigenfunctions of the discretized
        schrodinger equation.

        **expval:** Two-column array that contains the expected uncertainty of
        the position operator in the first, and expected uncertainty
        when measuring the position in the second column.
    """

    pot = _discrpot(inp)
    energies, wavefuncs = _solve_schrodinger(inp, pot)
    expval = _expected_values(inp, wavefuncs)

    return pot, energies, wavefuncs, expval


def _discrpot(data, deg=None):

    window = np.asarray(data[1].split(" "), dtype=float)

    # Creating empty arrays to fill with data
    xpoint = np.zeros(int(data[4]), dtype=float)
    ypoint = np.zeros(int(data[4]), dtype=float)
    potential = np.zeros(shape=(int(window[2]), 2), dtype=float)
    xval = np.linspace(window[0], window[1], int(window[2]))

    for i in range(5, len(data)):  # Seperating x and y values of points
        xpoint[i-5] = np.asarray(data[i].split())[0]
        ypoint[i-5] = np.asarray(data[i].split())[1]

    if data[3] == "linear":
        yval = np.interp(xval, xpoint, ypoint)

    if data[3] == "polynomial":
        if deg is None:
            deg = input("Please enter the degree of the fitting polynomial: ")
        fit = np.polyfit(xpoint, ypoint, int(deg))
        yval = np.zeros(shape=int(window[2]), dtype=float)
        for j in range(int(window[2])):
            for k in range(int(deg)+1):  # assigning correct xVal to polyfit
                yval[j] += fit[k]*xval[j]**(int(deg)-k)

    if data[3] == "cspline":
        # Interp. data with piecewise cubic poly. with natural boundry cond.
        spline = interpolate.CubicSpline(xpoint, ypoint, bc_type="natural")
        yval = spline.__call__(xval)  # Evaluate spline at x

    for ii in range(int(window[2])):
        potential[ii, 0] = xval[ii]
        potential[ii, 1] = yval[ii]
    return potential


def _solve_schrodinger(data, pot):

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


def _expected_values(data, wfuncs):

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
