from analysis_lib.Analysis import Analysis
from scipy.stats import ttest_ind


class Ttest(Analysis):

    name = "t-test"

    def __init__(self, rtx_run_ids, alpha=0.05):
        super(self.__class__, self).__init__(rtx_run_ids)
        self.alpha = alpha

    def run(self, data):

        x1 = [d["overhead"] for d in data[0]]
        x2 = [d["overhead"] for d in data[1]]

        tstat, pvalue = ttest_ind(x1, x2, equal_var = False)

        different_averages = bool(pvalue <= self.alpha)

        result = dict()
        result["tstat"] = tstat
        result["pvalue"] = pvalue
        result["alpha"] = self.alpha
        result["different_averages"] = different_averages

        return result
