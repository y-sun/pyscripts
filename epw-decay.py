#!/usr/bin/env python3

import pylab as plt
import numpy as np

plt.figure(figsize=(12,10))
plt.rcParams.update({'font.size': 16})

plt.subplot(2,2,1)
data=np.loadtxt("decay.H",skiprows=2)
plt.plot(data[:,0],data[:,1],'o',label='Hamiltonian')
plt.xlabel("$R_e\ (\AA)$")
plt.ylabel("$max\ H_{nm} $ (Ry)")
plt.yscale('log')
plt.legend()

plt.subplot(2,2,3)
data=np.loadtxt("decay.epmate",skiprows=1)
plt.plot(data[:,0],data[:,1],'o',label='el-ph matrix elec.')
plt.xlabel("$R_e\ (\AA)$")
plt.ylabel("$max\ g_{nm} $ (Ry)")
plt.yscale('log')
plt.legend()

plt.subplot(2,2,2)
data=np.loadtxt("decay.dynmat",skiprows=2)
plt.plot(data[:,0],data[:,1],'o',label='dynamical matrix')
plt.xlabel("$R_p\ (\AA)$")
plt.ylabel("$max\ D_{nm} $ (Ry)")
plt.yscale('log')
plt.legend()

plt.subplot(2,2,4)
data=np.loadtxt("decay.epmatp",skiprows=1)
plt.plot(data[:,0],data[:,1],'o',label='el-ph matrix phonon')
plt.xlabel("$R_p\ (\AA)$")
plt.ylabel("$max\ g_{nm} $ (Ry)")
plt.yscale('log')
plt.legend()

plt.tight_layout()
plt.savefig('decay.png')
