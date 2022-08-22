#!/usr/bin/env python3

scut=0.02
print("strain larger than 0.02:")
fin=open("checkrelax.out",'r')
for line in fin:
    ll=line.split()
    if(float(ll[0]) > scut):
        print(ll[1],end=" ")
print("")
fin.close()


scut=0.05
print("strain larger than 0.05:")
fin=open("checkrelax.out",'r')
for line in fin:
    ll=line.split()
    if(float(ll[0]) > scut):
        print(ll[1],end=" ")
print("")
fin.close()
