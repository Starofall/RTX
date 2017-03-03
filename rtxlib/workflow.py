import time

from colorama import Fore

from rtxlib import info, error, log_results
from rtxlib.changeproviders import init_change_provider
from rtxlib.dataproviders import init_data_providers
from rtxlib.executionstrategy import init_execution_strategy
from rtxlib.executionstrategy.SelfOptimizerStrategy import start_self_optimizer_strategy
from rtxlib.executionstrategy.SequencialStrategy import start_sequential_strategy
from rtxlib.executionstrategy.StepStrategy import start_step_strategy
from rtxlib.preprocessors import init_pre_processors, kill_pre_processors


def execute_workflow(wf):
    try:
        info("######################################", Fore.CYAN)
        info("> Workflow       | " + str(wf.name), Fore.CYAN)
        # check variables
        a = wf.pre_processors
        b = wf.change_provider
        c = wf.primary_data_provider
        c = wf.secondary_data_providers
        d = wf.execution_strategy
    except KeyError as e:
        error("definition.py is missing value " + str(e))
        exit(1)
    # initialize the test environment
    init_pre_processors(wf)
    init_change_provider(wf)
    init_data_providers(wf)
    init_execution_strategy(wf)
    kill_pre_processors(wf)
    info("> Finished workflow")
