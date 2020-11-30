#!/usr/bin/env python3

import pylab as plt
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-i","--input", help="input lammps out file",action='store')
parser.add_argument("-e","--every", help="output data every this step",action='store')
parser.add_argument("-j","--jump", help="jump this steps", action='store')
parser.add_argument("-p","--plot", help="plot", action='store_true')
args = parser.parse_args()

fin=open(args.input, "r")

natom=5000; timestep=0.0025
njump=int(args.jump)
for i in range( njump ):
   line=fin.readline()
   if('Time step' in line):
      timestep= float( line.split()[3] )
   if('atoms' in line):
      if('group' in line):
         continue
      try:
         int(line.split()[0])
      except ValueError:
         continue
      else:
         natom=int(line.split()[0])
print(njump, "steps jumped")

for line in fin:
   if('Time step' in line):
      timestep= float( line.split()[3] )
   if('atoms' in line):
      if('group' in line):
         continue
      try:
         int(line.split()[0])
      except ValueError:
         continue
      else:
         natom=int(line.split()[0])
   if('Step Temp' in line):
      l_arg=line.split()
      break
print("natom",natom, "timestep",timestep)
if (natom==''):
   print("can not find 'atom number'")
   exit()
if (l_arg==''):
   print("cannot find 'Step Temp'")
   exit()
if (timestep==''):
   print("cannot find 'Time step'")
   exit()

step=[]; temp=[]; Et=[]; Ep=[]; Ek=[]; press=[]; Etp=[]; Esp=[]
xbox=[]; vol=[]; msd=[]; msd1=[]; msd2=[]; Pxx=[]; Pyy=[]; Pzz=[]
dic={'Step':step, 'Temp':temp, 'TotEng':Et, 'PotEng':Ep,
      'KinEng':Ek, 'Press':press, 'Enthalpy':Etp, 'spring':Esp, 'spring0':Esp,
      'Lx':xbox, 'Volume':vol, 'msd[4]':msd,  'c_msd[4]':msd,'c_msdNi[4]':msd1,
      'c_msdZr[4]':msd2,'c_msd1[4]':msd1, 'c_msd2[4]':msd2, 'msd1[4]':msd1, 'msd2[4]':msd2,
      'Pxx':Pxx, 'Pyy':Pyy, 'Pzz':Pzz}

for line in fin:
   if("Loop" in line):
      break
   ll=line.split()
   if(len(ll) != len(l_arg)):
      break
   try:
      int(ll[0])
   except ValueError:
      break
   for j in range( len(l_arg) ):
      if( l_arg[j] in dic):
         dic[ l_arg[j] ].append(ll[j])
fin.close()

if(len(Ep) == 0):
   print('cannot find PotEng')
   exit() 

fout=open("Ep.dat","w+")
print("#time Ep Ep-3/2kBT Esp(optional)",file=fout)
step0=float(step[0])
nevery=int(args.every)
time=[]
Ep_kbt=[]; Ep_a=[]
for i in range( len(Ep) ):
   time.append((float(step[i])-step0)*timestep*0.001) # ns
   Ep_kbt.append( float(Ep[i])/natom - 1.5*8.617*0.00001*float(temp[i]) )
   Ep_a.append( float(Ep[i])/natom )
   if( i%nevery==0 ):
      if(len(Esp)!=0):
         print( time[i], Ep_a[i], Ep_kbt[i], Esp[i], file=fout)
      else:
         print( time[i], Ep_a[i], Ep_kbt[i],file=fout)
fout.close()

# summary
E_init =  sum(Ep_kbt[i] for i in range(10)) / 10
if(len(xbox)!=0):
   bsum=0
   for bb in xbox:
      bsum += float(bb)
   print("boxsize x:", bsum/len(xbox))

if(len(vol)!=0):
   vsum=0
   for i in range(len(vol)):
      vol[i]=float(vol[i])
   print("volume:", np.mean(np.array(vol)),np.std(np.array(vol)))
   print("rho:", natom/np.mean(np.array(vol)))
Esum=0
for eee in Ep_a:
   Esum += eee
print("Ep_total:", Esum/len(Ep_a))
Hsum=0
for hhh in Etp:
   Hsum += float(hhh)
print("Enthalpy_ave:", Hsum/len(Etp)/natom)
print("# of steps:",len(Ep))

if(args.plot):
   fig1=plt.figure( figsize=(8,6) )
   plt.plot(time,Ep_kbt)
   plt.xlabel('time (ns)', fontsize=24)
   plt.ylabel('Ep-3/2*kB*T (ev/atom)', fontsize=24)
   plt.xticks(fontsize=22)
   plt.yticks(fontsize=22)
   plt.title(args.input,fontsize=22)
   current_plt=plt.gca()
   current_plt.get_yaxis().get_major_formatter().set_useOffset(False)
   plt.tight_layout()
   plt.savefig("pe-kBT.png")
   
   fig666=plt.figure( figsize=(8,6) )
   plt.plot(time,Ep_a)
   plt.xlabel('time (ns)', fontsize=24)
   plt.ylabel('Ep (ev/atom)', fontsize=24)
   plt.xticks(fontsize=22)
   plt.yticks(fontsize=22)
   plt.title(args.input,fontsize=22)
   current_plt=plt.gca()
   current_plt.get_yaxis().get_major_formatter().set_useOffset(False)
   plt.tight_layout()
   plt.savefig("pe.png")
   
   #msd
   if( len(msd) != 0 ):
      fig2=plt.figure()
      fout=open("msd.dat","w+")
      print("#time(ps) msd(A^2)",file=fout)
      for i in range(len(msd)):
         msd[i]=float(msd[i])
         time[i] *= 1000
         print( time[i], msd[i],file=fout) #ps
      fout.close()
      fit_a,fit_b=np.polyfit(time,msd,1)
      print("diffusivity_D:",fit_a/6," A^2/ps")
      plt.plot(time,msd,'.')
      fitted_x=[0,time[len(time)-1]]
      fitted_y=[0*fit_a+fit_b,time[len(time)-1]*fit_a+fit_b]
      plt.plot(fitted_x,fitted_y,'-')
      plt.savefig('msd.png')
   # msd 1& 2
   if( len(msd1) != 0 and len(msd2)!= 0 ):
      fig2=plt.figure()
      fout=open("msd.dat","w+")
      print("#time(ps) msd(A^2)",file=fout)
      for i in range(len(msd1)):
         msd1[i]=float(msd1[i])
         msd2[i]=float(msd2[i])
         time[i] *= 1000
         print( time[i], msd1[i], msd2[i],file=fout) #ps
      fout.close()
      fit_a1,fit_b1=np.polyfit(time,msd1,1)
      fit_a2,fit_b2=np.polyfit(time,msd2,1)
      print("diffusivity_D:",fit_a1/6, fit_a2/6," A^2/ps")
      plt.plot(time,msd1,'.',color='r')
      plt.plot(time,msd2,'.',color='blue')
      fitted_x=[0,time[len(time)-1]]
      fitted_y=[0*fit_a1+fit_b1,time[len(time)-1]*fit_a1+fit_b1]
      plt.plot(fitted_x,fitted_y,'-',color='r',label='1')
      fitted_y=[0*fit_a2+fit_b2,time[len(time)-1]*fit_a2+fit_b2]
      plt.plot(fitted_x,fitted_y,'-',color='blue',label='2')
      plt.legend()
      plt.savefig('msd.png')
   if( len(vol) !=0 ):
      fout=open("vol.dat","w+")
      for i in range(len(vol)):
         print(time[i], vol[i], file=fout)
      fout.close()
   
   #pressure
   if( len(press) != 0 ):
      fig3=plt.figure()
      for i in range(len(press)):
         press[i]=float(press[i])
      plt.plot(time,press,'.')
      plt.savefig('pressure.png')
   
   if( len(Pxx) != 0 ):
      fout=open("stress.dat","w+")
      for i in range(len(time)):
         print(time[i],Pxx[i],Pyy[i],Pzz[i],file=fout)
      fout.close()
