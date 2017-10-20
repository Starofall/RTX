#!/usr/bin/python
from rtxlib.rtx_run import setup_database
from rtxlib.rtx_run import RTXRun
from analysis_lib.one_sample_tests import AndersonDarling
from analysis_lib.one_sample_tests import DAgostinoPearson
from analysis_lib.one_sample_tests import KolmogorovSmirnov
from analysis_lib.one_sample_tests import ShapiroWilk
from analysis_lib.two_sample_tests import Ttest
from analysis_lib.two_sample_tests import TtestSampleSizeEstimation
from analysis_lib.n_sample_tests import OneWayAnova
from analysis_lib.n_sample_tests import KruskalWallis
from analysis_lib.factorial_tests import FactorialAnova
from analysis_lib.n_sample_tests import Levene
from analysis_lib.n_sample_tests import FlignerKilleen
from analysis_lib.n_sample_tests import Bartlett
from rtxlib.rtx_run import db


class TestData:

    primary_data_provider = {
        "type": "kafka_consumer",
        "kafka_uri": "kafka:9092",
        "topic": "crowd-nav-trips",
        "serializer": "JSON"
    }

    change_provider = {
        "type": "kafka_producer",
        "kafka_uri": "kafka:9092",
        "topic": "crowd-nav-commands",
        "serializer": "JSON",
    }


if __name__ == '__main__':

    execution_strategy = {
        "ignore_first_n_results": 0,
        "sample_size": 2,
        "type": "step_explorer",
        "knobs": {
            "route_random_sigma": ([0.0, 0.2], 0.2),
            "max_speed_and_length_factor": ([0.0, 0.4], 0.4),
            # "exploration_percentage": ([0.0, 0.2], 0.2),
            # "average_edge_duration_factor": ([0.8, 1], 0.2),
        }
        # "type": "sequential",
        # "knobs": [
        #     {"route_random_sigma": 0.0},
        # {"route_random_sigma": 0.2},
        # {"route_random_sigma": 0.4}
        # ]
    }

    setup_database()

    target_system_id = "CrowdNav"
    db().save_target_system(target_system_id, TestData.primary_data_provider, TestData.change_provider)

    rtx_run_ids = list()
    rtx_run = RTXRun.create(target_system_id, execution_strategy)

    if not rtx_run:
        exit(0)

    rtx_run_ids.append(rtx_run.start())

    # rtx_run = RTXRun.create(target_system_id, execution_strategy)
    # rtx_run_ids.append(rtx_run.start())

    y_key = "overhead"

    ##########################
    ## One sample tests (Normality tests)
    ##########################
    # DAgostinoPearson(rtx_run_ids, y_key, alpha=0.05).start()
    # ShapiroWilk(rtx_run_ids, y_key, alpha=0.05).start()
    # AndersonDarling(rtx_run_ids, y_key, alpha=0.05).start()
    # KolmogorovSmirnov(rtx_run_ids, y_key, alpha=0.05).start()

    ##########################
    ## Two-sample tests
    ##########################
    # Ttest(rtx_run_ids, y_key, alpha=0.05).start()
    # TtestSampleSizeEstimation(rtx_run_ids, y_key, mean_diff=0.1, alpha=0.05, power=0.8).start()

    ##########################
    ## N-sample tests
    ##########################

    ##########################
    ## Different distributions tests
    ##########################
    # OneWayAnova(rtx_run_ids, y_key).start()
    # KruskalWallis(rtx_run_ids, y_key).start()

    ##########################
    ## Equal variance tests
    ##########################
    # Levene(rtx_run_ids, y_key).start()
    # Bartlett(rtx_run_ids, y_key).start()
    # FlignerKilleen(rtx_run_ids, y_key).start()

    ##########################
    ## Two-way anova
    ##########################
    FactorialAnova(rtx_run_ids, y_key, execution_strategy["knobs"].keys()).start()

    # TODO: check:
    # racing algorithms: irace
    # distribution-free statistics: histogram




