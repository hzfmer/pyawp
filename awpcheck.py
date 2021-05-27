"""usage: awpcheck <pmcl3d ... >
Check the correctness of a AWP configuration.


"""

import os
import sys
import pyawp

def main():
    if len(sys.argv) == 1:
        print(__doc__)
    exe = sys.argv[1]
    args = sys.argv[2:]
    call = exe + ' ' + ' '.join(args)
    c = pyawp.command.Command(call)
    pyawp.check.check_paths(c.dict())
    print("calling:", call)
    #os.system(call)
