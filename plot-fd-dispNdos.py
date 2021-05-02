#!/usr/bin/env python3

import glob
import numpy as np
import pylab as plt
from matplotlib import gridspec

#nspacing=50; kpoints=['G','X','M','G','Z','R','A','Z']
nspacing=51; kpoints=['G','H','N','P','G','N']

plt.figure(figsize=(10,6))
plt.rcParams.update({'font.size': 16})
cm2Thz=0.02998
yrange=[-15,30]

gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1]) 

# dispersion
ax0=plt.subplot(gs[0])
data=np.loadtxt("band.dat.gp")
data[:,0]=data[:,0]/data[-1][0]
colors=plt.cm.rainbow(np.linspace(0,1,data.shape[1]))
for k in range(1,data.shape[1]):
    if(k==1):
        ax0.plot(data[:,0],data[:,k]*cm2Thz,lw=2.0,color=colors[k])
    else:
        ax0.plot(data[:,0],data[:,k]*cm2Thz,lw=2.0,color=colors[k])

ndata=data.shape[0]
nv=int((ndata-1)/nspacing+0.5)
vx=[data[k*nspacing][0] for k in range(1,nv)]
for iv in vx:
    ax0.axvline(iv,color='k',lw=0.5)
ax0.axhline(0,color='k',lw=0.5)
ax0.set_xlim(data[0][0],data[-1][0])
a=[data[0][0]]; b=[data[-1][0]]
xlb=a+vx+b
ax0.set_xticks(xlb)
ax0.set_xticklabels(kpoints)
ax0.set_ylim(yrange)
ax0.set_xlabel(r'Wave Vector')
ax0.set_ylabel(r"Frequency (THz)")
#ax0.legend(ncol=2,prop={'size': 14})

ax1=plt.subplot(gs[1])
data=np.loadtxt("total_dos.dat",skiprows=1)
data_partial=np.loadtxt("projected_dos.dat",skiprows=1)
ax1.plot(data[:,1],data[:,0],c='k',label='total')
ax1.plot(data_partial[:,1],data_partial[:,0],c='r',label='Fe')
ax1.plot(data_partial[:,2],data_partial[:,0],c='g',label='O')
#ax1.plot(data[:,5]/cm2Thz,data[:,0]*cm2Thz,c='c',label='O_2')
ax1.set_ylim(yrange); #ax1.set_xlim(left=0.0)
ax1.yaxis.tick_right()
ax1.set_xlabel(r'PhDoS(THz$^{-1}$)')
ax1.legend()

plt.tight_layout()
#plt.title(r"FeO-B2,AFM,V$_3$")
plt.savefig("dispNdos.png")
plt.show()
