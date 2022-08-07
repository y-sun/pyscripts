#!/usr/bin/env python3

from py4vasp import Calculation
calc = Calculation.from_path(".")
data=calc.dos.read(selection="1(fy3x2) 1(fxyz) 1(fyz2) 1(fz3) 1(fxz2) 1(fzx2) 1(fx3)")
ldata=list(data)

fout=open("PDOS_f_angular.dat","w+")
for k in range(9):
    print(ldata[k].split("_")[-1],end=" ",file=fout)
print("", file=fout)
for k in range(data['energies'].size):
    for i in range(9):
        print(data[ ldata[i] ][k], end=" ", file=fout)
    print("",file=fout)
fout.close()