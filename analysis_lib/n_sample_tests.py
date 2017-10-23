from abc import ABCMeta, abstractmethod
from scipy.stats import f_oneway
from scipy.stats import kruskal
from scipy.stats import levene
from scipy.stats import fligner
from scipy.stats import bartlett
from rtxlib import error
from analysis_lib import Analysis


class NSampleTest(Analysis):

    def run(self, data, knobs):

        if len(data) < 2:
            error("Cannot run " + self.name + " on less than two samples.")
            return False

        self.y = [[d[self.y_key] for d in data[i]] for i in range(self.exp_count)]

        return True


class DifferentDistributionsTest(NSampleTest):

    __metaclass__ = ABCMeta

    def __init__(self, rtx_run_ids, y_key, alpha=0.05):
        super(DifferentDistributionsTest, self).__init__(rtx_run_ids, y_key)
        self.alpha = alpha

    def run(self, data, knobs):

        if not super(DifferentDistributionsTest, self).run(data, knobs):
            error("Aborting analysis.")
            return

        statistic, pvalue = self.get_statistic_and_pvalue(self.y)

        different_distributions = bool(pvalue <= self.alpha)

        result = dict()
        result["statistic"] = statistic
        result["pvalue"] = pvalue
        result["alpha"] = self.alpha
        result["different_distributions"] = different_distributions

        return result

    @abstractmethod
    def get_statistic_and_pvalue(self, args):
        """ Specific to each different-distribution test """
        pass


class OneWayAnova(DifferentDistributionsTest):
    """Tests the null hypothesis that two or more groups have the same population mean.

    The ANOVA test has important assumptions that must be satisfied in order
    for the associated p-value to be valid.

    1. The samples are independent.
    2. Each sample is from a normally distributed population.
    3. The population standard deviations of the groups are all equal.  This
       property is known as homoscedasticity.

    If these assumptions are not true for a given set of data, it may still be
    possible to use the Kruskal-Wallis although with some loss of power.
    """
    name = "one-way-anova"

    def get_statistic_and_pvalue(self, args):
        return f_oneway(*args)


class KruskalWallis(DifferentDistributionsTest):
    """Tests the null hypothesis that the population median of all of the groups are equal.

    It is a non-parametric version of one-way ANOVA.
    """
    name = "kruskal-wallis"

    def get_statistic_and_pvalue(self, args):
        return kruskal(*args)


class EqualVarianceTest(NSampleTest):

    __metaclass__ = ABCMeta

    def __init__(self, rtx_run_ids, y_key, alpha=0.05):
        super(EqualVarianceTest, self).__init__(rtx_run_ids, y_key)
        self.alpha = alpha

    def run(self, data, knobs):

        if not super(EqualVarianceTest, self).run(data, knobs):
            error("Aborting analysis.")
            return

        statistic, pvalue = self.get_statistic_and_pvalue(self.y)

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

