import pyawp
from pyawp.command import Command

def test_command():
 call = """${AWP_WORK}/pmcl3d   -X 120 -Y 120 -Z 64 -x 1 -y 1   --TMAX 1 --DH 100
 --DT 0.001   --NSRC 1 --NST 4000   --NVAR 5   -s 0   --IFAULT 1   --MEDIASTART
 0   --READ_STEP 2000 --WRITE_STEP 1000   --NBGX 1 --NEDX 120 --NSKPX 1   --NBGY
 1 --NEDY 120 --NSKPY 1   --NBGZ 1 --NEDZ 1 --NSKPZ 1   --NTISKP 1   --INSRC
 input/source   --INVEL input/material   --NVE 1   --NGRIDS 1   --ND 20 -c
 output/serial/ckp -o output/serial"""
 c = pyawp.command.Command(call)
 assert c['X'] == 120.0
 assert c['Y'] == 120.0
 assert c['Z'] == 64.0
 assert c['INSRC'] == 'input/source'

def test_parse():
    call = ["source", "a=b", "c=1.0", "d=-0.4", "file=/path/to/file"]
    d = pyawp.command.parse(call)
    assert d['a'] == 'b'
    assert d['c'] == '1.0'
    assert d['d'] == '-0.4'
    assert d['file'] == '/path/to/file'
