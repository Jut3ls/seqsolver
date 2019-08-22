# -*- coding: utf-8 -*-
"""
Main function for creating plots from data-files

@author: Ruben
"""
import numpy as np
# import matplotlib.pyplot as plt


def importdata(directory):
    '''Function, which creates six arrays from given data:
        energies_data
        potential_xdata
        potential_ydata
        wavefuncs_data_x
        wavefuncs_data_y [[y(x1)], ..., [y(xn)]]
        expvalues_xdata
        expvalues_ydata
        '''

    energiesdir = ".\\" + directory + "\energies.dat"
    potentialdir = ".\\" + directory + "\potential.dat"
    wavefuncsdir = ".\\" + directory + "\wavefuncs.dat"
    expvaluesdir = ".\\" + directory + "\expvalues.dat"

    with open(str(energiesdir), "r"):
        energies_data = np.loadtxt(str(energiesdir))

    with open(str(potentialdir), "r"):
        potential_rawdata = np.loadtxt(str(potentialdir))

        potential_xdata = np.zeros(len(potential_rawdata), dtype=float)
        potential_ydata = np.zeros(len(potential_rawdata), dtype=float)
        for i in range(0, len(potential_rawdata)):
            potential_xdata[i] = potential_rawdata[i, 0]
            potential_ydata[i] = potential_rawdata[i, 1]

    with open(str(wavefuncsdir), "r"):
        wavefuncs_rawdata = np.loadtxt(str(wavefuncsdir))

        wavefuncs_xdata = np.zeros(len(wavefuncs_rawdata), dtype=float)
        for k in range(0, len(wavefuncs_rawdata)):
            wavefuncs_xdata[k] = wavefuncs_rawdata[k, 0]

        wavefuncs_ydata = np.zeros((len(wavefuncs_rawdata),
                                    len(wavefuncs_rawdata[0])-1), dtype=float)
        for n in range(0, len(wavefuncs_rawdata)):
            for m in range(0, len(wavefuncs_rawdata[0])-1):
                wavefuncs_ydata[n, m] = wavefuncs_rawdata[n, m+1]

    with open(str(expvaluesdir), "r"):
        expvalues_rawdata = np.loadtxt(str(expvaluesdir))

        expvalues_xdata = np.zeros(len(expvalues_rawdata), dtype=float)
        expvalues_ydata = np.zeros(len(expvalues_rawdata), dtype=float)
        for j in range(0, len(expvalues_rawdata)):
            expvalues_xdata[j] = expvalues_rawdata[j, 0]
            expvalues_ydata[j] = expvalues_rawdata[j, 1]

    return energies_data, potential_xdata, potential_ydata, wavefuncs_xdata
           wavefuncs_ydata, expvalues_xdata, expvalues_ydata;


directory = str()

energies, pot_x, pot_y, wave_x, wave_y, exp_x, exp_y = importdata(directory)

print(energies_123, pot_1, pot_2, wave_1, wave_2, exp_1, exp_2)