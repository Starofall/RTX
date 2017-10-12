from analysis_lib.Analysis import Analysis
from scipy.stats import kstest


class KolmogorovSmirnov(Analysis):
    """This normality test can be applied more broadly than Shapiro-Wilk, but is less powerful for testing normality.

    Tests the null hypothesis that the sample comes from a normal distribution.
    The Kolmogorov-Smirnov statistic quantifies a distance between the empirical distribution function (here, normal)
    of the sample and the cumulative distribution function of the reference distribution.
    """

    name = "kolmogorov-smirnov"

    def __init__(self, rtx_run_ids, alpha=0.05):
        super(self.__class__, self).__init__(rtx_run_ids)
        self.alpha = alpha

    def run(self, data):

        x1 = [d["overhead"] for d in data[0]]
        x2 = [d["overhead"] for d in data[1]]

        statistic, pvalue = kstest(x1 + x2, "norm")

        not_normal = bool(pvalue <= self.alpha)

        result = dict()
        result["statistic"] = statistic
        result["pvalue"] = pvalue
        result["alpha"] = self.alpha
        result["not_normal"] = not_normal

        return result