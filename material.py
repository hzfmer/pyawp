from pyawp import utils
import os
import numpy as np

class Material(object):

    def __init__(self, config, **kwargs):
        self.config = config
        self.settings = get_defaults(config)

        for arg in kwargs:
            self.settings[arg] = kwargs[arg]

        self.set_resolution()
        self.init_profiles()

    def is_serial(self):
        if self.num_processes == 1:
            return True
        else:
            return False

    def file(self, param, ext=None):
        if not ext:
            ext = self.settings.ext

        return os.path.join(self.settings['file_material'] + '_' + self.settings["file_" + param]
                + ext)

    def output_file(self, filename):
        return filename + "_%d" % self.settings.grid_num

    def init_profiles(self, rho=2800, cp=6000, cs=3000, qp=1e10, qs=1e10):
        grid_num = self.settings.grid_num
        nz = self.settings.nz
        self.profiles = utils.Struct()
        self.profiles.rho = np.ones((nz,))*rho
        self.profiles.cp = np.ones((nz,))*cp
        self.profiles.cs = np.ones((nz,))*cs
        self.profiles.qp = np.ones((nz,))*qp
        self.profiles.qs = np.ones((nz,))*qs

    def write_profiles(self, project=''):
        if self.topo_auto_adjust:
            self.topo_adjust()
        for param in self.settings.variables:
            filename = project + self.file(param)
            np.savetxt(filename, self.profiles[param], delimiter="\n")

    def write_config(self, filename, ext=".ini"):
        out  = "[media]         \n"
        out += "filename=%s     \n" % self.output_file(
                                      self.settings.file_material)
        out += "x=%d            \n" % self.settings.px
        out += "y=%d            \n" % self.settings.py
        out += "nx=%d           \n" % self.settings.nx
        out += "ny=%d           \n" % self.settings.ny
        out += "nvars=%d        \n" % self.settings.nvars
        out += "serial=%d       \n" % self.is_serial()
        out += "layers = layer1 \n"
        out += "                \n"
        out += "[layer1]        \n"
        out += "nz = %d         \n" % self.settings.nz
        for param in self.settings.variables:
            out += "%s  = %s        \n" % (param, self.file(param))
        out += "format = ascii  \n"
        self.configname = self.get_ini_filename(filename, ext=ext)
        fh = open(self.get_ini_filename(filename, ext=ext), 'w')
        fh.write(out)
        fh.close()
        return out

    def write_launch(self, filename, path="", ext=".sh", verbose=0):
        cfg = self.config.settings
        out = "%s\n" % cfg.shell
        out += "%s %s\n" % (cfg.material_exe, self.configname)
        output_file = os.path.join(path, filename + ext)
        fh = open(output_file, "w")
        fh.write(out)
        fh.close()
        if verbose:
            print("Writing: %s" % output_file)

    def get_ini_filename(self, filename, ext=".ini"):
        return filename + self.config.topo_str + "_%d"%self.settings.grid_num +\
               ext

    def build(self, filename, exe="awp-media", ext=".ini"):
        import subprocess
        mpi = self.settings.mpi
        subprocess.run([mpi, "-np", str(self.num_processes), exe, 
                        self.get_ini_filename(filename, ext=ext)])

    @property
    def mu(self):
        return self.profiles.rho*self.profiles.cs**2

    @property
    def lame(self):
        return self.profiles.rho*self.profiles.cp**2 - 2*self.mu

    @property
    def num_processes(self):
        return self.settings.px*self.settings.py

    @property
    def cmin(self):
        return min(self.profiles.cs)

    @property
    def cmax(self):
        return max(self.profiles.cp)

    def __str__(self):
        return str(vars(self.settings))

    def topo_adjust(self):
        """
        Adjust profiles when topography is enabled
        """
        if not self.settings.use_topo:
            return

    def set_resolution(self):
        grid_num = self.settings.grid_num
        num_grids = self.settings.num_grids
        self.settings.nx = self.settings.nx*3**(num_grids-grid_num-1)
        self.settings.ny = self.settings.ny*3**(num_grids-grid_num-1)
        self.settings.nz = self.settings.nz[grid_num]

    @property
    def topo_auto_adjust(self):
        return self.settings.topo_auto_adjust

def get_defaults(cfg):
        settings = cfg.settings
        nz = settings.nz
        mat = utils.Struct()
        mat.file_rho = "rho"
        mat.file_cp = "cp"
        mat.file_cs = "cs"
        mat.file_qp = "qp"
        mat.file_qs = "qs"
        mat.ext = ".txt"
        mat.project = "default"
        mat.path = settings.input_path
        mat.nvars = settings.nvar
        mat.nx = settings.nx
        mat.ny = settings.ny
        mat.nz = settings.nz
        mat.px = settings.px
        mat.py = settings.py
        mat.mpi = settings.mpi
        mat.use_topo = settings.use_topo
        mat.topo_auto_adjust = settings.topo_auto_adjust
        mat.file_material = cfg.file(settings.material)
        mat.grid_num = 0
        mat.num_grids = settings.ngrids
        mat.variables = ["rho", "cs", "cp", "qp", "qs"]

        return mat


