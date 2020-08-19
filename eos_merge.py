#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input", help="PH eos", nargs='*',action='store')
args = parser.parse_args() 

all_sys=[]
for k in range(1,len(args.input)):
    all_sys.append(args.input[k])

ct=0
H=[]
for isys in all_sys:
    fin=open(isys+".PH_fit.dat","r")
    P=[]; ent=[]
    for line in fin:
        ll=line.split()
        P.append(float(ll[0]))
        ent.append(float(ll[1]))
    H.append(ent)
    fin.close()

dH=[]
for iH in H:
    d_ent=[]
    for k in range(len(iH)):
        d_ent.append( iH[k]-H[0][k] )
    dH.append(d_ent)

fout=open("P-H.dat","w+")
print("P", *all_sys, file=fout)
for k in range(len(dH[0])):
    print(P[k],end=" ",file=fout)
    for j in range(len(dH)):
        print(dH[j][k],end=" ",file=fout)
    print("",file=fout)
fout.close()
