#!/usr/bin/env python3

import sys
import glob
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--infile", help="input outcar file",action='store')
parser.add_argument("-p","--percell", help="percell", action='store_true')
parser.add_argument("-e","--ele", help="including electronic entropy, TOTEN", action='store_true')
args = parser.parse_args()

J2eV= 1.602176634e-19
prefix=sys.argv[1].strip("*")
fin=open(args.infile,"r")
F=[];E=[]; press=[]; V=[]; Mag='NA'
natom=0; vtag=0
for line in fin:
    #if("external pressure " in line):
    #   ll=line.split()
    #   press.append(float(ll[3]))
    if("in kB" in line):
        ll=line.split()
        try:
            press.append((float(ll[2])+float(ll[3])+float(ll[4]))/3)
        except:
            press.append(-99999)
    if(("volume of cell" in line) and vtag==0):
        vtag = 1
    elif(("volume of cell" in line) and vtag==1):
        vol_vasp=float(line.split()[4])
        fin.readline()
        vec=[]
        for k in range(3):
            ll=fin.readline().split()
            fl=[float(ll[s]) for s in range(3) ]
            vec.append(fl)
        vec=np.array(vec)
        vol=np.dot(np.cross(vec[0],vec[1]),vec[2])
        if(abs(vol-vol_vasp)>0.1): print("wrong volume!")
        V.append(vol)
    if("NIONS" in line):
        ll=line.split()
        natom=int(ll[len(ll)-1])
    if("energy  without entropy=" in line):
        ll=line.split()
        E.append(float(ll[-1])) #"sigma->0"
        #E.append(float(ll[3])) #"without entropy"
    if("free  energy   TOTEN" in line):
        ll=line.split()
        F.append(float(ll[-2]))
    if("NELM" in line):
        ll=line.split()
        nelm=int(ll[2].strip(";"))
    if("magnetization (x)" in line):
        for line in fin:
            ll=line.split()
            if(len(ll)>0):
                if(ll[0]=="tot"):
                    Mag=float(ll[-1])
                    break
    #if("enthalpy is  TOTEN" in line):
    #    ll=line.split()
    #    Ep.append(float(ll[4])/natom)

aE=np.array(E)
aF=np.array(F)
ap=np.array(press)
aV=np.array(V)
Ep=aE /natom
Fp=aF /natom

if(args.percell):
    print("#V(A3/cell) E(eV/cell) P(kbar)")
    if(args.ele):
        for kk in range(aF.size):
            print("%10.6f %10.6f %10.4f"%(aV[kk], aF[kk],ap[kk]))
    else:
        for kk in range(aE.size):
            print("%10.6f %10.6f %10.4f"%(aV[kk], aE[kk],ap[kk]))
else:
    print("V(A3/atom) E(eV/atom) P(kbar)")
    if(args.ele):
        for kk in range(Fp.size):
            print("%10.6f %10.6f %10.4f"%(aV[kk]/natom, Fp[kk], ap[kk]))
    else:
        for kk in range(Ep.size):
            print("%10.6f %10.6f %10.4f"%(aV[kk]/natom, Ep[kk], ap[kk]))

        #print("%10.6f %10.6f %10.4f %4d"%(aV[kk]/natom, Ep[kk], press[kk],kk+1))
