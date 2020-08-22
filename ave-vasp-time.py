#!/usr/bin/env python3

import sys
import numpy as np

fin=open(sys.argv[1],"r")
times=[]
for line in fin:
    if("LOOP+:" in line):
        ll=line.split()
        times.append(float(ll[-1]))
fin.close()

times=np.array(times)
ftime=times[:39]
print(ftime.size,np.mean(ftime))
print(times.size,np.mean(times))
