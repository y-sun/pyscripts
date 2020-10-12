#!/usr/bin/env python3

# nspin = 1 case
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input", help="input file of SCF",action='store')
parser.add_argument("-m","--mag", help="nspin 1 or 2",action='store')
args = parser.parse_args()

fin=open(args.input,"r")
fout=open('soc.in',"w+")

if(args.mag=="1"):
    for line in fin:
        if("nspin" in line):
            print("! ",line.strip("\n"),file=fout)
        elif("lda_plus_u_kind" in line):
            print("lda_plus_u_kind = 1, lspinorb = .true. , noncolin = .true.",file=fout)
        elif("Hubbard_U" in line):
            U=float(line.split()[-1])
            uid=line.split("(")[1].split(")")[0]
            print("Hubbard_U(%s) = %8.4f, Hubbard_J0(%s) = 0.9,"%(uid, U+0.9, uid),file=fout)
        elif("pseudo_dir" in line):
            print("pseudo_dir = \'/home/yangsun/QE-PSEUDO/pslibrary/rel-pz/PSEUDOPOTENTIALS\'",file=fout)
        elif("occupations" in line):
            print("occupations=\'fixed\',",file=fout)
        elif("mixing_beta" in line):
            print("mixing_beta = 0.3",file=fout)
        elif("UPF" in line):
            ll=line.split()
            PP=ll[-1]; sep=PP.split(".")
            newPP=sep[0]+".rel-"+sep[1]+"."+sep[2]+"."+sep[3]+"."+sep[4]+"."+sep[5]
            print(ll[0],ll[1],newPP,file=fout)
        else:
            print(line.strip("\n"),file=fout)
elif(args.mag=="2"):
    for line in fin:
        if("nspin" in line):
            print("nspin = 4, starting_magnetization(1)=4.0, starting_magnetization(2)=4.0, starting_magnetization(3)=4.0 ",file=fout)
        elif("lda_plus_u_kind" in line):
            print("lda_plus_u_kind = 1, lspinorb = .true. , noncolin = .true.",file=fout)
        elif("Hubbard_U" in line):
            U=float(line.split()[-1])
            uid=line.split("(")[1].split(")")[0]
            print("Hubbard_U(%s) = %8.4f, Hubbard_J0(%s) = 0.9, starting_ns_eigenvalue(3,1,%s)=1.0"%(uid, U+0.9, uid,uid),file=fout)
        elif("pseudo_dir" in line):
            print("pseudo_dir = \'/home/yangsun/QE-PSEUDO/pslibrary/rel-pz/PSEUDOPOTENTIALS\'",file=fout)
        elif("occupations" in line):
            #print("occupations=\'fixed\',",file=fout)
            print("occupations=\'smearing\', smearing=\'fd\', degauss = 0.002",file=fout)
        elif("mixing_beta" in line):
            print("mixing_beta = 0.3, mixing_fixed_ns = 300",file=fout)
        elif("UPF" in line):
            ll=line.split()
            PP=ll[-1]; sep=PP.split(".")
            newPP=sep[0]+".rel-"+sep[1]+"."+sep[2]+"."+sep[3]+"."+sep[4]+"."+sep[5]
            print(ll[0],ll[1],newPP,file=fout)
        else:
            print(line.strip("\n"),file=fout)

fin.close()
fout.close()
