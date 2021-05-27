class MomentTensor:

    def __init__(self, mxx, myy, mzz, mxy, mxz, myz, pos=[]):
        """
        The MomentTensor class is used to construct an object
        that holds all of the necessary data needed to build 
        moment tensors.

        Parameters 

        mxx ... mzz : float, np.array,
                      Moment tensor components containing one time function per 
                      component. The length of component must be the same.
                pos : integer, np.array, length 3, optional,
                      Position vector containing the indices at which the 
                      moment tensor acts

        """
        import numpy as np

        self.xx = mxx
        self.yy = myy
        self.zz = mzz
        self.xy = mxy
        self.xz = mxz
        self.yz = myz

        if len(pos) == 0:
            self.pos = np.array([0, 0, 0])
        else:
            self.pos = np.array(pos)

    def stack(self):
        """
        Constructs a matrix by stacking all of the moment tensor components
        in a row-wise fashion.

        Returns

        out : `np.array`, size `m x n`, 
              out[i,j]  accesses component `i` of the moment tensor at
                        time sample `j`.
              `i = 0 : mxx`
              `i = 1 : myy`
              `i = 2 : mzz`
              `i = 3 : mxy`
              `i = 4 : mxz`
              `i = 6 : myz`
              
        """

        import numpy as np
        return np.vstack((self.xx, self.yy, self.zz, 
                                self.xy, self.xz, self.yz))

    def write(self, filename, output='awp'):
        """ 
        Writes the moment tensor to disk.

        Parameters

        filename : string,
                   Path and name including extension to the file to write to
                   The file will be created if does not exist or overwritten
                   if it already exists.

        output : string, optional, 
                 Specifies the format to output to
                 `output = awp` : Write binary file for AWP moment tensor. 

        """
        import pyawp
        pyawp.source.write(filename, self.stack(), self.pos)
