from math import sqrt, floor
from numpy import var
from scipy.stats import ttest_ind
from statsmodels.stats.power import tt_ind_solve_power
from rtxlib import warn, error
from analysis_lib import Analysis


class TwoSampleTest(Analysis):

    def run(self, data, knobs):

        if len(data) < 2:
            error("Cannot run " + self.name + " on less than two samples.")
            return False

        if len(data) > 2:
            warn("Cannot run " + self.name + " on more than two samples.")
            warn("Comparing only the first two samples.")

        self.y1 = [d[self.y_key] for d in data[0]]
        self.y2 = [d[self.y_key] for d in data[1]]

        return True

class Ttest(TwoSampleTest):

    name = "t-test"

    def __init__(self, rtx_run_ids, y_key, alpha=0.05):
        super(self.__class__, self).__init__(rtx_run_ids, y_key)
        self.alpha = alpha

    def run(self, data, knobs):

        if not super(self.__class__, self).run(data, knobs):
            error("Aborting analysis.")
            return

        statistic, pvalue = ttest_ind(self.y1, self.y2, equal_var = False)

        different_averages = bool(pvalue <= self.alpha)

        result = dict()
        result["statistic"] = statistic
        result["pvalue"] = pvalue
        result["alpha"] = self.alpha
        result["different_averages"] = different_averages

        return result


class TtestSampleSizeEstimation(TwoSampleTest):

    name = "t-test-sample-estimation"

    def __init__(self, rtx_run_ids, y_key, mean_diff, alpha=0.05, power=0.8):
        super(self.__class__, self).__init__(rtx_run_ids, y_key)
        self.alpha = alpha
        self.power = power
        self.mean_diff = mean_diff

    def run(self, data, knobs):

        if not super(self.__class__, self).run(data, knobs):
            error("Aborting analysis.")
            return

        pooled_std = sqrt((var(self.y1) + var(self.y2)) / 2)

        effect_size = self.mean_diff / pooled_std

        sample_size = tt_ind_solve_power(effect_size=effect_size, nobs1=None, alpha=self.alpha, power=self.power, alternative='two-sided')

        result = dict()
        result["effect_size"] = effect_size
        result["sample_size"] = floor(sample_size)
        result["alpha"] = self.alpha
        result["power"] = self.power
        result["mean_diff"] = self.mean_diff
        result["pooled_std"] = pooled_std

        return result
