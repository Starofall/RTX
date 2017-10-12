from analysis_lib.Analysis import Analysis
from scipy.stats import normaltest


class DAgostinoPearson(Analysis):

    name = "dagostino-pearson"

    def __init__(self, rtx_run_ids, alpha=0.05):
        super(self.__class__, self).__init__(rtx_run_ids)
        self.alpha = alpha

    def run(self, data):

        x1 = [d["overhead"] for d in data[0]]
        x2 = [d["overhead"] for d in data[1]]

        statistic, pvalue = normaltest(x1 + x2)

        not_normal = bool(pvalue <= self.alpha)

        result = dict()
        result["statistic"] = statistic
        result["pvalue"] = pvalue
        result["alpha"] = self.alpha
        result["not_normal"] = not_normal

        return result