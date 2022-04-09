#!/usr/bin/env python3

import  numpy as np
import argparse
# band.dat 's distance is under the cartesian coordinate

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="band.dat file", action='store')
parser.add_argument("-n","--nk", help="number of kpoints, sum of k-path + 1",action='store')
parser.add_argument("-e","--fermi", help="fermi level",action='store')
parser.add_argument("-p","--prefactor", help="a prefactor for unit conversion",action='store')
args = parser.parse_args()

fin=open(args.file,"r")
nk=int(args.nk)
Ef=float(args.fermi)
factor=float(args.prefactor)

tot_line=len(fin.readlines())
fin.seek(0)

nband=int(  (tot_line)/(nk+1) + 0.5 )
print("# of band:", nband)

x=[]
y=[]
for n in range(nband):
   kx=[]; ky=[]
   for k in range(nk):
      ll=fin.readline().split()
      kx.append(float(ll[0]))
      ky.append((float(ll[1])-Ef)*factor)   # eV
   fin.readline()
   x.append(kx); y.append(ky)
fin.close()

fout=open(args.file+".gp","w+")
for k in range(nk):
   print("%18.6f"%(x[0][k]),end=" ",file=fout)
   for i in range(nband):
      print("%18.6f"%(y[i][k]),end=" ",file=fout)
   print("",file=fout)
fout.close()
print("Transformed to "+args.file+".gp!")
