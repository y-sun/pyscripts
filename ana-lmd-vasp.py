#!/usr/bin/env python3

import numpy as np

natom=999

# scr
fin=open("scr/OUTCAR","r")
scr_f=[]; scr_eig=[]
scr_eig_x=[]; scr_eig_y=[]; scr_eig_z=[]
for line in fin:
    if("NIONS" in line):
        natom=int(line.split()[-1])
    if("2PiTHz" in line):
        ll=line.split()
        scr_f.append(float(ll[-2]))
        fin.readline()
        eig=[]; x=[]; y=[]; z=[]
        for i in range(natom):
            ll=fin.readline().split()
            for j in range(3):
                eig.append(np.abs(float(ll[j+3])))
                x.append(float(ll[3]))
                y.append(float(ll[4]))
                z.append(float(ll[5]))
        scr_eig.append(eig)
        scr_eig_x.append(x)
        scr_eig_y.append(y)
        scr_eig_z.append(z)
fin.close()

# unscr
fin=open("unscr/OUTCAR","r")
unscr_f=[]; unscr_eig=[]
unscr_eig_x=[]; unscr_eig_y=[]; unscr_eig_z=[]
for line in fin:
    if("NIONS" in line):
        natom=int(line.split()[-1])
    if("2PiTHz" in line):
        ll=line.split()
        unscr_f.append(float(ll[-2]))
        fin.readline()
        eig=[]; x=[]; y=[]; z=[]
        for i in range(natom):
            ll=fin.readline().split()
            for j in range(3):
                eig.append(np.abs(float(ll[j+3])))
                x.append(float(ll[3]))
                y.append(float(ll[4]))
                z.append(float(ll[5]))
        unscr_eig.append(eig)
        unscr_eig_x.append(x)
        unscr_eig_y.append(y)
        unscr_eig_z.append(z)
fin.close()

# transform
scr_f=np.array(scr_f)
scr_eig=np.array(scr_eig)
unscr_f=np.array(unscr_f)
unscr_eig=np.array(unscr_eig)

scr_eig_x=np.array(scr_eig_x)
scr_eig_y=np.array(scr_eig_y)
scr_eig_z=np.array(scr_eig_z)

unscr_eig_x=np.array(unscr_eig_x)
unscr_eig_y=np.array(unscr_eig_y)
unscr_eig_z=np.array(unscr_eig_z)

#print(scr_eig)
#print(unscr_eig)

nmode=scr_eig.shape[0]-3 # disregard last 3

# match eigenvectors between scr and unscr
matcher=[-1 for k in range(nmode)]
dev=[-9999 for k in range(nmode)]

tag=[1 for k in range(nmode)]
for i in range(nmode):
    diff=99999; sel=-1
    for j in range(nmode):
        if(tag[j]==0):
            continue
        
        dx=scr_eig_x[i]-unscr_eig_x[j]
        dy=scr_eig_y[i]-unscr_eig_y[j]
        dz=scr_eig_z[i]-unscr_eig_z[j]
        dd1=np.sum(np.sqrt(dx**2+dy**2+dz**2))

        dx=scr_eig_x[i]+unscr_eig_x[j]
        dy=scr_eig_y[i]+unscr_eig_y[j]
        dz=scr_eig_z[i]+unscr_eig_z[j]
        dd2=np.sum(np.sqrt(dx**2+dy**2+dz**2))

#        dd1 = np.sum((scr_eig[i] - unscr_eig[j])**2)
#        dd2 = np.sum((scr_eig[i] + unscr_eig[j])**2) # symmetry reversed
        dd = np.min([dd1,dd2])
        
        # xy symmetry
        #dd1 = np.sum((scr_eig_x[i] - unscr_eig_x[j])**2) + np.sum((scr_eig_y[i] - unscr_eig_y[j])**2) + np.sum((scr_eig_z[i] - unscr_eig_z[j])**2)
        #dd2 = np.sum((scr_eig_y[i] - unscr_eig_x[j])**2) + np.sum((scr_eig_x[i] - unscr_eig_y[j])**2) + np.sum((scr_eig_z[i] - unscr_eig_z[j])**2)  # symmetry
        #dd3 = np.sum((scr_eig_x[i] + unscr_eig_x[j])**2) + np.sum((scr_eig_y[i] + unscr_eig_y[j])**2) + np.sum((scr_eig_z[i] + unscr_eig_z[j])**2)
        #dd4 = np.sum((scr_eig_y[i] + unscr_eig_x[j])**2) + np.sum((scr_eig_x[i] + unscr_eig_y[j])**2) + np.sum((scr_eig_z[i] + unscr_eig_z[j])**2)  # symmetry
        #dd = np.min([dd1,dd2,dd3,dd4])
        
        if(dd<diff):
            sel=j
            diff=dd
#    tag[sel]=0
    matcher[i]=sel
    dev[i]=diff

#print("id matcher eig_dev")
#for k in range(len(matcher)):
#    print("%d %d %.2f"%(k, matcher[k], dev[k]))

# check repeated matcher
from collections import Counter
repeated=[k for k,v in Counter(matcher).items() if v>1]
if(len(repeated)!=0):
    print("Error: repeated matcher! Check eigenvectors")
    print("Repeatd:",end=" ")
    for ir in repeated:
        print(ir,end=" ")
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
print("#mode_id omega_scr oemga_unscr",file=fout)
k=1
for i in range(nmode):
    print(k,scr_f[i],unscr_f[matcher[i]],file=fout)
    k+=1
for i in range(-3,0):
    print(k,scr_f[i],unscr_f[i],file=fout)
    k+=1
fout.close()

#print("lmd:", end=" ")
#for ilmd in lmd:
#    print("%.2f"%(ilmd), end=" ")
#print("")
print("lmd_max",np.max(lmd))
