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
    c = 0
    for l in file_content.split('\n'):
        if len(l) == 0:
            continue
        l = l.strip().split('\t')
        temp = l[0].split(':')
        chrm = temp[0]
        temp = temp[1].split('-')
        start = int(temp[0])
        end = int(temp[1])
        seq = l[1]
        for i in range(len(seq)):
            ref = seq[i].upper()
            for char in bases:
                if char == ref:
                    continue
                else:
                    line = '{chrm}\t{start}\t{end}\t{ref}\t{alt}'.format(chrm=chrm, start=start + i, end=start + i + 1, ref=ref, alt=char)
                    print(line)
        if start + i + 1 != end:
            o.write('Wrong number of SNVs in {line}\n'.format(line='--'.join([chrm, str(start), str(end)])))
o.close()
