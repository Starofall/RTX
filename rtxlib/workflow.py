from colorama import Fore

from rtxlib import info, error
from rtxlib.changeproviders import init_change_provider
from rtxlib.dataproviders import init_data_providers
from rtxlib.executionstrategy import run_execution_strategy
from rtxlib.preprocessors import init_pre_processors, kill_pre_processors


def execute_workflow(wf):
    """ this is the main workflow for executing a given workflow """
    try:
        # check that the definition is correct
        info("######################################", Fore.CYAN)
        info("> Workflow       | " + str(wf.name), Fore.CYAN)
        # check variables
        b = wf.change_provider
        c = wf.primary_data_provider
        d = wf.execution_strategy
    except KeyError as e:
        error("definition.py is missing value " + str(e))
        exit(1)
    # initialize the test environment
    init_pre_processors(wf)
    init_change_provider(wf)
    init_data_providers(wf)
    # here we also execute the strategy
    run_execution_strategy(wf)
    # we are done, now we clean up
    kill_pre_processors(wf)
    info("> Finished workflow")
