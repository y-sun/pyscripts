#!/usr/bin/env python3

import ase.build
import ase.io.vasp
import sys
cell = ase.io.vasp.read_vasp(sys.argv[1])
#P = [[9,0,0],[6,12,0],[0,0,3]]
P = [[1,0,0],[1,2,0],[0,0,1]] # HCP -> SC
sc = ase.build.make_supercell(cell, P)
ase.io.vasp.write_vasp("POSCAR.sc",sc, label='supercell',direct=True,sort=True)
