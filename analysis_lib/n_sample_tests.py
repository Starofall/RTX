from abc import ABCMeta, abstractmethod
from analysis_lib import Analysis
from scipy.stats import f_oneway
from scipy.stats import kruskal
from statsmodels.formula.api import ols
import pandas as pd
from rtxlib.rtx_run import get_data_for_run
from rtxlib.rtx_run import get_list_of_configurations_for_run
from rtxlib.rtx_run import get_sample_size_for_run
from rtxlib import error
from statsmodels.stats.anova import anova_lm
import json


class DifferentDistributionsTest(Analysis):

    __metaclass__ = ABCMeta

    def __init__(self, rtx_run_ids, y_key, alpha=0.05):
        super(DifferentDistributionsTest, self).__init__(rtx_run_ids, y_key)
        self.alpha = alpha

    def run(self, data):

        y = []
        for i in range(0, self.exp_count):
            y.append([d[self.y_key] for d in data[i]])

        statistic, pvalue = self.get_statistic_and_pvalue(y)

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


class TwoWayAnova(Analysis):
    """ For explanation of the different types of ANOVA check:
    https://mcfromnz.wordpress.com/2011/03/02/anova-type-iiiiii-ss-explained/
    """

    name = "two-way-anova"

    def get_data(self):
        first_rtx_run_id = self.rtx_run_ids[0]
        data, exp_count = get_data_for_run(first_rtx_run_id)
        self.exp_count = exp_count
        self.list_of_configurations = get_list_of_configurations_for_run(first_rtx_run_id)
        self.sample_size = get_sample_size_for_run(first_rtx_run_id)

        for rtx_run_id in self.rtx_run_ids[1:]:
            new_data, new_exp_count, new_list_of_cofigurations = get_data_for_run(rtx_run_id)
            for i in range(0,exp_count):
                data[i] += new_data[i]

        if not data:
            error("Tried to run analysis on empty data. Aborting.")
            return

        return data

    def run(self, data):

        x1 = [config[0] for config in self.list_of_configurations for _ in xrange(self.sample_size)]
        x2 = [config[1] for config in self.list_of_configurations for _ in xrange(self.sample_size)]
        y = [d["overhead"] for i in range(0, self.exp_count) for d in data[i]]

        data = dict()
        data["overhead"] = y
        data["route_random_sigma"] = x1
        data["max_speed_and_length_factor"] = x2

        df = pd.DataFrame(data)
        print df
        print "------------------"

        formula = 'overhead ~ C(route_random_sigma) + C(max_speed_and_length_factor) ' \
                  '+ C(route_random_sigma):C(max_speed_and_length_factor)'
        data_lm = ols(formula, data=data).fit()
        print data_lm.summary()
        print "------------------"

        aov_table = anova_lm(data_lm, typ=2)
        self.eta_squared(aov_table)
        self.omega_squared(aov_table)
        print(aov_table)
        print "------------------"

        return json.loads(json.dumps(aov_table, default=lambda df: json.loads(df.to_json())))

        # TODO: store only selected values from the anova table.
        #
        # different_averages = bool(pvalue <= self.alpha)
        #
        # result = dict()
        # result["tstat"] = tstat
        # result["pvalue"] = pvalue
        # result["alpha"] = self.alpha
        # result["different_averages"] = different_averages
        #
        # return result

    def eta_squared(self, aov):
        aov['eta_sq'] = 'NaN'
        aov['eta_sq'] = aov[:-1]['sum_sq']/sum(aov['sum_sq'])

    def omega_squared(self, aov):
        mse = aov['sum_sq'][-1]/aov['df'][-1]
        aov['omega_sq'] = 'NaN'
        aov['omega_sq'] = (aov[:-1]['sum_sq']-(aov[:-1]['df']*mse))/(sum(aov['sum_sq'])+mse)


