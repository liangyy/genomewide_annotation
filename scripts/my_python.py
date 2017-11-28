import subprocess
import h5py
import numpy as np
import pandas as pd
import os

# From Internet
# https://stackoverflow.com/questions/36133716/how-to-skip-reading-empty-files-with-panda-in-python
def is_non_zero_file(fpath):
    return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False
# END

def get_number_of_lines(filename):
    cmd = 'cat ' + filename + ' | wc -l'
    result = subprocess.check_output(cmd, shell=True)
    nrow = int(result.decode().split('\n')[0])
    return nrow

def read_hdf5_by_name(filename, name):
    f_scores = h5py.File(filename, 'r')
    scores = f_scores[name][()]
    f_scores.close()
    return scores

def _logit(a):
    return np.log((a + 1e-10) / (1 - a + 1e-10))

class ScoreCalculater:
    def get_scores(self, scores):
        i = [ float(i) for i in scores.strip().split(',') ]
        return i
    def abs_logit_change(self, scores):
        scores = self.get_scores(scores)
        ref_score = scores.pop(0)
        for_return = []
        for i in scores:
            for_return.append(abs(_logit(i) - _logit(ref_score)))
        return for_return
    def log_odds_ratio(self, scores):
        scores = self.get_scores(scores)
        ref_score = scores.pop(0)
        for_return = []
        for i in scores:
            for_return.append(_logit(i) - _logit(ref_score))
        return for_return, ref_score
    def nothing(self, scores):
        scores = self.get_scores(scores)
        return scores
    def abs_change(self, scores):
        scores = self.get_scores(scores)
        ref_score = scores.pop(0)
        for_return = []
        for i in scores:
            for_return.append(abs(i - ref_score))
        return for_return
    def change(self, scores):
        scores = self.get_scores(scores)
        ref_score = scores.pop(0)
        for_return = []
        for i in scores:
            for_return.append(i - ref_score)
        return for_return, ref_score
        
class Filter:
    def percentage_thresholding(self, all_scores, all_original_scores, percentage):
        threshold = np.percentile(all_scores, float(percentage) * 100)
        # print(threshold)
        all_scores = pd.DataFrame(all_scores)
        passed_idx = all_scores[all_scores.max(axis=1) >= threshold].index.tolist()
        return passed_idx
    def hard_log_thresholding(self, all_scores, all_original_scores, threshold):
        all_scores = pd.DataFrame(all_scores)
        passed_idx = all_scores[all_scores.max(axis=1) >= np.log(float(threshold))].index.tolist()
        return passed_idx
    def binding_variant(self, all_scores, all_original_scores, thresholds):
        thresholds = [ float(i) for i in thresholds.split(',') ]
        temp_all_scores = pd.DataFrame(all_scores)
        temp_all_original_scores = pd.DataFrame(all_original_scores)
        temp_ind = (temp_all_original_scores.max(axis=1) >= _logit(thresholds[0])) & (temp_all_scores.max(axis=1) >= np.log(thresholds[1]))
        passed_idx = temp_all_scores[temp_ind].index.tolist()
        return passed_idx
    def footprint_snp(self, all_scores, all_original_scores, thresholds):
        return [ i for i in range(len(all_scores)) ]
