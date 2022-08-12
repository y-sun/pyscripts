#!/usr/bin/env python3

import argparse
from py4vasp import Calculation

parser = argparse.ArgumentParser()
parser.add_argument("-p","--plot", help="plot histogram", action='store_true')
parser.add_argument("-n","--name", help="plot name",action='store')
args = parser.parse_args()

calc = Calculation.from_path(".")
data=calc.dos.read(selection="1(fy3x2) 1(fxyz) 1(fyz2) 1(fz3) 1(fxz2) 1(fzx2) 1(fx3)")
ldata=list(data)

fout=open("PDOS_f_angular.dat","w+")
for k in range(9):
    print(ldata[k].split("_")[-1],end=" ",file=fout)
print("", file=fout)
for k in range(data['energies'].size):
    for i in range(9):
        print(data[ ldata[i] ][k], end=" ", file=fout)
    print("",file=fout)
fout.close()

if (args.plot):
   import pylab as plt
   import numpy as np
   plt.figure(figsize=(8,6))
   plt.rcParams.update({'font.size': 15})

   fin=open("PDOS_f_angular.dat","r")
   name=fin.readline().split()
   fin.close()

   col=['r','c','g','y','m','olive','b']

   data=np.loadtxt("PDOS_f_angular.dat",skiprows=1)
   for k in range(7):
       if(k>4): lsp='dashed'
       else:   lsp='-'
       lb=name[k+2]
       plt.plot(data[:,0], data[:,k+2], c=col[k], ls=lsp,label=lb)

   if(args.name is not None):
       plt.title(args.name)
   plt.axvline(0,ls='dotted',c='k')
   plt.xlim(-2,6)
   #plt.ylim(-10,10)
   plt.xlabel('E-E$_f$ (eV/atom)')
   plt.ylabel('PDOS')
   plt.legend()
   plt.tight_layout()
   plt.savefig('fig.png')

