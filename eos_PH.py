#!/usr/bin/env python3

import sys
import numpy as np
import math
from scipy.optimize import leastsq
from scipy.optimize import fsolve 

# Birch-Murnaghan equation of state
def eos_birch_murnaghan(params, vol):
    'From Phys. Rev. B 70, 224107'
    E0, B0, Bp, V0 = params 
    eta = (V0/vol)**(1.0/3.0)
    E = E0 + 9.0*B0*V0/16.0 * (eta**2-1.0)**2 * (6.0 + Bp*(eta**2-1.0) - 4.0*eta**2)
    return E

def pv_BM(params, vol):
    'From Phys. Rev. B 70, 224107'
    E0, B0, Bp, V0 = params 
    eta = (V0/vol)**(1.0/3.0)
    p=3*B0/2*(eta**7-eta**5)*(1+3/4*(Bp-4)*(eta**2-1))*160.21765 # GPa
    return p


fin=open(sys.argv[1],"r")
vol=[]; ene=[]; press=[]
fin.readline()
for line in fin:
    ll=line.split()
#    if(float(ll[2]) > 200):
#        continue
    vol.append(float(ll[1]))
    ene.append(float(ll[2]))
#    press.append(float(ll[2]))

# transform to numpy arrays
vol = np.array(vol)
ene = np.array(ene)
#press = np.array(press)

# fit a parabola to the data and get inital guess for equilibirum volume
# and bulk modulus
a, b, c = np.polyfit(vol, ene, 2)
V0 = -b/(2*a)
E0 = a*V0**2 + b*V0 + c
B0 = 2*a*V0
Bp = 4.0

# initial guesses in the same order used in the Murnaghan function
x0 = [E0, B0, Bp, V0]

# fit the equations of state
target = lambda params, y, x: y - eos_birch_murnaghan(params, x)
birch_murn, ier = leastsq(target, x0, args=(ene,vol))
print("E0 + 9.0*B0*V0/16.0 * (eta**2-1.0)**2 * (6.0 + Bp*(eta**2-1.0) - 4.0*eta**2)")
#print("E0, B0, Bp, V0=",birch_murn)
print("E0, B0, Bp, V0=",birch_murn[0], birch_murn[1]*160.21765, birch_murn[2], birch_murn[3])
E_fitted=eos_birch_murnaghan(birch_murn, vol)
P_fitted=pv_BM(birch_murn,vol)
print("vol E_org E_fit P_fit")
for k in range(len(vol)):
    print(vol[k],ene[k],E_fitted[k],P_fitted[k])

vfit = np.linspace(min(vol),max(vol),100)
fout=open(sys.argv[1].strip(".dat")+".PH_fit.dat","w+")
out_P=pv_BM(birch_murn,vfit)
out_H=eos_birch_murnaghan(birch_murn,vfit)+pv_BM(birch_murn,vfit)*vfit/160.21765
for k in range(len(out_P)):
    print(out_P[k],out_H[k],file=fout)
fout.close()

fout=open(sys.argv[1].strip(".dat")+".PV_fit.dat","w+")
out_P=pv_BM(birch_murn,vfit)
for k in range(len(out_P)):
    print(out_P[k],vfit[k],file=fout)
fout.close()

#'''
import pylab as plt

# EV
plt.subplot(2,1,1)
plt.plot(vol, ene, 'ro')
plt.plot(vfit, eos_birch_murnaghan(birch_murn,vfit), label='Birch-Murnaghan')
plt.xlabel('Volume ($\AA^3$/atom)')
plt.ylabel('Energy (eV/atom)')
plt.legend(loc='best')

# PV
#plt.subplot(1,2,2)
#plt.plot(vol, press, 'ro')
#plt.plot(vfit, pv_BM(birch_murn,vfit), label="BM fit")
#plt.xlabel('Volume ($\AA^3$/atom)')
#plt.ylabel('P (GPa)')
#plt.legend(loc='best')

# PH
# solve V for a specific P
pfit = np.linspace(150,400,100)
vfit = []
for Pi in pfit:
    func = lambda V : pv_BM(birch_murn,V)-Pi
    vok  = fsolve(func,x0=vol.min())
    #print(vok[0],Pi, pv_BM(birch_murn,vok[0]))
    vfit.append(vok[0])

plt.subplot(2,1,2)
plt.plot(pv_BM(birch_murn,vfit), eos_birch_murnaghan(birch_murn,vfit)+pv_BM(birch_murn,vfit)*vfit/160.21765, "-o",label="by BM fit")
plt.xlabel('P (GPa)')
plt.ylabel('H (eV/atom)')
plt.legend(loc='best')
plt.tight_layout()
plt.savefig(sys.argv[1].strip(".dat")+".png")
plt.show()

#'''
