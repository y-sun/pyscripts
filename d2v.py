#!/usr/bin/env python3

import dpdata
import sys
d_outcar = dpdata.LabeledSystem(sys.argv[1],fmt = 'deepmd/raw')
nf=d_outcar.get_nframes()
#nsize=int(nf/7)+1
#outcar = dpdata.MultiSystems.from_dir(dir_name='./', file_name='OUTCAR', fmt='vasp/>
#vasp_multi_systems.to_deepmd_raw('./deepraw/')

#d_outcar.to('deepmd/raw', 'dpmd_raw')
#d_outcar.to_deepmd_raw('deepmd')
#d_outcar.to_deepmd_npy('deepmd') #,set_size=n0)

print('total frame:',nf)
for k in range(nf):
    d_outcar.to('vasp/poscar', f'POSCAR_{k}', frame_idx=k)

#print("total set_size nf_per_set nf_in_last")
#print(nf, nsize,n0, nf-nsize*n0)
