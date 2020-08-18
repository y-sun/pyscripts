#!/usr/bin/env python3

import sys

fout=open("merge.xdatcar","w+")
fin=open(sys.argv[1],"r")
for line in fin:
   print(line.strip("\n"),file=fout)
fin.close()

fls=[sys.argv[k] for k in range(2,len(sys.argv)-2+2)]

#for i in range(2,int(sys.argv[1])+1):
#   fin=open(str(i)+"/XDATCAR","r")
for ifl in fls:
   fin=open(ifl,"r")
   for k in range(7):
      fin.readline()
   for line in fin:
      print(line.strip("\n"),file=fout)
   fin.close()

fout.close()
