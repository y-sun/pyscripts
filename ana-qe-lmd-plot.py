#!/usr/bin/env python3

import sys
import pylab as plt
import numpy as np
import itertools
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-q","--qp", help="q points relating to dyn*.elph.*", nargs='*',action='store')
args = parser.parse_args()

titles=args.qp
nq=len(titles)

for nf in range(nq):
    fin=open("dyn"+str(nf+1)+".elph."+str(nf+1),"r")
    ll=fin.readline().split()
    
    ngauss=int(ll[3])
    nmode=int(ll[4])
    
    dgauss=[]; lmd=[]
    for line in fin:
        if("Gaussian Broadening" in line):
            dg=float(line.split()[2])*13.6056980659  # Ry to eV
            dgauss.append(dg)
            fin.readline()
            ld=[]
            for k in range(nmode):
                ld.append(fin.readline().split()[2])
            lmd.append(ld)
    fin.close()

    fout=open("g-lmd"+str(nf+1)+".dat","w+")
    print("#gaussian(eV)",end=" ",file=fout)
    for k in range(nmode):
        print("mode"+str(k+1),end=" ",file=fout)
    print("",file=fout)
    
    for k in range(ngauss):
        print(dgauss[k],end=" ",file=fout)
        for j in range(nmode):
            print(lmd[k][j],end=" ",file=fout)
        print("",file=fout)
    fout.close()

# plot

plt.figure(figsize=(nq*3.2,4))
plt.rcParams.update({'font.size': 14})

#titles=["$\Gamma$(0 0 0)","A(0 0 1/2)","M(1/2 0 0)", "L(1/2 0 1/2)"]
marker = ['x', '+', 'v', 'o', '^',"*",'x', '+', 'v', 'o', '^',"*",'x', '+', 'v', 'o', '^',"*",'x', '+', 'v', 'o', '^',"*"]

ymax=5
for k in range(nq):
    data=np.loadtxt("g-lmd"+str(k+1)+".dat",skiprows=1)
    ymax=max(ymax,np.max(data))+0.5
    plt.subplot(1,nq,k+1)
    for i in range(nmode):
        plt.plot(data[:,0],data[:,i+1],marker=marker[i],label="mode"+str(i))
    if(k==0):
        plt.ylabel("$\lambda_{qv}$")
    plt.xlabel("Gaussian broadening (eV)")
    plt.ylim(-0.5,ymax)
    plt.title(titles[k])
    if(k==nq-1):
        plt.legend(ncol=2,fontsize=6)

plt.tight_layout()
plt.savefig("fig.png")
#plt.show()
