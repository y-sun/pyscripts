#!/usr/bin/env python3

import glob
import numpy as np
import pylab as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d","--disp", help="dispersions", action='store')
parser.add_argument("-g","--gamma", help="elph.gamma file", action='store')
parser.add_argument("-a","--a2f", help="a2f.dos file", action='store')
parser.add_argument("-k","--kp", help="k points", nargs='*',action='store')
parser.add_argument("-n","--number", help="number of spacing",action='store')
parser.add_argument("-p","--pdos", help="partial dos",action='store')
parser.add_argument("-s","--scf", help="scf file",action='store')
args = parser.parse_args()

# disperion parameters
#nspacing=50; kpoints=['G','M','K','G','A','M','H']
nspacing=int(args.number); kpoints=args.kp
comment='tst'
# files
fls=args.disp  #"band.gp" # dispersion file
ngauss=10
gamma_fls=args.gamma #"elph.gamma.3"
a2F_fls=args.a2f #"a2F.dos2"
#gamma_fls=["elph.gamma."+str(k) for k in range(1,1+ngauss)] # gamma files
#a2F_fls=["a2F.dos"+str(k) for k in range(1,1+ngauss)]  # a^2F(w)

plt.rcParams.update({'font.size': 14})
f, (a0, a1, a2) = plt.subplots(1, 3, gridspec_kw={'width_ratios': [2, 1, 1]}, figsize=(12,6))

cm2Thz=0.02998

# read gamma file
fin=open(gamma_fls,"r")
ll=fin.readline().split()
nbnd=int(ll[2].strip(",")) 
nks=int(ll[-2])
gdata=[]
nl=int((nbnd-1)/6)+1
for k in range(nks):
    fin.readline()
    ng=[]
    for j in range(nl):
        ll=fin.readline().split()
        for il in ll:
            ng.append(float(il))
    gdata.append(ng)
fin.close()
gdata=np.array(gdata)

# read dispersion
ct=0
data=np.loadtxt(fls)

#print(gdata.shape)
#print(data.shape)

for k in range(1,data.shape[1]):
    if(k==1):
        a0.plot(data[:,0],data[:,k]*cm2Thz,linestyle='-',color='k',label=comment)
    else:
        a0.plot(data[:,0],data[:,k]*cm2Thz,linestyle='-',color='k')
    a0.scatter(data[:,0],data[:,k]*cm2Thz,s=abs(gdata[:,k-1])*.01,color='r')
ct+=1


ndata=data.shape[0]
nv=int((ndata-1)/nspacing+0.5)
vx=[data[k*nspacing][0] for k in range(1,nv)]
for iv in vx:
    a0.axvline(iv,color='k',lw=0.5)
a0.axhline(0,color='k',lw=0.5)

a0.set_xlim(data[0][0],data[-1][0])
ymax=np.amax(data[:,1:])
ymin=np.amin(data[:,1:])
a0.set_ylim(ymin*cm2Thz-5,ymax*cm2Thz+5)

a=[data[0][0]]; b=[data[-1][0]]
xlb=a+vx+b
a0.set_xticks(xlb)
a0.set_xticklabels(kpoints)
a0.set_ylabel(r"Frequency (THz)")
#a0.legend()

# get pdos
## get atoms
fin=open(args.scf,'r')
for line in fin:
    if("ATOMIC_POSITIONS" in line):
        break
atoms={}
for line in fin:
    if("K_POINTS" in line):
        break
    ll=line.split()
    if(len(ll) != 4):
        break
    elem=ll[0]
    if(elem in atoms):
        atoms[elem]+=1
    else:
        atoms[elem]=1
fin.close()

## get dos
pdata=np.loadtxt(args.pdos,skiprows=1)
ct=2
for elem in atoms:
    data=pdata[:,ct]
    for i in range(atoms[elem]-1):
        data+=pdata[:,ct+i] 
    ct+=atoms[elem]
    a1.plot(data, pdata[:,0]*cm2Thz, label=elem)
a1.set_ylim(ymin*cm2Thz-5,ymax*cm2Thz+5)
a1.set_xlabel(r"PhDOS")
a1.legend()

# read a2F
fin=open(a2F_fls,"r")
freq=[]; a2F=[]
for k in range(5):
    fin.readline()
lmd=-1
for line in fin:
    if("lambda" in line):
        lmd=float(line.split()[2])
        break
    ll=line.split()
    freq.append(float(ll[0]))
    a2F.append(float(ll[1]))
fin.close()

Ry2Thz=3289.8449
a2.plot(a2F, np.array(freq)*Ry2Thz,label=r"$\lambda=$%.2f"%(lmd))
a2.set_ylim(ymin*cm2Thz-5,ymax*cm2Thz+5)
a2.set_xlabel(r"$\alpha^2F(\omega)$")
a2.legend()

f.tight_layout()
f.savefig("elph.png")
