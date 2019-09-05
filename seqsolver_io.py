#!/usr/bin/env python3
"""
Main user interface for reading and converting input data from schrodinger.inp
"""

import numpy as np
from eqnsolver import solve
from visualizer import visualize


def main():
    """Calls eqnsolver.solve() and visualizer.visualize() in a different manner
    depending on user input. User can choose between one of these tree
    options:

    *1: Solve the 1D SEQ*:
        Converts schrodinger.inp input data to a list and calls
        eqnsolver.solve() with that list as an argument, then saves the
        returned values as .dat output files.
    *2: Solve the 1D SEQ and visualize the created data*:
        Runs the same routines as option 1, but also calls
        visualizer.visualize() to visualize the data obtained by
        eqnsolver.solve().
    *3: Visualize your own data*:
        Only calls visualizer.visualize to plot existing data from a given
        directory if .dat files follow the 'potential', 'wavefuncs', 'eigenval'
        and 'expval' naming convention.

    """

    print("What do you want to do?\n")
    print("1: Solve the 1D SEQ")
    print("2: Solve the 1D SEQ and visualize the created data")
    print("3: Visualize your own data")

    what_to_do = input("Please select one of the options above: ")

    if what_to_do == "1" or what_to_do == "2":
        directory = input("Please enter the directory of your input file: ")
        fp = open(directory + r"\schrodinger.inp", "r")
        lines = fp.readlines()
        data = []
        for i in range(len(lines)):
            data.append(lines[i].split("#")[0])
            data[i] = data[i].split("\t")[0]
            data[i] = data[i].split("\n")[0]
        fp.close()

        discrpot, eigenval, wfuncs, expval = solve(data)

        np.savetxt("potential.dat", discrpot)
        np.savetxt("energies.dat", eigenval)
        np.savetxt("wavefuncs.dat", wfuncs)
        np.savetxt("expvalues.dat", expval)

        if what_to_do == "2":
            visualize(".")

    elif what_to_do == "3":
        visualdir = input("Please enter the directory of the data ds"
                          "that should be visualized: ")
        visualize(visualdir)

    else:
        print("Could not understand input. Exiting...")


if __name__ == '__main__':
    main()
