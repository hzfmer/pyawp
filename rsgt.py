"""
Module for working with SGT data from Rob Graves' RWG code.

"""
import os
import numpy as np

def fromrsgtfile(filename, sgt_index, nt):
    ncomp = 6
    float_bytes = 4
    offset = float_bytes  * sgt_index * ncomp * nt
    f = open(filename, "rb")
    f.seek(offset, os.SEEK_SET) 
    sgt = np.fromfile(f, dtype=np.float32,
        count=nt * ncomp)
    sgt = sgt.reshape((ncomp, nt)).T
    f.close()
    return sgt


def rwgtoawp(sgt):
    # Convert to AWP format
    # Swaps XX and YY, XZ and YZ, multiplies XZ and YZ by -1
    awp_sgt = sgt.copy()

    xx = sgt[:,0]
    yy = sgt[:,1]
    zz = sgt[:,2]
    xy = sgt[:,3]
    xz = sgt[:,4]
    yz = sgt[:,5]
    
    awp_sgt[:,0] = yy
    awp_sgt[:,1] = xx
    awp_sgt[:,4] = -yz
    awp_sgt[:,5] = -xz

    return awp_sgt
