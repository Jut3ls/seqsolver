#!/usr/bin/env python3
"""
Contains routines to test the eqnsolver module.
"""

import numpy as np
import pytest
import eqnsolver

_TOL = 1e-10
_DIR = ["inf", "as", "harmonic", "fin", "dl", "cdl"]


@pytest.mark.parametrize("dir1", _DIR)
def test_parametrized(dir1):
    """Testing the eqnsolver module for a set of six reference potentials and
    eigenvalues. Test can be executed from shell.


    :param dir1: Internal list of directories leading to the reference files\
    used for parametrization by pytest.

    """

    exppot = np.loadtxt("tests/ref_{arg}/potential_{arg}.dat".format(arg=dir1))
    expeig = np.loadtxt("tests/ref_{arg}/energies_{arg}.dat".format(arg=dir1))

    fp = open(r"tests/ref_{arg}/{arg}.inp".format(arg=dir1))
    lines = fp.readlines()
    data = []

    for line in lines:
        data.append(line.split("#")[0])
    # removing whitespaces and newlines from list
    newdata = [entry.strip().split("\n")[0] for entry in data]
    fp.close()

    recpot = eqnsolver._discrpot(newdata, 2)
    receig = eqnsolver._solve_schrodinger(newdata, recpot)[0]

    assert np.all(np.abs(recpot - exppot) < _TOL)
    assert np.all(np.abs(receig - expeig) < _TOL)


if __name__ == '__main__':
    pytest.main()
