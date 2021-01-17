#!/usr/bin/env python3

import  numpy as np
import argparse
# band.dat 's distance is under the cartesian coordinate

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="band.dat file", action='store')
parser.add_argument("-s","--spacing", help="spacing, same to band.conf",action='store')
args = parser.parse_args()



fin=open(args.file,"r")
nk=int(args.spacing)


tot_line=len(fin.readlines())
fin.seek(0)

for k in range(2):
   fin.readline()
ll=fin.readline().split()
kp=[float(ll[k]) for k in range(1,len(ll))]
ct=0
nsep=len(kp)-1
nband=int( (tot_line-3-1)/((nk+1)*nsep+1) + 0.5 )

print("# of band:",nband)

x=[]
y=[]
for nband in range(nband):
   kx=[]; ky=[]
   for k in range(nsep):
      for i in range(nk):
         ll=fin.readline().split()
         kx.append(float(ll[0]))
         ky.append(float(ll[1])/0.02998)   # THz to cm^-1
      fin.readline()
   fin.readline()
   x.append(kx); y.append(ky)
fin.close()

#import pylab as plt
#for k in range(6):
#   plt.plot(x[k],y[k],label=str(k))
#for kk in kp:
#   plt.axvline(kk,ls='--',color='k')
#plt.show()

fout=open("band.dat.gp","w+")
for k in range(nk*nsep):
   print(x[0][k],end=" ",file=fout)
   for i in range(nband):
      print(y[i][k],end=" ",file=fout)
   print("",file=fout)
fout.close()
print("Transformed to band.dat.gp!")
