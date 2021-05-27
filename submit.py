"""
Module that contains submit scripts and templates for different systems.

"""
def submit(system, job_type):
    """
    Return function handle to function that generates submit script for a
    particular system.

    Args:
        system(string): System to generate submission script for.
        job_type(string): Type of job to generate ('GPU', 'CPU')

    """
    if system == 'summit' and job_type == 'run':
        return summit
    if system == 'summit' and job_type == 'material':
        return summit_material
    else:
        raise ValueError('Unknown system: %s' % system)

def write(job_name, job, system, ext, verbose=1):
    """
    Write job submission script to disc.

    Args:
        job_name(string): Filename excluding extension.
        job(string): Contents of submission script.
        system(string): System to generate submission script for.
        ext(string): File extension.
        verbose(bool, optional): Show output.

    """

    job_out = '%s.%s.%s' % (job_name, system, ext)
    with open(job_out, 'w') as fh:
        fh.write(job)
        print("Writing:", job_out)

def summit(jobname, path, px, py, clear=True, build=True, time='2:00',
           project='GEO112'):
    """
    Build job submission script for summit

    Args:
        jobname: Job submission script name (also name of stdout and stderr
            output files)
        px : Number of GPUs in x
        py : Number of GPUs in y

    Returns:
        out(string) : Job submission script
        ext : File extension

    """
    nodes = max(int(px * py / 6), 1)
    out = []
    out += ['#!/bin/bash']
    out += ['# Begin LSF Directives']
    out += ['#BSUB -P %s' % project]
    out += ['#BSUB -W %s' % time]
    out += ['#BSUB -nnodes %d'%nodes]
    out += ['#BSUB -alloc_flags "gpumps smt1"']
    out += ['#BSUB -J %s' % jobname]
    out += ['#BSUB -o %s.out' % jobname]
    out += ['#BSUB -e %s.err' % jobname]
    out += ['source vars.sh']
    out += ['module load cuda']
    out += ['cd $AWP_BENCH_WORK/$base']
    if build:
        out += ['bash build.sh summit']
    if clear:
        out += ['rm -r output/*']
    res = px * py   
    # Can at most use 6 GPUs per node
    res_per_node = min(res, 6)
    out += ['jsrun -n %d -a 3 -c 3 -g 1 -r %d -d cyclic bash %s/%s.sh' %
            (res, res_per_node, path, jobname)]
    out = '\n'.join(out) + '\n'
    ext = 'lsf'
    return out, ext

def summit_material(jobname, path, px, py, time='2:00',
           project='GEO112'):
    """
    Build job submission script for summit

    Args:
        jobname: Job submission script name (also name of stdout and stderr
            output files)
        px : Number of CPUs in x
        py : Number of CPUs in y

    Returns:
        out(string) : Job submission script
        ext : File extension

    """
    nodes = max(int(px * py / 42), 1)
    out = []
    out += ['#!/bin/bash']
    out += ['# Begin LSF Directives']
    out += ['#BSUB -P %s' % project]
    out += ['#BSUB -W %s' % time]
    out += ['#BSUB -nnodes %d'%nodes]
    out += ['#BSUB -J %s' % jobname]
    out += ['#BSUB -o %s.out' % jobname]
    out += ['#BSUB -e %s.err' % jobname]
    out += ['source vars.sh']
    out += ['cd $AWP_BENCH_WORK/$base']
    res = px * py
    res_per_node = min(res, 42)
    out += ['jsrun -n %d -a 1 -c 1 -r %d bash %s/%s.sh' %
            (res, res_per_node, path, jobname)]
    out = '\n'.join(out) + '\n'
    ext = 'lsf'
    return out, ext
