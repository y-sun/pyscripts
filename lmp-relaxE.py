#!/usr/bin/env python3

import sys
import glob
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--infile", help="input log.lammps file",action='store')
parser.add_argument("-c","--cell", help="per cell", action='store_true')
parser.add_argument("-s","--simple", help="only E & V", action='store_true')
args = parser.parse_args()

J2eV= 1.602176634e-19
prefix=sys.argv[1].strip("*")
fin=open(args.infile,"r")
F=[];E=[]; press=[]; stress=[]; V=[]; Mag='NA'
natom=0; vtag=0
recording=[]
for line in fin:
    if("Loop time" in line):
        recording.append(prev)
        natom=int(line.split()[-2])
    else:
        prev=line

for iln in recording:
    ll=iln.split()
    E.append(float(ll[2]))
    press.append(float(ll[3])*1e-3) # kBar 
    V.append(float(ll[1]))
    stress.append([float(ll[4])*1e-3, float(ll[5])*1e-3, float(ll[6])*1e-3])

aE=np.array(E)
ap=np.array(press)
aV=np.array(V)
Ep=aE /natom
Vp=aV /natom

if(args.cell):
    if(args.simple):
        print("#V(A3/cell) E(eV/cell)")
    else:
        print("#V(A3/cell) E(eV/cell) P(kbar) Stress(kbar)")
    for kk in range(aE.size):
        if(args.simple):
            print("%10.6f %10.6f"%(aV[kk], aE[kk]))
        else:
            print("%10.6f %10.6f %10.4f %10.4f %10.4f %10.4f"%(aV[kk], aE[kk],ap[kk],stress[kk][0],stress[kk][1],stress[kk][2]))
else:
    if(args.simple):
        print("V(A3/atom) E(eV/atom)")
    else:
        print("V(A3/atom) E(eV/atom) P(kbar) Stress(kbar)")
    for kk in range(Ep.size):
        if(args.simple):
            print("%10.6f %10.6f"%(Vp[kk], Ep[kk]))
        else:
            print("%10.6f %10.6f %10.4f %10.4f %10.4f %10.4f"%(Vp[kk], Ep[kk],ap[kk],stress[kk][0],stress[kk][1],stress[kk][2]))
