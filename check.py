import os

def check_path(args, mkdir=0):
    path = ['c', 'o']
    for key in path:
        ensure_dir(args[key])

def ensure_dir(path, mkdir=0):
    if os.path.exists(path):
        return 1
    else:
        if mkdir:
            os.makedirs(path)
        return 0

    

