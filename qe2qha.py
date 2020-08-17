#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s","--scf", help="QE SCF results",action='store')
parser.add_argument("-m","--matdyn", help="matdyn file",action='store')
args = parser.parse_args()

fscf=open(args.scf,"r")
P=999; V='NA'; E='NA' # P in a.u., V in bohr^3, E in Ry
for line in fscf:
    if("unit-cell volume" in line):
        V=float(line.split()[-2])
    if("!    total energy" in line):
        E=float(line.split()[-2])
fscf.close()

fout=open("in.qha","w+")
print("P=", P, "V=", V, "E=", E,file=fout)
fq=open(args.matdyn,"r")
ll=fq.readline().split()
np=int(ll[2].strip(","))
nk=int(ll[-2])

for k in range(nk):
    print(fq.readline().strip("\n"),file=fout)
    ip=np
    for line in fq:
        ll=line.split()
        ip-=len(ll)
        for il in ll:
            print(il,file=fout)
            if(float(il)<-1.0):
                print("Warning - negative frequency :",il)
        if(ip==0):
            break
fout.close()
fq.close()
