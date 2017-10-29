from colorama import Fore

from rtxlib import info, error
from rtxlib.execution import experimentFunction


def start_step_strategy(wf):
    """ implements the step strategy, a way to explore a hole feature area """
    info("> ExecStrategy   | Step", Fore.CYAN)

    # we look at the ranges and the steps the user has specified in the knobs
    knobs = wf.execution_strategy["knobs"]
    # we create a list of variable names and a list of lists of values:
    # [[par1_val1, par1_val2, par1_val3], [par2_val1, par2_val2, par2_val3], [...],...]
    variables = []
    parameters_values = []
    # we create a list of parameters to look at
    for key in knobs:
        variables += [key]
        lower = knobs[key][0][0]
        upper = knobs[key][0][1]
        step = knobs[key][1]
        decimal_points = str(step)[::-1].find('.')
        multiplier = pow(10, decimal_points)
        value = lower
        parameter_values = []
        while value <= upper:
            # create a new list for each item
            parameter_values += [[value]]
            value = float((value * multiplier) + (step * multiplier)) / multiplier
        parameters_values += [parameter_values]
    list_of_configurations = reduce(lambda list1, list2: [x + y for x in list1 for y in list2], parameters_values)
    wf.list_of_configurations = list_of_configurations
    # we run the list of experiments
    wf.totalExperiments = len(list_of_configurations)
    info("> Steps Created  | Count: " + str(wf.totalExperiments), Fore.CYAN)
    for configuration in list_of_configurations:
        step_execution(wf, configuration, variables)


def recreate_knob_from_step_explorer_values(variables, configuration):
    knob_object = {}
    # create the knobObject based on the position of the configuration and variables in their array
    for idx, val in enumerate(variables):
        knob_object[val] = configuration[idx]
    return knob_object


def step_execution(wf, configuration, variables):
    """ runs a single step_execution experiment """
    knob_object = recreate_knob_from_step_explorer_values(variables, configuration)
    # create a new experiment to run in execution
    exp = dict()
    exp["ignore_first_n_results"] = wf.execution_strategy["ignore_first_n_results"]
    exp["sample_size"] = wf.execution_strategy["sample_size"]
    exp["knobs"] = knob_object
    return experimentFunction(wf, exp)
