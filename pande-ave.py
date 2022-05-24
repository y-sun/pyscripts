#!/usr/bin/env python3

import numpy as np
import sys

data=np.loadtxt('pande.dat',skiprows=1)

fin=open('merge.xdatcar','r')
fin.readline()
fac=float(fin.readline().split()[0])
box=[]
for k in range(3):
    ll=fin.readline().split()
    box.append(float(ll[k]))
fin.readline()
ll=fin.readline().split()
na=[float(k) for k in ll]
natom=np.sum(na)
V=box[0]*box[1]*box[2]/natom

E=np.mean(data[:,2])/natom
P=np.mean(data[:,1])
H=E+P*V*1E-21/1.602176634E-19

print('aved E:', E)
print('aved P:', P)
print('aved V:', V)
print('H:', H)
