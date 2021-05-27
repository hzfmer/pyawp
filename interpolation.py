import numpy as np

def nearest(query, data):
    """
    Find grid point closest to query point using nearest neighbor 
    interpolation (L1 distance).

    Args:
        query(np.array): Query grid points ( number of queries x 3 )
        data(Struct): Field data array that contains (x, y, z, and data)

    """
    out = np.zeros((query.shape[0], len(data.t)))
    for l, qp in enumerate(query):
        i = argnearest(qp[0], data.x)
        j = argnearest(qp[1], data.y)
        k = argnearest(qp[2], data.z)
        out[l,:] = data.data[i, j, k, :]
    return out

def lagrange(query, data, degree=None):
    """
    Estimate solution at query points using Lagrange interpolation.

    Args:
        query(np.array): Query grid points ( number of queries x 3 )
        data(Struct): Field data array that contains (x, y, z, and data)
        degree(optional): Degree of Lagrange interpolating polynomial. Defaults
            to `degree = 1` (linear interpolation).

    """
    from pyawp.lagrange import lagrange
    
    if degree is None:
        degree = np.ones((3,))

    out = np.zeros((query.shape[0], len(data.t)))
    nnodes = degree + 1
    left = [np.floor(ni/2) for ni in nnodes]
    right = [np.floor(ni/2) for ni in nnodes]

    for l, qp in enumerate(query):
        xn, idx_x = argnearest_range(qp[0], data.x, left[0], right[0])
        yn, idx_y = argnearest_range(qp[1], data.y, left[1], right[1])
        zn, idx_z = argnearest_range(qp[2], data.z, left[2], right[2])

        Lx = lagrange(qp[0], data.x[idx_x])
        Ly = lagrange(qp[1], data.y[idx_y])
        Lz = lagrange(qp[2], data.z[idx_z])

        for i, xi in enumerate(idx_x):
            for j, yj in enumerate(idx_y):
                for k, zk in enumerate(idx_z):
                    out[l,:] += Lx[i]*Ly[j]*Lz[k]*data.data[xi, yj, zk, :]
        return out

def argnearest(qp, x):
    """
    Find the index of the grid point nearest the query point qp.

    Args:
        qp(float) : Query point.
        x(np.array) : Grid points.

    Returns:
        inearest : Index of grid point nearest to query point.

    """
    inearest = np.argmin(abs(qp - x))
    return inearest

def argnearest_range(qp, x, left=0, right=0):
    """
    Find the range of indices nearest the query point qp. 

    --------[---*----)---------

    * index of grid point nearest to query point
    [ left index (`left` steps away from qp) 
    ) right index (`right` steps away + 1 from qp) 

    If the stencil hits the boundary, then the stencil length is preserved.

    Args:
        qp(float) : Query point 
        x(np.array) : Grid points
        left(int, optional) : Number of points to the left.
        right(int, optional) : Number of points to the right.

    Returns:
        inearest : Index of grid point nearest to query point.
        irange(tuple) : First and last index + 1 of grid points in stenci.

    """
    left = int(left)
    right = int(right)

    inearest = argnearest(qp, x)
    diffleft = inearest - left
    diffright = len(x) - inearest - right - 1
    ileft = max(diffleft, 0) + min(diffright, 0)
    iright = min(inearest + right + 1, len(x)) - min(diffleft, 0)

    # Check that stencil length is preserved
    assert iright - ileft == left + right + 1

    return inearest, range(ileft, iright)
