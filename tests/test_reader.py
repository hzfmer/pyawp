import pyawp
import numpy as np

def test_load_selected():
    # Load receiver data from file that contains 25 receivers
    t, v = pyawp.load("fixtures/recv_x", num_outputs=25)
    # Select receivers to load
    # Load all 25 receivers, but load them in reverse order
    selection = range(25)[::-1]
    w = pyawp.load_selected("fixtures/recv_x", 1000, selection=selection)
    for i in range(len(selection)):
        assert np.all(np.isclose(w[:,i], v[:,selection[i]]))
