#!/usr/bin/env python3
import os,sys
import numpy as np

def inverse(m):
    #calculate the inverse of a 3*3 matrix
    invm=[[0 for i in range(3)] for j in range(3)]
    SINGULAR = 1.E-8
    #mdet, mtemp[3][3];
    mdet = np.linalg.det(m)
    if (abs(mdet) < SINGULAR):     
        #Matrix is singular.
        for i in range(3):
            for j in range(3): 
                invm[i][j] = 0
        return -1
    mtemp=[[0 for i in range(3)] for j in range(3)]
    mtemp[0][0]= (m[1][1]*m[2][2] - m[2][1]*m[1][2])
    mtemp[0][1]=-(m[0][1]*m[2][2] - m[2][1]*m[0][2])
    mtemp[0][2]= (m[0][1]*m[1][2] - m[1][1]*m[0][2])
    mtemp[1][0]=-(m[1][0]*m[2][2] - m[2][0]*m[1][2])
    mtemp[1][1]= (m[0][0]*m[2][2] - m[2][0]*m[0][2])
    mtemp[1][2]=-(m[0][0]*m[1][2] - m[1][0]*m[0][2])
    mtemp[2][0]= (m[1][0]*m[2][1] - m[2][0]*m[1][1])
    mtemp[2][1]=-(m[0][0]*m[2][1] - m[2][0]*m[0][1])
    mtemp[2][2]= (m[0][0]*m[1][1] - m[1][0]*m[0][1])
    for i in range(3):
        for j in range(3): 
            invm[i][j] = mtemp[i][j] / mdet
    return invm 

def recp_length(latt):
    a=np.array(latt)
    c23=np.cross(a[1],a[2])
    c31=np.cross(a[2],a[0])
    c12=np.cross(a[0],a[1])
    b1=2*np.pi*c23/np.dot(a[0],c23)
    b2=2*np.pi*c31/np.dot(a[1],c31)
    b3=2*np.pi*c12/np.dot(a[2],c12)
    lb1=np.sqrt(np.sum(b1*b1))/(2*np.pi)  # vasp Auto modes does not apply 2PI
    lb2=np.sqrt(np.sum(b2*b2))/(2*np.pi)
    lb3=np.sqrt(np.sum(b3*b3))/(2*np.pi) 
    return [lb1,lb2,lb3]



if(len(sys.argv) != 4):
    print("./pos2QE.py qe_init kpoint.in POSCAR")
    sys.exit()
    
qeinput = sys.argv[1]
kps = sys.argv[2]
posfile = sys.argv[3]

atom_n = []
atom_c = []
latt=[[0 for i in range(3)] for j in range(3)]
elong=[0 for i in range(3)]

fpos=open(posfile,"r")
lines = fpos.readlines()
factor=float(lines[1].split()[0])
for i in range(2, 5):
    line=lines[i].split()
    for j in range(3):
        latt[i-2][j]=float(line[j])*factor
#print(latt)

atom_type = lines[5].split()
ll = lines[5].split() 
num = 5
if(ll[0].isalpha()):
    ll = lines[6].split()
    num = 6
if(ll[0].isdigit()):
    tmp_cd = lines[num + 1][0]
    dir_mark = 1
    if(tmp_cd == 'C' or tmp_cd == 'c'):
        #ilatt = inverse(latt)
        ilatt = np.linalg.inv(np.array(latt))
        dir_mark = 0
    type_n = len(ll)
    num += 2
    for k in range(type_n):
        sym_type = atom_type[k]
        n_per = int(ll[k])
        atom_n.append(n_per)
        #atom_per = []
        for m in range(num, num + n_per):
            #print(ll, n_per, lines[m])
            l3 = lines[m].split()
            atom_per3 = []
            for car in range(3):
                xyz = float(l3[car])
                atom_per3.append(xyz)
            if(dir_mark == 0):
                convert_0=atom_per3[0]*ilatt[0][0]+atom_per3[1]*ilatt[1][0]+atom_per3[2]*ilatt[2][0];
                convert_1=atom_per3[0]*ilatt[0][1]+atom_per3[1]*ilatt[1][1]+atom_per3[2]*ilatt[2][1];
                convert_2=atom_per3[0]*ilatt[0][2]+atom_per3[1]*ilatt[1][2]+atom_per3[2]*ilatt[2][2];
                atom_per = [sym_type, convert_0, convert_1, convert_2]
            else:
                atom_per = [sym_type, atom_per3[0], atom_per3[1], atom_per3[2]]
            atom_c.append(atom_per)
        num = num + n_per
else:
    print("poscar wrong")
    sys.exit()
fpos.close()


fk=open(kps, "r")
lines = fk.readlines()
kpoints=[4,4,4] # default
if("MP" in lines[0]):
    ll=lines[1].split()
    kpoints=[int(k) for k in ll]
elif("Auto" in lines[0]):
    Rk=float(lines[1].split()[0])
    blatt = recp_length(latt)
    N1=int(max(1,Rk*blatt[0]+0.5))
    N2=int(max(1,Rk*blatt[1]+0.5))
    N3=int(max(1,Rk*blatt[2]+0.5))
    kpoints=[N1,N2,N3]
fk.close()
        
#print(atom_n)
type_num_line = "    ibrav = 0,nat = "+str(len(atom_c))+",ntyp = "+str(len(atom_n))+","
with open(qeinput, "r") as fp:
    lines = fp.readlines()
    with open("scf.in", "w+") as fout:
        for i in range(len(lines)):
            if("nat" in lines[i]):
                fout.write(type_num_line)
                fout.write("\n")
            elif("CELL_PARAMETERS" in lines[i]):
                fout.write(lines[i])
                for a in range(len(latt)):
                    for b in range(len(latt[a])):
                        fout.write("%15.9f" %(latt[a][b]))
                    fout.write("\n")
                fout.write("ATOMIC_POSITIONS {crystal}\n")
                for n in range(len(atom_c)):
                    #print(atom_c[n])
                    fout.write("%5s%15.9f%15.9f%15.9f\n" %(atom_c[n][0], atom_c[n][1], atom_c[n][2], atom_c[n][3]))
                fout.write("K_POINTS {automatic}\n")
                fout.write("%d %d %d %d %d %d\n"%(kpoints[0],kpoints[1],kpoints[2],0,0,0))
            else:
                fout.write(lines[i])

