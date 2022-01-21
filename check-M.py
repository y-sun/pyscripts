#!/usr/bin/env python3
  
import sys

fin=open(sys.argv[1],"r")

M=[999 for k in range(4)]

for line in fin:
    if("magnetization (x)" in line):
        for k in range(3):
            fin.readline()
        for k in range(4):
            ll=fin.readline().split()
            M[k]=ll[-1]


for k in range(4):
    if(k!=3):
        print(M[k], end=" ")
    else:
        print(M[k], end="")
print("")
