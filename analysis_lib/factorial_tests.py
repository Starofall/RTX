import json
import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from rtxlib import error
from analysis_lib import Analysis


class TwoWayAnova(Analysis):
    """ For explanation of the different types of ANOVA check:
    https://mcfromnz.wordpress.com/2011/03/02/anova-type-iiiiii-ss-explained/
    """

    name = "two-way-anova"

    def run(self, data, knobs):

        # TODO: Make this check stricter
        if len(data) < 2:
            error("Cannot run " + self.name + " on less than two samples.")
            error("Aborting analysis")
            return

        # TODO: Remove hard-coded key names
        y_flattened = [d[self.y_key] for i in range(0, self.exp_count) for d in data[i]]
        x1 = [d["route_random_sigma"] for i in range(0, self.exp_count) for d in knobs[i]]
        x2 = [d["max_speed_and_length_factor"] for i in range(0, self.exp_count) for d in knobs[i]]

        data = dict()
        data[self.y_key] = y_flattened
        data["route_random_sigma"] = x1
        data["max_speed_and_length_factor"] = x2

        df = pd.DataFrame(data)
        print df
        print "------------------"

        formula = self.y_key + ' ~ C(route_random_sigma) + C(max_speed_and_length_factor) ' \
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