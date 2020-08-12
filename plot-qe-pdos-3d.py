#!/usr/bin/env python3

import numpy as np
import sys
import pylab as plt

#get Ef 
fscf=open(sys.argv[1],"r")
for line in fscf:
    if("the Fermi energy is" in line):
        Ef=float(line.split()[-2])
    if("total magnetization" in line):
        mag=line.split()[-3]
fscf.close()

# fe pdos
data=np.loadtxt(sys.argv[2],skiprows=1)
E=data[:,0]-Ef
t2g_up=data[:,5]+data[:,7]+data[:,11]
t2g_dn=data[:,6]+data[:,8]+data[:,12]
eg_up=data[:,3]+data[:,9]
eg_dn=data[:,4]+data[:,10]

plt.figure(figsize=(8,3.3))
plt.rcParams.update({'font.size': 14})
plt.axhline(0,ls='--',color='k',lw=0.5)
plt.plot(E, t2g_up,label=r"$t_{2g}$",c='r')
plt.plot(E,-t2g_dn,c='r')
plt.plot(E, eg_up,label=r"$e_{g}$",c='b')
plt.plot(E,-eg_dn,c='b')
plt.axvline(0,ls='--',color='k',lw=0.5)
plt.legend()
plt.xlim(-12,5)
plt.xlabel(r"$E-E_f (eV)$")
plt.ylabel(r"ProjDOS")
plt.title(sys.argv[3]+", M= "+mag+r" $\mu_B$")
plt.tight_layout()
plt.savefig("pdos.png")
