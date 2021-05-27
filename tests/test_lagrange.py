from pyawp import lagrange
import numpy as np

def test_accuracy():
    x0 = 0.25
    x = np.array([0, 1, 2, 3])
    L = lagrange.lagrange(x0, x)
    degrees = range(3)
    for p in degrees:
        y = x**p
        assert np.isclose(L.dot(y), x0**p)
