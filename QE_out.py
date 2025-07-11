#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input", help="input file of QE results",action='store')
parser.add_argument("-c","--cell", help="per cell", action='store_true')
parser.add_argument("-s","--simple", help="EV only", action='store_true')
parser.add_argument("-n","--notitle", help="no title", action='store_true')
parser.add_argument("-y","--hybrid", help="hybrid functional", action='store_true')
args = parser.parse_args()

def read_QE(fin, vol0, cal_tag):
    vol='NA';press='NA';  pxx=[]; 
    tot_mag='NA'; ab_mag='NA'; ene='NA'; force='NA';
    new_tag=cal_tag
    if(args.hybrid):
        for line in fin:
           if("!!   total energy" in line):
             ll=line.split()
             ene="%.6f"%(float(ll[-2])*Ry2eV/natom) # Ry -> eV/atom
    #         print(ll[-2],Ry2eV, natom,ene)
           elif("P=" in line):
             ll=line.split()
             press=float(ll[-1].strip("P=")) # kBar
             for k in range(3):
                 ll=fin.readline().split()
                 pxx.append(ll[k+3])
           elif("total magnetization" in line):
             ll=line.split()
             tot_mag=ll[3] # uB 
           elif("absolute magnetization" in line):
             ll=line.split()
             ab_mag=ll[3] # uB
           elif('Forces acting on atoms' in line):
             tag=1
             fin.readline()
             for line in fin:
                 if("atom" not in line):
                     break
                 ll=line.split()
                 for k in range(6,9):
                     if( abs(float(ll[k])*(Ry2eV/au2ang)) > 0.01):
                         tag=0
             if(tag==1):force="T"
             else: force="F"
           elif("new unit-cell volume" in line):
               ll=line.split()
               vol=float(ll[-3])
           elif(("convergence has been achieved" in line) and cal_tag=="scf"):
               #break
               continue
           elif(("convergence has been achieved" in line) and cal_tag=="Str_Opt"):
               continue
           elif("output data" in line):
               break
           elif("End of BFGS Geometry Optimization" in line):
               new_tag="Str_Opt_end"
    else:
        for line in fin:
           if("!    total energy" in line):
             ll=line.split()
             ene="%.6f"%(float(ll[-2])*Ry2eV/natom) # Ry -> eV/atom
    #         print(ll[-2],Ry2eV, natom,ene)
           elif("P=" in line):
             ll=line.split()
             press=float(ll[-1].strip("P=")) # kBar
             for k in range(3):
                 ll=fin.readline().split()
                 pxx.append(ll[k+3])
           elif("total magnetization" in line):
             ll=line.split()
             tot_mag=ll[3] # uB 
           elif("absolute magnetization" in line):
             ll=line.split()
             ab_mag=ll[3] # uB
           elif('Forces acting on atoms' in line):
             tag=1
             fin.readline()
             for line in fin:
                 if("atom" not in line):
                     break
                 ll=line.split()
                 for k in range(6,9):
                     if( abs(float(ll[k])*(Ry2eV/au2ang)) > 0.01):
                         tag=0
             if(tag==1):force="T"
             else: force="F"
           elif("new unit-cell volume" in line):
               ll=line.split()
               vol=float(ll[-3])
           elif(("convergence has been achieved" in line) and cal_tag=="scf"):
               #break
               continue
           elif(("convergence has been achieved" in line) and cal_tag=="Str_Opt"):
               continue
           elif("output data" in line):  # for QE7, in QE6 this should be "Writing output data"
               break
           elif("End of BFGS Geometry Optimization" in line):
               new_tag="Str_Opt_end"
    if(vol=="NA"):
        vol=vol0
    return new_tag, vol, ene, press, pxx, tot_mag, ab_mag, force

fin=open(args.input,"r")

Ry2eV=13.6056980659  # 1 Rydberg constant = 13.6056980659 eV
eV2Ry=1/Ry2eV # 1 eV = 0.0734986176 Rydberg constant
au2ang=0.529177249 # 1 a.u., b = 0.529177249 A
ang2au=1/au2ang

natom=0
line=0

if(not args.notitle):
    if(args.cell):
        if(args.simple):
            print("V(A^3/cell) E(eV/cell)")
        else:
            print("#cal_type V(A^3/cell) E(eV/cell) press(kBar) (Pxx Pyy Pzz) Mag_tot(uB/cell) Mag_ab(uB/cell) Force(all<0.01eV/A)")
    else:
        if(args.simple):
            print("V(A^3/atom) E(eV/atom)")
        else:
            print("#cal_type V(A^3/atom) E(eV/atom) press(kBar) (Pxx Pyy Pzz) Mag_tot(uB/cell) Mag_ab(uB/cell) Force(all<0.01eV/A)")

cal_type="scf"
for line in fin:
    if("number of atoms/cell" in line):
        ll=line.split()
        natom=int(ll[-1])
    if("   unit-cell volume" in line):
        ll=line.split()
        vol=float(ll[-2])*au2ang**3
    if("Geometry Optimization" in line):
        cal_type="Str_Opt"
    if("Fermi energ" in line or "highest occupied" in line):
        new_type, vol, ene, press, pxx, tot_mag, ab_mag, force=read_QE(fin,vol,cal_type)
        if(args.cell):
            ene_pc="%.6f"%(float(ene)*natom) 
            if(args.simple):
                print(vol,ene_pc)
            else:
                print(new_type,vol,ene_pc,press,'(',*pxx,')', tot_mag, ab_mag, force)
        else:
            if(args.simple):
                print(vol/natom,ene)
            else:
                print(new_type,vol/natom,ene,press,'(',*pxx,')', tot_mag, ab_mag, force)
        if(new_type=="Str_Opt_end"):
            cal_type="scf"



#for line in fin:
#  if("number of atoms/cell" in line):
#    ll=line.split()
#    natom=int(ll[-1])
#  if("   unit-cell volume" in line):
#    ll=line.split()
#    vol=float(ll[-2])*au2ang**3
#  if("!    total energy" in line):
#    press='NA';  pxx=[]; 
#    tot_mag='NA'; ab_mag='NA'; ene='NA'; force='NA';
#    ll=line.split()
#    ene="%.6f"%(float(ll[-2])*Ry2eV/natom) # Ry -> eV/atom
#    for line in fin:
#      if("P=" in line):
#        ll=line.split()
#        press=float(ll[-1]) # kBar
#        for k in range(3):
#            ll=fin.readline().split()
#            pxx.append(ll[k+3])
#      if("total magnetization" in line):
#        ll=line.split()
#        tot_mag=ll[3] # uB 
#      if("absolute magnetization" in line):
#        ll=line.split()
#        ab_mag=ll[3] # uB
#      if('Forces acting on atoms' in line):
#        tag=1
#        fin.readline()
#        for line in fin:
#            if("atom" not in line):
#                break
#            ll=line.split()
#            for k in range(6,9):
#                if( abs(float(ll[k])*(Ry2eV/au2ang)) > 0.01):
#                    tag=0
#        if(tag==1):force="T"
#        else: force="F"
#      if("new unit-cell volume" in line):
#          ll=line.split()
#          vol=float(ll[-3])
#      if("Writing output data" in line):
#        print(vol/natom,ene,press,'(',*pxx,')', tot_mag, ab_mag, force)
#        break
