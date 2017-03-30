from colorama import Fore
from rtxlib.executionstrategy.SelfOptimizerStrategy import self_optimizer_execution, recreate_knob_from_optimizer_values

from skopt import gp_minimize
from rtxlib import info, error
from rtxlib.execution import experimentFunction


def start_uncorrelated_self_optimizer_strategy(wf):
    """ executes a self optimizing strategy """

    optimizer_method = wf.execution_strategy["optimizer_method"]
    info("> ExecStrategy   | UncorrelatedSelfOptimizer", Fore.CYAN)
    info("> Optimizer      | " + optimizer_method, Fore.CYAN)

    knobs = wf.execution_strategy["knobs"]
    wf.totalExperiments = len(knobs) * wf.execution_strategy["optimizer_iterations"]

    total_result = dict()
    # we fill the arrays and use the index to map from gauss-optimizer-value to variable
    for key in knobs:
        optimal_knob_value = optimizeOneVariable(wf, wf.execution_strategy["optimizer_iterations"], key,
                                                 (knobs[key][0], knobs[key][1]))
        total_result[key] = optimal_knob_value
        wf.change_provider["instance"].applyChange(total_result)
    info(">")
    info("> FinalResult    | Best Values: " + str(total_result))


#  we also use code from the SelfOptimizerStrategy as it is the same here

def optimizeOneVariable(wf, totalExperiments, key, range):
    variables = [key]
    range_tuples = [range]
    optimizer_random_starts = wf.execution_strategy["optimizer_random_starts"]
    optimizer_result = gp_minimize(lambda opti_values: self_optimizer_execution(wf, opti_values, variables),
                                   range_tuples, n_calls=totalExperiments, n_random_starts=optimizer_random_starts)
    info(">")
    info("> OptimalResult  | Knobs:  " + str(recreate_knob_from_optimizer_values(variables, optimizer_result.x)))
    info(">                | Result: " + str(optimizer_result.fun))
    return optimizer_result.x
