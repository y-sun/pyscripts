#!/usr/bin/env python3

import numpy as np

# scr
fin=open("scr/OUTCAR","r")
scr_f=[]; scr_eig=[]
for line in fin:
    if("2PiTHz" in line):
        ll=line.split()
        scr_f.append(float(ll[-2]))
        fin.readline()
        eig=[]
        for i in range(3):
            ll=fin.readline().split()
            for j in range(3):
                eig.append(np.abs(float(ll[j+3])))  
                # ignore the sign change due to symmetry
        scr_eig.append(eig)
fin.close()

# unscr
fin=open("unscr/OUTCAR","r")
unscr_f=[]; unscr_eig=[]
for line in fin:
    if("2PiTHz" in line):
        ll=line.split()
        unscr_f.append(float(ll[-2]))
        fin.readline()
        eig=[]
        for i in range(3):
            ll=fin.readline().split()
            for j in range(3):
                eig.append(np.abs(float(ll[j+3])))
        unscr_eig.append(eig)
fin.close()

# transform
scr_f=np.array(scr_f)
scr_eig=np.array(scr_eig)
unscr_f=np.array(unscr_f)
unscr_eig=np.array(unscr_eig)

#print(scr_eig)
#print(unscr_eig)

nmode=scr_eig.shape[0]-3 # disregard last 3

# match eigenvectors between scr and unscr
matcher=[-1 for k in range(nmode)]
dev=[-9999 for k in range(nmode)]
for i in range(nmode):
    diff=99999; sel=-1
    for j in range(nmode):
        dd = np.sum((scr_eig[i] - unscr_eig[j])**2)
        if(dd<diff):
            sel=j
            diff=dd
    matcher[i]=sel
    dev[i]=diff

print("matcher:",matcher)
#print(dev)

# check repeated matcher
from collections import Counter
repeated=[k for k,v in Counter(matcher).items() if v>1]
if(len(repeated)!=0):
    print("Error: repeated matcher! Check eigenvectors")


# get lambda
lmd=[]
for i in range(nmode):
    scr_i=scr_f[i]
    unscr_i=unscr_f[matcher[i]]
    lmd_i= ((scr_i**2-unscr_i**2)/scr_i**2)/(-2)
    lmd.append(lmd_i)

# print
fout=open("omega.dat","w+")
print("#omega_scr oemga_unscr lamda",file=fout)
for i in range(nmode):
    print(scr_f[i],unscr_f[matcher[i]],lmd[i],file=fout)
fout.close()
