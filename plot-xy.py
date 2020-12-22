#!/usr/bin/env python3

import glob
import numpy as np
import pylab as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--inputs", help="input files", nargs='*',action='store')
parser.add_argument("-l","--legend", help="legends", nargs='*',action='store')
parser.add_argument("-s","--range", help="span", nargs='*',action='store')
parser.add_argument("-t","--title", help="plot title",action='store')
parser.add_argument("-j","--jump", help="skip rows",action='store')
parser.add_argument("-r","--rainbow", help="rainbow as color", action='store_true')
parser.add_argument("-n","--noshow", help="not shown interactively", action='store_true')
parser.add_argument("-x","--xlabel", help="x label name",action='store')
parser.add_argument("-y","--ylabel", help="y label name",action='store')

args = parser.parse_args()

fls=args.inputs
plt.figure(figsize=(8,6))
plt.rcParams.update({'font.size': 14})

if(args.legend is None):
    names=args.inputs
else:
    names=args.legend
if(args.rainbow):
    colors=plt.cm.rainbow(np.linspace(0,1,len(fls)))
    lshp=['-' for k in range(100)]
else:
    lshp=['-','--',':','-.']
    colors=['k','r','b','g','c','m']
cm2Thz=0.02998

ct=0
for ifl in fls:
    name=ifl.split("/")[0]
    data=np.loadtxt(ifl,skiprows=int(args.jump))
    plt.plot(data[:,0],data[:,1],linestyle=lshp[ct],color=colors[ct],label=names[ct])
    ct+=1

if(len(fls) > 4):
    plt.legend(ncol=2,prop={'size': 12}) #bbox_to_anchor=(1, .95))
else:
    plt.legend()
if(args.title is not None): 
    plt.title(args.title)
if(args.xlabel is not None):
    plt.xlabel(args.xlabel)
if(args.ylabel is not None):
    plt.ylabel(args.ylabel)
if(len(args.range) != 0):
    plt.xlim(float(args.range[0]),float(args.range[1]))
plt.tight_layout()
plt.savefig("fig.png")
if(not args.noshow):
    plt.show()
