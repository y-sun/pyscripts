#!/usr/bin/env python3

from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.plotter import DosPlotter

vasprun = Vasprun("./vasprun.xml")
cdos = vasprun.complete_dos
data = cdos.get_site_t2g_eg_resolved_dos(vasprun.structures[0][0])
element_dos = cdos.get_element_dos()

plot = DosPlotter()
plot.add_dos_dict(element_dos)
plot.add_dos(r'$t_{2g}$',data['t2g'])
plot.add_dos(r'$e_{g}$',data['e_g'])

plot.show(xlim=[-10, 5], ylim=[-2, 2])
