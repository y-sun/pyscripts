#!/usr/bin/env python3

import yaml
import sys
import numpy as np

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

latt=data.get('lattice')
latt=np.array(latt)
alat=np.sqrt(np.dot(latt[0],latt[0]))
latt=latt/alat
print("lattice:")
print(latt)

c12=np.cross(latt[1],latt[2])
c20=np.cross(latt[2],latt[0])
c01=np.cross(latt[0],latt[1])

b0=c12 / np.dot(latt[0],c12)
b1=c20 / np.dot(latt[1],c20)
b2=c01 / np.dot(latt[2],c01)

recp=np.array([b0,b1,b2])
print("reciprocal lattice:")
print(recp)

# phonons
nbnd=natom*3
ph=data.get('phonon')
num_ph=len(ph)

fout=open("phy.matdyn","w+")
print("&plot nbnd=   "+str(nbnd)+", nks=  "+str(num_ph)+" /",file=fout)
fw=open("weight","w+")
print("weight",file=fw)
for i in range(num_ph):
    #Qp=np.array(ph[i]['q-position'])
    qp_dirt=np.array(ph[i]['q-position'])
    qp_cart=np.dot(qp_dirt,recp)
    Qp=qp_cart
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

