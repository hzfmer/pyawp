class Command:
    """
    Parses the command line arguments that are supplied to pmcl3d.
     
    """

    def __init__(self, args):
        """
        Initialize Command.

        Args: 

            args : List of command line arguments. 

            parse : If `parse = `true` the awp input file is parsed
                automatically.  Otherwise, you need to call ``parse()`` before
                accessing any of the parameters. 

        """
        if (isinstance(args, str)):
            args = argsplit(args)
        self.parameters = self.defaults()
        self.parse(args)

    def parse(self, args):
        """
        Parse command line arguments.

        Args:
            args : List of command line arguments.

        """
        self.exe = args[0]
        for i, argi in enumerate(args):
            if i % 2 == 0:
                continue
            val = args[i+1]
            try:
                val = float(val)
            except:
                pass
            self.parameters[args[i].strip('-')] = val

    def __getitem__(self, parameter):
        """
        Return parsed parameter value.

        Args:

            parameter : Name of parameter to return value for.

        Returns: 
            The value of the selected parameter if it is found, and raises an
            exception otherwise.

        """

        return self.parameters[parameter]

    def __setitem__(self, parameter, value):
        """
        Set parameter value

        Args:

        parameter : Name of parameter to set value for.
        value : The value to set.

        """
        self.parameters[parameter] = value

    def dict():
        out = {}
        for key in self.parameters:
            out[key] = self.parameters[value]
        return out

    def x(self):
        return self.size('X')
    
    def y(self):
        return self.size('Y')
    
    def z(self):
        return self.size('Z')

    # Compute the size of the output data in the direction 'dim'
    # This function takes start, end, and striding into account
    def size(self, dim='X'):

        if not dim == 'X' and not dim == 'Y' and not dim == 'Z':
            raise ValueError("Undefined dimension. Expected, 'X', 'Y', or 'Z'.")

        if not self._parsed:
            raise ValueError("Unable to determine dimensions before parsing.")

        defs = self.defaults()
        
        # Parameters to load
        params = ('NBG' + dim, 'NED' + dim, 'NSKP' + dim)

        # Loaded parameters values
        val = [0, 0, 0]

        for i in range(0, 3):
            # Get assigned value or default
            if params[i] in self.parameters:
                val[i] = self.parameters[params[i]]
            else:
                val[i] = defs[params[i]]

        if val[1] == -1:
            val[1] = self.parameters[dim]

        
        # Take into account that output data size is specified using one-indexing
        one_index = 1
        
        # Size = max - min / stride. Minimum size is 1.
        return max(int(math.floor( (val[1] - val[0] + one_index)/val[2] )), 1)


    # Returns the default values for some of the parameters
    def defaults(self):
        d = {}

        d['NBGX']       =  1
        d['NEDX']       = -1  
        d['NSKPX']      =  1
        d['NBGY']       =  1
        d['NEDY']       = -1  
        d['NSKPY']      =  1
        d['NBGZ']       =  1
        d['NEDZ']       =  1   
        d['NSKPZ']      =  1

        return d

def argsplit(instr):
    """
    Convert arguments in string format to list.

    """
    args = instr.rstrip().split(' ')
    newargs = []
    for arg in args:
        if arg != '' and arg != ' ':
            newargs.append(arg.rstrip())
    return newargs

def parse(argv):
    """
    Convert arguments key=value into dictionary.

    """
    argv=argv[1::]
    out = {}
    for a in argv:
        k, v = a.split('=')
        try:
            v= float(v)
        except:
            pass
        out[k] = v
    return out

def write_awp_input(filename, exe, args, verbose=True):
    with open(filename, "w") as f:
        f.write("%s " % exe)
        for arg in args:
            val = args[arg]
            if val == '':
                continue
            if arg == 'X' or arg == 'Y' or arg == 'Z' or arg == 'x' or arg ==\
            'y' or arg == 'NTISKP' or arg == 'NSRC' or arg == 'MEDIASTART' or\
            arg == 'NVE' or arg == 'ND':
                try:
                    val = int(val)
                except:
                    val = ','.join(['%d' % vi for vi in val])

            if len(arg) == 1:
                f.write("-%s %s " % (arg, str(val)))
            else:
                f.write("--%s %s " % (arg, str(val)))
        f.write("\n")
    if verbose:
        print("Wrote AWP input file: %s" % filename)
