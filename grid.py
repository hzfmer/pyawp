import numpy as np


def shifts():
    """
    Flags that indicate if the grid is shifted in the particular direction or
    not.
    
    Example: v = (1, 0, 0) 
    implies that v = v(x_i+1/2, y_j, z_k)

    These shifts match the choice of coordinate system in AWP-ODC.

    """
    u1 = (1, 1, 1)
    v1 = (0, 0, 1)
    w1 = (0, 1, 0)
    return u1, v1, w1


def grid(first, last, stride, npts, gridspacing, axis=0, field=0,
         topography=False, index='fortran'):
    """
    Return grid vector for a particular axis.

    The free surface is at z = 0 and the z-axis increases with depth.

    Args:
        first: Index of first grid point (NBG).
        last: Index of last grid point, inclusive (NED).
        stride: Grid point stride (NSKP).
        gridspacing: Grid spacing.
        npts: Number of grid points (X, Y, Z).
        axis(optional): Axis discretize along. 
                Use `axis=0` for the x-direction.
        field(optional): Specify the field to obtain grid points for. 
                Use `field=0` for the velocity component in the x-direction.
        topography(optional): Set to `True` if the topography feature is
                enabled.  
        index(optional): Set to `'fortran'` if indices start at 1.

    Returns:
        np.array

    """

    if index == 'fortran':
        offset = 1
    else:
        offset = 0

    out = gridspacing * np.array(range(first - offset, last + 1 - offset,
                                 stride))
    out = out + 0.5 * gridspacing * shifts()[field][axis]

    if axis == 2 and topography and first - offset == 0:
            out[0] = 0

    return out


def vx(cfg, gridnum=0):
        x = grid(cfg.nbgx[gridnum], cfg.nedx[gridnum], cfg.nskpx[gridnum],
                 cfg.nx, cfg.h, axis=0, field=0, index='fortran') 
        y = grid(cfg.nbgy[gridnum], cfg.nedy[gridnum], cfg.nskpy[gridnum],
                 cfg.ny, cfg.h, axis=1, field=0, index='fortran') 
        z = grid(cfg.nbgz[gridnum], cfg.nedz[gridnum], cfg.nskpz[gridnum],
                 cfg.nz, cfg.h, axis=2, field=0, index='fortran') 
        return x, y, z


def vy(cfg, gridnum=0):
        x = grid(cfg.nbgx[gridnum], cfg.nedx[gridnum], cfg.nskpx[gridnum],
                 cfg.nx, cfg.h, axis=0, field=1, index='fortran') 
        y = grid(cfg.nbgy[gridnum], cfg.nedy[gridnum], cfg.nskpy[gridnum],
                 cfg.ny, cfg.h, axis=1, field=1, index='fortran') 
        z = grid(cfg.nbgz[gridnum], cfg.nedz[gridnum], cfg.nskpz[gridnum],
                 cfg.nz, cfg.h, axis=2, field=1, index='fortran') 
        return x, y, z


def vz(cfg, gridnum=0):
        x = grid(cfg.nbgx[gridnum], cfg.nedx[gridnum], cfg.nskpx[gridnum],
                 cfg.nx, cfg.h, axis=0, field=2, index='fortran') 
        y = grid(cfg.nbgy[gridnum], cfg.nedy[gridnum], cfg.nskpy[gridnum],
                 cfg.ny, cfg.h, axis=1, field=2, index='fortran') 
        z = grid(cfg.nbgz[gridnum], cfg.nedz[gridnum], cfg.nskpz[gridnum],
                 cfg.nz, cfg.h, axis=2, field=2, index='fortran') 
        return x, y, z
