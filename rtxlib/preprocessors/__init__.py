from colorama import Fore

from rtxlib import info, error, debug
from rtxlib.preprocessors.SparkPreProcessor import SparkPreProcessor


def init_pre_processors(wf):
    pp = wf.pre_processors
    for p in pp:
        if p["type"] == "spark":
            p["instance"] = SparkPreProcessor(wf, p)
        else:
            info("> Preprocessor   | None", Fore.CYAN)


def kill_pre_processors(wf):
    try:
        for p in wf.pre_processors:
            p["instance"].shutdown()
            info("> Shutting down Spark preprocessor")
    except AttributeError:
        pass