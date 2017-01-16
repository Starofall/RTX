from colorama import Fore

from rtxlib import info, error
from rtxlib.execution import experimentFunction


def start_sequential_strategy(wf):
    info("> ExecStrategy   | Sequential", Fore.CYAN)
    for exp in wf.experiments_seq:
        experimentFunction(wf, exp)
