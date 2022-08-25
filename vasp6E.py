#!/usr/bin/env python3

import sys
import glob
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--infile", help="input outcar file",action='store')
parser.add_argument("-c","--cell", help="per cell", action='store_true')
parser.add_argument("-m","--magmom", help="find magnetization (sum of spdf, no interstitial!!!)", action='store_true')
parser.add_argument("-n","--noext", help="no extropolation to sigma->0", action='store_true')
parser.add_argument("-s","--simple", help="only E & V", action='store_true')
parser.add_argument("-e","--ele", help="including electronic entropy, TOTEN", action='store_true')
args = parser.parse_args()

J2eV= 1.602176634e-19
prefix=sys.argv[1].strip("*")
fin=open(args.infile,"r")
F=[];E=[]; press=[]; stress=[]; V=[]; Mag='NA'
natom=0; vtag=0
for line in fin:
    #if("external pressure " in line):
    #   ll=line.split()
    #   press.append(float(ll[3]))
    if("in kB" in line):
       ll=line.split()
       stress.append(ll[2]+" "+ll[3]+" "+ll[4]+" "+ll[5]+" "+ll[6]+" "+ll[7])
       px=float(ll[2]); py=float(ll[3]); pz=float(ll[4])
       pp = (px+py+pz)/3
       try:
           press.append(pp)
       except:
           press.append(-99999)

#    if("in kB" in line):
#        ll=line.split()
#        stress.append(ll[2]+" "+ll[3]+" "+ll[4]+" "+ll[5]+" "+ll[6]+" "+ll[7])
#        try:
#            press.append((float(ll[2])+float(ll[3])+float(ll[4]))/3)
#        except:
#            press.append(-99999)
    if(("volume of cell" in line) and vtag!=2):
        vtag += 1
    elif(("volume of cell" in line) and vtag==2):
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
        if(args.noext):
            E.append(float(ll[3])) #"without entropy"
        else:
            E.append(float(ll[-1])) #"sigma->0"
    if("free  energy   TOTEN" in line):
        ll=line.split()
        F.append(float(ll[-2]))
    if("NELM" in line and ("=" in line)):
        ll=line.split()
        nelm=int(ll[2].strip(";"))
    if("magnetization (x)" in line):
        tag=0; Mab=0 ; mab=0
        for line in fin:
            ll=line.split()
            if(len(ll)>0):
                if(ll[0]=="tot"):
                    Mag=ll[-1] #float(ll[-1])
                    break
                elif(tag==0 and "----" in line):
                    tag=1
                elif(tag==1  and "----" in line):
                    tag=0
                    Mab=mab
                elif(tag==1):
                    mab += abs(float(ll[-1]))
    #if("enthalpy is  TOTEN" in line):
    #    ll=line.split()
    #    Ep.append(float(ll[4])/natom)

aE=np.array(E)
aF=np.array(F)
ap=np.array(press)
aV=np.array(V)
Ep=aE /natom
Fp=aF /natom
tag_size=(aF.size-aE.size)+(ap.size-aE.size)+(aV.size-aE.size)
if(tag_size!=0):
    print("size error!!")
if(args.cell):
    if(args.simple):
        print("#V(A3/cell) E(eV/cell)")
    else:
        print("#V(A3/cell) E(eV/cell) P(kbar) Stress(kbar)")
    if(args.ele):
        for kk in range(aF.size):
            if(args.simple):
                print("%10.6f %10.6f"%(aV[kk], aF[kk]))
            else:
                print("%10.6f %10.6f %10.4f "%(aV[kk], aF[kk],ap[kk])+stress[kk])
    else:
        for kk in range(aE.size):
            if(args.simple):
                print("%10.6f %10.6f"%(aV[kk], aE[kk]))
            else:
                print("%10.6f %10.6f %10.4f "%(aV[kk], aE[kk],ap[kk])+stress[kk])
else:
    if(args.simple):
        print("V(A3/atom) E(eV/atom)")
    else:
        print("V(A3/atom) E(eV/atom) P(kbar) Stress(kbar)")
    if(args.ele):
        for kk in range(Fp.size):
            if(args.simple):
                print("%10.6f %10.6f"%(aV[kk]/natom, Fp[kk]))
            else:
                print("%10.6f %10.6f %10.4f "%(aV[kk]/natom, Fp[kk], ap[kk])+stress[kk])
    else:
        for kk in range(Ep.size):
            if(args.simple):
                print("%10.6f %10.6f"%(aV[kk]/natom, Ep[kk]))
            else:
                print("%10.6f %10.6f %10.4f "%(aV[kk]/natom, Ep[kk], ap[kk])+stress[kk])
if(args.magmom):
    print("magnetization, mag.abs: %s uB/cell, %10.4f uB/cell (from sum of spdf, no interstitial!!!)"%(Mag, Mab))
        #print("%10.6f %10.6f %10.4f %4d"%(aV[kk]/natom, Ep[kk], press[kk],kk+1))
