#!/usr/bin/env python3

import pylab as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="lambda.phself.* file", action='store')
args = parser.parse_args()

data=np.loadtxt(args.file,skiprows=4)
nmode=data.shape[1]-1

plt.figure(figsize=(8,6))
plt.rcParams.update({'font.size': 16})

for k in range(nmode):
    plt.plot(data[:,0],data[:,k+1],label=f'mode{k}')

plt.xlabel('q-path')
plt.ylabel('$\lambda_{qv}$')
plt.legend()
plt.tight_layout()
plt.savefig('lambda.png')
