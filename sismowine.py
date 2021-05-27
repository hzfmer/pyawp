"""
Read and write sismowine solutions files:

http://www.sismowine.org/index.html?page=sol_for

"""
import numpy as np


def read(filename, record_skip=2):
    """
    Read sismowine solution file.

    Args:
        filename : Name of solution file to read.

    Returns:
        time : Time vector
        solutions : List of solution array (`np.array`). 

    """
    f = open(filename).read().split('\n')
    nt, dt, nr = f[0].strip().split(' ')
    nt = int(nt[0:])
    dt = float(dt)
    nr = int(nr)
    solutions = [0]*nr
    skip = 0
    for i in range(nr):
        solutions[i] = np.array(f[1 + skip + nt * i: 1 +
                                skip + nt * (i + 1)]).astype(np.float64)
        # Each new data record comes after two empty lines
        skip += record_skip
    time = [dt * i for i in range(nt)]
    return solutions, time


def write(filename, solutions, dt):
    """
    Write sismowine solution file.

    Args:
        filename : Name of the solution file to write.
        solutions : List of solution arrays (`np.array`). 

    """
    nr = len(solutions)
    f = open(filename, 'w')
    nt = len(solutions[0])
    f.write('#%d %g %d\n' % (nt, dt, nr))
    for i in range(nr):
        f.write('\n'.join(['%e' % si for si in solutions[i]]))
        f.write('\n\n\n')

