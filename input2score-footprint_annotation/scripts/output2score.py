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
import numpy as np

input_score = pd.read_table(args.input_score, compression='gzip', header=0,
    usecols=[0, 3, 8, 9],
    dtype={'SNP.ID': np.int32,
        'Motif.ID': str,
        'LogRatioPrior.Ref': np.float64,
        'LogRatioPrior.Alt': np.float64})
        # 'Motif.Chr': str})
        # 'Motif.Start', np.int32,
        # 'Motif.End': np.int32})

if input_score.shape[0] == 0:
    temp = pd.DataFrame([])
    temp.to_csv(args.output,
        sep='\t',
        compression='gzip',
        header=False)
    sys.exit()
input_snp = pd.read_table(args.input_snp, header=None, compression='gzip',
    converters={'Chr': str,
        'Start': np.int32,
        'End': np.int32,
        'Allele1': str,
        'Allele2': str,
        'ID': np.int32,
        'Motif': str,
        'Motif.Start': np.int32,
        'Motif.End': np.int32},
    usecols=[0, 1, 2, 3, 4, 5, 9],
    names=['Chr', 'Start', 'End', 'Allele1', 'Allele2', 'ID', 'Motif', 'Motif.Start'])
input_snp['Motif.Start'] = input_snp['Motif.Start'] - 1
# input_snp['Motif.End'] = input_snp['Motif.End'] - 1
feature_a1 = input_score['LogRatioPrior.Ref']
feature_a2 = input_score['LogRatioPrior.Alt']
feature = [ ','.join([str(a), str(b)]) for (a, b) in zip(feature_a1, feature_a2) ]
input_snp['LogRatioPrior'] = feature
input_snp['Allele'] = input_snp.apply(lambda x: ','.join([x['Allele1'], x['Allele2']]), axis=1)

grouped = input_snp.groupby(['Chr', 'Start', 'End', 'Motif', 'Motif.Start'], sort=False)
feature_agg = grouped.agg({
    'Allele' : lambda x: ','.join(x),
    'LogRatioPrior' : lambda x: ','.join(x)
})
feature_agg.to_csv(args.output,
    sep='\t',
    compression='gzip',
    header=False)
