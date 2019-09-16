Schrodinger-equation solver Copyright (C) 2019 Julian Bartels, Ruben Neelissen

This programs purpose is to solve the one dimensional time independent schrodinger equation for any potential
specified by an input file, with the option of visualizing the results.

This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

Link to repository: <https://github.com/Jut3ls/seqsolver>

Requirements:
	Python3, numpy, scipy, matplotlib.pyplot, pytest

Usage:

Schrodinger-equation solver:
1) Launch seqsolver_io.py from command line.
   Default directory of the schrodinger.inp input file is the home directory,
   changeable by optional command line argument -d or --directory. Type python seqsolver_io.py -h for help. 

Visualizer:
1) Launch visualizer.py from command line for visualization of your data.
   Visualizer checks if data files are in home directory. If not you will be asked to specify the directory yourself.
   Generates a plot from created or given data. Program sets limits itself. In addition you are able to manually set the limits and modify the amplitude.
	2.1) No manual limits set. Plot saved as plots.pdf in home directory.
	2.2) Manual limits and amplitude modifyer set: 
		 Set amplitude modyfier.
		 Set manual limits. Format: x-min, x-max, y-min, y-max;  default = d 
	Automatic and manually created plots are saved as plots.pdf and manual_plots.pdf respectively.
	
Unit-tests:
1) To start unit tests for six different reference potentials, launch python -m pytest in home directory.



Format of input file (schrodinger.inp):

e.g:
2.0 			# mass
-2.0 2.0 1999 	# xMin xMax nPoint 
1 5 			# first and last eigenvalue to print
linear 			# interpolation type (linear, polynomial, cspline)
2 				# nr. of interpolation points and xy declarations
-2.0 0.0
 2.0 0.0

Units follow the atomic units system where distance is measured in Bohr and mass is described in multiples of electron mass. Unit of energy is Hartree.


Format of data files:

energies.dat:
E1
E2
...


potential.dat:
x1	V(x1)
x2	V(x2)
... ...


wavefuncs.dat:
x1	wf1(x1)	wf2(x1)	wf3(x1)	...
x2	wf1(x2)	wf2(x2)	wf3(x2)	...
x3	wf1(x3)	wf2(x3)	wf3(x3)	...
...	...		...		...


expvalues.dat:
<x1>, sigma(x1)
<x2>, sigma(x2)
...


For additional information regarding public functions of package modules, check out the API documentation under \docs\_build\html\index.html
