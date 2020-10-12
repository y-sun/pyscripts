#!/usr/bin/env python3

import dpdata
import sys
d_outcar = dpdata.LabeledSystem(sys.argv[1],fmt = 'vasp/outcar')
#outcar = dpdata.MultiSystems.from_dir(dir_name='./', file_name='OUTCAR', fmt='vasp/ou>
#vasp_multi_systems.to_deepmd_raw('./deepraw/')

d_outcar.to('deepmd/raw', 'dpmd_raw')
