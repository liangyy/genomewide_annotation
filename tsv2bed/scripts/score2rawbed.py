import argparse
parser = argparse.ArgumentParser(prog='score2rawbed.py', description='''
    Given the output of input2score-METHOD module, output the BED file by
    applying the threshold
''')
parser.add_argument('--input')
parser.add_argument('--output')
parser.add_argument('--method')
parser.add_argument('--percentage', type=float, help='''
    Top `percentage` percent (bigger ones have higher percentage)
''')
args = parser.parse_args()

import sys
if '../scripts/' not in sys.path:
    sys.path.insert(0, '../scripts/')
import my_python
import pandas as pd
import numpy as np
import h5py

input_table = pd.read_table(args.input, header=None, nrows=2)
scores_n_alleles = input_table[[-2, -1]]
if scores_n_alleles[0, 0].split(',')[0] in ['A', 'T', 'G', 'C', 'N']:
    allele_col = -2
    score_col = -1
else:
    allele_col = -2
    score_col = -1
calculator_cls = ScoreCalculater()
calculator = getattr(calculator_cls, args.method)
all_scores = []
positions = []
with f as open(args.input, 'r'):
    for i in f:
        i = i.split('\t')
        scores = i[score_col]
        alleles = i[allele_col]
        positions.append(i[:3])
        all_scores.append(calculator(scores, alleles))
threshold = np.percentile(all_scores, args.percentage * 100)
positions = pd.DataFrame(positions)
all_scores = pd.DataFrame(all_scores)
passed_idx = all_scores[all_scores.max(axis=1) >= threshold].index.tolist()
passed_positions = positions.ix[passed_idx]
pd.to_csv(args.output,
    sep='\t',
    compression='gzip',
    header=False)
