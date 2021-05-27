import matplotlib.pyplot as plt

def save(show_plot=0, save=None, dpi=300, fmt='.png', verbose=True, **kwargs):
    """

    Optional:
        show_plot : Show plot.
        save : Save figure to file.

    """
    if save:
        filename = save + fmt 
        if verbose:
            print("Writing:", filename)
        plt.savefig(save, dpi=300, **kwargs)
    if show_plot:
        plt.show()
