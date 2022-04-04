#!/usr/bin/env python3

import numpy as np
import yaml

# atom info
fin=open("POSCAR","r")
for k in range(5):
    fin.readline()
ll=fin.readline().split()
ele=[k for k in ll]
ll=fin.readline().split()
pop=[int(k) for k in ll]
fin.close()

# scr
fin=open("scr/band.yaml","r")
scr_f=[]; 
scr_eig_x=[]; scr_eig_y=[]; scr_eig_z=[]; scr_v2=[]
for line in fin:
    if("natom:" in line):
        natom=int(line.split()[-1])
    if("q-position: [    0.0000000,    0.0000000,    0.0000000" in line):
        break

for line in fin:
    if("frequency:" in line):
        f=float(line.split()[-1])*4.136 # THz -> meV
        scr_f.append(f)
        fin.readline()
        eigx=[]
        eigy=[]
        eigz=[]
        v2=[]
        for k in range(natom):
            fin.readline()
            ll=fin.readline().split()
            x=float(ll[2].strip(","))
            ll=fin.readline().split()
            y=float(ll[2].strip(","))
            ll=fin.readline().split()
            z=float(ll[2].strip(","))
            
            eigx.append(x)
            eigy.append(y)
            eigz.append(z)
            v2.append(x**2+y**2+z**2)
        v2_ele=[]; ct=0
        for i in range(len(ele)):
            same_ele=0
            for k in range(pop[i]):
                same_ele+=v2[ct]
                ct+=1
            v2_ele.append(same_ele)
        
        scr_eig_x.append(eigx)
        scr_eig_y.append(eigy)
        scr_eig_z.append(eigz)
        scr_v2.append(v2_ele)
    if("q-position" in line):
        break
fin.close()

# unscr
fin=open("unscr/band.yaml","r")
unscr_f=[]; 
unscr_eig_x=[]; unscr_eig_y=[]; unscr_eig_z=[]
for line in fin:
    if("q-position: [    0.0000000,    0.0000000,    0.0000000" in line):
        break

for line in fin:
    if("frequency:" in line):
        f=float(line.split()[-1])*4.136 # THz -> meV
        unscr_f.append(f)
        fin.readline()
        eigx=[]
        eigy=[]
        eigz=[]
        for k in range(natom):
            fin.readline()
            ll=fin.readline().split()
            eigx.append(float(ll[2].strip(",")))
            ll=fin.readline().split()
            eigy.append(float(ll[2].strip(",")))
            ll=fin.readline().split()
            eigz.append(float(ll[2].strip(",")))
        unscr_eig_x.append(eigx)
        unscr_eig_y.append(eigy)
        unscr_eig_z.append(eigz)
    if("q-position" in line):
        break
fin.close()

# output unsorted
#fout=open("omega-no-match.dat","w+")
#print("#order scr unscr", file=fout)
#for k in range(len(scr_f)):
#    print(k,scr_f[k], unscr_f[k], file=fout)
#fout.close()

# remove first three
nr=3

# transform
scr_f_tra=np.array(scr_f[:nr])
unscr_f_tra=np.array(unscr_f[:nr])

scr_f=np.array(scr_f[nr:])
scr_eig_x=np.array(scr_eig_x[nr:])
scr_eig_y=np.array(scr_eig_y[nr:])
scr_eig_z=np.array(scr_eig_z[nr:])

unscr_f=np.array(unscr_f[nr:])
unscr_eig_x=np.array(unscr_eig_x[nr:])
unscr_eig_y=np.array(unscr_eig_y[nr:])
unscr_eig_z=np.array(unscr_eig_z[nr:])

#print(scr_eig)
#print(unscr_eig)

nmode=scr_eig_x.shape[0] 

# match eigenvectors between scr and unscr
matcher=[-1 for k in range(nmode)]
dev=[-9999 for k in range(nmode)]
for i in range(nmode): 
    diff=9999; sel=-1
    for j in range(nmode):
        dx=scr_eig_x[i]-unscr_eig_x[j]
        dy=scr_eig_y[i]-unscr_eig_y[j]
        dz=scr_eig_z[i]-unscr_eig_z[j]
        dd1=np.sum(np.sqrt(dx**2+dy**2+dz**2))
        
        dx=scr_eig_x[i]+unscr_eig_x[j]
        dy=scr_eig_y[i]+unscr_eig_y[j]
        dz=scr_eig_z[i]+unscr_eig_z[j]
        dd2=np.sum(np.sqrt(dx**2+dy**2+dz**2))



        #dd = np.sum(abs(scr_eig[i]**2 - unscr_eig[j]**2))
        #dd = np.sum(scr_eig[i]*unscr_eig[j])
        #dd1 = np.sum((scr_eig[i] - unscr_eig[j])**2)
        #dd2 = np.sum((scr_eig[i] + unscr_eig[j])**2)
        dd=np.min([dd1,dd2])
        if(dd<diff):
            sel=j
            diff=dd
    matcher[i]=sel
    dev[i]=diff



#print("matcher:",matcher)
#print(dev)

# check repeated matcher
from collections import Counter
repeated=[k for k,v in Counter(matcher).items() if v>1]
if(len(repeated)!=0):
    print("Error: repeated matcher! Check eigenvectors")
    print("Repeatd:",end=" ")
    for ir in repeated:
        print(ir,end=" ")
    print("matcher:",matcher)
    print("")


# get lambda
lmd=[]
for i in range(nmode):
    scr_i=scr_f[i]
    unscr_i=unscr_f[matcher[i]]
    lmd_i= ((scr_i**2-unscr_i**2)/scr_i**2)/(-2)
    lmd.append(lmd_i)

# print
fout=open("omega.dat","w+")
print("#id unscr_id  omega_scr oemga_unscr",end=" ",file=fout)
for k in ele:
    print(k, end=" ",file=fout)
print("",file=fout)

ntotal=nr+nmode
k=0
for i in range(nr):
    print(ntotal-k,ntotal-k, scr_f_tra[i], unscr_f_tra[i],end=" ", file=fout)
    for j in range(len(ele)):
        print("%6.3f"%(scr_v2[i][j]),end=" ",file=fout)
    print("",file=fout)
    k+=1
for i in range(nmode):
    print(ntotal-k,matcher[i]+1, scr_f[i],unscr_f[matcher[i]],end=" ",file=fout)
    for j in range(len(ele)):
        print("%6.3f"%(scr_v2[i][j]),end=" ",file=fout)
    print("",file=fout)
    k+=1
fout.close()

print("lmd_max/lmd_sum",np.max(lmd),np.sum(lmd))
