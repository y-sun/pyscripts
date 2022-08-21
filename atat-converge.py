#!/usr/bin/env python3

import glob

files=sorted(glob.glob("*/vasp.out.static"))
unconverge=[]
fout=open("converge.log","w+")
for ifl in files:
    fin=open(ifl,'r')
    tag=0
    for line in fin:
        if("reached" in line):
            tag=1
            break
    fin.close()
    if(tag==0):
        print(ifl, "not converged")
        print(ifl, "not converged",file=fout)
        unconverge.append(ifl.split('/')[0])
for i in unconverge:
    print(i,end=" ",file=fout)
    print(i,end=" ")
print("")
fout.close()
