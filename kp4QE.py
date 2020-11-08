#!/usr/bin/env python3

import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input", help="QE input",action='store')
parser.add_argument("-k","--kpoint", help="k density",action='store')
args = parser.parse_args()

def recp_length(latt):
    a=np.array(latt)
    c23=np.cross(a[1],a[2])
    c31=np.cross(a[2],a[0])
    c12=np.cross(a[0],a[1])
    b1=2*np.pi*c23/np.dot(a[0],c23)
    b2=2*np.pi*c31/np.dot(a[1],c31)
    b3=2*np.pi*c12/np.dot(a[2],c12)
    lb1=np.sqrt(np.sum(b1*b1))/(2*np.pi)  # vasp Auto modes does not apply 2PI
    lb2=np.sqrt(np.sum(b2*b2))/(2*np.pi)
    lb3=np.sqrt(np.sum(b3*b3))/(2*np.pi)
    return [lb1,lb2,lb3]

Rk=float(args.kpoint)
fin=open(args.input,"r")

for line in fin:
    if("CELL_PARAMETERS" in line):
        break
latt=[]
for k in range(3):
    ll=fin.readline().split()
    latt.append([float(ll[0]), float(ll[1]), float(ll[2])])
fin.close()

blatt = recp_length(latt)
N1=int(max(1,Rk*blatt[0]+0.5))
N2=int(max(1,Rk*blatt[1]+0.5))
N3=int(max(1,Rk*blatt[2]+0.5))
kpoints=[N1,N2,N3]
print(*kpoints)
