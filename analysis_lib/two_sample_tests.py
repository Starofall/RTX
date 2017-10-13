from analysis_lib import Analysis
from scipy.stats import ttest_ind
from math import sqrt, floor
from numpy import var
from statsmodels.stats.power import tt_ind_solve_power


class Ttest(Analysis):

    name = "t-test"

    def __init__(self, rtx_run_ids, alpha=0.05):
        super(self.__class__, self).__init__(rtx_run_ids)
        self.alpha = alpha

    def run(self, data):

        x1 = [d["overhead"] for d in data[0]]
        x2 = [d["overhead"] for d in data[1]]

        tstat, pvalue = ttest_ind(x1, x2, equal_var = False)

        different_averages = bool(pvalue <= self.alpha)

        result = dict()
        result["tstat"] = tstat
        result["pvalue"] = pvalue
        result["alpha"] = self.alpha
        result["different_averages"] = different_averages

        return result


class TtestSampleSizeEstimation(Analysis):

    name = "t-test-sample-estimation"

    def __init__(self, rtx_run_ids, mean_diff, alpha=0.05, power=0.8):
        super(self.__class__, self).__init__(rtx_run_ids)
        self.alpha = alpha
        self.power = power
        self.mean_diff = mean_diff

    def run(self, data):

        x1 = [d["overhead"] for d in data[0]]
        x2 = [d["overhead"] for d in data[1]]

        pooled_std = sqrt((var(x1) + var(x2)) / 2)

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