import matplotlib.pyplot as plt

def velocity(data, xidx, yidx, zidx, component='z', label='', show_plot=0,
        save=None, kwargs={}):
    """
    Make a timeseries plot that is useful for example showing a component of the
    particle velocity field at a particular grid point.

    Arguments:
        data : Struct containing data and time-vector: Data must be array of
            dimensions `[xidx, yidx, zidx, tidx]`.
        xidx : x-index
        yidx : y-index
        zidx : z-index

    Optional:
        component : Component of the velocity (will be displayed in the title)
        label : Label displayed in the title. Useful for describing the method
            used.
        show_plot : Show plot.
        save : Save figure to file.

    """
    plt.plot(data.t, data.data[xidx,yidx,zidx,:],label=label, **kwargs)
    plt.ylabel('$v_%s$'%component)
    plt.xlabel('t (s)')
    plt.title('(x/h, y/h, z/h) = (%g, %g, %g)' % (data.x[xidx], data.y[yidx],
              data.z[zidx]))
    if save:
        print("Writing:", save)
        plt.savefig(save, dpi=300)
    if show_plot:
        plt.show()
