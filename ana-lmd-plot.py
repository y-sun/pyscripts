#!/usr/bin/env python3

import sys
import numpy as np

data=np.loadtxt("omega.dat",skiprows=1)
fin=open("omega.dat","r")
ll=fin.readline().split()
elem=[ll[k] for k in range(4,len(ll))]

diff=-(data[:,2]**2-data[:,3]**2)
deon=2*data[:,2]**2
lmd_star=diff/deon

import pylab as plt
plt.figure(figsize=(8,16))
plt.rcParams.update({'font.size': 20})

plt.subplot(3,1,1)
plt.plot(data[:,0], data[:,2],"-o", label="scr", color="b")
plt.plot(data[:,0], data[:,3],"-o", label="unscr", color="r")
plt.title(sys.argv[1])
plt.legend()
plt.tick_params(bottom='off')
plt.xlim(-0.5, max(data[:,0]+0.5))
plt.ylabel("$\omega$ (meV)")

plt.subplot(3,1,2)
plt.plot(data[:-3,0], lmd_star[:-3],"-o", color="k")
plt.xlim(-0.5, max(data[:,0]+0.5))
plt.ylim(-0.05, max(1.05,max(lmd_star[:-3])))
plt.ylabel("$\lambda^{*}$")

plt.subplot(3,1,3)
for k in range(len(elem)):
    plt.plot(data[:,0], data[:,4+k],"-o", label=elem[k])
plt.legend()
plt.xlabel("Mode ID")
plt.ylabel("Fraction")

print(max(lmd_star[:-3]), sum(lmd_star[:-3]))

plt.tight_layout()
plt.savefig("lmd.png")
#plt.show()
