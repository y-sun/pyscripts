#!/usr/bin/env python3

import sys

fin=open(sys.argv[1],'r')
fout=open('OUTCAR.simp','w+')

for line in fin:
   if("Total+kin" in line):
      line_P=line.strip('\n')
      for line in fin:
          if("free  energy   TOTEN  =" in line):
              line_E=line.strip('\n')
              break
        
      print(line_P,file=fout)
      print(line_E,file=fout)
      print("",file=fout)

fin.close()
fout.close()


