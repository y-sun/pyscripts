#!/usr/bin/env python3

import numpy as np
import sys
import argparse
import pylab as plt

parser = argparse.ArgumentParser()
parser.add_argument("-s","--scf", help="input file of SCF results",action='store')
parser.add_argument("-p","--pdos", help="input file of projected dos",action='store')
parser.add_argument("-d","--degenerate", help="plot each orbital", action='store_true')
parser.add_argument("-t","--transform", help="swap xy <-> x2-y2", action='store_true')
parser.add_argument("-o","--output", help="output raw data", action='store_true')
parser.add_argument("-x","--xlim", help="x range", nargs='*',action='store')
parser.add_argument("-y","--ylim", help="y range", nargs='*',action='store')

args = parser.parse_args()

#get Ef 
fscf=open(args.scf,"r")
for line in fscf:
    if("the Fermi energy is" in line):
        Ef=float(line.split()[-2])
    if("highest occupied level " in line):
        Ef=float(line.split()[-1])
    if("total magnetization" in line):
        mag=line.split()[-3]
fscf.close()

# fe pdos
data=np.loadtxt(args.pdos,skiprows=1)
E=data[:,0]-Ef
if(args.transform):
    t2g_up=data[:,5]+data[:,7]+data[:,9] # 5 zx, 7 zy, 9 xy
    t2g_dn=data[:,6]+data[:,8]+data[:,10]
    eg_up=data[:,3]+data[:,11]     # 3 z2 11 x2-y2
    eg_dn=data[:,4]+data[:,12]
else:
    t2g_up=data[:,5]+data[:,7]+data[:,11] # 5 zx, 7 zy, 11 xy
    t2g_dn=data[:,6]+data[:,8]+data[:,12]
    eg_up=data[:,3]+data[:,9]     # 3 z2 9 x2-y2
    eg_dn=data[:,4]+data[:,10]

plt.figure(figsize=(8,3.3))
plt.rcParams.update({'font.size': 14})
plt.axhline(0,ls='--',color='k',lw=0.5)
plt.plot(E, t2g_up,label=r"$t_{2g}$",c='r')
plt.plot(E,-t2g_dn,c='r')
plt.plot(E, eg_up,label=r"$e_{g}$",c='b')
plt.plot(E,-eg_dn,c='b')
plt.axvline(0,ls='--',color='k',lw=0.5)
plt.legend()
if(args.xlim is None):
    plt.xlim(-12,5)
else:
    plt.xlim(float(args.xlim[0]),float(args.xlim[1]))
if(args.ylim is not None):
    plt.ylim(float(args.ylim[0]),float(args.ylim[1]))
plt.xlabel(r"$E-E_f\ (eV)$")
plt.ylabel(r"ProjDOS")
plt.title("M= "+mag+r" $\mu_B$")
plt.tight_layout()
plt.savefig("pdos.png")
plt.close()

if(args.output):
    fout=open("pdos.t2g_eg.dat","w+")
    print("E-Ef(eV) t2g_up t2g_dn eg_up eg_dn",file=fout)
    for k in range(E.size):
        print(E[k],t2g_up[k],t2g_dn[k],eg_up[k],eg_dn[k],file=fout)
    fout.close()

    fout=open("pdos.d_orbitals.dat","w+")
    print("E-Ef(eV) z2_up z2_dn x2-y2_up x2-y2_dn zx_up zx_dn zy_up zy_dn xy_up xy_dn",file=fout)
    for k in range(E.size):
        print(E[k],data[k,3],data[k,4],data[k,9],data[k,10],
                data[k,5],data[k,6],data[k,7],data[k,8],data[k,11],data[k,12],file=fout)
    fout.close()


if (args.degenerate):
    plt.figure(figsize=(8,7))
    plt.rcParams.update({'font.size': 14})
    plt.subplot(2,1,1)
    plt.axhline(0,ls='--',color='k',lw=0.5)
    plt.axvline(0,ls='--',color='k',lw=0.5)
    plt.plot(E, data[:,3] ,label=r"$z^2$",c='b')
    plt.plot(E,-data[:,4] ,c='b')
    if(args.transform):
        plt.plot(E, data[:,11] ,ls='--',label=r"$x^2-y^2$",c='r')
        plt.plot(E,-data[:,12],ls='--',c='r')
    else: 
        plt.plot(E, data[:,9] ,ls='--',label=r"$x^2-y^2$",c='r')
        plt.plot(E,-data[:,10],ls='--',c='r')
    plt.legend()
    if(args.xlim is None):
        plt.xlim(-12,5)
    else:
        plt.xlim(float(args.xlim[0]),float(args.xlim[1]))
    if(args.ylim is not None):
        plt.ylim(float(args.ylim[0]),float(args.ylim[1]))
    plt.ylabel(r"ProjDOS")
   

    plt.subplot(2,1,2)
    plt.axhline(0,ls='--',color='k',lw=0.5)
    plt.axvline(0,ls='--',color='k',lw=0.5)
    plt.plot(E, data[:,5] ,marker='x',label=r"$zx$",c='b')
    plt.plot(E,-data[:,6] ,marker='x',c='b')
    plt.plot(E, data[:,7] ,label=r"$zy$",c='g')
    plt.plot(E,-data[:,8] ,c='g')
    if(args.transform):
        plt.plot(E, data[:,9] ,ls='--',label=r"$xy$",c='r')
        plt.plot(E,-data[:,10] ,ls='--',c='r')
    else:
        plt.plot(E, data[:,11] ,ls='--',label=r"$xy$",c='r')
        plt.plot(E,-data[:,12] ,ls='--',c='r')
    plt.legend()
    if(args.xlim is None):
        plt.xlim(-12,5)
    else:
        plt.xlim(float(args.xlim[0]),float(args.xlim[1]))
    if(args.ylim is not None):
        plt.ylim(float(args.ylim[0]),float(args.ylim[1]))
    plt.xlabel(r"$E-E_f\ (eV)$")
    plt.ylabel(r"ProjDOS")
    plt.tight_layout()
    plt.savefig("3d.png")
    plt.close()

