#!/usr/bin/env python3
import sys
sys.path.append('/home/yangsun/git/pylib')
import MD

#mass=[58.933,91.224] #Co Zr
mass=[]
filename=sys.argv[1]
step=sys.argv[2]
leng=len(sys.argv)
dic={'Tb': 158.92534,'Co':58.933,'Zr':91.224,'Hf':178.490,'Al':26.983,'Fe':55.845,
     'Sm':150.360,'Cu':63.546,'Ni':58.71, 'Mg':24.305, 'P': 30.974, 'Si': 28.0855 , 'Sn': 118.71 }
for i in range(1,leng-2): 
   mass.append(dic[sys.argv[2+i]])

MD.dump2datain(filename,int(step),mass)
