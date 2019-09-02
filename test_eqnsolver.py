#!/usr/bin/env python3
"""
Contains routines to test the eqnsolver module
"""

import numpy as np
import pytest
import eqnsolver

_TOL = 1e-10
_DIR = ["inf", "as", "harmonic", "fin", "dl"]


def _get_input(pos):
    """Get input of the reference files"""
    for i in range(int(pos)):
        fp = open(r"tests/ref_{}/{}.inp".format(_DIR[i], _DIR[i]))
        lines = fp.readlines()
        data = []
        pot_exp = np.loadtxt("tests/ref_{}/potential_{}.dat".format(_DIR[i],
                                                                    _DIR[i]))
        eig_exp = np.loadtxt("tests/ref_{}/energies_{}.dat".format(_DIR[i],
                                                                   _DIR[i]))
        for ii in range(len(lines)):
            data.append(lines[ii].split("#")[0])
            data[ii] = data[ii].split("\t")[0]
            data[ii] = data[ii].split("\n")[0]
    fp.close()
    return data, pot_exp, eig_exp


def test_all():
    """Test all the potentials and energies by iterating"""
    for j in range(len(_DIR)):
        print("\nTest {}".format(j+1))

        data, pot_expected, eigen_expected = _get_input(j+1)

        pot_rec = eqnsolver.discrpot(data, 2)
        eigen_rec = eqnsolver.solve_schrodinger(data, pot_rec)[0]

        assert np.all(np.abs(pot_rec - pot_expected) < _TOL)
        assert np.all(np.abs(eigen_rec - eigen_expected) < _TOL)


if __name__ == '__main__':
    pytest.main()
