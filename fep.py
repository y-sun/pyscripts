#!/usr/bin/env python3

import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t","--temp", help="temperature", action='store')
parser.add_argument("-f","--file", help="Ep-ti.dat at lambda=0",action='store')
parser.add_argument("-n","--number", help="desired averaged steps",action='store')
parser.add_argument
args = parser.parse_args()

data_in=np.loadtxt(args.file,skiprows=1)

T=float(args.temp)
kB=8.61733326E-5
ntotal=data_in.shape[0]
if(args.number is not None):
    nave=int(args.number)
else:
    nave=ntotal

data=data_in[np.random.choice(ntotal, nave, replace=False), :]
Ea=data[:,1]
Ec=data[:,2]
dE=Ea-Ec
print("total steps:",ntotal)
print("averaged steps:",nave)
print("mean, std. of energy difference:",np.mean(dE),np.std(dE))

e_dE = np.exp( -(Ea-Ec)/kB/T )

fep = -kB*T*np.log( np.mean(e_dE))

print("dF:",fep)
#print(np.mean(Ea-Ec))
