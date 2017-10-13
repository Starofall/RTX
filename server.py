#!/usr/bin/python
from rtxlib.rtx_run import setup_database
from rtxlib.rtx_run import RTXRun
from analysis_lib.normality_tests import AndersonDarling
from analysis_lib.normality_tests import DAgostinoPearson
from analysis_lib.normality_tests import KolmogorovSmirnov
from analysis_lib.normality_tests import ShapiroWilk
from analysis_lib.two_sample_tests import Ttest
from analysis_lib.two_sample_tests import TtestSampleSizeEstimation
from analysis_lib.n_sample_tests import OneWayAnova
from analysis_lib.n_sample_tests import KruskalWallis
from analysis_lib.n_sample_tests import TwoWayAnova

if __name__ == '__main__':

    setup_database()
    rtx_run_ids = list()
    rtx_run_ids.append(RTXRun().start())
    # rtx_run_ids.append(RTXRun().start())

    # Ttest(rtx_run_ids, alpha=0.05).start()
    # TtestSampleSizeEstimation(rtx_run_ids, mean_diff=0.1, alpha=0.05, power=0.8).start()
    # DAgostinoPearson(rtx_run_ids, alpha=0.05).start()
    # ShapiroWilk(rtx_run_ids, alpha=0.05).start()
    # AndersonDarling(rtx_run_ids, alpha=0.05).start()
    # KolmogorovSmirnov(rtx_run_ids, alpha=0.05).start()
    # OneWayAnova(rtx_run_ids).start()
    # KruskalWallis(rtx_run_ids).start()
    # TwoWayAnova(rtx_run_ids).start()

