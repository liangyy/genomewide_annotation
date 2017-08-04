import argparse
parser = argparse.ArgumentParser(prog='output2score.py', description='''
    Given the DeepVariantPrediction output (raw output: score in hdf5)
''')
parser.add_argument('--input_passed')
parser.add_argument('--input_allele1')
parser.add_argument('--input_allele2')
parser.add_argument('--out_prefix')
parser.add_argument('--labels', nargs='+')
parser.add_argument('--idxs', nargs='+', type=int)
args = parser.parse_args()

import sys
if '../scripts/' not in sys.path:
    sys.path.insert(0, '../scripts/')
import my_python
import pandas as pd
import h5py

allele1_score = my_python.read_hdf5_by_name(args.input_allele1, 'y_pred')
allele2_score = my_python.read_hdf5_by_name(args.input_allele2, 'y_pred')
passed_list = pd.read_table(args.input_passed, header=None, names=['Chr', 'Start', 'End', 'Info'], usecols=[0, 1, 2, 3])
passed_list['ID'] = passed_list.apply(lambda x: int(x['Info'].split(':')[0]), axis=1)
passed_list['Allele'] = passed_list.apply(lambda x: ','.join(x['Info'].split(':')[1:3]), axis=1)

for i in range(len(args.labels)):
    label_name = args.labels[i]
    label_idx = args.idxs[i] - 1  # Input is 1-based
    feature_a1 = allele1_score[:, label_idx]
    feature_a2 = allele2_score[:, label_idx]
    feature = [ ','.join([str(a), str(b)]) for (a, b) in zip(feature_a1, feature_a2) ]
    passed_list[label_name] = feature
    grouped = passed_list.groupby(['Chr', 'Start', 'End'], sort=False)
    feature_agg = grouped.agg({
        'Allele' : lambda x: ','.join(x),
        label_name : lambda x: ','.join(x)
    })
    feature_agg.to_csv('{prefix}.{feature}.score.gz'.format(prefix=args.out_prefix, feature=label_name),
        sep='\t',
        compression='gzip',
        header=False)
