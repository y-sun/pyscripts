#!/usr/bin/env python3

import sys
import glob
import numpy as np

files=sorted(glob.glob(sys.argv[1]))
J2eV= 1.602176634e-19
prefix=sys.argv[1].strip("*")
for ifile in files:
    fin=open(ifile,"r")
    E=[]; press=[]; V=[]
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
            #E.append(float(ll[3]))
       # if("NELM" in line):
       #     ll=line.split()
       #     nelm=int(ll[2].strip(";"))
        #if("enthalpy is  TOTEN" in line):
        #    ll=line.split()
        #    Ep.append(float(ll[4])/natom)
    
    aE=np.array(E)
    ap=np.array(press)
    aV=np.array(V)
    print(aE.size, ap.size, aV.size)
    Ep=(aE + ap*aV*0.1*1E9*1E-30/J2eV)/natom
    if(len(Ep)>=1 and len(sys.argv)==2):
       print("#",ifile,ifile.strip(prefix))
       for kk in range(len(Ep)):
          print("%4d %10.6f %10.6f %8.2f"%(kk+1,aV[kk]/natom, Ep[kk], press[kk]))
    elif(len(sys.argv)>2):
       Ptar=float(sys.argv[2])
       Htar = Ep[-1] + (Ptar-press[-1])*V[-1]*0.1*1E9*1E-30/J2eV/natom
       print("#",ifile,ifile.strip(prefix),Ep[-1],press[-1], Htar)
    else:
       print("#",ifile,ifile.strip(prefix),*Ep,*press)
