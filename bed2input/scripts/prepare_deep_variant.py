import argparse
parser = argparse.ArgumentParser(prog='prepare_deep_variant.py', description='''
    Given the split bed file, output the input ready for DeepVariantPrediction
''')
parser.add_argument('--input_seq')
parser.add_argument('--log')
args = parser.parse_args()

bases = ['A', 'C', 'G', 'T']

# order = {
#     'A': ['A', 'C', 'G', 'T'],
#     'C': ['C', 'G', 'T', 'A'],
#     'G': ['G', 'T', 'A', 'C'],
#     'T': ['T', 'A', 'C', 'G']
# }

import gzip

o = open(args.log, 'w')

with gzip.open(args.input_seq, 'rb') as f:
    file_content = f.read().decode()
    for l in file_content.split('\n'):
        l = l.strip().split(' ')
        chrm = l[0]
        start = int(l[1])
        end = int(l[2])
        seq = l[3]
        for i in range(len(seq)):
            ref = seq[i].upper()
            for char in bases:
                if char is ref:
                    continue
                else:
                    line = '{chrm}\t{start}\t{end}\t{ref}\t{alt}\n'.format(chrm=chrm, start=start + i, end=start + i + 1)
                    print(line)
            if start + i != end:
                o.write('Wrong number of SNVs in {line}'.format(line='--'.join(l)))
o.close()
