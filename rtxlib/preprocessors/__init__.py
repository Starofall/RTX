from colorama import Fore

from rtxlib import info, error, debug
from rtxlib.preprocessors.SparkPreProcessor import SparkPreProcessor


def init_pre_processor(wf):
    pp = wf.system["pre_processor"]
    if pp == "spark":
        wf.preprocessor = SparkPreProcessor(wf)
    else:
        info("> Preprocessor   | None", Fore.CYAN)
