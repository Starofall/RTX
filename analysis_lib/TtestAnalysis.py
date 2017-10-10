import scipy.stats as stats

from analysis_lib.Analysis import Analysis


class TtestAnalysis(Analysis):
    """ implements a ttest analysis """

    def __init__(self, alpha):
        super(self.__class__, self).__init__()

        self.analysis = "t-test"
        self.alpha = alpha

    def workflow_evaluator(self, wf, data):

        x1 = [d["overhead"] for d in data[0]]
        x2 = [d["overhead"] for d in data[1]]

        tstat, pvalue = stats.ttest_ind(x1, x2, equal_var = False)

        different_distributions = bool(pvalue <= self.alpha)

        result = dict()
        result["tstat"] = tstat
        result["pvalue"] = pvalue
        result["alpha"] = self.alpha
        result["different_distributions"] = different_distributions

        super(self.__class__, self).workflow_evaluator(wf, result)





