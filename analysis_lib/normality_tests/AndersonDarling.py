from analysis_lib.Analysis import Analysis
from scipy.stats import anderson
from rtxlib import error


class AndersonDarling(Analysis):
    """Derived from Kolmogorov test.

    Tests the null hypothesis is that the sample comes from a normal distribution.
    """

    name = "anderson-darling"

    def __init__(self, rtx_run_ids, alpha=0.05):
        super(self.__class__, self).__init__(rtx_run_ids)
        if alpha not in [0.15, 0.10, 0.05, 0.02, 0.01]:
            error("For Anderson-Darling test, please select as alpha one of 0.15, 0.10, 0.05, 0.02, or 0.01. "
                  "Falling back to default value of alpha = 0.05")
            self.alpha = 0.05
        else:
            self.alpha = alpha

    def run(self, data):

        x1 = [d["overhead"] for d in data[0]]
        x2 = [d["overhead"] for d in data[1]]

        statistic, critical_values, significance_level = anderson(x1 + x2)

        pvalue = critical_values[significance_level.tolist().index(100 * self.alpha)]

        not_normal = bool(pvalue <= self.alpha)

        result = dict()
        result["statistic"] = statistic
        result["pvalue"] = pvalue
        result["alpha"] = self.alpha
        result["not_normal"] = not_normal

        return result