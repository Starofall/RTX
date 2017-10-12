from analysis_lib.Analysis import Analysis
import scipy.stats as stats


class Ttest(Analysis):

    name = "t-test"

    def __init__(self, rtx_run_ids, alpha=0.05):
        super(self.__class__, self).__init__(rtx_run_ids)
        self.alpha = alpha

    def run(self, data):

        x1 = [d["overhead"] for d in data[0]]
        x2 = [d["overhead"] for d in data[1]]

        tstat, pvalue = stats.ttest_ind(x1, x2, equal_var = False)

        different_distributions = bool(pvalue <= self.alpha)

        result = dict()
        result["tstat"] = tstat
        result["pvalue"] = pvalue
        result["alpha"] = self.alpha
        result["different_distributions"] = different_distributions

        return result





