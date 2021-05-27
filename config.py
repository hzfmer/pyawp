from pyawp import utils, grid
import os
import numpy as np


class Config(object):

    def __init__(self, *arg, **kwarg):
        self.settings = get_defaults()
        for argi in kwarg:
            self.settings[argi.lower()] = kwarg[argi]

        # Handle config read from launch script
        if 'X' in kwarg:
            self.settings.nx = kwarg['X']

        if 'Y' in kwarg:
            self.settings.ny = kwarg['Y']

        if 'Z' in kwarg:
            self.settings.nz = kwarg['Z']

        if 'DH' in kwarg:
            self.settings.h = kwarg['DH']

        if 'o' in kwarg:
            self.settings.output_path = kwarg['o']

        if 'c' in kwarg:
            self.settings.check_path = os.path.dirname(kwarg['c'])
        
        if 'INSRC' in kwarg:
            self.settings.source = kwarg['INSRC']

        if 'INVEL' in kwarg:
            self.settings.material = kwarg['INVEL']

        if 'INTOPO' in kwarg:
            self.settings.topography = kwarg['INTOPO']
            self.settings.use_topo = False

        if self.settings.check_dirs:
                utils.check_dirs([self.settings.input_path,
                                  self.settings.output_path, 
                                  self.settings.check_path])

        if self.settings.check_grid_variables:
                self.check_grid_variables()

        if self.settings.check_parameters:
                self.check_parameters()

    @property
    def num_proc(self):
        return self.settings.px*self.settings.py*3

    def file(self, filename):
        return self.settings.input_path + "/" + filename + self.topo_str

    def refine(self, grid_num):
        return 3**(self.settings.ngrids - grid_num - 1)

    def grid_size(self, grid_num):
        gp = lambda x: x*self.refine(grid_num)
        return (gp(self.settings.nx), gp(self.settings.ny),
                self.settings.nz[grid_num])

    def grid_center(self, gridnum=0):
            print("xyz", self.settings.nx, self.settings.ny, self.settings.nz)
            return np.array([
                    self.gridspacing(gridnum) * self.settings.nx / 2, 
                    self.gridspacing(gridnum) * self.settings.ny / 2,
                    self.gridspacing(gridnum) * self.settings.nz[gridnum] / 2])

    def output_size(self, grid_num):
        size_x = len(range(self.settings.nbgx[grid_num]-1,
                           self.settings.nedx[grid_num],
                           self.settings.nskpx[grid_num]))

        size_y = len(range(self.settings.nbgy[grid_num]-1,
                           self.settings.nedy[grid_num],
                           self.settings.nskpy[grid_num]))

        size_z = len(range(self.settings.nbgz[grid_num]-1,
                           self.settings.nedz[grid_num],
                           self.settings.nskpz[grid_num]))
        return (int(size_x), int(size_y), int(size_z))

    def load_data(self, field, grid_num, num=1, verbose=0, normalize=1,
                  center=None):
        """
        Load velocity component data from file.

        Args:
            field: Velocity field component to load ('x', 'y', 'z').
            grid_num: Grid block ID. Top block is `0`.
            num(optional):  file number to load (starts at 1).
            verbose(optional): Give verbose output.
            normalize(optional): Normalize grid points by grid spacing.
            center(optional): Shift grid vectors so that center lies at (0, 0,
                0)

        Returns:
                Struct: Grid vectors (x, y, z) Time vector (t), and data
                (np.array [x, y, z, t])

        """
        write_step = self.settings.write_step
        nsteps = write_step*self.settings.ntiskp

        frame = nsteps*num
        filename = 'S%s_%d_%07d' % (field.upper(), grid_num, frame)
        size = self.output_size(grid_num)
        out = np.fromfile('%s/%s' % (self.output_path, 
                          filename),
                          dtype=self.settings.prec).reshape(write_step, 
                                                            size[2],
                                                            size[1], size[0])
        t = self.settings.dt*np.array(range(nsteps*(num-1), nsteps*num,
                                      self.settings.ntiskp))

        if center is None:
                center = (0, 0, 0)

        if field == 'x':
            x, y, z = grid.vx(self.settings)
        if field == 'y':
            x, y, z = grid.vy(self.settings)
        if field == 'z':
            x, y, z = grid.vz(self.settings)

        if normalize:
                x = x / self.settings.h
                y = y / self.settings.h
                z = z / self.settings.h

        x = x - center[0]
        y = y - center[1]
        z = z - center[2]

        if verbose:
            print("Loaded: %s/%s, number of steps: %d, grid size: [%d, %d, %d], "
                  % (self.output_path, filename, write_step, *size) )

        out_struct = utils.Struct()
        out_struct.data = out.T
        out_struct.t = t
        out_struct.x = x
        out_struct.y = y
        out_struct.z = z
        out_struct.normalize = normalize

        return out_struct

    def check_grid_variables(self):

        variables = ["nbgx",
                     "nedx",
                     "nskpx",
                     "nbgy",
                     "nedy",
                     "nskpy",
                     "nbgz",
                     "nedz", 
                     "nskpz",
                     "nz", 
                     "nsrc"]
        for var in variables:
            self.settings[var] = to_array(self.settings[var], dtype=np.int32)
            try:
                if len(self.settings[var]) != self.settings.ngrids:
                    raise IndexError("%s must be array of length %d"%(var,
                        self.settings.ngrids))
            except:
                raise IndexError("%s must be an array" % var)

    def check_parameters(self):
        ints = ['px', 'py', 'read_step', 'write_step', 'nst', 'ntiskp']
        for inti in ints:
            self.settings[inti] = int(self.settings[inti])

    @property
    def topo_str(self):
        if self.settings.use_topo:
            return self.settings.topo_ext
        else:
            return ""

    def __str__(self):
        return str(vars(self.settings))

    def topo_adjust(self):
        """
        Fix receiver positions when topography is enabled
        """
        if not self.settings.use_topo:
            return
        self.settings.nbgz += 1
        self.settings.nedz += 1

    @property
    def topo_auto_adjust(self):
        return self.settings.topo_auto_adjust

    
    def write_launch(self, filename, path="", ext=".sh", verbose=0,
                     mpi_launch=0):
        if self.topo_auto_adjust:
            self.topo_adjust()

        cfg = self.settings
        out = "%s\n" % self.settings.shell
        if mpi_launch:
            out += "%s -np %d " % (self.settings.mpi, self.num_proc)
        out += "%s " % cfg.exe
        out += "  -X %d -Y %d -Z %s -x %d -y %d " % (cfg.nx, cfg.ny, 
                                                     print_vec(cfg.nz),
                                                     cfg.px, cfg.py)
        out += "  --TMAX %g --DH %g --DT %g " % (cfg.tmax, cfg.h,
                                                 cfg.dt)
        out += "  --NSRC %s --NST %d " % (print_vec(cfg.nsrc), cfg.nst)
        out += "  --NVAR %d " % (cfg.nvar)
        out += "  -s %s " % (cfg.s)
        out += "  --IFAULT %d " % (cfg.ifault)
        out += "  --MEDIASTART %d " % (cfg.mediastart)
        out += "  --READ_STEP %d --WRITE_STEP %d " % (cfg.read_step,
                                                      cfg.write_step)
        out += "  --NBGX %s --NEDX %s --NSKPX %s "  % (
                    print_vec(cfg.nbgx), print_vec(cfg.nedx),
                    print_vec(cfg.nskpx))
        out += "  --NBGY %s --NEDY %s --NSKPY %s " % (
                    print_vec(cfg.nbgy), print_vec(cfg.nedy),
                    print_vec(cfg.nskpy))
        out += "  --NBGZ %s --NEDZ %s --NSKPZ %s " % (
                    print_vec(cfg.nbgz), print_vec(cfg.nedz),
                    print_vec(cfg.nskpz))
        out += "  --NTISKP %d " % cfg.ntiskp
        out += "  --INSRC %s " % self.file(cfg.source)
        out += "  --INVEL %s " % self.file(cfg.material)
        out += "  --NVE %d " % cfg.nve
        out += "  --NGRIDS %d " % cfg.ngrids
        out += "  --ND %d " % cfg.nd
        if cfg.use_topo:
            out += "--INTOPO %s " % self.file(cfg.topography)
        out += "-c %s " % os.path.join(self.check_path, cfg.check_file) 
        out += "-o %s \n" % (self.output_path)
        output_file = os.path.join(path, filename + self.topo_str + ext)
        if verbose:
            print("Writing: %s" % output_file)
        fh = open(output_file, "w")
        fh.write(out)
        fh.close()

    def dump(self, filename, verbose=1):
        import pickle
        output_file = "%s.p" % (filename+self.topo_str)
        if verbose:
            print("Writing %s" % output_file)
        
        pickle.dump(self, open(output_file, "wb"))

    @property
    def output_path(self):
        return self.settings.output_path + self.topo_str

    @property
    def check_path(self):
        return self.settings.check_path + self.topo_str

    def gridspacing(self, grid_num):
        return self.settings.h/self.refine(grid_num)


def get_defaults():
    obj = utils.Struct()
    obj.shell = "#!/usr/bin/bash"
    obj.exe = "pmcl3d"
    obj.material_exe = "awp-media"
    obj.mpi = "mpirun"
    obj.prec = np.float32
    obj.topo_ext = "_topo"
    obj.use_topo = 0
    obj.nx = 128
    obj.ny = 128
    obj.nz = 128
    obj.px = 1
    obj.py = 1
    obj.tmax = 5
    obj.h = 100.0
    obj.dt = 0.005
    obj.ifault = 1
    obj.nsrc = 1
    obj.nst = 4000
    obj.mediastart = 2
    obj.nvar = 5
    obj.read_step = 1000
    obj.write_step = 1000
    obj.nd = 20
    obj.nbgx = 74
    obj.nedx = 74
    obj.nskpx = 400
    obj.nbgy = 64
    obj.nedy = 64
    obj.nskpy = 400
    obj.nbgz = 1
    obj.nedz = 1
    obj.topo_auto_adjust = True
    obj.nskpz = 400
    obj.ntiskp = 1
    obj.nve = 1
    obj.s = 0
    obj.ngrids = 1
    obj.input_path = "input"
    obj.output_path = "output_sfc"
    obj.check_path = "output_ckp"
    obj.check_file = "ckp"
    obj.source = "source"
    obj.material = "material"
    obj.topography = "topography"
    obj.check_dirs = True
    obj.check_grid_variables = True
    obj.check_parameters = True

    return obj


def print_vec(vec):
    try:
        len(vec)
        return ",".join([str(vi) for vi in vec])
    except:
        return str(vec)


def to_array(vec, dtype=np.float):
    try:
        len(vec)
        return np.array(vec, dtype=dtype)
    except:
        return np.array((vec,), dtype=dtype)

