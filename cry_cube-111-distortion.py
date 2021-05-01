#!/usr/bin/env python3

import numpy as np

# cubic info
a=8.51420
vol0=a**3


# rhombohedra
alpha_rhom=91.5304

theta=alpha_rhom/180*np.pi
cos_b= (np.cos(theta)-np.cos(theta)**2)/np.sin(theta)**2
sin_b= np.sqrt(1-cos_b**2)

va = np.array([ 1.0, 0.0,0.0])
vb = np.array([ np.cos(theta), np.sin(theta), 0.0])
vc = np.array([ np.cos(theta), np.sin(theta)*cos_b, np.sin(theta)*sin_b])

vol = np.dot(np.cross(va,vb), vc)


ra = (vol0/vol)**(1/3)

aa = va*ra
bb = vb*ra
cc = vc*ra

print(aa)
print(bb)
print(cc)
