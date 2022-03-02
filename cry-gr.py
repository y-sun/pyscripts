#!/usr/bin/env python3

import numpy as np
import pylab as plt
import sys

def read_pos(fname):
    fin=open(fname,"r")
    fin.readline()
    fac=float(fin.readline().split()[0])
    
    v=[[0 for i in range(3)] for j in range(3)]
    for i in range(3):
        ll=fin.readline().split()
        for j in range(3):
            v[i][j]=float(ll[j])
    v=np.array(v)*fac
    
    atype=fin.readline().split()
    ll=fin.readline().split()
    na = [int(k) for k in ll]
    
    line=fin.readline()
    if(("Direct" not in line) and ("direct" not in line)):
        print("use direct coordinate")
        exit()
    
    atoms=[]
    for i in range(sum(na)):
        ll=fin.readline().split()
        la=[float(k) for k in ll]
        atoms.append(la)
    fin.close()
    
    atoms=np.array(atoms)
    return atype,na,v,atoms

def gr_cal(pA,pB,vec,nrep,rrange):
    dr = 0.1
    nr=int(rrange/dr)
    mesh=[k*dr for k in range(1,nr+1)]
    hist=[0 for k in range(1,nr+1)]
    nA=pA.shape[0]
    nB=pB.shape[0]
    for i in range(nA):
        for j in range(nB):
            for k0 in range(-(nrep[0]-1),nrep[0]):
                for k1 in range(-(nrep[1]-1),nrep[1]):
                    for k2 in range(-(nrep[2]-1),nrep[2]):
                        pnew=pB[j]+np.array([k0,k1,k2])
                        dis=pA[i]-pnew
                        dis_car = dis[0]*vec[0]+dis[1]*vec[1]+dis[2]*vec[2]
                        dd=np.sqrt(np.dot(dis_car,dis_car))
                        if(dd<rrange):
                            if(1<dd<1.6):
                                print(pA[i],pB[j],dis,dis_car)
                            rmesh=int(dd/dr)
                            hist[rmesh]+=1


#            dis=( (abs(pA[i]-pA[j])+1)%1.0 )
#            dis_car = dis[0]*vec[0]+dis[1]*vec[1]+dis[2]*vec[2]
#            dd=np.sqrt(np.dot(dis_car,dis_car))
#            if(dd<rrange):
#                rmesh=int(dd/dr)
#                hist[rmesh]+=1
    hist[0]=0 # remove self
    print(nA,nB)
    const=np.dot(np.cross(vec[0],vec[1]),vec[2])/4/np.pi/nA/nB
    for k in range(nr):
        #hist[k]=hist[k]/(mesh[k]*mesh[k]*dr*dr)*const
        hist[k]=hist[k]/nA

    return mesh,hist

fname=sys.argv[1] #"POSCAR"
atp, anum, vec, atoms=read_pos(fname)
Rc=8.0
n_elong=[]
for i in range(3):
    vl=np.sqrt(np.dot(vec[i],vec[i]))
    n=int(Rc/vl)+1
    n_elong.append(n)

# A-A
nelm=len(atp)
plt.figure(figsize=(8,2.5*nelm))
plt.rcParams.update({'font.size': 12})
ct=0
print("AA pairs")
for k in range(nelm):
    A = atoms[ct:ct+anum[k]]
    ct+= anum[k]
    mesh,hist=gr_cal(A,A,vec,n_elong,Rc)
    plt.subplot(nelm,1,k+1)
    plt.plot(mesh,hist,label=atp[k]+"-"+atp[k])
    plt.legend(loc='upper left')
    if(k==nelm-1):
        plt.xlabel("r ($\AA$)")
    plt.xlim(0,Rc)
plt.tight_layout()
plt.savefig("gr-AA.png")
plt.close()

# A-B
print("AB pairs")
plt.figure(figsize=(8,2.5*(nelm-1)))
plt.rcParams.update({'font.size': 12})
ct1=0
for i in range(nelm-1):
    A = atoms[ct1:ct1+anum[i]]
    plt.subplot(nelm-1,1,i+1)
    ct2=ct1+anum[i]
    for j in range(i+1,nelm):
        B = atoms[ct2:ct2+anum[j]]
        mesh,hist=gr_cal(A,B,vec,n_elong,Rc)
        plt.plot(mesh,hist,label=atp[i]+"-"+atp[j])
        ct2+=anum[j]
    ct1+= anum[i]
    plt.legend(loc='upper left')
    plt.xlim(0,Rc)
    if(i==nelm-2):
        plt.xlabel("r ($\AA$)")
plt.tight_layout()
plt.savefig("gr-AB.png")
plt.close()


