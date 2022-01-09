#!/usr/bin/env python3

import sys
import glob
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p","--path", help="vasp working path",action='store')
parser.add_argument("-m","--magmom", help="find magnetization", action='store_true')
parser.add_argument("-n","--noext", help="no extropolation to sigma->0", action='store_true')
parser.add_argument("-e","--ele", help="including electronic entropy, TOTEN", action='store_true')
args = parser.parse_args()

J2eV= 1.602176634e-19
#prefix=sys.argv[1].strip("*")
fin=open(args.path+"/OUTCAR","r")
F=[];E=[]; press=[]; stress=[]; V=[]; Mag='NA'
natom=0; vtag=0
for line in fin:
    #if("external pressure " in line):
    #   ll=line.split()
    #   press.append(float(ll[3]))
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

fin.close()

# atom info
fin=open(args.path+"/CONTCAR","r")
for k in range(5):
    fin.readline()
ele=fin.readline().split()

natom=fin.readline().split()
fin.close()


if(args.ele):
    print("%10.6ff"%(Fp[-1]), end=" ")

else:
    print("%10.6f"%(Ep[-1]), end=" ")

for k in range(len(ele)):
    print(ele[k]+"_"+natom[k],end=" ")
print("")

if(args.magmom):
    print("magnetization, mag.abs: %s uB/cell, %10.4f uB/cell"%(Mag, Mab))

