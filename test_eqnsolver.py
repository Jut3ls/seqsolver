#!/usr/bin/env python3
"""
Contains routines to test the eqnsolver module
"""

import numpy as np
import pytest
import eqnsolver

_TOL = 1e-10
_DIR = ["inf", "as", "harmonic", "fin", "dl", "cdl"]


@pytest.mark.parametrize("dir1", _DIR)
def test_parametrized(dir1):
    """Testing all the problems at once using directory as parameter"""

    fp = open(r"tests/ref_{arg}/{arg}.inp".format(arg=dir1))
    lines = fp.readlines()
    data = []

    exppot = np.loadtxt("tests/ref_{arg}/potential_{arg}.dat".format(arg=dir1))
    expeig = np.loadtxt("tests/ref_{arg}/energies_{arg}.dat".format(arg=dir1))

    for ii in range(len(lines)):
        data.append(lines[ii].split("#")[0])
        data[ii] = data[ii].split("\t")[0]
        data[ii] = data[ii].split("\n")[0]
    fp.close()

    recpot = eqnsolver.discrpot(data, 2)
    receig = eqnsolver.solve_schrodinger(data, recpot)[0]

    assert np.all(np.abs(recpot - exppot) < _TOL)
    assert np.all(np.abs(receig - expeig) < _TOL)


if __name__ == '__main__':
    pytest.main()
