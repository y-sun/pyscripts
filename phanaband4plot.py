#!/usr/bin/env python3

import  numpy as np
import argparse
# band.dat 's distance is under the cartesian coordinate

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="band.dat file", action='store')
args = parser.parse_args()

data=np.loadtxt(args.file, skiprows=2)
ndata=data.shape[0]

nband=data.shape[1]-4
print(ndata, nband)
fout=open("band.dat.gp","w+")
for k in range(ndata):
   print("%18.6f"%(data[k][3]/0.02998),end=" ",file=fout)  # THz to cm^-1
   for i in range(nband):
      print("%18.6f"%(data[k][4+i]),end=" ",file=fout)
   print("",file=fout)
fout.close()
print("Transformed to band.dat.gp!")
