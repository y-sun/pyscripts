#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

#plt.figure(figsize=(8,10))
plt.rcParams.update({'font.size': 12})
f, (p0, p1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]},figsize=(8,10))

# qha
fin=open("results/f_tv_nonfitted_ev_ang3.txt","r")
vol=[]
ll=fin.readline().split()
for k in range(1,len(ll)):
    vol.append(float(ll[k]))

temp=[str(k) for k in range(0,10000,2000)]
print(len(temp))
colors=['b', 'g', 'r', 'c', 'm', 'y', 'k'] 
ck=0
hybrid=[]
for line in fin:
    ll=line.split()
    if(ll[0] in temp):
        helm=[]
        for k in range(1,len(ll)):
            helm.append(float(ll[k]))
        if(ll[0]=='0'):
            p0.plot(vol, helm,  "-x", label=r"hybrid, "+ll[0]+"K+ZPE",c=colors[ck])
        else:
            p0.plot(vol, helm,  "-x", label="hybrid, "+ll[0]+"K",c=colors[ck])
        ck+=1
        helm.reverse()
        hybrid.append(helm)

fin.close()


# Phonopy-QHA
ck=0
fin=open("0805-phonopy/B2-18p/helmholtz-volume.dat","r")
phy=[]
mk=['o','v','x','s','h']
for line in fin:
    if("Temperature" in line):
        ll=line.split()
        tt=ll[2].split(".")[0]
        if(tt in temp):
            fin.readline()
            vol=[]; helm=[]
            for line2 in fin:
#            for kk in range(26):
                lll=line2.split()
                if(len(lll)!=2):
                    break
                vol.append(float(lll[0]))
                helm.append(float(lll[1]))
            if(tt=='0'):
                p0.plot(vol, helm, lw=0, marker='o', fillstyle='none', label="Phonopy, "+tt+"K+ZPE",c=colors[ck])
            else:
                p0.plot(vol, helm, lw=0, marker='o', fillstyle='none', label="Phonopy, "+tt+"K",c=colors[ck])
            ck+=1
            phy.append(helm)

p0.set_xlabel(r"volume ($\AA^3$/cell)")
p0.set_ylabel(r"helmholtz free energy (eV/cell)")
p0.legend(ncol=2)

hybrid=np.array(hybrid)
phy=np.array(phy)
for k in range(len(temp)):
    if(temp[k]=='0'):
        p1.plot(vol,(hybrid[k,:]-phy[k,:])*1000/64,c=colors[k],marker=mk[k],fillstyle='none',label=temp[k]+r"K+ZPE")
    else:
        p1.plot(vol,(hybrid[k,:]-phy[k,:])*1000/64,c=colors[k],marker=mk[k],fillstyle='none',label=temp[k]+r"K")
p1.legend(ncol=2)
p1.set_xlabel(r"volume ($\AA^3$/cell)")
p1.set_ylabel("$\Delta F=F_{hybrid}-F_{phonopy}$\n(meV/atom)")
p1.set_ylim(-1,1)

#f.suptitle("fp-B2, 18%")
p0.set_title("fp-B2-18%, hybrid: DFT+U&Phonopy for phonon with $qha$ for QHA")
f.tight_layout()
f.savefig("fig.png")
plt.show()
