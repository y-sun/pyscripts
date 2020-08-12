#!/usr/bin/env python3

import pylab as plt
import argparse
import numpy as np
parser = argparse.ArgumentParser()
parser.add_argument("-i","--infile", help="input file",action='store')
parser.add_argument("-p","--plot", help="plot", action='store_true')
parser.add_argument("-a","--allstress", help="also plot off-diagnal stress tensor", action='store_true')
parser.add_argument("-o","--output", help="output", action='store_true')
args = parser.parse_args()

fin=open(args.infile,"r")

pa=0; ct=0
print("#istep P(GPa) P(kbar) Etot(eV)")
pxx=[]; pyy=[]; pzz=[] ;  pxy=[]; pyz=[]; pzx=[]
ee=[]; step=[]
for line in fin:
   if("Total+kin" in line):
      ll=line.split()
      px=float(ll[1]); py=float(ll[2]); pz=float(ll[3])
      ipxy=float(ll[4]); ipyz=float(ll[5]); ipzx=float(ll[6])
      pa += (px+py+pz)/3
      ct += 1
      E=999999
      for line in fin:
          if("entropy=" in line):
              E=float(line.split()[3])
              break
      print(ct,"%.3f"%((px+py+pz)/3*0.1), "%.3f"%((px+py+pz)/3), E)
      pxx.append(px*0.1); pyy.append(py*0.1); pzz.append(pz*0.1)
      pxy.append(ipxy*0.1); pyz.append(ipyz*0.1); pzx.append(ipzx*0.1)
      ee.append(E); step.append(ct)

px_ave=np.mean(pxx); py_ave=np.mean(pyy); pz_ave=np.mean(pzz)
print("steps pave(GPa) pxx pyy pzz")
print(len(pxx), (px_ave+py_ave+pz_ave)/3, px_ave, py_ave, pz_ave)

if(args.plot and args.allstress):
    plt.figure(figsize=(6,8))
    plt.rcParams.update({'font.size': 12})
    plt.subplot(3,1,1)
    plt.plot(step,pxx,label='pxx')
    plt.plot(step,pyy,label='pyy')
    plt.plot(step,pzz,label='pzz')
    plt.ylabel("P (GPa)")
    plt.legend()

    plt.subplot(3,1,2)
    plt.plot(step,pxy,label='pxy')
    plt.plot(step,pyz,label='pyz')
    plt.plot(step,pzx,label='pzx')
    plt.ylabel("P (GPa)")
    plt.legend()

    plt.subplot(3,1,3)
    plt.plot(step,ee,label='total energy')
    plt.ylabel("E (eV)")
    plt.xlabel("MD step")
    plt.legend()

    plt.tight_layout()
    plt.savefig('pande.png')

elif(args.plot):
    plt.figure(figsize=(6,8))
    plt.rcParams.update({'font.size': 12})
    plt.subplot(2,1,1)
    plt.plot(step,pxx,label='pxx')
    plt.plot(step,pyy,label='pyy')
    plt.plot(step,pzz,label='pzz')
    plt.ylabel("P (GPa)")
    plt.legend()

    plt.subplot(2,1,2)
    plt.plot(step,ee,label='total energy')
    plt.ylabel("E (eV)")
    plt.xlabel("MD step")
    plt.legend()

    plt.tight_layout()
    plt.savefig('pande.png')
    #plt.show()

if(args.output):
    fout=open("pande.dat","w+")
    if(args.allstress):
        print("#MDstep p(GPa) E(eV) pxx pyy pzz pxy pyz pzx",file=fout)
        for k in range(len(ee)):
            print(step[k],(pxx[k]+pyy[k]+pzz[k])/3,ee[k],
                pxx[k],pyy[k],pzz[k],pxy[k],pyz[k],pzx[k],file=fout)
    else:
        print("#MDstep p(GPa) E(eV) pxx pyy pzz",file=fout)
        for k in range(len(ee)):
            print(step[k],(pxx[k]+pyy[k]+pzz[k])/3,ee[k],
                pxx[k],pyy[k],pzz[k],file=fout)
    fout.close()
