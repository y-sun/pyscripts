#!/usr/bin/env python3

import numpy as np
import math
from scipy.optimize import leastsq
from scipy.optimize import fsolve 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input", help="input file of helmholtz-volume from Phonopy",action='store')
parser.add_argument("-t","--temperatures", help="temperatures to be output", nargs='*',action='store')
parser.add_argument("-p","--press", help="pressure range", nargs='*',action='store')
args = parser.parse_args()

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

def get_BM(eos,name,temp):
    birch_murn = eos
    # compute PH
    Pmin=float(args.press[0]); Pmax=float(args.press[1])
    Pn=int(Pmax-Pmin+0.5)+1
    pfit = np.linspace(Pmin,Pmax,Pn)
    vfit = []
    for Pi in pfit:
        func = lambda V : pv_BM(birch_murn,V)-Pi
        vok  = fsolve(func,x0=2.0)
        vfit.append(vok[0])
    vfit=np.array(vfit)
    out_P=pv_BM(birch_murn,vfit)
    out_G=eos_birch_murnaghan(birch_murn,vfit)+pv_BM(birch_murn,vfit)*vfit/160.21765
    fout=open(name,"w+")
    print("#P(GPa) G(eV/cell)  #T=",temp,"K",file=fout)
    for k in range(len(out_P)):
        print("%.6f  %.10f"%(out_P[k],out_G[k]),file=fout)
    fout.close()

temp=args.temperatures
# Phonopy-QHA
fin=open(args.input,"r")
for line in fin:
    if("Temperature" in line):
        ll=line.split()
        tt=ll[2].split(".")[0]
        if(tt in temp):
            lB=fin.readline().split() # E0 B0 Bp V0 of helmholtz
            eos=[float(lB[k]) for k in range(2,6)]
            get_BM(eos,"PG_"+tt+"K.dat",tt)