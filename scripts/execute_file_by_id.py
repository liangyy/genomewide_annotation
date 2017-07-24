import argparse
parser = argparse.ArgumentParser(prog='execute_file_by_id.py', description='''
    Execute file by the given ID list.
''')
parser.add_argument('--prefix', help='''
    Prefix of filename (exclude dirname)
''')
parser.add_argument('--suffix')
parser.add_argument('--execute')
parser.add_argument('--id_list', help = 'Separate by ,')
args = parser.parse_args()

import os

ids = [ i for i in args.id_list.split(',') ]

for idx in ids:
	filename = '{prefix}{idx}{suffix}'.format(prefix=args.prefix, suffix=args.suffix, idx=idx)
	cmd = '{exe} {file}'.format(exe=args.execute, file=filename)
	os.system(cmd)
