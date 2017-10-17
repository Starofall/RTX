from abc import ABCMeta, abstractmethod
from analysis_lib import Analysis
from scipy.stats import levene
from scipy.stats import fligner
from scipy.stats import bartlett


class EqualVarianceTest(Analysis):

    __metaclass__ = ABCMeta

    def __init__(self, rtx_run_ids, y_key, alpha=0.05):
        super(EqualVarianceTest, self).__init__(rtx_run_ids, y_key)
        self.alpha = alpha

    def run(self, data):

        y = []
        for i in range(0, self.exp_count):
            y.append([d[self.y_key] for d in data[i]])

        statistic, pvalue = self.get_statistic_and_pvalue(y)

        not_equal_variance = bool(pvalue <= self.alpha)

        result = dict()
        result["statistic"] = statistic
        result["pvalue"] = pvalue
        result["alpha"] = self.alpha
        result["not_equal_variance"] = not_equal_variance

        return result

    @abstractmethod
    def get_statistic_and_pvalue(self, args):
        """ Specific to each different-distribution test """
        pass


class Levene(EqualVarianceTest):
    """Tests the null hypothesis that all input samples are from populations with equal variances.

    It is a parametric test with robustness w.r.t to deviations from normality.
    """
    name = "levene"

    def get_statistic_and_pvalue(self, y):
        return levene(*y, center="mean")


class Bartlett(EqualVarianceTest):
    """Tests the null hypothesis that all input samples are from populations with equal variances.

    It is a parametric test. To be used when samples come from normal populations.
    For samples from significantly non-normal populations, Levene's test is more robust.
    """
    name = "bartlett"

    def get_statistic_and_pvalue(self, y):
        return bartlett(*y)


class FlignerKilleen(EqualVarianceTest):
    """Tests the null hypothesis that all input samples are from populations with equal variances.

    It is a non-parametric test. It is distribution free when populations are identical.
    """
    name = "fligner-killeen"

    def get_statistic_and_pvalue(self, y):
        return fligner(*y, center="mean")
