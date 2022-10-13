#!/usr/bin/env python3

import numpy as np
import sys
import pylab as plt
import argparse
from matplotlib import gridspec

parser = argparse.ArgumentParser()
parser.add_argument("-b","--band", help="REFORMATTED_BAND file", nargs='*', action='store')
parser.add_argument("-p","--pdos", help="PDOS files", nargs='*',action='store')
parser.add_argument("-k","--klab", help="KLABELS file", action='store')
parser.add_argument("-t","--title", help="plot title",action='store')
parser.add_argument("-e","--energy", help="fermi energy (0 for vaspkit)",action='store')
parser.add_argument("-x","--xlim", help="range for dos", nargs='*',action='store')
parser.add_argument("-y","--ylim", help="range for band", nargs='*',action='store')
parser.add_argument("-c","--scaling", help="multiply the PDOS by a factor", action='store')
parser.add_argument("-s","--show", help="show plot", action='store_true')

args = parser.parse_args()

plt.figure(figsize=(12,6))
plt.rcParams.update({'font.size': 14})
gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])

if (args.energy is not None):
    Ef=float(args.energy)
else:
    Ef=0

# band dispersion
ax0=plt.subplot(gs[0])

colors=['b','r']
shape=['-','--']
for j in range(len(args.band)):
    data=np.loadtxt(args.band[j],skiprows=1)
    nband=data.shape[1]-1
    for k in range(nband):
        ax0.plot(data[:,0],data[:,k+1]-Ef,c=colors[j],ls=shape[j])

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

ax0.set_xticks(k_pos)
ax0.set_xticklabels(k_name,fontsize=12)

for kp in k_pos:
    ax0.axvline(kp,ls='--',c='k')
ax0.axhline(0,ls='--',c='k')
ax0.set_xlim(min(data[:,0]),max(data[:,0]))
if(args.ylim is not None):
    ax0.set_ylim(float(args.ylim[0]), float(args.ylim[1]))
ax0.set_ylabel('$E-E_f$ (eV)')

# dos
ax1=plt.subplot(gs[1])
nfile=len(args.pdos)
if(args.scaling is not None):
    scaling=float(args.scaling)
else:
    scaling=1.0
for i in range(nfile):
    data=np.loadtxt(args.pdos[i],skiprows=1)
    ax1.plot(data[:,-1]*scaling,(data[:,0]-Ef),label=args.pdos[i].split('.')[0])
ax1.axhline(0.0,ls='--',c='k')
ax1.yaxis.tick_right()
if(args.xlim is not None):
	ax1.set_xlim(float(args.xlim[0]), float(args.xlim[1]))
if(args.ylim is not None):
	ax1.set_ylim(float(args.ylim[0]), float(args.ylim[1]))
ax1.set_xlabel('DOS (States/eV/spin/f.u.)')
ax1.legend(loc='upper right',fontsize=12)

plt.title(args.title)
plt.tight_layout()
plt.savefig('bandNdos.png')
if (args.show):
    plt.show()
