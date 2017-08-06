import numpy as np

def _logit(a):
    return np.log(a / (1 - a + 1e-10))
class ScoreCalculater:
    def abs_logit_change(self, scores, alleles):
        scores = self.get_scores(scores)
        alleles = self.get_alleles(alleles)
        ref_score = scores.pop(0)
        for_return = []
        for i in scores:
            for_return.append(abs(_logit(i) - _logit(ref_score)))
        return for_return
class Filter:
    def get_scores(self, scores):
        i = [ float(i) for i in scores.split(',') ]
        return i
    def get_alleles(self, alleles):
        i = [ i for i in scores.split(',') ]
        return i
