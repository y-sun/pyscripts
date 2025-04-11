#!/usr/bin/env python3

fin=open("cluster-todo.dat","r")
f1=open("cluster-AA.dat","w+")
f2=open("cluster-BB.dat","w+")
f3=open("cluster-CC.dat","w+")

for line in fin:
    natom=int(line.split()[0])
    comment=fin.readline().strip("\n")
    ll=fin.readline().split()
    if(ll[0]=="AA"):
        print(natom, file=f1)
        print(comment, file=f1)
        print(*ll, file=f1)
        for k in range(natom-1):
            print(fin.readline().strip("\n"),file=f1)
    elif(ll[0]=="BB"):
        print(natom, file=f2)
        print(comment, file=f2)
        print(*ll, file=f2)
        for k in range(natom-1):
            print(fin.readline().strip("\n"),file=f2)
    elif(ll[0]=="CC"):
        print(natom, file=f3)
        print(comment, file=f3)
        print(*ll, file=f3)
        for k in range(natom-1):
            print(fin.readline().strip("\n"),file=f3)

fin.close(); f1.close();f2.close()

