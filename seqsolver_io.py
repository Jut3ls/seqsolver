#!/usr/bin/env python3
"""
Main interface for reading and converting input data from schrodinger.inp
"""

import numpy as np
import eqnsolver
from visualizer import visualizer_main as visualize


def main():
    """Main script functionality"""

    print("What do you want to do?\n")
    print("1: Solve the 1D SEQ")
    print("2: Solve the 1D SEQ and visualize the created data")
    print("3: Visualize your own data")

    what_to_do = input("Please select one of the options above: ")

    if what_to_do == "1" or what_to_do == "2":
        directory = input("Please enter the directory of your input file:")
        fp = open(directory + r"\schrodinger.inp", "r")
        lines = fp.readlines()
        data = []
        for i in range(len(lines)):
            data.append(lines[i].split("#")[0])
            data[i] = data[i].split("\t")[0]
            data[i] = data[i].split("\n")[0]
        fp.close()

        discrpot = eqnsolver.discrpot(data)
        eigenval, wfuncs = eqnsolver.solve_schrodinger(data, discrpot)
        expval = eqnsolver.expected_values(data, wfuncs)

        np.savetxt("potential.dat", discrpot)
        np.savetxt("energies.dat", eigenval)
        np.savetxt("wavefuncs.dat", wfuncs)
        np.savetxt("expvalues.dat", expval)

        if what_to_do == "2":
            visualize(".")

    elif what_to_do == "3":
        visualdir = input("Please enter th directory of the data\
                          that should be visualized: ")
        visualize(visualdir)

    else:
        print("Could not understand input. Exiting...")


if __name__ == '__main__':
    main()
