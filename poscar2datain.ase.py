#!/usr/bin/env python3

from ase.io import read as io_read
from ase.io import write as io_write
import sys

stru=io_read(sys.argv[1],index=0,format='vasp')
io_write("in.data",stru,format='lammps-data')
