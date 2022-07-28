#!/usr/bin/env python3

import argparse
import numpy as np
import pylab as plt
from py4vasp import Calculation

parser = argparse.ArgumentParser()
parser.add_argument("-o","--orbitals", help="orbital, e.g. 1(d) 2(f)", action='store')
parser.add_argument("-t","--title", help="plot title",action='store')
parser.add_argument("-x","--xlim", help="xrange", nargs='*',action='store')
parser.add_argument("-y","--ylim", help="yrange", nargs='*',action='store')
args = parser.parse_args()

plt.figure(figsize=(8,6))
plt.rcParams.update({'font.size': 16})

calc = Calculation.from_path(".")
data = calc.dos.read(selection=args.orbitals)


d=data[ list(data)[2] ] 
f=data[ list(data)[3] ]
plt.plot(data['energies'],d,c='g',label=list(data)[2])
plt.plot(data['energies'],f,c='r',label=list(data)[3])
plt.axvline(0.0,ls='--',c='k')

if(args.xlim is not None):
    plt.xlim(float(args.xlim[0]), float(args.xlim[1]))
else:
    plt.xlim(-5,5)

if(args.ylim is not None):
    plt.ylim(float(args.ylim[0]), float(args.ylim[1]))

plt.xlabel('$E-E_f$ (eV)')
plt.ylabel('PDOS (states/eV/atom)')
plt.title(args.title)
plt.tight_layout()
plt.savefig("dos.png")
#plt.show()
