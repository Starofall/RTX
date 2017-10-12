#!/usr/bin/python
from RTXRun import RTXRun
from analysis_lib import setup_database

from analysis_lib.normality_tests import AndersonDarling
from analysis_lib.normality_tests import KolmogorovSmirnov
from analysis_lib.normality_tests import ShapiroWilk
from analysis_lib.normality_tests import DAgostinoPearson

if __name__ == '__main__':

    setup_database()
    rtx_run_ids = []
    rtx_run_ids.append(RTXRun().start())
    rtx_run_ids.append(RTXRun().start())

    # ttest_analysis = Ttest(rtx_run_ids, alpha=0.05)
    # ttest_analysis = TtestSampleSizeEstimation(rtx_run_ids, mean_diff=0.1, alpha=0.05, power=0.8)
    ttest_analysis = DAgostinoPearson(rtx_run_ids, alpha=0.05).start()
    ttest_analysis = ShapiroWilk(rtx_run_ids, alpha=0.05).start()
    ttest_analysis = AndersonDarling(rtx_run_ids, alpha=0.05).start()
    ttest_analysis = KolmogorovSmirnov(rtx_run_ids, alpha=0.05).start()

