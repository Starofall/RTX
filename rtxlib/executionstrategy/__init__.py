from rtxlib.executionstrategy.StepStrategy import start_step_strategy
from rtxlib.executionstrategy.SelfOptimizerStrategy import start_self_optimizer_strategy
from rtxlib.executionstrategy.SequencialStrategy import start_sequential_strategy

from rtxlib import log_results, error, info


def applyInitKnobs(wf):
    # we are done, so revert to default if given
    if "init_knobs" in wf.execution_strategy:
        try:
            info("> Set the initial knobs for this workflow")
            wf.change_provider["instance"] \
                .applyChange(wf.change_event_creator(wf.execution_strategy["init_knobs"]))
        except:
            error("apply changes did not work")


def applyDefaultKnobs(wf):
    # we are done, so revert to default if given
    if "default_knobs" in wf.execution_strategy:
        try:
            info("> Reverted back system knobs to default")
            wf.change_provider["instance"] \
                .applyChange(wf.change_event_creator(wf.execution_strategy["default_knobs"]))
        except:
            error("apply changes did not work")


def init_execution_strategy(wf):
    applyInitKnobs(wf)
    try:
        # start the right execution strategy
        if wf.execution_strategy["type"] == "sequential":
            log_results(wf.folder, wf.execution_strategy["knobs"][0].keys() + ["result"], append=False)
            start_sequential_strategy(wf)

        elif wf.execution_strategy["type"] == "self_optimizer":
            log_results(wf.folder, wf.execution_strategy["knobs"].keys() + ["result"], append=False)
            start_self_optimizer_strategy(wf)

        elif wf.execution_strategy["type"] == "step_explorer":
            log_results(wf.folder, wf.execution_strategy["knobs"].keys() + ["result"], append=False)
            start_step_strategy(wf)
    except RuntimeError:
        error("Stopped the whole workflow as requested by a RuntimeError")
    # finished
    info(">")
    applyDefaultKnobs(wf)
