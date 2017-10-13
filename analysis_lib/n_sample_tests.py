from abc import ABCMeta, abstractmethod
from analysis_lib import Analysis
from scipy.stats import f_oneway
from scipy.stats import kruskal
from statsmodels.formula.api import ols
import pandas as pd


class DifferentDistributionsTest(Analysis):

    __metaclass__ = ABCMeta

    def __init__(self, rtx_run_ids, alpha=0.05):
        super(DifferentDistributionsTest, self).__init__(rtx_run_ids)
        self.alpha = alpha

    def run(self, data):

        x1 = [d["overhead"] for d in data[0]]
        x2 = [d["overhead"] for d in data[1]]
        x3 = [d["overhead"] for d in data[2]]

        statistic, pvalue = self.get_statistic_and_pvalue(x1, x2, x3)

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

    def get_statistic_and_pvalue(self, *args):
        return f_oneway(*args)


class KruskalWallis(DifferentDistributionsTest):
    """Tests the null hypothesis that the population median of all of the groups are equal.

    It is a non-parametric version of ANOVA.
    """
    name = "kruskal-wallis"

    def get_statistic_and_pvalue(self, *args):
        return kruskal(*args)


# class TwoWayAnova(Analysis):
#
#     name = "one-way-anova"
#
#     def run(self, data):
#
#         x1 = [d["overhead"] for d in data[0]]
#
#         print data[0]
#
#         x1_labels = ["0.0" for d in x1]
#         print x1_labels
#
#         x2 = [d["overhead"] for d in data[1]]
#         x2_labels = ["0.2" for d in x2]
#         x3 = [d["overhead"] for d in data[2]]
#         x3_labels = ["0.4" for d in x3]
#
#         print "x1: [" + ", ".join(str(x) for x in x1) + "]"
#         print "x2: [" + ", ".join(str(x) for x in x2) + "]"
#         print "x3: [" + ", ".join(str(x) for x in x3) + "]"
#
#
#         data = dict()
#         data["overhead"] = x1 + x2 + x3
#         data["route_random_sigma"] = x1_labels + x2_labels + x3_labels
#
#
#         df = pd.DataFrame(data)
#         print df
#
#         data_lm = ols("overhead ~ route_random_sigma", data=data).fit()
#
#         print data_lm
#
#         anova_result = anova_lm(data_lm)
#
#         print anova_result
#
#         exit(0)
        # different_averages = bool(pvalue <= self.alpha)
        #
        # result = dict()
        # result["tstat"] = tstat
        # result["pvalue"] = pvalue
        # result["alpha"] = self.alpha
        # result["different_averages"] = different_averages
        #
        # return result
