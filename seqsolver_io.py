#!/usr/bin/env python3
"""
Main interface for reading and converting input data from schrodinger.inp
"""

import numpy as np
import eqnsolver
import visualizer


def main():
    """Main script functionality"""

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

    plotinp = input("Should the generated data be visualized? [y/n]: ")
    if plotinp == "y":
        visualdir = input(
            "Please enter the directory of the data that should be plotted:")
        visualizer.visualizer_main(visualdir)
    elif plotinp == "n":
        print("Data will not be visualized.")
    else:
        print("Could not understand your input. Data will not be visualized.")


if __name__ == '__main__':
    main()
