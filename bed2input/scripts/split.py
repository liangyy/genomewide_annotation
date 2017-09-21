import argparse
parser = argparse.ArgumentParser(prog='split.py', description='''
    Split the input file into [nchunk] files
''')
parser.add_argument('--input')
parser.add_argument('--nchunk', type=int)
parser.add_argument('--outdir')
parser.add_argument('--prefix')
args = parser.parse_args()

import sys
if '../scripts/' not in sys.path:
    sys.path.insert(0, '../scripts/')
import my_python

size = int(my_python.get_number_of_lines(args.input) / args.nchunk)

line_counter = 0
file_counter = 0
with open(args.input, 'r') as lines:
    o_name = '{outdir}/{prefix}.chunk_{i}.raw'.format(outdir=args.outdir, i=file_counter, prefix = args.prefix)
    file_counter += 1
    o = open(o_name, 'w')
    for l in lines:
        o.write(l)
        # print(l)
        line_counter += 1
        if line_counter >= size and file_counter < args.nchunk:
            o_name = '{outdir}/{prefix}.chunk_{i}.raw'.format(outdir=args.outdir, i=file_counter, prefix = args.prefix)
            file_counter += 1
            o.close()
            o = open(o_name, 'w')
            line_counter = 0
o.close()
