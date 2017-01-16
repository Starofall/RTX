import time

from colorama import Fore

from rtxlib import info, error, log_results
from rtxlib.changeproviders import init_change_provider
from rtxlib.dataproviders import init_data_provider
from rtxlib.executionstrategy.SelfOptimizerStrategy import start_self_optimizer_strategy
from rtxlib.executionstrategy.SequencialStrategy import start_sequential_strategy
from rtxlib.executionstrategy.StepStrategy import start_step_strategy
from rtxlib.preprocessors import init_pre_processor


def execute_workflow(wf):
    try:
        info("######################################", Fore.CYAN)
        info("> Workflow       | " + str(wf.name), Fore.CYAN)
        a = wf.system["pre_processor"]
        b = wf.system["change_provider"]
        c = wf.system["data_provider"]
        d = wf.system["execution_strategy"]
    except KeyError as e:
        error("definition.py is missing value " + str(e))
        exit(1)
    # initialize the test environment
    init_pre_processor(wf)
    init_change_provider(wf)
    init_data_provider(wf)
    # start the right execution strategy
    if wf.system["execution_strategy"] == "sequential":
        log_results(wf.folder, wf.experiments_seq[0]["knobs"].keys() + ["result"], append=False)
        start_sequential_strategy(wf)

    elif wf.system["execution_strategy"] == "self_optimizer":
        log_results(wf.folder, wf.self_optimizer["knobs"].keys() + ["result"], append=False)
        start_self_optimizer_strategy(wf)

    elif wf.system["execution_strategy"] == "step":
        log_results(wf.folder, wf.step_explorer["knobs"].keys() + ["result"], append=False)
        start_step_strategy(wf)

    else:
        error("no valid execution_strategy")
    # finished
    info(">")
    try:
        wf.preprocessor.shutdown()
        info("> Shutting down Spark preprocessor")
    except AttributeError:
        pass
    info("> Finished workflow")
