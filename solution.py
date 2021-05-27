"""

This module provides helper functions for computing the error in the numerical
solution.

"""

def init_fields(fields, num_refine=1):
    import pyawp
    soln = pyawp.utils.Struct()
    for field in fields.split(' '):
        soln[field] = [0] * num_refine
    return soln

def print_difference(field, u, v, relative=0):
    """

    """
    err = norm(u[field], v[field], relative)
    print("|%s|_2 \t\t |%s|_1 \t |%s|_inf" % (field, field, field))
    for e1, e2, einf in zip(err.e1, err.e2, err.inf):
        print("%e \t %e \t %e"% (e1, e2, einf))
    return err

def norm(u, v, relative=0):
    """

    Compute the norm difference \| u - v\| using the 1-norm, 2-norm, and
    infinity norm. If `relative = 0` then the norm is normalized by `\| u|`.

    """
    import pyawp
    import numpy as np
    err = init_fields('e1 e2 inf', num_refine=len(u))
    i = 0
    for ui, vi in zip(u, v):
        ui = ui.squeeze()
        vi = vi.squeeze()
        err.e2[i] = np.linalg.norm(ui - vi, ord=2)
        err.e1[i] = np.linalg.norm(ui - vi, ord=1)
        err.inf[i] = np.max(np.abs(ui - vi))
        if relative:
           err.e2[i]  = err.e2[i] / np.linalg.norm(ui, ord=2)
           err.e1[i]  = err.e1[i] / np.linalg.norm(ui, ord=1)
           err.inf[i] = err.inf[i] / np.max(np.abs(ui))
        i += 1
    return err


