# -*- coding: utf-8 -*-
"""
Main function for creating plots from data-files

@author: Ruben
"""
import numpy as np
import matplotlib.pyplot as plt



def importdata(directory):
    '''Function, which creates four arrays from given data:
    energies_data
    discrpot_xdata
    discrpot_ydata
    wfuncs_data    '''

    energiesdir = ".\\" + directory + "\energies.dat"
    discrpotdir = ".\\" + directory + "\discrpot.dat"
    wfuncsdir = ".\\" + directory + "\wfuncs.dat"


    with open(str(energiesdir), "r"):
        energies_data = np.loadtxt(str(energiesdir))


    with open(str(discrpotdir), "r"):
        discrpot_rawdata = np.loadtxt(str(discrpotdir))

        discrpot_xdata = np.zeros(len(discrpot_rawdata), dtype=float)
        for i in range(0, len(discrpot_rawdata)):
            discrpot_xdata[i] = discrpot_rawdata[i, 0]

        discrpot_ydata = np.zeros(len(discrpot_rawdata), dtype=float)
        for j in range(0, len(discrpot_rawdata)):
            discrpot_ydata[j] = discrpot_rawdata[j, 1]


    with open(str(wfuncsdir), "r"):
        wfuncs_rawdata = np.loadtxt(str(wfuncsdir))

        wfuncs_data = np.zeros((len(wfuncs_rawdata), len(wfuncs_rawdata[0])-1), dtype=float)
        for n in range(0, len(wfuncs_rawdata)):
            for m in range(0, len(wfuncs_rawdata[0])-1):
                wfuncs_data[n, m] = wfuncs_rawdata[n, m+1]

    return energies_data, discrpot_xdata, discrpot_ydata, wfuncs_data