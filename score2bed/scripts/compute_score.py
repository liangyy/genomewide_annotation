import argparse
parser = argparse.ArgumentParser(prog='compute_score.py', description='''
    Given the output of input2score-METHOD module (merged file), output the
    computed scores
''')
parser.add_argument('--input')
parser.add_argument('--output')
parser.add_argument('--calculator')
parser.add_argument('--extra_info')
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
extra_col = None
if args.extra_info != '-1':
    extra_col = args.extra_info.split(',')
    extra_col = [ int(i) for i in extra_col ]
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
        
        extra_info = []
        if extra_col is not None:
            # position = i[:3]
            # extra_info = []
            for e in extra_col:
                extra_info.append(i[e - 1])
        
        position = i[:3]

        this_scores, ref_score = calculator(scores)
        for s in range(len(this_scores)):
            # if extra_col:
            this_line = position + [ref, alleles[s + 1], this_scores[s], ref_score] + extra_info
            # this_line = position + [ref, alleles[s + 1], this_scores[s], ref_score]
            all_scores.append(this_line)

all_scores = pd.DataFrame(all_scores)
all_scores.to_csv(args.output,
    sep='\t',
    compression='gzip',
    header=False, index=False)
