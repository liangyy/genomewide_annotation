import numpy as np

def _logit(a):
    return np.log(a / (1 - a + 1e-10))
class ScoreCalculater:
    def get_scores(self, scores):
        i = [ float(i) for i in scores.split(',') ]
        return i
    def abs_logit_change(self, scores):
        scores = self.get_scores(scores)
        ref_score = scores.pop(0)
        for_return = []
        for i in scores:
            for_return.append(abs(_logit(i) - _logit(ref_score)))
        return for_return
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
class Filter:
    def percentage_thresholding(all_scores, all_original_scores, percentage):
        threshold = np.percentile(all_scores, float(percentage) * 100)
        all_scores = pd.DataFrame(all_scores)
        passed_idx = all_scores[all_scores.max(axis=1) >= threshold].index.tolist()
        return passed_idx
    def binding_variant(all_scores, all_original_scores, thresholds):
        thresholds = [ float(i) for i in thresholds.split(',') ]
        temp_ind = all_original_scores.max(axis=1) >= np.log(thresholds[0]) & all_scores.max(axis=1) >= np.log(thresholds[1])
        passed_idx = all_scores[temp_ind].index.tolist()
        return passed_idx
    def footprint_snp(all_scores, all_original_scores, thresholds):
        return [ i for i in range(all_scores.shape[0]) ]
