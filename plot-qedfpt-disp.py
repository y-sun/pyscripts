#!/usr/bin/env python3

import glob
import numpy as np
import pylab as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d","--disp", help="dispersions", nargs='*',action='store')
parser.add_argument("-k","--kp", help="k points", nargs='*',action='store')
parser.add_argument("-l","--legend", help="legends", nargs='*',action='store')
parser.add_argument("-y","--ylim", help="yrange", nargs='*',action='store')
parser.add_argument("-n","--number", help="number of spacing",action='store')
parser.add_argument("-t","--title", help="plot title",action='store')
parser.add_argument("-r","--rainbow", help="rainbow as color", action='store_true')
parser.add_argument("-m","--match", help="match with the first coordinate", action='store_true')
args = parser.parse_args()

#nspacing=50; kpoints=['G','X','W','K','G','L']
nspacing=int(args.number); kpoints=args.kp

#fls=sorted(glob.glob("*/qedfpt444/merge-dyns/disp.freq.gp"))
#fls=["./disp.freq.gp","../disp.freq.gp"]
fls=args.disp
plt.figure(figsize=(8,6))
plt.rcParams.update({'font.size': 14})


#fin=open("v2p.dat")
#vp={}
#for line in fin:
#    ll=line.split()
#    vp.update({ll[0]:ll[1]})
if(args.legend is None):
    names=args.disp
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
    data=np.loadtxt(ifl)
    if(ct==0 and args.match):
        xm=data[:,0]

    if(args.match):
        for k in range(1,data.shape[1]):
            if(k==1):
                plt.plot(xm,data[:,k]*0.02998,linestyle=lshp[ct],color=colors[ct],label=names[ct])
            else:
                plt.plot(xm,data[:,k]*0.02998,linestyle=lshp[ct],color=colors[ct])
    else:
        for k in range(1,data.shape[1]):
            if(k==1):
                plt.plot(data[:,0],data[:,k]*0.02998,linestyle=lshp[ct],color=colors[ct],label=names[ct])
            else:
                plt.plot(data[:,0],data[:,k]*0.02998,linestyle=lshp[ct],color=colors[ct])
    ct+=1

data=np.loadtxt(fls[0])
ndata=data.shape[0]
nv=int((ndata-1)/nspacing+0.5)
vx=[data[k*nspacing][0] for k in range(1,nv)]

for iv in vx:
    plt.axvline(iv,color='k',lw=0.5)
plt.axhline(0,color='k',lw=0.5)

plt.xlim(data[0][0],data[-1][0])

a=[data[0][0]]; b=[data[-1][0]]
xlb=a+vx+b
ax = plt.subplot(111)
ax.set_xticks(xlb)
ax.set_xticklabels(kpoints)
#plt.ylabel(r"Frequency (cm$^{-1}$)")
plt.ylabel(r"Frequency (THz)")
if(len(fls) > 4):
    plt.legend(ncol=2,prop={'size': 12}) #bbox_to_anchor=(1, .95))
else:
    #plt.legend() 
    plt.legend(loc="upper left")
if(args.title is not None): 
    plt.title(args.title)
if(args.ylim is not None):
    ymin=float(args.ylim[0])
    ymax=float(args.ylim[1])
    plt.ylim(ymin,ymax)
plt.tight_layout()
plt.savefig("total-dispersion.png")
plt.show()
