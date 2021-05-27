import matplotlib.pyplot as plt


def velocity_xy(data, zidx, tidx, component='z', label='', kwargs={}):
    """
    Make a pcolor plot that is useful for example showing a component of the
    particle velocity field at the free surface.

    Arguments:
        data : Struct containing data and time-vector: Data must be array of
            dimensions `[xidx, yidx, zidx, tidx]`.
        zidx : z-index
        tidx : time-index

    Optional:
        component : Component of the velocity (will be displayed in the title)
        label : Label displayed in the title. Useful for describing the method
            used.
        kwargs : Any extra key-value arguments to pass to plot function.

    """
    plt.pcolormesh(data.x, data.y, data.data[:, :, zidx, tidx], **kwargs)

    if data.normalize:
        plt.xlabel('x/h')
        plt.ylabel('y/h')
    else:
        plt.xlabel('x')
        plt.ylabel('y')

    plt.title('%s\n  $v_%s$, t = %g (s)' % (label, component, data.t[tidx]))

def velocity_xz(data, yidx, tidx, component='z', label='', kwargs={}):
    """
    Make a pcolor plot that is used for showing a cross-section using the
    xz-plane.

    Arguments:
        data : Struct containing data and time-vector: Data must be array of
            dimensions `[xidx, yidx, zidx, tidx]`.
        yidx : y-index
        tidx : time-index

    Optional:
        component : Component of the velocity (will be displayed in the title)
        label : Label displayed in the title. Useful for describing the method
            used.
        kwargs : Any extra key-value arguments to pass to plot function.

    """
    arr = data.data[:, yidx, ::-1, tidx].T
    plt.pcolormesh(data.x, data.z, arr, **kwargs)

    if data.normalize:
        plt.xlabel('x/h')
        plt.ylabel('z/h')
    else:
        plt.xlabel('x')
        plt.ylabel('z')

    plt.title('%s\n  $v_%s$, y/h = %g t = %g (s)' %
              (label, component, data.y[yidx], data.t[tidx]))
