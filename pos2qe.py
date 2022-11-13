#!/usr/bin/env python3

import sys

fin=open(sys.argv[1],"r")
fin.readline()
scaler=float(fin.readline().split()[0])

fout=open("QE.pos","w+")

print("CELL_PARAMETERS {angstrom}",file=fout)
for k in range(3):
    ll=fin.readline().split()
    box=[float(lk) for lk in ll]
    for i in range(3):
        print(scaler*box[i],end=" ",file=fout)
    print("",file=fout)

chem=fin.readline().split()
ll=fin.readline().split()
npop=[int(lk) for lk in ll]
cart=fin.readline().split()[0]
if(cart != "Direct"):
    print("change to Direct positions")
    exit()

print("ATOMIC_POSITIONS {crystal}", file=fout)
for i in range(len(chem)):
    for k in range(npop[i]):
        ll=fin.readline().split()
        print(chem[i], ll[0],ll[1],ll[2], file=fout)
fin.close()
fout.close()
        

