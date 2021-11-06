#!/usr/bin/env python3

import numpy as np
import pylab as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-k","--kp", help="k points", nargs='*',action='store')
parser.add_argument("-n","--number", help="number of spacing",action='store')
args = parser.parse_args()

nspacing=int(args.number); kpoints=args.kp
plt.figure(figsize=(8,6))
plt.rcParams.update({'font.size': 14})

fs=open("scr/band.dat.gp","r")
nbnd=len(fs.readlines())
fs.seek(0)

fu=open("unscr/band.dat.gp","r")
fout=open("lambd.dat","w+")
data=[]
for k in range(nbnd):
    ls=fs.readline().split()
    lu=fu.readline().split()
    print(ls[0],end=" ",file=fout)
    kdata=[]
    kdata.append(float(ls[0]))
    for k in range(1,len(ls)):
        os=float(ls[k])
        ou=float(lu[k])
        lmd=-(os**2-ou**2)/2/os**2
        print("%12.6f"%(lmd), end=" ",file=fout)
        kdata.append(lmd)
    print("", file=fout)
    data.append(kdata)

data=np.array(data)
nbnd=data.shape[1]
nl=data.shape[0]
nv=int(nl/nspacing+0.5)
vx=[data[k*nspacing][0] for k in range(1,nv)]

for k in range(1,nbnd):
    plt.plot(data[:,0], data[:,k], label="mode"+str(k))

for iv in vx:
    plt.axvline(iv,color='k',lw=0.5)
plt.axhline(0,color='k',lw=0.5)
plt.xlim(data[0][0],data[-1][0])
a=[data[0][0]]; b=[data[-1][0]]
xlb=a+vx+b
print(xlb)
ax = plt.subplot(111)
ax.set_xticks(xlb)
ax.set_xticklabels(kpoints)

plt.ylabel(r"$\lambda$")

plt.legend()
plt.tight_layout()
plt.savefig('fig.png')
plt.show()

fs.close()
fu.close()
fout.close()

