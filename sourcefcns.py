import numpy as np
"""
Collection of source time functions

"""

def ricker(fp, t0, t):
    """
    Ricker wavelet function.

    Input arguments:
        fp : Central frequency
        t0 : Time delay
        t : Time array.

    Return:
        out : Discretization of Ricker wavelet, same length as `t`.
    """
    a = np.pi**2*fp**2
    tau = t - t0
    out = (1 - 2*a*(t-t0)**2)*np.exp(-a*(t - t0)**2)
    return out

def minimum_phase(T, t0, t):
    """
    Minimum phase function.

    Input arguments:
        T : Characteristic source time
        t0 : Time delay
        t : Time array
    """
    return np.exp(-t/T) * t / T**2
