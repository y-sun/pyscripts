#!/usr/bin/env python3

import sys
import numpy as np
import math
from scipy.optimize import leastsq
from scipy.optimize import fsolve 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input", help="input file of EV curve, first line ignore",action='store')
parser.add_argument("-p","--prange", help="pressure range", nargs='*',action='store')
parser.add_argument("-n","--noplot", help="no plotting", action='store_true')
parser.add_argument("-f","--fix", help="fix B'", action='store')

args = parser.parse_args()

# Birch-Murnaghan equation of state
def eos_birch_murnaghan(params, vol):
    'From Phys. Rev. B 70, 224107'
    E0, B0, Bp, V0 = params 
    eta = (V0/vol)**(1.0/3.0)
    E = E0 + 9.0*B0*V0/16.0 * (eta**2-1.0)**2 * (6.0 + Bp*(eta**2-1.0) - 4.0*eta**2)
    return E

def eos_birch_murnaghan_fix(params, vol, Bf):
    'From Phys. Rev. B 70, 224107'
    E0, B0, Bp, V0 = params 
    eta = (V0/vol)**(1.0/3.0)
    E = E0 + 9.0*B0*V0/16.0 * (eta**2-1.0)**2 * (6.0 + Bf*(eta**2-1.0) - 4.0*eta**2)
    return E

def pv_BM(params, vol):
    'From Phys. Rev. B 70, 224107'
    E0, B0, Bp, V0 = params 
    eta = (V0/vol)**(1.0/3.0)
    p=3*B0/2*(eta**7-eta**5)*(1+3/4*(Bp-4)*(eta**2-1))*160.21765 # GPa
    return p


fin=open(args.input,"r")
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
if(args.fix is not None):
    Bp=float(args.fix)
else:
    Bp = 4.0

# initial guesses in the same order used in the Murnaghan function
x0 = [E0, B0, Bp, V0]

# fit the equations of state
if(args.fix is not None):
    Bf=float(args.fix)
    target = lambda params, y, x: y - eos_birch_murnaghan_fix(params, x, Bf)
else:
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

# PV
# solve V for a specific P, or verse vise
if(args.prange is None):
    vfit = np.linspace(min(vol),max(vol),100)
    pfit = pv_BM(birch_murn,vfit)
    pfit = np.array(pfit)
else:
    dP=float(args.prange[1])-float(args.prange[0])
    nP=int(dP+0.5)+1
    pfit=np.linspace(float(args.prange[0]),float(args.prange[1]),nP)
    vfit=[]
    for Pi in pfit:
        func = lambda V : pv_BM(birch_murn,V)-Pi
        vok  = fsolve(func,x0=vol.min())
        #print(vok[0],Pi, pv_BM(birch_murn,vok[0]))
        vfit.append(vok[0])
    vfit=np.array(vfit)

fout=open(args.input.strip(".dat")+".PH_fit.dat","w+")
out_H=eos_birch_murnaghan(birch_murn,vfit)+pv_BM(birch_murn,vfit)*vfit/160.21765
print("#P(GPa) H(same_to_input)",file=fout)
for k in range(pfit.size):
    print(pfit[k],out_H[k],file=fout)
fout.close()

fout=open(args.input.strip(".dat")+".PV_fit.dat","w+")
print("#P(GPa) V(same_to_input)",file=fout)
for k in range(pfit.size):
    print(pfit[k],vfit[k],file=fout)
fout.close()

# plot
if (args.noplot):
    exit()

import pylab as plt
vraw = np.linspace(min(vol),max(vol),100)
# EV
plt.subplot(2,1,1)
plt.plot(vol, ene, 'ro', label="raw")
plt.plot(vraw, eos_birch_murnaghan(birch_murn,vraw), label='Birch-Murnaghan 3rd')
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
plt.subplot(2,1,2)
if(args.prange is None):
    plt.plot(pv_BM(birch_murn,vfit), eos_birch_murnaghan(birch_murn,vfit)+pv_BM(birch_murn,vfit)*vfit/160.21765, "-x",
            markersize=5,label="P range from raw")
else:
    plt.plot(pv_BM(birch_murn,vfit), eos_birch_murnaghan(birch_murn,vfit)+pv_BM(birch_murn,vfit)*vfit/160.21765, "-x",
            markersize=5,label="P range from input")
plt.xlabel('P (GPa)')
plt.ylabel('H (eV/atom)')
plt.legend(loc='best')
plt.tight_layout()
plt.savefig(args.input.strip(".dat")+".png")
plt.show()
