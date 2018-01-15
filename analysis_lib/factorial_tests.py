import json
import pandas as pd
from itertools import combinations
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from rtxlib import error
from analysis_lib import Analysis


class FactorialAnova(Analysis):
    """ For explanation of the different types of ANOVA check:
    https://mcfromnz.wordpress.com/2011/03/02/anova-type-iiiiii-ss-explained/
    """

    name = "two-way-anova"

    def __init__(self, rtx_run_ids, y_key, knob_keys, exp_count):
        super(FactorialAnova, self).__init__(rtx_run_ids, y_key)
        self.knob_keys = knob_keys
        self.exp_count = exp_count

    def run(self, data, knobs):

        if len(self.knob_keys) < 2:
            error("Cannot run " + self.name + " on one factor.")
            error("Aborting analysis")
            return

        dataframe_data = dict()
        dataframe_data[self.y_key] = [d[self.y_key] for i in range(self.exp_count) for d in data[i]]
        for knob_key in self.knob_keys:
            dataframe_data[knob_key] = [d[knob_key] for i in range(self.exp_count) for d in knobs[i]]

        # data for quick tests:
        # dataframe_data = {}
        # dataframe_data["overhead"] = [2.3, 1.3, 2.8, 2.5, 2.9, 2.4, 1.4, 2.6, 1.8, 1.9, 1.2, 3.0]
        # dataframe_data["route_random_sigma"] = [0, 0, 0, 0.2, 0.2, 0.2, 0, 0, 0, 0, 0, 0]
        # dataframe_data["exploration_percentage"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2, 0.2, 0.2]

        df = pd.DataFrame(dataframe_data)
        # print df
        # print "------------------"

        formula = self.create_formula()
        # formula = "overhead ~ route_random_sigma * exploration_percentage"
        # print formula
        # print "------------------"

        data_lm = ols(formula, data=dataframe_data).fit()
        # print data_lm.summary()
        # print "------------------"

        aov_table = anova_lm(data_lm, typ=2)
        self.eta_squared(aov_table)
        self.omega_squared(aov_table)
        # with pd.option_context('display.max_rows', self.exp_count, 'display.max_columns', 6, 'max_colwidth', 10000):
            # print(aov_table)
        # print "------------------"

        return aov_table

        # return json.loads(json.dumps(aov_table, default=lambda df: json.loads(df.to_json())))

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

    def create_formula(self):
        """Example for 3 factors:
             overhead ~ C(route_random_sigma) + C(exploration_percentage) + C(max_speed_and_length_factor)' \
                    ' + C(route_random_sigma):C(exploration_percentage)' \
                    ' + C(route_random_sigma):C(max_speed_and_length_factor)' \
                    ' + C(exploration_percentage):C(max_speed_and_length_factor)' \
                    ' + C(route_random_sigma):C(exploration_percentage):C(max_speed_and_length_factor)'
        """

        formula = self.y_key + " ~ "
        formula += " + ".join("C(" + knob_key + ")" for knob_key in self.knob_keys)
        formula += " + "

        formula += \
            " + ".join(
                " + ".join(
                    ":".join("C(" + c + ")" for c in comb)
                    for comb in combinations(self.knob_keys, comb_num))
                for comb_num in range(2, len(self.knob_keys)+1))

        return formula

    def eta_squared(self, aov):
        aov['eta_sq'] = 'NaN'
        aov['eta_sq'] = aov[:-1]['sum_sq']/sum(aov['sum_sq'])

    def omega_squared(self, aov):
        mse = aov['sum_sq'][-1]/aov['df'][-1]
        aov['omega_sq'] = 'NaN'
        aov['omega_sq'] = (aov[:-1]['sum_sq']-(aov[:-1]['df']*mse))/(sum(aov['sum_sq'])+mse)