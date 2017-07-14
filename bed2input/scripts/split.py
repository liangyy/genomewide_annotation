import argparse
parser = argparse.ArgumentParser(prog='split.py', description='''
    Split the input file into [nchunk] files
''')
parser.add_argument('--input')
parser.add_argument('--nchunk', type=int)
parser.add_argument('--outdir')
args = parser.parse_args()

import sys
if '../scripts/' in sys.path:
    sys.path.insert(0, '../scripts/')
import my_python

size = int(my_python.get_number_of_lines(args.input) / nchunk)

line_counter = 0
file_counter = 0
with lines as open(args.input, 'r'):
    o_name = '{outdir}/chunk_{i}.raw'.format(outdir=args.outdir, i=file_counter)
    file_counter += 1
    o = open(o_name, 'w')
    for l in lines:
        o.write(l)
        line_counter += 1
        if line_counter >= size and line_counter < args.nchunk:
            o_name = '{outdir}/chunk_{i}.raw'.format(outdir=args.outdir, i=file_counter)
            file_counter += 1
            o.close()
            o = open(o_name, 'w')
            line_counter = 0
o.close()
