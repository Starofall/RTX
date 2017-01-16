from colorama import Fore

from rtxlib import info, error
from rtxlib.execution import experimentFunction


def recreate_knob_from_step_explorer_values(variables, configuration):
    knob_object = {}
    # create the knobObject based on the position of the configuration and variables in their array
    for idx, val in enumerate(variables):
        knob_object[val] = configuration[idx]
    return knob_object


def step_execution(wf, configuration, variables):
    knob_object = recreate_knob_from_step_explorer_values(variables, configuration)
    # create a new experiment to run in execution
    exp = dict()
    exp["ignore_first_n_results"] = wf.step_explorer["ignore_first_n_results"]
    exp["sample_size"] = wf.step_explorer["sample_size"]
    exp["knobs"] = knob_object
    return experimentFunction(wf, exp)


def start_step_strategy(wf):
    info("> ExecStrategy   | Step", Fore.CYAN)

    # we look at the ranges and the steps the user has specified in the knobs
    knobs = wf.step_explorer["knobs"]
    # we create a list of variable names and a list of lists of values:
    # [[par1_val1, par1_val2, par1_val3], [par2_val1, par2_val2, par2_val3], [...],...]
    variables = []
    parameters_values = []

    for key in knobs:
        variables += [key]
        lower = knobs[key][0][0]
        upper = knobs[key][0][1]
        step = knobs[key][1]
        value = lower
        parameter_values = []
        while value <= upper:
            # create a new list for each item
            parameter_values += [[value]]
            value += step
        parameters_values += [parameter_values]

    list_of_configurations = reduce(lambda list1,list2: [x + y for x in list1 for y in list2], parameters_values)

    info("> Experiments generated  | Count: " + str(len(list_of_configurations)))

    for configuration in list_of_configurations:
        step_execution(wf, configuration, variables)