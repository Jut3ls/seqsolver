# -*- coding: utf-8 -*-
"""Routines for solving the one dimensional time independent schrodinger
equation for any given potential specified by input data.
"""

import numpy as np
from scipy import interpolate, linalg


def solve(inp, deg=None):
    """Creates discrete potentials from data provided by input file, then
    solves the discretized 1D SEQ and calculates derived units from discrete
    eigenfunctions.


    :param inp: List of data created from schrodinger.inp by\
    seqsolver_io.main() that specifies the potential, sets interpolation\
    points and declares the interpolation type.

    :param deg: Only for polynomial fit. If omitted, the program will ask for\
    an input later, if the 'polynomial' option was selected in the input file.\
    Mainly used by the test_eqnsolver module because the degree of the\
    polynomial used in reference data does not change.

    :return: **pot:** Array containing the discrete potential.

        **energies:** The desired eigenvalues of each wavefunction

        **wavefuncs:** Array containing the eigenfunctions of the discretized
        schrodinger equation.

        **expval:** Two-column array that contains the expected uncertainty of
        the position operator in the first, and expected uncertainty
        when measuring the position in the second column.
    """
    mass, window, eigen, xpoint, ypoint, npoint, inttype = _importdata(inp)

    pot = _discrpot(window, xpoint, ypoint, npoint, inttype, deg)

    energies, wavefuncs = _solve_schrodinger(npoint, eigen, mass, pot)

    expval = _expected_values(eigen, npoint, wavefuncs)

    return pot, energies, wavefuncs, expval


def _importdata(data):
    window = np.asarray(data[1].split(" "), dtype=float)
    npoint = int(window[2])
    xpoint = np.zeros(int(data[4]), dtype=float)
    ypoint = np.zeros(int(data[4]), dtype=float)
    mass = float(data[0])
    eigen = np.asarray(data[2].split(" "), dtype=int)
    inttype = data[3]

    for i in range(5, len(data)):  # Seperating x and y values of points
        xpoint[i-5] = np.asarray(data[i].split())[0]
        ypoint[i-5] = np.asarray(data[i].split())[1]

    return mass, window, eigen, xpoint, ypoint, npoint, inttype


def _discrpot(window, xpoint, ypoint, npoint, inttype, deg=None):

    potential = np.zeros(shape=(npoint, 2), dtype=float)
    xval = np.linspace(window[0], window[1], npoint)

    if inttype == "linear":
        yval = np.interp(xval, xpoint, ypoint)

    if inttype == "polynomial":
        if deg is None:
            deg = input("Please enter the degree of the fitting polynomial: ")
        fit = np.polyfit(xpoint, ypoint, int(deg))
        yval = np.zeros(shape=npoint, dtype=float)
        for j in range(npoint):
            for k in range(int(deg)+1):  # assigning correct xVal to polyfit
                yval[j] += fit[k]*xval[j]**(int(deg)-k)

    if inttype == "cspline":
        spline = interpolate.CubicSpline(xpoint, ypoint, bc_type="natural")
        yval = spline.__call__(xval)  # Evaluate spline at x

    potential[:, 0], potential[:, 1] = xval, yval

    return potential


def _solve_schrodinger(npoint, eigen, mass, pot):

    delta_sq = (abs(pot[1, 0])-abs(pot[0, 0]))**2
    add = 1/(mass*delta_sq)

    # Filling matrix with data to solve with linalg.eigh_tridiagonal()
    diag = np.zeros(shape=npoint, dtype=float)
    off_diag = np.zeros(shape=npoint-1, dtype=float)

    diag = add + pot[:, 1]
    off_diag[:] = -0.5*add

    energies, wavefuncs = linalg.eigh_tridiagonal(diag, off_diag, select="i",
                                                  select_range=eigen-1)

    wave_new = np.zeros(shape=(npoint, eigen[1]+1), dtype=float)
    wave_new[:, 0] = pot[:, 0]
    for mm in range(eigen[1]):
        wave_new[:, mm+1] = wavefuncs[:, mm]

    return energies, wave_new


def _expected_values(eigen, npoint, wfuncs):

    x_expected = np.zeros(shape=eigen[1], dtype=float)
    x_squared, x_uncertainty = np.array(x_expected), np.array(x_expected)
    expvalues = np.zeros(shape=(eigen[1], 2), dtype=float)

    for nn in range(eigen[1]):
        for i in range(npoint):
            x_expected[nn] += wfuncs[i, nn+1]*wfuncs[i, 0]*wfuncs[i, nn+1]
            x_squared[nn] += wfuncs[i, nn+1]*wfuncs[i, 0]**2*wfuncs[i, nn+1]
        x_uncertainty[nn] = (x_squared[nn] - x_expected[nn]**2)**0.5
        expvalues[nn, 0], expvalues[nn, 1] = x_expected[nn], x_uncertainty[nn]

    return expvalues
