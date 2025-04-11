#!/usr/bin/env python3

'''
pip install pymatgen
pip install rdfpy
'''

import numpy as np
from rdfpy import rdf
from pymatgen.core import Structure
import pylab as plt
import sys
import matplotlib

if __name__ == '__main__':
    structure = Structure.from_file(sys.argv[1])
    structure.make_supercell(4)
    
    coords = structure.cart_coords
    noise = np.random.normal(loc=0.0, scale=0.01, size=(coords.shape))
    coords = coords + noise
    
    g_r, radii = rdf(coords, dr=0.05)
    
    plt.figure(figsize=(8,6))
    plt.rcParams.update({'font.size': 16})
    plt.plot(radii, g_r)
    plt.xlim(0,8)
    plt.xlabel('r (Angstrom)')
    plt.ylabel('g(r)')
    plt.savefig('rdf.png')
    plt.show()
