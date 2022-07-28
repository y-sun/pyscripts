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

d_up=data[ list(data)[3] ] 
d_dn=data[ list(data)[4] ] 
f_up=data[ list(data)[5] ]
f_dn=data[ list(data)[6] ]

fout=open("PDOS_df.dat",'w+')
print("#E-Ef dos_d_up dos_d_dn dos_f_up dos_f_dn",file=fout)
for k in range(data['energies'].size):
    print(data['energies'][k],d_up[k],d_dn[k],f_up[k],f_dn[k],file=fout)
fout.close()

plt.plot(data['energies'],d_up,c='g',label=list(data)[3])
plt.plot(data['energies'],-d_dn,c='g')
plt.plot(data['energies'],f_up,c='r',label=list(data)[5])
plt.plot(data['energies'],-f_dn,c='r')
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
