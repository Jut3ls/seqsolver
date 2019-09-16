#!/usr/bin/env python3
"""
Main user interface for reading and converting input data from schrodinger.inp
"""

import numpy as np
import os.path
import argparse
from eqnsolver import solve

_DESCRIPTION = "Explaining command line arguments"


def main():
    """
    Solves the 1D SEQ by converting schrodinger.inp input data to a list
    and calls eqnsolver.solve() with that list as an argument, then saves the
    returned values as .dat output files. The input data directory can be
    passed with the optional argument -d or --directory.
    """

    parser = argparse.ArgumentParser(description=_DESCRIPTION)
    msg = "Directory  (default: .)"
    parser.add_argument("-d", "--directory", default=".", help=msg)
    args = parser.parse_args()

    path = os.path.join(args.directory, "schrodinger.inp")
    fp = open(path, "r")
    lines = fp.readlines()
    data = []

    for line in lines:
        data.append(line.split("#")[0])
    # removing whitespaces and newlines from list
    newdata = [entry.strip().split("\n")[0] for entry in data]
    fp.close()

    discrpot, eigenval, wfuncs, expval = solve(newdata)

    np.savetxt("potential.dat", discrpot)
    np.savetxt("energies.dat", eigenval)
    np.savetxt("wavefuncs.dat", wfuncs)
    np.savetxt("expvalues.dat", expval)


if __name__ == '__main__':
    main()
