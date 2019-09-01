# -*- coding: utf-8 -*-
"""
Main function for creating plots from data-files

@author: Ruben
"""
import numpy as np
import matplotlib.pyplot as plt


def visualizer_main():
    '''
    Creates plot from given directory, with optional scaling adjustments and
    save options.
    Args:
        directory: directory containing .dat files.

    Returns:
        Plot-file saved as "plots.pdf"
    '''
    directory = str()

    # import data:
    (energies_data, potential_xdata, potential_ydata, wavefuncs_xdata,
     wavefuncs_ydata, expvalues_data) = _importdata(directory)

    # make plot automaticly:
    _auto_make_plot(energies_data, potential_xdata, potential_ydata,
                    wavefuncs_xdata, wavefuncs_ydata, expvalues_data)

    # manually adjust scale:
    adjust_limits = input("Manually adjust limits and amplitude? [y/n]")
    if str(adjust_limits) == "y":
        _manual_make_plot(energies_data, potential_xdata, potential_ydata,
                          wavefuncs_xdata, wavefuncs_ydata, expvalues_data)
    else:
        print("Plot created!")


def _importdata(directory):
    '''Function, which creates six arrays from potential.dat, energies.dat,
    wavefunc.dat and expvalues.dat files.

    Args:
        directory: Argument containing the directory of input .dat files.

    Returns:
        energies_data: Array with energie data (eigenvalues).
        potential_xdata: Array with potential x-data.
        potential_ydata: Array with potential y-data.
        wavefuncs_xdata: Array with wavefunction x-data.
        wavefuncs_ydata: Array with wavefunction y-data
                         [[y1(x1), y2(x1), ...], ..., [y1(xn), y2(xn), ...]].
        expvalues_xdata: Array with expvalues x-data.
        '''
    energiesdir = "./" + directory + "/energies.dat"
    potentialdir = "./" + directory + "/potential.dat"
    wavefuncsdir = "./" + directory + "/wavefuncs.dat"
    expvaluesdir = "./" + directory + "/expvalues.dat"

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
        expvalues_data = np.loadtxt(str(expvaluesdir))

    return(energies_data, potential_xdata, potential_ydata, wavefuncs_xdata,
           wavefuncs_ydata, expvalues_data)


def _auto_make_plot(energies_data, potential_xdata, potential_ydata,
                    wavefuncs_xdata, wavefuncs_ydata, expvalues_data):
    '''Trying to make two plots from data createn by importdata-function.

    Args:
        energies_data: Array with energie data (eigenvalues).
        potential_xdata: Array with potential x-data.
        potential_ydata: Array with potential y-data.
        wavefuncs_xdata: Array with wavefunction x-data.
        wavefuncs_ydata: Array with wavefunction y-data
                         [[y1(x1), y2(x1), ...], ..., [y1(xn), y2(xn), ...]].
        expvalues_xdata: Array with expvalues x-data.
        expvalues_ydata: Array with expvalues y-data.

    Returns:
        Plot saved as pdf file.
    '''
    plt.figure(figsize=(10, 10), dpi=80)

    # plot 1:
    plt.subplot(1, 2, 1)  # plotting wavefunctions, energies and potential

    # energy levels
    for y_energy_data in energies_data:
        x_energy = [wavefuncs_xdata[0],
                    wavefuncs_xdata[len(wavefuncs_xdata)-1]]
        y_energy = [y_energy_data, y_energy_data]
        plt.plot(x_energy, y_energy, linestyle="--", color="grey")

    # wavefunctions
    y_wave = np.zeros(len(wavefuncs_xdata), dtype=float)
    for j in range(0, len(energies_data), 2):
        for k in range(0, len(wavefuncs_xdata)):
            y_wave[k] = wavefuncs_ydata[k, j] + energies_data[j]
        plt.plot(wavefuncs_xdata, y_wave, linestyle="-", color="red")

    for j in range(1, len(energies_data), 2):
        for k in range(0, len(wavefuncs_xdata)):
            y_wave[k] = wavefuncs_ydata[k, j] + energies_data[j]
        plt.plot(wavefuncs_xdata, y_wave, linestyle="-", color="blue")

    # potential
    plt.plot(potential_xdata, potential_ydata, linestyle="-", color="black")

    # expected values x
    for o in range(0, len(expvalues_data)):
        plt.plot(expvalues_data[o, 0], energies_data[o], 'x', markersize=10,
                 color="purple")

    # format
    # setting some variables
    # lim_wave = [x_min, x_max, y_min, y_max]
    lim_wave = [min(potential_xdata),
                max(potential_xdata),
                min(potential_ydata) - abs(min(potential_ydata)-0.5) * 0.1,
                (energies_data[len(energies_data)-1] +
                 energies_data[len(energies_data)-1] * 0.1)]
    if abs(lim_wave[3]) <= 0.5:
        lim_wave[3] = 0.1 * abs(min(lim_wave))

    # setting format
    plt.xlabel("x [Bohr]", size=16)
    plt.ylabel("Energies [Hartree]", size=16)
    plt.title("Potential, Eigenstates", size=20)
    _format(lim_wave)

    # plot 2: ###################################################
    plt.subplot(1, 2, 2)  # plotting energy levels and exp-values

    # energy levels
    for y_energy_data in energies_data:
        x_energy = [wavefuncs_xdata[0],
                    wavefuncs_xdata[len(wavefuncs_xdata)-1]]
        y_energy = [y_energy_data, y_energy_data]
        plt.plot(x_energy, y_energy, linestyle="--", color="grey")

    # exp-values (sigma)
    for m in range(0, len(expvalues_data)):
        plt.plot(expvalues_data[m, 1], energies_data[m], 'x', markersize=10,
                 color="purple")

    # format
    # setting some variables
    x_max_exp = np.zeros(len(expvalues_data), dtype=float)
    for i in range(len(expvalues_data)):
        x_max_exp[i] = expvalues_data[i, 1]

    # lim_exp = [x_min, x_max, y_min, y_max]
    lim_exp = [0,
               max(x_max_exp) + max(x_max_exp) * 0.1,
               lim_wave[2],
               lim_wave[3]]

    # setting format
    plt.xlabel("[Bohr]", size=16)
    plt.title(r'$\sigma_x$', size=20)
    _format(lim_exp)

    # saving plot
    plt.savefig('plots.pdf', format='pdf')
    print("Plot image saved as plots.pdf")


def _manual_make_plot(energies_data, potential_xdata, potential_ydata,
                      wavefuncs_xdata, wavefuncs_ydata, expvalues_data):
    '''Making two plots with manual set amplitude and limits.

    Args:
        energies_data: Array with energie data (eigenvalues).
        potential_xdata: Array with potential x-data.
        potential_ydata: Array with potential y-data.
        wavefuncs_xdata: Array with wavefunction x-data.
        wavefuncs_ydata: Array with wavefunction y-data
                         [[y1(x1), y2(x1), ...], ..., [y1(xn), y2(xn), ...]].
        expvalues_xdata: Array with expvalues x-data.
        expvalues_ydata: Array with expvalues y-data.

    Returns:
        Manual created plot saved as pdf file.
    '''
    # set manual limits and amplitude factor

    # format (variables)
    # plot 1:
    lim_wave = [min(potential_xdata),
                max(potential_xdata),
                min(potential_ydata) - abs(min(potential_ydata)-0.5) * 0.1,
                (energies_data[len(energies_data)-1] +
                 energies_data[len(energies_data)-1] * 0.1)]
    if abs(lim_wave[3]) <= 0.5:
        lim_wave[3] = 0.1 * abs(min(lim_wave))

    # plot 2:
    x_max_exp = np.zeros(len(expvalues_data), dtype=float)
    for i in range(len(expvalues_data)):
        x_max_exp[i] = expvalues_data[i, 1]

    lim_exp = [0,
               max(x_max_exp) + max(x_max_exp) * 0.1,
               lim_wave[2],
               lim_wave[3]]

    # make plots:
    plt.figure(figsize=(10, 10), dpi=80)

    # plot 2:
    plt.subplot(1, 2, 2)  # plotting energy levels and exp-values

    # energy levels
    for y_energy_data in energies_data:
        x_energy = [wavefuncs_xdata[0],
                    wavefuncs_xdata[len(wavefuncs_xdata)-1]]
        y_energy = [y_energy_data, y_energy_data]
        plt.plot(x_energy, y_energy, linestyle="--", color="grey")

    # exp-values (sigma)
    for m in range(0, len(expvalues_data)):
        plt.plot(expvalues_data[m, 1], energies_data[m], 'x', markersize=10,
                 color="purple")

    # setting format
    plt.xlabel("[Bohr]", size=16)
    plt.title(r'$\sigma_x$', size=20)
    _format(lim_exp)

    # plot 1
    # set amplitude factor
    amplitude = 1
    input_amplitude = input("set amplitude (default: 1):")
    amplitude = float(input_amplitude)

    # setting manual limits of wave plot
    manual_limits = input("Set limits of wavefunction plot (format: [x-min,\
x-max, y-min, y-max], default = d)")
    manual_lim_wave = manual_limits.split(", ")

    for i in range(len(lim_wave)):
        if manual_lim_wave[i].lstrip('-').isdigit():
            lim_wave[i] = int(manual_lim_wave[i])

    # make plot:
    plt.subplot(1, 2, 1)  # plotting wavefunctions, energies and potential

    # energy levels
    for y_energy_data in energies_data:
        x_energy = [wavefuncs_xdata[0],
                    wavefuncs_xdata[len(wavefuncs_xdata)-1]]
        y_energy = [y_energy_data, y_energy_data]
        plt.plot(x_energy, y_energy, linestyle="--", color="grey")

    # wavefunctions
    y_wave = np.zeros(len(wavefuncs_xdata), dtype=float)
    for j in range(0, len(energies_data), 2):
        for k in range(0, len(wavefuncs_xdata)):
            y_wave[k] = wavefuncs_ydata[k, j] * amplitude + energies_data[j]
        plt.plot(wavefuncs_xdata, y_wave, linestyle="-", color="red")

    for j in range(1, len(energies_data), 2):
        for k in range(0, len(wavefuncs_xdata)):
            y_wave[k] = wavefuncs_ydata[k, j] * amplitude + energies_data[j]
        plt.plot(wavefuncs_xdata, y_wave, linestyle="-", color="blue")

    # potential
    plt.plot(potential_xdata, potential_ydata, linestyle="-", color="black")

    # expected values x
    for o in range(0, len(expvalues_data)):
        plt.plot(expvalues_data[o, 0], energies_data[o], 'x', markersize=10,
                 color="purple")

    # setting format
    plt.xlabel("x [Bohr]", size=16)
    plt.ylabel("Energies [Hartree]", size=16)
    plt.title("Potential, Eigenstates\nAmplitude {}"
              .format(amplitude), size=20)
    _format(lim_wave)

    # saving plot
    plt.savefig('manual_plots.pdf', format='pdf')
    print("Plot image saved as manual_plots.pdf")


def _format(array):
    plt.xlim(array[0], array[1])
    plt.ylim(array[2], array[3])
    plt.xticks(np.arange(round(array[0]),
                         round(array[1]) + 0.0001,
                         round((np.absolute(array[1] -
                                            array[0])) + .5) * 0.2),
               fontsize=12)
    plt.yticks(np.arange(round(array[2]),
                         round(array[3]) + 0.0001,
                         round((np.absolute(array[3] -
                                            array[2])) + .5) * 0.2),
               fontsize=12)
