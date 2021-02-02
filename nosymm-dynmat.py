#!/usr/bin/env python3

import glob
import shutil
from subprocess import Popen, PIPE

file0=glob.glob("dyn*")
files=[]
for k in range(len(file0)):
    files.append("dyn"+str(k))
#files=sorted(glob.glob("dyn*"))

count=1
Qp=[]; mesh=''
for ifl in files:
    if(ifl == "dyn0"):
        fin=open(ifl,"r")
        mesh=fin.readline().strip("\n")
        fin.close()
        continue
    fin=open(ifl,"r")
    heads=[]
    for line in fin:
        if("Dynamical  Matrix in cartesian axes" in line):
            break
        heads.append(line.strip("\n"))
#    print(count,heads[2])
    natom=int(heads[2].split()[1])
    for line in fin:
        if("q =" in line):
            ll = line.split()
            Qp.append([ll[3],ll[4],ll[5]])
            fout=open("tmp-dyn","w+")
            for ll in heads:
                print(ll,file=fout)
            print("     Dynamical  Matrix in cartesian axes",file=fout)
            print("",file=fout)
            print(line.strip("\n"),file=fout)
            for k in range(4*natom*natom+1):
                print(fin.readline().strip("\n"),file=fout)
            fout.close()
            
            process = Popen(['q2qstar.x', "tmp-dyn"], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()

            fout=open("Dyn-nosym"+str(count),"w+")
            f1=open("tmp-dyn","r")
            for line in f1:
                print(line.strip("\n"),file=fout)
            f1.close()
            f2=open("rot_tmp-dyn","r")
            for line in f2:
                if("Diagonalizing" in line):
                    print(line.strip("\n"),file=fout)
                    break
            for line in f2:
                if("q2qstar.x" in line):
                    break
                print(line.strip("\n"),file=fout)
            fout.close()
            print(ifl,"->","Dyn-nosym"+str(count))
            count += 1
        elif("Diagonalizing" in line):
            break
    fin.close()

fout=open("Dyn-nosym0","w+")
print(mesh,file=fout)
print(len(Qp),file=fout)
for iq in Qp:
    print(*iq,file=fout)
fout.close()
