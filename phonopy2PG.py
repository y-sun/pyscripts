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
parser.add_argument("-n","--natom", help="atom #, changes results to per-atom value", action='store')
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

def get_BM(eos,name,temp,vmin):
    birch_murn = eos
    # compute PH
    Pmin=float(args.press[0]); Pmax=float(args.press[1])
    dP=1.0
    Pn=int((Pmax-Pmin)/dP+0.5)+1
    pfit = np.linspace(Pmin,Pmax,Pn)
    vfit = []
    for Pi in pfit:
        func = lambda V : pv_BM(birch_murn,V)-Pi
        vok  = fsolve(func,x0=vmin)
        vfit.append(vok[0])
    vfit=np.array(vfit)
    out_P=pv_BM(birch_murn,vfit)
    out_G=eos_birch_murnaghan(birch_murn,vfit)+pv_BM(birch_murn,vfit)*vfit/160.21765
    fout=open(name,"w+")
    if(args.natom is not None):
        print("#P(GPa) G(eV/atom) V(A3/atom)  #T=",temp,"K",file=fout)
    else:
        print("#P(GPa) G(eV/cell) V(A3/cell)  #T=",temp,"K",file=fout)
    for k in range(len(out_P)):
        if(args.natom is not None):
            sc=float(args.natom)
        else:
            sc=1.0
        print("%.6f  %.10f  %.6f"%(out_P[k],out_G[k]/sc,vfit[k]/sc),file=fout)
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
            if(eos[2] < 2 or eos[2] > 8):
                print("Check your EOS fitting, current B' is",eos[2])
            vol=[]; helm=[]
            for line2 in fin :
                lll=line2.split()
                if(len(lll)!=2):
                    break
                vol.append(float(lll[0]))
                helm.append(float(lll[1]))
            vol=np.array(vol)
            ene=np.array(helm)
            get_BM(eos,"PG_"+tt+"K.dat",tt, vol.min())
