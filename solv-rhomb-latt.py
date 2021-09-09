#!/usr/bin/env python3

# transfer L theta to
# a a b
# a b a
# b a a

import numpy as np

L=5.2542006667
theta=55.5617930000/180*np.pi


# 4th order
para = [1, 8, -(2+np.cos(theta))*2*L**2, 0, L**4*np.cos(theta)**2 ]

a = np.roots(para)

b = (L**2 - 2*a**2)**(1/2)

print("solved a:")
print(a)
print("solved b:")
print(b)

