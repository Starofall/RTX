#!/usr/bin/python
from RTXRun import RTXRun
from analysis_lib import setup_database
from analysis_lib.two_sample.Ttest import Ttest
from analysis_lib.two_sample.TtestSampleSizeEstimation import TtestSampleSizeEstimation
from analysis_lib.normality_tests.DAgostinoPearson import DAgostinoPearson
from analysis_lib.normality_tests.ShapiroWilk import ShapiroWilk
from analysis_lib.normality_tests.AndersonDarling import AndersonDarling
from analysis_lib.normality_tests.KolmogorovSmirnov import KolmogorovSmirnov

if __name__ == '__main__':

    setup_database()
    rtx_run_ids = []
    rtx_run_ids.append(RTXRun().start())
    # rtx_run_ids.append(RTXRun().start())

    # ttest_analysis = Ttest(rtx_run_ids, alpha=0.05)
    # ttest_analysis = TtestSampleSizeEstimation(rtx_run_ids, mean_diff=0.1, alpha=0.05, power=0.8)
    # ttest_analysis = DAgostinoPearson(rtx_run_ids, alpha=0.05)
    # ttest_analysis = ShapiroWilk(rtx_run_ids, alpha=0.05)
    # ttest_analysis = AndersonDarling(rtx_run_ids, alpha=0.05)
    ttest_analysis = KolmogorovSmirnov(rtx_run_ids, alpha=0.05)
    ttest_analysis.start()

