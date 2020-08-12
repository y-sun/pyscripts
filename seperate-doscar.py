#!/usr/bin/env python3

import numpy as np
import sys
import argparse
import pylab as plt

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input", help="input DOSCAR file",action='store')
parser.add_argument("-s","--spin", help="spin polarized", action='store_true')
args = parser.parse_args()

if(args.spin):
    print("Spin Polarized!")
else:
    print("Spin Unpolarized!")

fin=open(args.input,"r")
ll=fin.readline().split()
natom=int(ll[0])
for k in range(4):
    fin.readline()
ll=fin.readline().split()
ndata=int(ll[2]); Ef=float(ll[3])

fout=open("total_dos.dat","w+")
if(args.spin):
    print("E-Ef total_up total_dn",file=fout)
    for k in range(ndata):
        ll=fin.readline().split()
        print(float(ll[0])-Ef, ll[1],'-'+ll[2],file=fout)
    fout.close()
else:
    print("E-Ef DOS",file=fout)
    for k in range(ndata):
        ll=fin.readline().split()
        print(float(ll[0])-Ef, ll[1],file=fout)
    fout.close()

for k in range(natom):
    fout=open("pdos_atom_"+str(k)+".dat","w+")
    if(args.spin):
        print("E-Ef s_up s_dn py_up py_dn pz_up pz_dn px_up px_dn dxy_up dxy_dn dyz_up dyz_dn dz2_up dz2_dn dxz_up dxz_dn dx2-y2_up dx2-y2_dn",file=fout)
        fin.readline()
        for k in range(ndata):
            ll=fin.readline().split()
            print(float(ll[0])-Ef, end=" ",file=fout)
            for j in range(1,len(ll)):
                if(j%2==0):
                    print("-"+ll[j],end=" ",file=fout)
                else:
                    print(ll[j],end=" ",file=fout)
            print("",file=fout)
        fout.close()
    else:
        print("E-Ef s py pz px dxy dyz dz2 dxz dx2-y2",file=fout)
        fin.readline()
        for k in range(ndata):
            ll=fin.readline().split()
            print(float(ll[0])-Ef, end=" ",file=fout)
            for j in range(1,len(ll)):
                print(ll[j],end=" ",file=fout)
            print("",file=fout)
        fout.close()
        
