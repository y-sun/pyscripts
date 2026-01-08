#!/usr/bin/env python3

from ase import io
import sys
atoms = io.read(sys.argv[1])
atoms.write('cif2pos.vasp', format = 'vasp')
