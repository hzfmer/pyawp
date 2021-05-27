import pyawp
import numpy as np

def test_vector_xz():
    phi = np.pi / 2
    vx = 0
    vy = 0
    vz = 1
    vxp, vyp, vzp = pyawp.rotate.vector_xz(phi, vx, vy, vz)
    assert np.isclose(vxp, -vz)


def test_tensor_xz():
    phi = np.pi / 2
    mxx = 0
    myy = 0
    mzz = 1
    mxy = 0
    mxz = 0
    myz = 0
    mxxp, myyp, mzzp, mxyp, mxzp, myzp = pyawp.rotate.tensor_xz(phi, mxx, myy,
            mzz, mxy, mxz, myz)
    assert np.isclose(mxx, -mzzp)
