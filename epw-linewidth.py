#!/usr/bin/env python3

import pylab as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="linewidth.phself.* file", action='store')
parser.add_argument("-n","--nmode", help="number of modes",action='store')
args = parser.parse_args()

data=np.loadtxt(args.file,skiprows=2)
nmode=int(args.nmode)
nq=data.shape[0]//nmode

plt.figure(figsize=(8,10))
plt.rcParams.update({'font.size': 16})

plt.subplot(2,1,1)
for k in range(nmode):
    x=[]; y=[]
    for i in range(nq):
        x.append(data[ i*nmode+k, 0])
        y.append(data[ i*nmode+k, 3])
    plt.plot(x,y,label=f'mode{k}')
plt.xlabel('q-path')
plt.ylabel('$\gamma_{qv}$ (meV)')
plt.legend()

plt.subplot(2,1,2)
for k in range(nmode):
    x=[]; y=[]; z=[]
    for i in range(nq):
        x.append(data[ i*nmode+k, 0])
        y.append(data[ i*nmode+k, 2])
        z.append(data[ i*nmode+k, 3])
    mz=max(z)
    z=np.array(z)/mz*80.0
    plt.scatter(x,y,s=z, label=f'mode{k}')
plt.xlabel('q-path')
plt.ylabel('Phonon frequency (meV)')
plt.legend()







plt.tight_layout()
plt.savefig('linewidth.png')
