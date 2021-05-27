import numpy as np
import pyawp.interpolation as interp
from pyawp import Struct

def test_argnearest():

    x = np.arange(0,10)
    xs = 4.5
    inearest, idx = interp.argnearest_range(xs, x)
    assert inearest == 4

def test_argnearest_range():

    x = np.arange(0,10)

    # Query point in the interior of the domain, away from boundaries, no left,
    # right bounds
    xs = 4.3
    left = 0
    right = 0 
    inearest, idx = interp.argnearest_range(xs, x, left, right)
    assert inearest == 4
    assert idx[0] == 4
    assert idx[-1] == 4

    # Query point in the interior of the domain, away from boundaries, 
    # three point wide stencil
    left = 1
    right = 1 
    inearest, idx = interp.argnearest_range(xs, x, left, right)
    assert inearest == 4
    assert idx[0] == 3
    assert idx[-1] == 5

    # Query point close to the left boundary, 5 point wide stencil
    xs = 0.1
    left = 2
    right = 2 
    inearest, idx = interp.argnearest_range(xs, x, left, right)
    assert inearest == 0
    assert idx[0] == 0
    assert idx[-1] == 4

    # Query point close to the right boundary, 5 point wide stencil
    xs = 9.1
    left = 2
    right = 2 
    inearest, idx = interp.argnearest_range(xs, x, left, right)
    assert inearest == 9
    assert idx[0] == 5
    assert idx[-1] == 9

def test_lagrange():
    query = np.array([[1.1,1.5, 1.6]])
    x = np.arange(0, 10)
    y = np.arange(0, 10)
    z = np.arange(0, 10)
    t = np.linspace(0, 1, 50)
    data = np.random.rand(4,4,4,50)
    grid = Struct()
    grid.x = x
    grid.y = y
    grid.z = z
    grid.t = t
    grid.data = data
    nearest = interp.nearest(query, grid)
    degree = np.array([0, 0, 0])
    lagrn = interp.lagrange(query, grid, degree=degree)
    assert np.all(np.isclose(np.abs(nearest - lagrn), 0))
