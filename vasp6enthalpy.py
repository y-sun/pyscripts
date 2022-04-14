#!/usr/bin/env python3

import sys
import glob
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--infile", help="input outcar files",action='store')
parser.add_argument("-e","--ele", help="including electronic entropy, TOTEN", action='store_true')
parser.add_argument("-t","--target", help="target pressure (kbar)", action='store')
args = parser.parse_args()

J2eV= 1.602176634e-19
fin=open(args.infile,"r")
E=[]; press=[]; V=[]; F=[]
natom=0; vtag=0
for line in fin:
    if("in kB" in line):
        ll=line.split()
        try:
            press.append((float(ll[2])+float(ll[3])+float(ll[4]))/3)
        except:
            press.append(-99999)
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
        E.append(float(ll[-1]))
    if("FREE ENERGIE" in line):
        fin.readline()
        ll=fin.readline().split()
        F.append(float(ll[-2]))
   # if("NELM" in line):
   #     ll=line.split()
   #     nelm=int(ll[2].strip(";"))
    #if("enthalpy is  TOTEN" in line):
    #    ll=line.split()
    #    Ep.append(float(ll[4])/natom)

aE=np.array(E)
aF=np.array(F)
ap=np.array(press)
aV=np.array(V)
#print(aE.size, ap.size, aV.size)
H_E=(aE + ap*aV*0.1*1E9*1E-30/J2eV)/natom
H_F=(aF + ap*aV*0.1*1E9*1E-30/J2eV)/natom


if(args.target is None):
   print("#ite V H P",end=' ')
   if(args.ele):
      print("using FREE ENERGY!")
      for kk in range(len(aE)):
         print("%4d %10.6f %10.6f %8.2f"%(kk+1,aV[kk]/natom, H_F[kk], press[kk]))
   else:
      print("")
      for kk in range(len(aE)):
         print("%4d %10.6f %10.6f %8.2f"%(kk+1,aV[kk]/natom, H_E[kk], press[kk]))
else:
   Ptar=float(args.target)
   print("V H P H_tar",end=" ")
   if(args.ele):
      print("using FREE ENERGY!")
      Htar = H_F[-1] + (Ptar-press[-1])*V[-1]*0.1*1E9*1E-30/J2eV/natom
      print(V[-1]/natom,H_F[-1],press[-1], Htar)
   else:
      print('')
      Htar = H_E[-1] + (Ptar-press[-1])*V[-1]*0.1*1E9*1E-30/J2eV/natom
      print(V[-1]/natom,H_E[-1],press[-1], Htar)
