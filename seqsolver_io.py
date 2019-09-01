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

    plotinp = input("Do you want to visualize your data? [y/n]:")
    if plotinp == "y":
        visualdir = str()
        use_generated_data = input("Use created data? [y/n]:")
        if use_generated_data == "y":
            visualizer.visualizer_main(visualdir)
        else:
            visualdir = input("Please enter the directory\
 of the data that should be plotted:")
            visualizer.visualizer_main(visualdir)
    else:
        print("Data will not be visualized.")


if __name__ == '__main__':
    main()
