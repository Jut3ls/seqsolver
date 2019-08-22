#!/usr/bin/env python3
"""
Main interface for reading and converting input data from schrodinger.inp
"""

import sys
import eqnsolver
import visualizer

def main():
    """Main script functionality"""

    directory = input("Please enter the directory of your input file:")
    try:
        fp = open(directory + r"\schrodinger.inp", "r")
    except FileNotFoundError:
        print("Can not open file {}".format("schrodinger.inp"))
        print("Exiting...")
        sys.exit(1)
    else:
        lines = fp.readlines()
        data = []
        for i in range(len(lines)):
            data.append(lines[i].split("#")[0])
            data[i] = data[i].split("\t")[0]
            data[i] = data[i].split("\n")[0]
    fp.close()

    eqnsolver.schrodinger(data)

    visualizer.plot(directory)

if __name__ == '__main__':
    main()
