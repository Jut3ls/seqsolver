#!/usr/bin/env python3
"""
Contains routines to test the eqnsolver module
"""

import eqnsolver
import pytest
import numpy as np

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


if __name__ == '__main__':
    pytest.main()
