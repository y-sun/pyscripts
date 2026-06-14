#!/usr/bin/env python3

from ase import io
import sys
atoms = io.read(sys.argv[1], format = 'cif')
atoms.write('cif2pos.vasp', format = 'vasp')
