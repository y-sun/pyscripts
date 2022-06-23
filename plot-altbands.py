#!/usr/bin/env python3

import numpy as np
import pylab as plt

data_up=np.loadtxt("REFORMATTED_BAND_UP.dat",skiprows=1)
data_dn=np.loadtxt("REFORMATTED_BAND_DW.dat",skiprows=1)
# k label
fin=open("KLABELS",'r')
fin.readline()
k_name=[]
k_pos=[]
for line in fin:
    ll=line.split()
    if(len(ll)==0):
        break
    k_name.append(ll[0])
    k_pos.append(float(ll[1]))
fin.close()

plt.figure(figsize=(8,6))
plt.rcParams.update({'font.size': 16})

ncol=data_up.shape[1]
colors=plt.cm.rainbow(np.linspace(0,1,(ncol-1)*2))
ic=0
for k in range(1,ncol):
   plt.plot(data_up[:,0], data_up[:,k], ls='-', c=colors[ic])
   ic+=1
for k in range(1,ncol):
   plt.plot(data_dn[:,0], data_dn[:,k], ls='--', c=colors[ic])
   ic+=1

plt.ylim([-2,1.5])
plt.xticks(k_pos, k_name)
#plt.xlim(min(data_up[:,0]),max(data_dn[:,0]))
plt.xlim(k_pos[0],k_pos[-1])
for kp in k_pos:
    plt.axvline(kp,ls='-',c='k')
plt.axhline(0,ls='--',c='k')
plt.ylabel("E-E$_f$ (eV)")

plt.tight_layout()
plt.savefig('bands.png')
plt.show()
