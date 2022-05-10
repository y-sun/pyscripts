#!/usr/bin/env python3

import numpy as np
from scipy.optimize import fsolve
from scipy.optimize import leastsq
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input", help="input file of xH curve, first line ignore",action='store')
parser.add_argument("-t","--title", help="add title", action='store')
parser.add_argument("-s","--show", help="show the figure", action='store_true')
args = parser.parse_args()

def Hm_model(para,x):
   b=para
   f=b*x-b*x*x
   return f

data=np.loadtxt('xH.dat',skiprows=1)
c=data[:,0]
H=data[:,-1]
H_A=data[0,-1]
H_B=data[-1,-1]
Hm=H - (1-c)*H_A - c * H_B

# least sq fit
target =  lambda para, y, x : y - Hm_model(para,x)
x0= 0.5
fitted, err = leastsq(target, x0, args=(Hm, c))

# plot
import pylab as plt
plt.figure(figsize=(8,6))
plt.rcParams.update({'font.size': 16})

craw = np.linspace(0,1,100)
plt.plot(c, Hm, 'ro', label='raw')
plt.plot(craw, Hm_model(fitted[0],craw), label='$H_m=bc(1-c)$, b=%.2f'%(fitted[0]))
plt.xlabel('$c$')
plt.ylabel('$H_m$ (eV/atom)')
plt.legend()
if(args.title is not None):
   plt.title(args.title)

plt.tight_layout()
plt.savefig('xH.png')
if (args.show):
   plt.show()

print('b=',fitted[0])
