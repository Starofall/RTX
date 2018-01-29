from math import sqrt, floor
from numpy import var
from scipy.stats import ttest_ind
from statsmodels.stats.power import tt_ind_solve_power
from rtxlib import warn, error
from analysis_lib import Analysis
from numpy import mean

class TwoSampleTest(Analysis):

    def run(self, data, knobs):

        if len(data) < 2:
            error("Cannot run " + self.name + " on less than two samples.")
            return False

        if len(data) > 2:
            warn("Cannot run " + self.name + " on more than two samples.")
            warn("Comparing only the first two samples.")

        from math import log
        print "with log transformation..."
        self.y1 = [log(d[self.y_key]) for d in data[0]]
        self.y2 = [log(d[self.y_key]) for d in data[1]]

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

        result["mean_diff"] = mean(self.y1) - mean(self.y2)

        # calculating cohen's d effect size ():
        pooled_std = sqrt((var(self.y1) + var(self.y2)) / 2)
        result["effect_size"] = result["mean_diff"] / pooled_std

        return result


class TtestPower(TwoSampleTest):

    name = "t-test-power"

    def __init__(self, rtx_run_ids, y_key, effect_size, alpha=0.05, alternative='two-sided'):
        super(self.__class__, self).__init__(rtx_run_ids, y_key)
        self.alpha = alpha
        self.effect_size = effect_size
        self.alternative = alternative

    def run(self, data, knobs):

        if not super(self.__class__, self).run(data, knobs):
            error("Aborting analysis.")
            return

        # pooled_std = sqrt((var(self.y1) + var(self.y2)) / 2)
        # effect_size = self.mean_diff / pooled_std

        sample_size = len(self.y1)

        power = tt_ind_solve_power(effect_size=self.effect_size, nobs1=sample_size, alpha=self.alpha, alternative=self.alternative)

        result = dict()
        result["effect_size"] = self.effect_size
        result["sample_size"] = sample_size
        result["alpha"] = self.alpha
        result["power"] = power
        # result["mean_diff"] = self.mean_diff
        # result["pooled_std"] = pooled_std

        return result

class TtestSampleSizeEstimation(TwoSampleTest):

    name = "t-test-sample-estimation"

    def __init__(self, rtx_run_ids, y_key, effect_size, mean_diff, alpha=0.05, power=0.8, alternative='two-sided'):
        super(self.__class__, self).__init__(rtx_run_ids, y_key)
        self.alpha = alpha
        self.power = power
        self.effect_size = effect_size
        self.mean_diff = mean_diff
        self.alternative = alternative

    def run(self, data, knobs):

        if not super(self.__class__, self).run(data, knobs):
            error("Aborting analysis.")
            return

        if not self.effect_size:
            if not self.mean_diff:
                raise Exception("You cannot leave both mean_diff and effect_size paramaters empty")
            pooled_std = sqrt((var(self.y1) + var(self.y2)) / 2)
            effect_size = self.mean_diff / pooled_std
        else:
            effect_size = self.effect_size

        sample_size = tt_ind_solve_power(effect_size=effect_size, nobs1=None, alpha=self.alpha, power=self.power, alternative=self.alternative)

        result = dict()
        result["effect_size"] = effect_size
        result["sample_size"] = floor(sample_size)
        result["alpha"] = self.alpha
        result["power"] = self.power
        # result["mean_diff"] = self.mean_diff
        # result["pooled_std"] = pooled_std

        return result
