#!/usr/bin/env python3

import MD
import sys
import pylab as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="input file (XDATCAR/POSCAR with direct coordinate)",action='store')
parser.add_argument("-j","--jump", help="jumped md step", action='store')
parser.add_argument("-a","--averaged", help="averaged md step", action='store')
parser.add_argument("-r","--radius", help="radius range", action='store')
parser.add_argument("-n","--nbin", help="number of bins", action='store')
args = parser.parse_args()

atom_type,x, grall, gr11, gr12, gr22=MD.gr(args.file, int(args.jump), int(args.averaged), float(args.radius), int(args.nbin))

fout=open('gr-vasp.dat','w')
print('%2s%24s%16s%16s%16s'%("#r","total",atom_type[0]+"-"+atom_type[0],atom_type[0]+"-"+atom_type[1],atom_type[1]+"-"+atom_type[1]),file=fout)
for i in range(len(x)):
    print('%10.4f%16.6f%16.6f%16.6f%16.6f'%(x[i],grall[i],gr11[i],gr12[i],gr22[i]),file=fout)
fout.close()

plt.figure(figsize=(8,6))
plt.rcParams.update({'font.size': 14})

plt.plot(x,grall,label='total',ls='--',marker='o',c='k')
plt.plot(x,gr11,label=atom_type[0]+"-"+atom_type[0],ls='--',marker='o',c='r')
plt.plot(x,gr12,label=atom_type[0]+"-"+atom_type[1],ls='--',marker='o',c='g')
plt.plot(x,gr22,label=atom_type[1]+"-"+atom_type[1],ls='--',marker='o',c='b')
plt.xlabel('r (angstrom)')
plt.ylabel('g(r)')
plt.legend()
plt.tight_layout()
plt.savefig('gr.png')
plt.close()
