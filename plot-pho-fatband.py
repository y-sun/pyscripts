#!/usr/bin/env python3

import  numpy as np
import argparse
import pylab as plt

parser = argparse.ArgumentParser()
parser.add_argument("-a","--atoms", help="atoms index", nargs='*', action='store')
parser.add_argument("-k","--kp", help="k points", nargs='*', action='store')
parser.add_argument("-s","--spacing", help="spacing, same to band.conf",action='store')
parser.add_argument("-t","--title", help="plot title",action='store')
args = parser.parse_args()

atoms=args.atoms
natom=len(atoms)
kpoints=args.kp
nk=len(kpoints)
nspacing=int(args.spacing)

nband=nspacing*(nk-1)


plt.figure(figsize=(8,6), dpi=200)
plt.rcParams.update({'font.size': 14})

if (natom<7):
    colors=['r','b','g','c','m','y']
else:
    colors=plt.cm.rainbow(np.linspace(0,1,natom))

for i in range(natom):
    fin=open("fat-band"+str(i),"r")
    for k in range(natom*3):
        xk=[]; yf=[]; cont=[]
        for ik in range(nk-1):
            for j in range(nspacing):
                ll=fin.readline().split()
                if(ik!=0 and j==0):
                    continue
                xk.append(float(ll[0]))
                yf.append(float(ll[1]))
                cont.append(float(ll[2])*150)  # 50 is factor for scatter size
        fin.readline()
        if(i==0):
            plt.plot(xk,yf,linestyle='-',color='k')
        if(k==0):
            plt.scatter(xk,yf,s=cont,color=colors[i], linewidths=0 ,alpha=0.2,label=atoms[i])
            #plt.scatter(xk,yf,s=cont,facecolors='none', edgecolors=colors[i], linewidths=0.4, label=atoms[i])
        else:
            plt.scatter(xk,yf,s=cont,color=colors[i], linewidths=0 ,alpha=0.2)
            #plt.scatter(xk,yf,s=cont,facecolors='none', edgecolors=colors[i], linewidths=0.4)
    fin.close()

# labels
plt.ylabel(r"Frequency (THz)")

vx=[]
for k in range(1,nk-1):
    vx.append(xk[k*nspacing-k])


for iv in vx:
    plt.axvline(iv,color='k',lw=0.5)
plt.axhline(0,color='k',lw=0.5)
plt.xlim(xk[0],xk[-1])

a=[xk[0]]; b=[xk[-1]]
xlb=a+vx+b
ax = plt.subplot(111)
ax.set_xticks(xlb)
ax.set_xticklabels(kpoints)

if(args.title is not None):
    plt.title(args.title)

plt.legend()
plt.tight_layout()
plt.savefig('fig.png')
plt.show()

