#!/usr/bin/env python3

import sys

fin=open(sys.argv[1],"r")

cell=[[0 for i in range(3)] for j in range(3)]
ntyp=[]; natom=[]; atoms=[]

for line in fin:
    if("CELL_PARAMETERS" in line):
        scaler=1.0
        if("alat" in line):
            scaler=float(line.split()[-1].strip(")"))
        elif("angstrom" in line):
            scaler=1.0

        for i in range(3):
            ll=fin.readline().split()
            for j in range(3):
                cell[i][j]=float(ll[j])*scaler
    if("ATOMIC_POSITIONS" in line):
        if('crystal' in line):
            ntyp=[]; natom=[]; atoms=[]
            for line in fin:
                ll=line.split()
                if(len(ll) != 4):
                    break
                if(ll[0] not in ntyp):
                    ntyp.append(ll[0])
                    natom.append(1)
                else:
                    idx=ntyp.index(ll[0])
                    natom[idx]+=1
                atoms.append([ll[1],ll[2],ll[3]])
fin.close()

fout=open("final.vasp","w+")
print("ibrav=0",sys.argv[1]+" to POSCAR",file=fout)
print("1.0",file=fout)
for mm in cell:
    print(*mm, file=fout)
print(*ntyp, file=fout)
print(*natom, file=fout)
print("Direct",file=fout)

ct=0
for i in range(len(ntyp)):
    for k in range(natom[i]):
        print(*atoms[ct], ntyp[i], file=fout)
        ct+=1

#for iatom in atoms:
#    print(*iatom, file=fout)
fout.close()


