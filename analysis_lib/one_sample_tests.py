from abc import ABCMeta, abstractmethod
from scipy.stats import normaltest
from scipy.stats import anderson
from scipy.stats import kstest
from scipy.stats import shapiro
from rtxlib import warn, error
from analysis_lib import Analysis


class OneSampleTest(Analysis):

    def run(self, data, knobs):
        if len(data) > 1:
            warn("Cannot run " + self.name + " on more than one sample.")
            warn("Running only for first sample.")

        self.y1 = [d[self.y_key] for d in data[0]]


class NormalityTest(OneSampleTest):
    """Tests the null hypothesis that the sample comes from a normal distribution."""

    __metaclass__ = ABCMeta

    def __init__(self, rtx_run_ids, y_key, alpha=0.05):
        super(NormalityTest, self).__init__(rtx_run_ids, y_key)
        self.alpha = alpha

    def run(self, data, knobs):

        super(NormalityTest, self).run(data, knobs)

        statistic, pvalue = self.get_statistic_and_pvalue(self.y1)

        not_normal = bool(pvalue <= self.alpha)

        result = dict()
        result["statistic"] = statistic
        result["pvalue"] = pvalue
        result["alpha"] = self.alpha
        result["not_normal"] = not_normal

        return result

    @abstractmethod
    def get_statistic_and_pvalue(self, y):
        """ Specific to each normality test """
        pass


class DAgostinoPearson(NormalityTest):
    """Combines skew and kurtosis to produce an omnibus test of normality.

    Need to use with samples with size>=8."""

    name = "dagostino-pearson"

    def get_statistic_and_pvalue(self, y):
        return normaltest(y)


class AndersonDarling(NormalityTest):
    """Derived from Kolmogorov test."""

    name = "anderson-darling"

    def __init__(self, rtx_run_ids, y_key, alpha=0.05):
        super(self.__class__, self).__init__(rtx_run_ids, y_key)
        if alpha not in [0.15, 0.10, 0.05, 0.02, 0.01]:
            error("For Anderson-Darling test, please select as alpha one of 0.15, 0.10, 0.05, 0.02, or 0.01. "
                  "Falling back to default value of alpha = 0.05")
            self.alpha = 0.05
        else:
            self.alpha = alpha

    def get_statistic_and_pvalue(self, y):
        statistic, critical_values, significance_level = anderson(y)
        pvalue = critical_values[significance_level.tolist().index(100 * self.alpha)]
        return statistic, pvalue


class KolmogorovSmirnov(NormalityTest):
    """This normality test can be applied more broadly than Shapiro-Wilk, but is less powerful for testing normality.

    The Kolmogorov-Smirnov statistic quantifies a distance between the empirical distribution function (here, normal)
    of the sample and the cumulative distribution function of the reference distribution.
    """

    name = "kolmogorov-smirnov"

    def get_statistic_and_pvalue(self, y):
        return kstest(y, "norm")


class ShapiroWilk(NormalityTest):
    """This normality test is reputedly more well suited to smaller datasets.

    This test is biased by sample size: the test may be statistically significant from a normal distribution
    in any large samples. Thus a Q-Q plot is required for verification in addition to the test.
    Also, the Shapiro-Wilk test is known not to work well in samples with many identical values.
    """

    name = "shapiro-wilk"

    def get_statistic_and_pvalue(self, y):
        return shapiro(y)