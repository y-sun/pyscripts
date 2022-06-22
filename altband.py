#!/usr/bin/env python3

import numpy as np 
import pylab as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--infile", help="input (OUTCAR)",action='store')
parser.add_argument("-p","--plot", help="plot difference", action='store_true')
args = parser.parse_args()

fin=open(args.infile,'r')
Ef=0; nbnd=0; nkpts=0
for line in fin:
   if("ISPIN" in line):
      ispin=line.split()[2]
      if(ispin != '2'):
         print('Error: ispin not 2!')
         exit()
   if("NBANDS" in line):
      nbnd=int(line.split()[-1])
   if("NKPTS" in line):
      nkpts=int(line.split()[3])
   if("E-fermi" in line):
      Ef=float(line.split()[2])
   if("spin component" in line):
      fin.readline()
      break

up_bands=[]
for ik in range(nkpts):
   kb=[]
   fin.readline()
   fin.readline()
   for ib in range(nbnd):
      ll=fin.readline().split()
      kb.append(float(ll[1]))
   fin.readline()
   up_bands.append(kb)
for k in range(2):
   fin.readline()
dn_bands=[]
for ik in range(nkpts):
   kb=[]
   fin.readline()
   fin.readline()
   for ib in range(nbnd):
      ll=fin.readline().split()
      kb.append(float(ll[1]))
   fin.readline()
   dn_bands.append(kb)
fin.close()

up=np.array(up_bands)
dn=np.array(dn_bands)

diff=up-dn

fout=open('altmag.dat','w+')
print('kpts',end=' ',file=fout)
for j in range(nbnd):
   print(f'band{j+1}', end=' ', file=fout)
print('',file=fout)
for i in range(nkpts):
   print(i,end=' ',file=fout)
   for j in range(nbnd):
      print(diff[i,j], end=' ',file=fout)
   print('',file=fout)
fout.close()


print('total abs. diff:  %.2f'%(np.sum(np.abs(diff))))

if(args.plot):
   import numpy as np
   plt.figure(figsize=(8,6))
   plt.rcParams.update({'font.size': 16})
   xk=[k for k in range(nkpts)]
   for i in range(nbnd):
      plt.plot(xk, diff[:,i])
   plt.xlabel('kpoints')
   plt.ylabel('up-dn splitting (eV)')
   ym=max(0.1,np.max(np.abs(diff)))
   plt.ylim(-ym,ym)
   plt.tight_layout()
   plt.savefig('altband.png')
   #plt.show()
