#!/usr/bin/env python3
"""
Contains routines to test the eqnsolver module
"""

import eqnsolver
import numpy as np
import pytest


TOL = 1e-10


def test_eqnsolver_infwell():
    """Test potential and eigenvalues of the infinite well problem"""
    print("\nTest 1")

    fp = open(r"tests/ref_inf/inf.inp", "r")
    lines = fp.readlines()
    inf_data = []
    for i in range(len(lines)):
        inf_data.append(lines[i].split("#")[0])
        inf_data[i] = inf_data[i].split("\t")[0]
        inf_data[i] = inf_data[i].split("\n")[0]
    fp.close()

    pot_rec = eqnsolver.discrpot(inf_data)
    eigen_rec, wfuncs_rec = eqnsolver.solve_schrodinger(inf_data, pot_rec)

    pot_expected = np.loadtxt(r"tests/ref_inf/potential_inf.dat")
    eigen_expected = np.loadtxt(r"tests/ref_inf/energies_inf.dat")

    assert np.all(np.abs(pot_rec - pot_expected) < TOL)
    assert np.all(np.abs(eigen_rec - eigen_expected) < TOL)


def test_eqnsolver_asymmetrical():
    """Test potential and eigenvalues of the asymmetrical potential problem"""
    print("\nTest 2")

    fp = open(r"tests/ref_asymmetric/as.inp", "r")
    lines = fp.readlines()
    as_data = []
    for i in range(len(lines)):
        as_data.append(lines[i].split("#")[0])
        as_data[i] = as_data[i].split("\t")[0]
        as_data[i] = as_data[i].split("\n")[0]
    fp.close()

    pot_rec = eqnsolver.discrpot(as_data)
    eigen_rec, wfuncs_rec = eqnsolver.solve_schrodinger(as_data, pot_rec)

    pot_expected = np.loadtxt(r"tests/ref_asymmetric/potential_as.dat")
    eigen_expected = np.loadtxt(r"tests/ref_asymmetric/energies_as.dat")

    assert np.all(np.abs(pot_rec - pot_expected) < TOL)
    assert np.all(np.abs(eigen_rec - eigen_expected) < TOL)


def test_eqnsolver_harmonic():
    """Test potential and eigenvalues of the harmonic potential problem"""
    print("\nTest 3")

    fp = open(r"tests/ref_harmonic/harmonic.inp", "r")
    lines = fp.readlines()
    h_data = []
    for i in range(len(lines)):
        h_data.append(lines[i].split("#")[0])
        h_data[i] = h_data[i].split("\t")[0]
        h_data[i] = h_data[i].split("\n")[0]
    fp.close()

    pot_rec = eqnsolver.discrpot(h_data)
    eigen_rec, wfuncs_rec = eqnsolver.solve_schrodinger(h_data, pot_rec)

    pot_expected = np.loadtxt(r"tests/ref_harmonic/potential_harmonic.dat")
    eigen_expected = np.loadtxt(r"tests/ref_harmonic/energies_harmonic.dat")

    assert np.all(np.abs(pot_rec - pot_expected) < TOL)
    assert np.all(np.abs(eigen_rec - eigen_expected) < TOL)


def test_eqnsolver_fin():
    """Test potential and eigenvalues of the finite potential well problem"""
    print("\nTest 4")

    fp = open(r"tests/ref_fin/fin.inp", "r")
    lines = fp.readlines()
    fin_data = []
    for i in range(len(lines)):
        fin_data.append(lines[i].split("#")[0])
        fin_data[i] = fin_data[i].split("\t")[0]
        fin_data[i] = fin_data[i].split("\n")[0]
    fp.close()

    pot_rec = eqnsolver.discrpot(fin_data)
    eigen_rec, wfuncs_rec = eqnsolver.solve_schrodinger(fin_data, pot_rec)

    pot_expected = np.loadtxt(r"tests/ref_fin/potential_fin.dat")
    eigen_expected = np.loadtxt(r"tests/ref_fin/energies_fin.dat")

    assert np.all(np.abs(pot_rec - pot_expected) < TOL)
    assert np.all(np.abs(eigen_rec - eigen_expected) < TOL)


def test_eqnsolver_double_linear():
    """Test potential and eigenvalues of the double well problem
    (linear interpolation)"""
    print("\nTest 5")

    fp = open(r"tests/ref_dl/double_linear.inp", "r")
    lines = fp.readlines()
    dl_data = []
    for i in range(len(lines)):
        dl_data.append(lines[i].split("#")[0])
        dl_data[i] = dl_data[i].split("\t")[0]
        dl_data[i] = dl_data[i].split("\n")[0]
    fp.close()

    pot_rec = eqnsolver.discrpot(dl_data)
    eigen_rec, wfuncs_rec = eqnsolver.solve_schrodinger(dl_data, pot_rec)

    pot_expected = np.loadtxt(r"tests/ref_dl/potential_double_linear.dat")
    eigen_expected = np.loadtxt(r"tests/ref_dl/energies_double_linear.dat")

    assert np.all(np.abs(pot_rec - pot_expected) < TOL)
    assert np.all(np.abs(eigen_rec - eigen_expected) < TOL)


if __name__ == '__main__':
    pytest.main()
