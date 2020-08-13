#!/usr/bin/env python3

import numpy as np
import sys
import argparse
import pylab as plt

parser = argparse.ArgumentParser()
parser.add_argument("-p","--pdos", help="seperated projected dos",action='store')
parser.add_argument("-d","--degenerate", help="plot each orbital", action='store_true')

args = parser.parse_args()

# fe pdos
data=np.loadtxt(args.pdos,skiprows=1)
E=data[:,0]
t2g_up=data[:,9]+data[:,11]+data[:,15]
t2g_dn=data[:,10]+data[:,12]+data[:,16]
eg_up=data[:,13]+data[:,17]
eg_dn=data[:,14]+data[:,18]

plt.figure(figsize=(8,3.3))
plt.rcParams.update({'font.size': 14})
plt.axhline(0,ls='--',color='k',lw=0.5)
plt.plot(E, t2g_up,label=r"$t_{2g}$",c='r')
plt.plot(E,t2g_dn,c='r')
plt.plot(E, eg_up,label=r"$e_{g}$",c='b')
plt.plot(E,eg_dn,c='b')
plt.axvline(0,ls='--',color='k',lw=0.5)
plt.legend()
plt.xlim(-12,5)
plt.xlabel(r"$E-E_f\ (eV)$")
plt.ylabel(r"ProjDOS")
plt.tight_layout()
plt.savefig("pdos.png")
plt.close()

if (args.degenerate):
    plt.figure(figsize=(8,7))
    plt.rcParams.update({'font.size': 14})
    plt.subplot(2,1,1)
    plt.axhline(0,ls='--',color='k',lw=0.5)
    plt.axvline(0,ls='--',color='k',lw=0.5)
    plt.plot(E,data[:,13] ,label=r"$z^2$",c='b')
    plt.plot(E,data[:,14] ,c='b')
    plt.plot(E,data[:,17] ,ls='--',label=r"$x^2-y^2$",c='r')
    plt.plot(E,data[:,18],ls='--',c='r')
    plt.legend()
    plt.xlim(-12,5)
    plt.ylabel(r"ProjDOS")
   

    plt.subplot(2,1,2)
    plt.axhline(0,ls='--',color='k',lw=0.5)
    plt.axvline(0,ls='--',color='k',lw=0.5)
    plt.plot(E,data[:,15] ,marker='x',label=r"$zx$",c='b')
    plt.plot(E,data[:,16] ,marker='x',c='b')
    plt.plot(E,data[:,11] ,label=r"$zy$",c='g')
    plt.plot(E,data[:,12] ,c='g')
    plt.plot(E,data[:,9] ,ls=':',label=r"$xy$",c='r')
    plt.plot(E,data[:,10] ,ls=':',c='r')
    plt.legend()
    plt.xlim(-12,5)
    plt.xlabel(r"$E-E_f\ (eV)$")
    plt.ylabel(r"ProjDOS")
    plt.tight_layout()
    plt.savefig("3d.png")
    plt.close()

