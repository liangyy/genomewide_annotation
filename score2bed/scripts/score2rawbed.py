import argparse
parser = argparse.ArgumentParser(prog='score2rawbed.py', description='''
    Given the output of input2score-METHOD module, output the BED file by
    applying the threshold
''')
parser.add_argument('--input')
parser.add_argument('--output')
parser.add_argument('--calculator')
parser.add_argument('--filter')
parser.add_argument('--param', help='''
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
import gzip

input_table = pd.read_table(args.input, header=None, nrows=2)
scores_n_alleles = input_table.iloc[:, [-2, -1]]
if scores_n_alleles.iloc[0, 0].split(',')[0] in ['A', 'T', 'G', 'C', 'N']:
    allele_col = -2
    score_col = -1
else:
    allele_col = -2
    score_col = -1
calculator_cls = my_python.ScoreCalculater()
calculator = getattr(calculator_cls, args.calculator)
filter_cls = my_python.Filter()
filterr = getattr(filter_cls, args.filter)
all_scores = []
all_original_scores = []
positions = []

with gzip.open(args.input, 'r') as f:
    for i in f:
        i = i.decode()
        i = i.split('\t')
        scores = i[score_col]
        alleles = i[allele_col]
        positions.append(i[:3])
        all_scores.append(calculator(scores))
        all_original_scores.append([ float(i) for i in scores.split(',') ])

passed_idx = filterr(all_scores, all_original_scores, args.threshold)
positions = pd.DataFrame(positions)
passed_positions = positions.ix[passed_idx]
pd.to_csv(args.output,
    sep='\t',
    compression='gzip',
    header=False)
