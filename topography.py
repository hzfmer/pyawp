import numpy as np

class Topography(object):

    def __init__(self, nx, ny, h, ngsl):
        self.nx = nx
        self.ny = ny
        self.h = h
        self.ngsl = ngsl

    def refine(self, refine_factor):
        """

        Apply a factor of two grid refinement.

        If `refine_factor = 0` then no grid refinement is performed.

        """
        r = 2 ** refine_factor
        self.h = self.h / r
        self.nx = self.nx * r
        self.ny = self.ny * r


    def xc(self):
        """
        X Axis, x = 0 is in the center of the domain.
        """
        mx = self.nx + 2 * self.ngsl
        x = np.linspace(0, (mx - 1) * self.h, mx)
        xm = (min(x) + max(x)) / 2
        x = x - xm
        return x

    def yc(self):
        """
        Y Axis, y = 0 is in the center of the domain.
        """
        my = self.ny + 2 * self.ngsl
        y = np.linspace(0, (my - 1) * self.h, my)
        ym = (min(y) + max(y)) / 2
        y = y - ym
        return y

    def x0(self):
        """
        X axis, having x[0] = -ngsl.

        """
        mx = self.nx + 2 * self.ngsl
        x = np.linspace(-self.ngsl * self.h, (mx - 1 - self.ngsl) * self.h, mx)
        return x

    def y0(self):
        """
        Y axis, having y[0] = -ngsl.

        """
        my = self.ny + 2 * self.ngsl
        y = np.linspace(-self.ngsl * self.h, (my - 1 - self.ngsl) * self.h, my)
        return y

    def map(self, func, x=None, y=None):
        """
        Generate topography data from function func(x, y)

        Args:
            func: Function handle

        Returns:
            z: A 1-D array containing (nx + 2 * ngsl) * (ny + 2 * ngsl) values,
                one per grid point. The y-direction is treated as the contiguous
                (fast) direction.
                


        """
        mx = self.nx + 2 * self.ngsl
        my = self.ny + 2 * self.ngsl
        z = np.zeros(mx * my).astype(np.float32)
        if x is None:
            x = self.x0()
        if y is None:
            y = self.y0()
        for i in range(mx):
            for j in range(my):
                z[j + my * i] = func(x[i], y[j])
        return z

    def write(self, z, filename):
        """
        Write topography data to binary file.

        Args:
            z : Topography data to write. This array can either be a nx x ny
                (2D) array or a 1D array in which the y-direction is the fast
                direction.

        """
        header = np.array([self.nx, self.ny, self.ngsl]).astype(np.int32)

        if len(z.shape) == 2:
            z_out = z.flatten()
        else:
            z_out = z
        
        mx = self.nx + 2 * self.ngsl
        my = self.ny + 2 * self.ngsl
        assert z_out.shape[0] == mx * my


        with open(filename, "wb") as fh:
            header.tofile(fh)
            z_out.astype(np.float32).tofile(fh)

    def write_grid(self, filename):
        """
        Writes the (x,y) coordinates to a csv ascii file.

        """

        X, Y = np.meshgrid(self.x0(), self.y0())
        arr = np.vstack((X.flatten(), Y.flatten())).T
        np.savetxt(filename, arr, delimiter=',')



    def load_xyz(self, filename):
        """
        Load topography data stored in tab-delimited ASCII file format.

        x_00    y_00    z_00
        x_01    y_01    z_01
          .
          .
          .

        """
        C = np.loadtxt(filename, delimiter='\t')
        x = C[:,0]
        y = C[:,1]
        z = C[:,2]
        assert np.all(np.isfinite(x))
        assert np.all(np.isfinite(y))
        assert np.all(np.isfinite(z))
        size = (self.nx + 2 * self.ngsl, self.ny + 2 * self.ngsl)
        X = np.reshape(x, size).astype(np.float32)
        Y = np.reshape(y, size).astype(np.float32)  
        Z = np.reshape(z, size).astype(np.float32)
        return X, Y, Z

    def load_xyz_bin(self, filename, nz):
        """
        Load curvilinear grid data stored in the binary (mesh) file format.

        Args:
            filename: Binary file to read.
            nz: Number of grid points in the z-direction

        Returns:
            X, Y, Z : np.Array of size nx x ny x nz. The operation `X[i,j,k]`
            accesses the x-coordinate of the grid point (i, j, k), etc.

        Notes:
            This binary file contains Cartesian coordinates (x_ijk, y_ijk,
            z_ijk), where the index i is the fastest index and (0, 0, 0) is
            positioned at the top of the free surface in the bottom left corner.  

            x_000 y_000 z_000 
            x_100 y_100 z_100
            .
            .
            .

            Another way to view this file is that one writes a depth slice of
            size 3 x nx x ny to the binary file. The first slice starts at the
            free surface and the next slice is one step below it.

        Warning: 
            This function should only be used for small test problems as it
            consumes significant amounts of memory: 
            `3 x nx x ny x x nz x sizeof(float)`

        """
        xyz = np.fromfile(filename, dtype=np.float32)
        XYZ = xyz.reshape((3, self.nx, self.ny, nz), order='F')
        X = XYZ[0, :, :, :] 
        Y = XYZ[1, :, :, :] 
        Z = XYZ[2, :, :, :] 

        return X, Y, Z

    def write_xyz(self, Z, filename):
        """
        Write ASCII file in the format described in `load_xyz`.
        """
        X, Y = np.meshgrid(self.x0(), self.y0())
        arr = np.vstack((X.flatten(), Y.flatten(), Z.flatten())).T
        np.savetxt(filename, arr, delimiter='\t')

    def get_XY(self):
        """
        Return the grid points (x_i, y_j) as 2D arrays
        """
        X, Y = np.meshgrid(self.x(), self.y())
        return X.astype(np.float32), Y.astype(np.float32)

    def reshape(self, z):
        """
        Reshape 1D array into 2D array. The 1D array assumes the organization
        described by the function `map`.
        """
        size = (self.nx + 2 * self.ngsl, self.ny + 2 * self.ngsl)
        return np.reshape(z, size).astype(np.float32)

    def imshow(self, z, padding=True):
        """
        Wrap matplotlib's imshow to view the topography map.

        Args:
            z: Topography map (m x n np.array) 
            padding: Show padded regions. The border between the padded and
                unpadded region is shown in a white line.

        """
        import matplotlib.pyplot as plt
        x0 = self.x0()
        y0 = self.y0()
        if not padding:
            plt.imshow(z[self.ngsl:-self.ngsl-1, self.ngsl:-self.ngsl-1],
                    extent=[x0[self.ngsl], x0[-self.ngsl-1], y0[self.ngsl],
                        y0[-self.ngsl-1]])
        else:
            plt.imshow(z, extent=[x0[0], x0[-1], y0[0], y0[-1]])
        plt.xlabel('X Axis (m)')
        plt.ylabel('Y Axis (m)')

    def box(self, dist, style='w'):
        """
        Draw a bounding box at a L1 distance `dist` away from the boundary.

        """
        import matplotlib.pyplot as plt
        x0 = self.x0()
        y0 = self.y0()
        plt.plot([x0[dist], x0[-dist-1]], [y0[dist],
                  y0[dist]], style)
        plt.plot([x0[dist], x0[-dist-1]], [y0[-dist-1],
                  y0[-dist-1]], style)
        plt.plot([x0[dist], x0[dist]], [y0[dist],
                  y0[-dist-1]], style)
        plt.plot([x0[-dist-1], x0[-dist-1]], [y0[dist],
                  y0[-dist-1]], style)
