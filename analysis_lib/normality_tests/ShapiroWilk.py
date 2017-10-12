from analysis_lib.Analysis import Analysis
from scipy.stats import shapiro


class ShapiroWilk(Analysis):
    """This normality test is reputedly more well suited to smaller datasets.

    Tests the null hypothesis is that the sample comes from a normal distribution.
    This test is biased by sample size: the test may be statistically significant from a normal distribution
    in any large samples. Thus a Q-Q plot is required for verification in addition to the test.
    """

    name = "shapiro-wilk"

    def __init__(self, rtx_run_ids, alpha=0.05):
        super(self.__class__, self).__init__(rtx_run_ids)
        self.alpha = alpha

    def run(self, data):

        x1 = [d["overhead"] for d in data[0]]
        x2 = [d["overhead"] for d in data[1]]

        statistic, pvalue = shapiro(x1 + x2)

        not_normal = bool(pvalue <= self.alpha)

        result = dict()
        result["statistic"] = statistic
        result["pvalue"] = pvalue
        result["alpha"] = self.alpha
        result["not_normal"] = not_normal

        return result