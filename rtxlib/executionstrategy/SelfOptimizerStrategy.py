from colorama import Fore

from skopt import gp_minimize
from rtxlib import info, error
from rtxlib.execution import experimentFunction


def recreate_knob_from_optimizer_values(variables, opti_values):
    knob_object = {}
    # create the knobObject based on the position of the opti_values and variables in their array
    for idx, val in enumerate(variables):
        knob_object[val] = opti_values[idx]
    return knob_object


def self_optimizer_execution(wf, opti_values, variables):
    knob_object = recreate_knob_from_optimizer_values(variables, opti_values)
    # create a new experiment to run in execution
    exp = dict()
    exp["ignore_first_n_results"] = wf.self_optimizer["ignore_first_n_results"]
    exp["sample_size"] = wf.self_optimizer["sample_size"]
    exp["knobs"] = knob_object
    return experimentFunction(wf, exp)


def start_self_optimizer_strategy(wf):
    info("> ExecStrategy   | SelfOptimizer", Fore.CYAN)
    method = wf.self_optimizer["method"]
    info("> Optimizer      | " + method, Fore.CYAN)

    # we look at the ranges the user has specified in the knobs
    knobs = wf.self_optimizer["knobs"]
    # we create a list of variable names and a list of knob (from,to)
    variables = []
    range_tuples = []
    # we fill the arrays and use the index to map from gauss-optimizer-value to variable
    for key in knobs:
        variables += [key]
        range_tuples += [(knobs[key][0], knobs[key][1])]

    optimizer_result = gp_minimize(lambda opti_values: self_optimizer_execution(wf, opti_values, variables),
                                   range_tuples)
    info(">")
    info("> OptimalResult  | Knobs:  " + str(recreate_knob_from_optimizer_values(variables, optimizer_result.x)))
    info(">                | Result: " + str(optimizer_result.fun))
