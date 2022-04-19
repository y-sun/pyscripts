#!/usr/bin/env python3

import numpy as np
import sys
import pylab as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f","--files", help="PDOS files", nargs='*',action='store')
parser.add_argument("-t","--title", help="plot title",action='store')
args = parser.parse_args()

plt.figure(figsize=(8,6))
plt.rcParams.update({'font.size': 16})

nfile=len(args.files)
for i in range(nfile):
    data=np.loadtxt(args.files[i],skiprows=1)
    plt.plot(data[:,0],data[:,-1],label=args.files[i].split('.')[0])
plt.axvline(0.0,ls='--',c='k')
plt.legend()
plt.xlim(-5,5)
plt.xlabel('E-Ef (eV)')
plt.ylabel('PDOS')
plt.title(args.title)
plt.tight_layout()
plt.show()
    
