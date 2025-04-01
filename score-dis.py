#!/usr/bin/env python3

import MD
import sys
import pylab as plt

if(len(sys.argv) != 3):
    print("exe file(only read last conlum) factor")
    exit()

factor=float(sys.argv[2])

fin=open(sys.argv[1],"r")
ll=fin.readline().split()
fin.seek(0)
nn=len(ll)
sc=[]
for line in fin:
    ll=line.split()
    sc.append(float(ll[nn-1])/factor)
fin.close()



q,f= MD.freq(sc, 0.002, 0, max(sc)+0.002)
fout=open("score-dis.dat","w+")
print("#score(rc="+sys.argv[2]+") freq",file=fout)

for k in range(len(q)):
    print(q[k],f[k]/sum(f),file=fout)
fout.close()

plt.plot(q,f)
plt.grid()
plt.savefig("his.png")
