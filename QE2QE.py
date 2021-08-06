#!/usr/bin/env python3

import sys

fin=open(sys.argv[1],"r")

cell=[[0 for i in range(3)] for j in range(3)]
ntyp=[]; natom=[]; atoms=[]

Ry2eV=13.6056980659  # 1 Rydberg constant = 13.6056980659 eV
eV2Ry=1/Ry2eV # 1 eV = 0.0734986176 Rydberg constant
au2ang=0.529177249 # 1 a.u., b = 0.529177249 A
ang2au=1/au2ang

for line in fin:
    if("CELL_PARAMETERS" in line):
        scaler=1.0
        if("alat" in line):
            scaler=float(line.split()[-1].strip(")"))*au2ang
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
                atoms.append(line.strip("\n"))
                #atoms.append([ll[1],ll[2],ll[3]])
                #atoms.append("%.6f %.6f %.6f"%(float(ll[1]),float(ll[2]),float(ll[3])))
fin.close()

fout=open("final.QE","w+")
print("Use ibrav=0!!")
print("CELL_PARAMETERS {angstrom}",file=fout)
for mm in cell:
    print(*mm, file=fout)
print("ATOMIC_POSITIONS {crystal}",file=fout)
ct=0
for i in range(len(atoms)):
    print(atoms[i],file=fout)

#for i in range(len(ntyp)):
#    for k in range(natom[i]):
#        print(ntyp[i], atoms[ct],  file=fout)
#        ct+=1

fout.close()


