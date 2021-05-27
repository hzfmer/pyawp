import numpy as np

def time(steps, dt):
    """
    Construct time vector of length `steps` using time step `dt`. First time
    step starts at time `t=0`.

    Args:
        steps: Number of time steps
        dt: Time step

    Return:
        np.array : Time vector.
    """
    t = np.linspace(0, (int(steps) - 1) * dt, int(steps))
    return t

def load(filename, num_outputs=1, dt=1, dtype=None, verbose=True):
    if not dtype:
        dtype = np.float32

    out = np.fromfile(filename, dtype=dtype)
    outlen = len(out)
    if outlen % num_outputs != 0:
        raise ValueError("num_outputs = %d is not divisible by len(output) = "\
                "%d." % (num_outputs, outlen))
    outlen = int(outlen/num_outputs)

    if verbose:
        print("Read: %s containing %s output(s)" % (filename, num_outputs))


    out = out.reshape((num_outputs, outlen)).T
    t = time(outlen, dt)

    return t, out

def load_selected(filename, length, selection=[], dtype=None, verbose=True):
    """
    Load a selected number of outputs from binary file. 

    Args:
        filename: name of binary file to load
        length: length of each output in counts (number of steps saved)
        selection: a list of indices to load from the file.
        dtype: Data type stored in the binary file. Defaults to `np.float32`
        verbose: print load message.

    """
    if not dtype:
        dtype = np.float32

    num_outputs = len(selection)
    out = np.zeros((length, num_outputs))

    i = 0
    for idx in selection:
        offset = np.dtype(dtype).itemsize * length * idx
        data = np.fromfile(filename, dtype=dtype, count=length, offset=offset)
        out[:, i] = data
        i += 1
    
    if verbose:
        print("Read: %s selecting %s output(s)" % (filename, num_outputs))

    return out


def load_all(filename, fields, refine=0, frame=1, num_outputs=1, dt=1,
             coarsen=1, dtype=None):
    """
    Load all files that follow a special naming
    convention: 'filename_field_refine_frame'.

    Args:
        filename: Name of the file.
        refine: Refinement number (starts at 0 for no refinement).
        frame: Number of frames in output.
        dt: Time step
        coarsen: Adjust output length so that it matches refinement 0.
    
    Example:
        load_all('output', 'x y z') loads
            'output_0_x_1'
            'output_0_y_1'
            'output_0_z_1'

    Returns:
        Returns a list that contains the data for the load files. The order of
        the items is first the time vector followed by each requested field in
        the order specified.

    """
    frame_ref = frame * 2 ** refine
    dt_ref = dt / 2 ** refine
    out = []
    first = 1
    for field in fields.split(' '):
        t, v = load('%s_%d_%s_0%d' % (filename, refine, field, frame_ref),
                    num_outputs, dt_ref)
        if coarsen:
            t = t[::2 ** refine]
            v = v[::2 ** refine]

        if first:
            out.append(t)
            first = 0
        out.append(v)
    return out

def load_edge_2d(path, name):
    from pyawp import Struct
    d = np.genfromtxt('%s/%s'%(path, name), delimiter=',')
    data = Struct()
    data.t = d[:,0]
    data.p = d[:,1]
    data.vy = d[:,4]
    data.vz = d[:,5]
    return data

def load_edge_3d(path, name):
    from pyawp import Struct
    d = np.genfromtxt('%s/%s'%(path, name), delimiter=',')
    data = Struct()
    data.t = d[1:,0]
    data.vx = d[1:,7]
    data.vy = d[1:,8]
    data.vz = d[1:,9]
    return data


