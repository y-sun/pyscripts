#!/usr/bin/env python3

import  numpy as np
import argparse
import pylab as plt

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="*.projbands",action='store')
parser.add_argument("-k","--kp", help="k points", nargs='*', action='store')
parser.add_argument("-l","--spacing", help="k spacing, same to band.conf",action='store')
parser.add_argument("-t","--title", help="plot title",action='store')
parser.add_argument("-n","--nband", help="number of bands",action='store')
parser.add_argument("-i","--id", help="states id", nargs='*', action='store')
parser.add_argument("-s","--states", help="states name", nargs='*', action='store')
parser.add_argument("-y","--ylim", help="yrange", nargs='*', action='store')
args = parser.parse_args()

kpoints=args.kp
nk=len(kpoints)
nspacing=int(args.spacing)
nbnds=int(args.nband)

states=[int(k) for k in args.id]
names=args.states

plt.figure(figsize=(8,6), dpi=200)
plt.rcParams.update({'font.size': 14})

if (len(states)<7):
    colors=['r','b','g','c','m','y']
else:
    colors=plt.cm.rainbow(np.linspace(0,1,natom))

fin=open(args.file,'r')
ct=0
for line in fin:
   ct+=1
   if("K-length" in line):
      break
fin.close()

data=np.loadtxt(args.file,skiprows=ct)

i=0
for sid in states:
   plt.scatter(data[:,1],data[:,2],s=data[:,3+sid]*100,color=colors[i], linewidths=0 ,alpha=0.5,label=names[i])
   i+=1

# labels
plt.ylabel(r"Frequency (THz)")

vx=[]
for k in range(1,nk-1):
    vx.append(data[k*nspacing*nbnds-k,1])


for iv in vx:
    plt.axvline(iv,color='k',lw=0.5)
plt.axhline(0,color='k',lw=0.5)
plt.xlim(data[0,1],data[-1,1])
if(args.ylim is not None):
   plt.ylim(float(args.ylim[0]), float(args.ylim[1]))

a=[data[0,1]]; b=[data[-1,1]]
xlb=a+vx+b
ax = plt.subplot(111)
ax.set_xticks(xlb)
ax.set_xticklabels(kpoints)

if(args.title is not None):
    plt.title(args.title)


plt.legend()
plt.tight_layout()
plt.savefig('fatband.png')
plt.show()
