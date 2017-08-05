import argparse
parser = argparse.ArgumentParser(prog='output2score.py', description='''
    Given the footprint_annotation output (raw output: score in bed,
    idx in tab-separated gz)
''')
parser.add_argument('--input_score')
parser.add_argument('--input_snp')
parser.add_argument('--output')
args = parser.parse_args()

import sys
if '../scripts/' not in sys.path:
    sys.path.insert(0, '../scripts/')
import my_python
import pandas as pd

input_snp = pd.read_table(args.input_snp, header=0, usecols=[0, 3, 4, 5, 6, 7, 8, 9])
input_score = pd.input_score(args.input_score, header=None, names=['Chr', 'Start', 'End', 'Allele1', 'Allele2', 'ID', 'Motif'], usecols=[0, 1, 2, 3, 4, 5, 9])
feature_a1 = input_snp['LogRatioPrior.Ref']
feature_a2 = input_snp['LogRatioPrior.Alt']
feature = [ ','.join([str(a), str(b)]) for (a, b) in zip(feature_a1, feature_a2) ]
input_score['LogRatioPrior'] = feature
combined = pd.concat([input_score, input_snp.ix[:, [-4, -2, -1]], axis=1, ignore_index=True)
grouped = combined.groupby(['Chr', 'Start', 'End', 'Motif'], sort=False)
feature_agg = grouped.agg({
    'Allele' : lambda x: ','.join(x),
    'LogRatioPrior' : lambda x: ','.join(x)
})
feature_agg.to_csv('{prefix}.{feature}.score.gz'.format(prefix=args.out_prefix, feature=label_name),
    sep='\t',
    compression='gzip',
    header=False)
