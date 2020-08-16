#!/usr/bin/env python3

import yaml
import sys

THz2cm=33.35641 # 1THz -> cm^-1

#with open("../mesh.yaml","r") as fin:
with open(sys.argv[1],"r") as fin:
    data=yaml.safe_load(fin)

# system
natom=data.get('natom')
atoms=data.get('points')
print(natom,'atoms:')
mass=[]
for i in range(natom):
    print(atoms[i]['symbol'],atoms[i]['mass'])
    mass.append(atoms[i]['mass'])

# phonons
nbnd=natom*3
ph=data.get('phonon')
num_ph=len(ph)

fout=open("phy.matdyn","w+")
print("&plot nbnd=   "+str(nbnd)+", nks=  "+str(num_ph)+" /",file=fout)
fw=open("weight","w+")
print("weight",file=fw)
for i in range(num_ph):
    Qp=ph[i]['q-position']
    weight=ph[i]['weight']
    freq=[]
    for k in range(nbnd):
        freq.append(ph[i]['band'][k]['frequency'])
    print("          %12.6f %12.6f %12.6f"%(Qp[0],Qp[1],Qp[2]),file=fout)
    for ifq in freq:
        print("%12.6f"%(ifq*THz2cm),end=" ",file=fout)
    print("",file=fout)
    print("%.6f %.6f %.6f    %6d"%(Qp[0],Qp[1],Qp[2],weight),file=fw)
fout.close()
fw.close()

