#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

def get_brillouin_zone_3d(cell):
    """
    Generate the Brillouin Zone of a given cell. The BZ is the Wigner-Seitz cell
    of the reciprocal lattice, which can be constructed by Voronoi decomposition
    to the reciprocal lattice.  A Voronoi diagram is a subdivision of the space
    into the nearest neighborhoods of a given set of points. 

    https://en.wikipedia.org/wiki/Wigner%E2%80%93Seitz_cell
    https://docs.scipy.org/doc/scipy/reference/tutorial/spatial.html#voronoi-diagrams
    """

    cell = np.asarray(cell, dtype=float)
    assert cell.shape == (3, 3)

    px, py, pz = np.tensordot(cell, np.mgrid[-1:2, -1:2, -1:2], axes=[0, 0])
    points = np.c_[px.ravel(), py.ravel(), pz.ravel()]

    from scipy.spatial import Voronoi
    vor = Voronoi(points)

    bz_facets = []
    bz_ridges = []
    bz_vertices = []

    for pid, rid in zip(vor.ridge_points, vor.ridge_vertices):
        if(pid[0] == 13 or pid[1] == 13):
            bz_ridges.append(vor.vertices[np.r_[rid, [rid[0]]]])
            bz_facets.append(vor.vertices[rid])
            bz_vertices += rid

    bz_vertices = list(set(bz_vertices))

    return vor.vertices[bz_vertices], bz_ridges, bz_facets

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input", help="input POSCAR file", action='store')
    parser.add_argument("-k","--kpoints", help="HIGH_SYMMETRY_POINTS generated by vaspkit", action='store')
    args = parser.parse_args()

    # Obtain 1st BZ according to the lattice parameters
    latt=[]
    fin=open(args.input,"r")
    fin.readline()
    fac=float(fin.readline().split()[0])
    for k in range(3):
        ll=fin.readline().split()
        latt.append([float(ll[0]),float(ll[1]),float(ll[2])])
    fin.close()

    cell = np.array(latt)
    icell = np.linalg.inv(cell).T                
    b1, b2, b3 = np.linalg.norm(icell, axis=1)   

    Verts_bz, Edges_bz, Facets_bz = get_brillouin_zone_3d(icell)

    # read the high symmetry points
    # this is fractional points
    fin=open(args.kpoints,"r")
    fin.readline()
    sym_points=[]
    sym_name=[]
    for line in fin:
        ll=line.split()
        if(len(ll)==0):
            break

        sym_points.append([float(ll[0]), 
                           float(ll[1]), 
                           float(ll[2])])
        sym_name.append(ll[-1])
    fin.close()

    # OUTPUT
    nV=Verts_bz.shape[0]
    nK=len(sym_points)
    scaling=50      # make the BZ cluster larger

    fout=open("1st-BZ.xyz", "w+")
    print(4+nV+nK,file=fout)
    print("1st BZ, scaled by ",scaling,file=fout)
    print("G   %16.6f%16.6f%16.6f"%(0,0,0)+"   # Gamma center",file=fout)
    print("A   %16.6f%16.6f%16.6f"%(icell[0][0]*scaling, icell[0][1]*scaling, icell[0][2]*scaling)+"   # recp. vect",file=fout)
    print("B   %16.6f%16.6f%16.6f"%(icell[1][0]*scaling, icell[1][1]*scaling, icell[1][2]*scaling)+"   # recp. vect",file=fout)
    print("C   %16.6f%16.6f%16.6f"%(icell[2][0]*scaling, icell[2][1]*scaling, icell[2][2]*scaling)+"   # recp. vect",file=fout)
    for k in range(nV):
        print("V   %16.6f%16.6f%16.6f"%(Verts_bz[k][0]*scaling, Verts_bz[k][1]*scaling, Verts_bz[k][2]*scaling), file=fout)
    for k in range(nK):
        cart=sym_points[k][0]*icell[0]+sym_points[k][1]*icell[1]+sym_points[k][2]*icell[2]
        print("K   %16.6f%16.6f%16.6f   #"%(cart[0]*scaling, cart[1]*scaling, cart[2]*scaling)+sym_name[k], file=fout)
    fout.close()
