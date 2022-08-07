#!/usr/bin/env python3

from py4vasp import Calculation
calc = Calculation.from_path(".")
data=calc.dos.read(selection="1(fy3x2) 1(fxyz) 1(fyz2) 1(fz3) 1(fxz2) 1(fzx2) 1(fx3)")
ldata=list(data)

fout=open("PDOS_f_angular.dat","w+")
tag=[1 for k in range(17)] # 17 = 1 + 2 + 7*2
for k in range(17):
    print(ldata[k],end=" ",file=fout)
    if("down" in ldata[k]):
        tag[k]=-1
print("", file=fout)
for k in range(data['energies'].size):
    for i in range(17):
        print(tag[k]*data[ ldata[i] ][k], end=" ", file=fout)
    print("",file=fout)
fout.close()
