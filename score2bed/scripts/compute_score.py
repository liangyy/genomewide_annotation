import argparse
parser = argparse.ArgumentParser(prog='compute_score.py', description='''
    Given the output of input2score-METHOD module (merged file), output the
    computed scores
''')
parser.add_argument('--input')
parser.add_argument('--output')
parser.add_argument('--calculator')
args = parser.parse_args()

import sys
if '../scripts/' not in sys.path:
    sys.path.insert(0, '../scripts/')
import my_python
import pandas as pd
import numpy as np
import h5py
import gzip

calculator_cls = my_python.ScoreCalculater()
calculator = getattr(calculator_cls, args.calculator)
all_scores = []
# positions = []

with gzip.open(args.input, 'r') as f:
    counter = 0
    for i in f:
        counter += 1
        # print(counter)
        i = i.decode()
        i = i.split('\t')
        if i[-1].split(',')[0] in ['A', 'T', 'G', 'C', 'N']:
            allele_col = -1
            score_col = -2
        else:
            allele_col = -2
            score_col = -1
        scores = i[score_col]
        alleles = i[allele_col].strip().split(',')
        ref = alleles[0]

        position = i[:3]

        this_scores = calculator(scores)
        for s in range(len(this_scores)):
            this_line = position + [ref, alleles[s + 1], this_scores[s]]
            all_scores.append(this_line)

all_scores = pd.DataFrame(all_scores)
all_scores.to_csv(args.output,
    sep='\t',
    compression='gzip',
    header=False, index=False)
