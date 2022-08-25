#!/usr/bin/env python3

import argparse
import numpy as np
import pylab as plt
parser = argparse.ArgumentParser()
parser.add_argument("-i","--input", help="emc2 output",action='store')
parser.add_argument("-r","--ref", help="reference energy at x=0 and 1",nargs="*",action='store')
parser.add_argument("-p","--plot", help="plot histogram", action='store_true')
parser.add_argument("-n","--name", help="plot name",action='store')
args = parser.parse_args()

data=np.loadtxt(args.input)

if (args.ref is None):
    E0=0
    E1=0
else:
    E0=float(args.ref[0])
    E1=float(args.ref[1])

#hte
xhte=(1+data[:,14])/2
Ghte=data[:,15]+data[:,1]*data[:,14] - (1-xhte)*E0 - xhte*E1
Hhte=data[:,13]+data[:,1]*data[:,14] - (1-xhte)*E0 - xhte*E1
TSchte=data[:,15]-data[:,13]
fout=open('hte.dat',"w+")
print("x H(eV/atom) G(eV/atom) TSc(eV/atom)",file=fout)
for k in range(xhte.size):
    print(xhte[k],Hhte[k],Ghte[k],TSchte[k],file=fout)
fout.close()

#lte
xlte=(1+data[:,8])/2
Glte=data[:,9]+data[:,1]*data[:,8] - (1-xlte)*E0 - xlte*E1
Hlte=data[:,7]+data[:,1]*data[:,8] - (1-xlte)*E0 - xlte*E1
TSclte=data[:,9]-data[:,7]
fout=open('lte.dat',"w+")
print("x H(eV/atom) G(eV/atom) Tsc(eV/atom)",file=fout)
for k in range(xlte.size):
    print(xlte[k],Hlte[k],Glte[k],TSclte[k],file=fout)
fout.close()

#mc w/ sro
xmc=(1+data[:,3])/2
Gmc=data[:,4]+data[:,1]*data[:,3] - (1-xmc)*E0 - xmc*E1
Hmc=data[:,2]+data[:,1]*data[:,3] - (1-xmc)*E0 - xmc*E1
TScmc=data[:,4]-data[:,2]
fout=open('mc-sro.dat',"w+")
print("x H(eV/atom) G(eV/atom) TSc(eV/atom)",file=fout)
for k in range(xmc.size):
    print(xmc[k],Hmc[k],Gmc[k],TScmc[k],file=fout)
fout.close()

TSc_ideal=8.61733326E-5*data[0,0]*(xmc*np.log(xmc)+(1-xmc)*np.log(1-xmc))

if(args.plot):
    plt.figure(figsize=(6,9))
    plt.rcParams.update({'font.size': 12})
    plt.subplot(3,1,1)
    plt.plot(xmc, Hmc,label='mc w/ sro')
    plt.plot(xhte, Hhte,label='high-temp. expans.')
    #plt.plot(xlte, Hlte,label='lte')
    plt.ylabel('$H_{mix}$ (eV/atom)')
    plt.legend()

    plt.subplot(3,1,2)
    plt.plot(xmc, Gmc,label='mc (w/ sro)')
    plt.plot(xhte, Ghte,label='hte')
    #plt.plot(xlte, Glte,label='lte')
    plt.ylabel('G (eV/atom)')
    plt.legend()
   
    plt.subplot(3,1,3)
    plt.plot(xmc, TScmc,label='mc w/ sro')
    plt.plot(xhte, TSchte,label='hte')
    plt.plot(xmc, TSc_ideal,ls="dashed",label='ideal',c='k')
    #plt.plot(xlte, TSclte,label='lte')
    plt.xlabel('x'); plt.ylabel(r'$-TS_{conf}$ (eV/atom)')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

