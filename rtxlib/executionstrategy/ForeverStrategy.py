from colorama import Fore

from rtxlib import info, error
from rtxlib.execution import experimentFunction


def start_forever_strategy(wf):
    """ executes forever - changes must come from definition file """
    info("> ExecStrategy   | Forever ", Fore.CYAN)
    wf.totalExperiments = -1
    while True:
        experimentFunction(wf, {
            "knobs": {"forever": True},
            "ignore_first_n_results": wf.execution_strategy["ignore_first_n_results"],
            "sample_size": wf.execution_strategy["sample_size"],
        })
