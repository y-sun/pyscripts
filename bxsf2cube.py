#!/usr/bin/env python3

import sys

angs2bohr=1.88973
fin=open(sys.argv[1],'r')
Ef=0
for line in fin:
   if("Fermi Energy:" in line):
      Ef=line.split()[-1]
   if("BANDGRID_3D_BANDS" in line):
      break

heads=['CUBE file',
      f'Ef: {Ef}']
nbnd=int(fin.readline().split()[0])
line=fin.readline().split()
nk=[int(n) for n in line]
fin.readline()
box=[]
for k in range(3):
   ll=fin.readline().split()
   bb=[float (x) for x in ll]
   box.append(bb)
fin.close()

name=sys.argv[1].split('.')[0]
fin=open(sys.argv[1],'r')
for k in range(18):
   fin.readline()

fout=open('.a','w+')
Ef=float(Ef)
for line in fin:
   if("BAND:" in line):
      fout.close()
      nbnd=line.split()[1]
      fout=open(f"{name}.{nbnd}.cube","w+")
      for il in heads:
         print(il,file=fout)
      print("0 0.0 0.0 0.0",file=fout)
      for k in range(3):
         print(nk[k], end=" ",file=fout)
         for j in range(3):
            print("%12.6f"%(box[k][j]/nk[k]*angs2bohr), end=" ", file=fout)
         print("",file=fout)
   elif("END_BANDGRID_3D" in line):
      fout.close()
      break
   else:
      ll=line.split()
      data=[float(k) for k in ll]
      for ida in data:
         print("%16.5e"%(ida-Ef),end=" ",file=fout)
      print("",file=fout)
#      print(line.strip('\n'), file=fout)
