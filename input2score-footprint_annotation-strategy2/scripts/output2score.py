import argparse
parser = argparse.ArgumentParser(prog='output2score.py', description='''
    Given the footprint_annotation/strategy2/annotation output (tab.gz with log odds ratio of prior)
''')
parser.add_argument('--input_score')
parser.add_argument('--output')
args = parser.parse_args()

import sys
import pandas as pd

snvs = pd.read_table(args.input_score, sep = '\t', compression = 'gzip', header = None, names = ['chr', 'start', 'end', 'a1', 'a2', 'strand', 's1', 's2', 'motif'])

if snvs.shape[0] == 0:
    temp = pd.DataFrame([])
    temp.to_csv(args.output,
        sep='\t',
        compression='gzip',
        header=False)
    sys.exit()

snvs['logratioprior'] = snvs.apply(lambda x: ','.join([x['s1'], x['s2']]), axis=1)
snvs['allele'] = snvs.apply(lambda x: ','.join([x['a1'], x['a2']]), axis=1)

grouped = snvs.groupby(['chr', 'start', 'end', 'strand', 'motif'], sort=False)
feature_agg = grouped.agg({
    'allele' : lambda x: ','.join(x),
    'logratioprior' : lambda x: ','.join(x)
})
feature_agg.to_csv(args.output,
    sep='\t',
    compression='gzip',
    header=False)
