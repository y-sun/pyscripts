#!/usr/bin/env python3

import numpy as np
import sys
import pylab as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-b","--band", help="REFORMATTED_BAND file", nargs='*', action='store')
parser.add_argument("-k","--klab", help="KLABELS file", action='store')
parser.add_argument("-t","--title", help="plot title",action='store')
parser.add_argument("-e","--energy", help="fermi energy (0 for vaspkit)",action='store')
parser.add_argument("-y","--ylim", help="yrange", nargs='*',action='store')
parser.add_argument("-s","--show", help="show plot", action='store_true')

args = parser.parse_args()

plt.figure(figsize=(8,6))
plt.rcParams.update({'font.size': 16})

if (args.energy is not None):
    Ef=float(args.energy)
else:
    Ef=0

colors=['b','r','k']

for j in range(len(args.band)):
    data=np.loadtxt(args.band[j],skiprows=1)
    nband=data.shape[1]-1
    for k in range(nband):
        plt.plot(data[:,0],data[:,k+1]-Ef,c=colors[j])

fin=open(args.klab,'r')
fin.readline()
k_name=[]
k_pos=[]
for line in fin:
    ll=line.split()
    if(len(ll)==0):
        break
    if(ll[0]=="GAMMA"):
        k_name.append("G")
    else:
        k_name.append(ll[0])
    k_pos.append(float(ll[1]))
fin.close()

plt.xticks(k_pos, k_name,fontsize=12)

for kp in k_pos:
    plt.axvline(kp,ls='--',c='k')
plt.axhline(0,ls='--',c='k')

plt.xlim(min(data[:,0]),max(data[:,0]))
if(args.ylim is not None):
    plt.ylim(float(args.ylim[0]), float(args.ylim[1]))

plt.ylabel('$E-E_f$ (eV)')
plt.title(args.title)
plt.tight_layout()
plt.savefig('band.png')
if (args.show):
    plt.show()
 
