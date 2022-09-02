#!/usr/bin/env python3

import sys
fin=open(sys.argv[1],'r')
fout=open("pure.vasp","w+")

for k in range(5):
    print(fin.readline().strip('\n'),file=fout)
fin.readline()
print("Fe",file=fout)
line=fin.readline().split()
pop=[int(k) for k in line]
print(sum(pop),file=fout)
for line in fin:
    print(line.strip("\n"),file=fout)
fout.close()
