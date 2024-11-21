#!/usr/bin/env python3

# output irreducible ijk and their multipilicity, only for cubic symmetry

import itertools

a=[-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6]
b=[-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6]
c=[-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6]

combinations=list(itertools.product(a,b,c))

distance=[]
member={}

for ic in combinations:
    dis=ic[0]**2+ic[1]**2+ic[2]**2
    if dis in member:
        member[dis].append(ic)
    else:
        member.update({dis:[ic]})

for key in member:
    print(key, member[key])
