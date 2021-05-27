import numpy as np

def vector_xz(phi, vx, vy, vz):
    """
    Rotate vector in phi radians counter-clockwise in the xz-plane.

    """
    vxp = vx * np.cos(phi) - vz * np.sin(phi)
    vyp = vy
    vzp = vx * np.sin(phi) + vz * np.cos(phi)
    return vxp, vyp, vzp


def tensor_xz(phi, mxx, myy, mzz, mxy, mxz, myz):
    """
    Rotate tensor in phi radians counter-clockwise in the xz-plane.

    """
    x = [np.cos(phi), 0, -np.sin(phi)]
    y = [0, 1, 0]
    z = [np.sin(phi), 0, np.cos(phi)]
    cont = lambda a, b : (  a[0] * b[0] * mxx 
                          + a[1] * b[1] * myy 
                          + a[2] * b[2] * mzz 
                          + (a[0] * b[1] + a[1] * b[0]) * mxy 
                          + (a[0] * b[2] + a[2] * b[0]) * mxz 
                          + (a[1] * b[2] + a[2] * b[1]) * myz )
    mxxp = cont(x, x)
    myyp = cont(y, y)
    mzzp = cont(z, z)
    mxyp = cont(x, y)
    mxzp = cont(x, z)
    myzp = cont(y, z)
    return mxxp, myyp, mzzp, mxyp, mxzp, myzp
