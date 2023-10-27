#!/usr/bin/env python3

import sys

fin=open("merge.xdatcar","r")
fout=open("combined.vasp","w+")

nstep=int(sys.argv[1])
for k in range(6):
    print(fin.readline().strip("\n"),file=fout)
ll=fin.readline().split()
n1=int(ll[0])
n2=int(ll[1])

print(n1*nstep, n2*nstep, file=fout)
print("Direct",file=fout)
Fe=[]; O=[] ; H=[]
for k in range(nstep):
    fin.readline()
    for i in range(n1):
        ll=fin.readline().split()
        pos=[float(x) for x in ll]
        for j in range(3):
            if(pos[j]<0):
                pos[j]+=1
            elif(pos[j]>1):
                pos[j]-=1         
        Fe.append('%.6f %.6f %.6f'%(pos[0],pos[1],pos[2]))
    for i in range(n2):
        ll=fin.readline().split()
        pos=[float(x) for x in ll]
        for j in range(3):
            if(pos[j]<0):
                pos[j]+=1
            elif(pos[j]>1):
                pos[j]-=1         
        O.append('%.6f %.6f %.6f'%(pos[0],pos[1],pos[2]))
fin.close()

for line in Fe:
    print(line,file=fout)
for line in O:
    print(line,file=fout)
fout.close()
