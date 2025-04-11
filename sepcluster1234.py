#!/usr/bin/env python3

fin=open("cluster-todo.dat","r")
f1=open("cluster-AA.dat","w+")
f2=open("cluster-BB.dat","w+")

for line in fin:
    natom=int(line.split()[0])
    comment=fin.readline().strip("\n")
    ll=fin.readline().split()
    if(ll[0]=="AA" or ll[0]=="CC"):
        print(natom, file=f1)
        print(comment, file=f1)
        print(*ll, file=f1)
        for k in range(natom-1):
            print(fin.readline().strip("\n"),file=f1)
    elif(ll[0]=="BB" or ll[0]=="DD"):
        print(natom, file=f2)
        print(comment, file=f2)
        print(*ll, file=f2)
        for k in range(natom-1):
            print(fin.readline().strip("\n"),file=f2)

fin.close(); f1.close();f2.close()

