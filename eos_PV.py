#!/usr/bin/env python3

import sys
import numpy as np
import math
from scipy.optimize import leastsq
from scipy.optimize import fsolve 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input", help="input file of PV curve, first line ignore",action='store')
parser.add_argument("-p","--prange", help="pressure range", nargs='*',action='store')
parser.add_argument("-n","--noplot", help="no plotting", action='store_true')
parser.add_argument("-o","--output", help="output fitting data", action='store_true')
parser.add_argument("-f","--fix", help="fix B'", action='store')
parser.add_argument("-t","--title", help="add title", action='store')

args = parser.parse_args()

# Birch-Murnaghan equation of state
def ev_BM(params, vol): ## E is F at high T
    'From Phys. Rev. B 70, 224107'
    E0, B0, Bp, V0 = params 
    eta = (V0/vol)**(1.0/3.0)
    E = E0 + 9.0*B0*V0/16.0 * (eta**2-1.0)**2 * (6.0 + Bp*(eta**2-1.0) - 4.0*eta**2)
    return E

def EV_BM_fix(params, vol, Bf):
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

def pv_BM_fix(params, vol, Bf):
    'From Phys. Rev. B 70, 224107'
    E0, B0, Bp, V0 = params 
    eta = (V0/vol)**(1.0/3.0)
    p=3*B0/2*(eta**7-eta**5)*(1+3/4*(Bf-4)*(eta**2-1))*160.21765 # GPa
    return p


fin=open(args.input,"r")
vol=[]; ene=[]; press=[]
fin.readline()
for line in fin:
    ll=line.split()
    vol.append(float(ll[1]))
    ene.append(float(ll[2]))
    press.append(float(ll[3]))

# transform to numpy arrays
vol = np.array(vol)
ene = np.array(ene)
press = np.array(press)

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
    target = lambda params, y, x: y - pv_BM_fix(params, x, Bf)
else:
    target = lambda params, y, x: y - pv_BM(params, x)
birch_murn, ier = leastsq(target, x0, args=(press,vol))
#print("BM 3rd fitted by P-V")
print("B0,Bp,V0=",birch_murn[1]*160.21765, birch_murn[2], birch_murn[3])
E_fitted=ev_BM(birch_murn,vol)
P_fitted=pv_BM(birch_murn,vol)
if(args.output):
   fout=open("fitted.dat","w+")
   print("vol P_org P_fit",file=fout)
   for k in range(len(vol)):
      print(vol[k],press[k],P_fitted[k],file=fout)
   fout.close()

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

#F=eos_birch_murnaghan(birch_murn,vfit)

fout=open(args.input.strip(".dat")+".PV_fit.dat","w+")
print("#P(GPa) V(same_to_input)",file=fout)
for k in range(pfit.size):
    print(pfit[k],vfit[k],file=fout)
fout.close()

# plot
if (args.noplot):
    exit()

import pylab as plt
plt.figure(figsize=(8,6))
plt.rcParams.update({'font.size': 16})
vraw = np.linspace(min(vol),max(vol),100)
# PV
plt.subplot(2,1,1)
plt.plot(vol, press, 'ro', label="raw")
plt.plot(vraw, pv_BM(birch_murn,vraw), label='Birch-Murnaghan 3rd')
#plt.xlabel('Volume ($\AA^3$/atom)')
plt.ylabel('P (GPa)')
plt.legend()

if(args.title is not None):
   plt.title(args.title)

plt.subplot(2,1,2)
plt.plot(vol, pv_BM(birch_murn,vol)-press, '-o')
plt.axhline(0,ls='--',c='k')
plt.xlabel('Volume ($\AA^3$/atom)')
plt.ylabel('$\Delta$P (GPa)')


plt.tight_layout()
plt.savefig("PV-fit.png")
#plt.show()
