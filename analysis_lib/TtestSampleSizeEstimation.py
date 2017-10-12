from analysis_lib.Analysis import Analysis
import math
import numpy as np
import statsmodels.stats.power as statpower


class TtestSampleSizeEstimation(Analysis):

    name = "t-test-sample-estimation"

    def __init__(self, rtx_run_ids, alpha=0.05, power=0.8, mean_diff=0.1):
        super(self.__class__, self).__init__(rtx_run_ids)
        self.alpha = alpha
        self.power = power
        self.mean_diff = mean_diff

    def run(self, data):

        x1 = [d["overhead"] for d in data[0]]
        x2 = [d["overhead"] for d in data[1]]

        pooled_std = math.sqrt((np.var(x1) + np.var(x2)) / 2)

        effect_size = self.mean_diff / pooled_std

        sample_size = statpower.tt_ind_solve_power(effect_size=effect_size, nobs1=None, alpha=self.alpha, power=self.power, alternative='two-sided')

        result = dict()
        result["effect_size"] = effect_size
        result["sample_size"] = math.floor(sample_size)
        result["alpha"] = self.alpha
        result["power"] = self.power
        result["mean_diff"] = self.mean_diff
        result["pooled_std"] = pooled_std

        return result





