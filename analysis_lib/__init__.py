from abc import ABCMeta, abstractmethod
from colorama import Fore
from rtxlib.rtx_run import get_data_for_run
from rtxlib.rtx_run import db
from rtxlib import info, error


class Analysis(object):

    __metaclass__ = ABCMeta

    def __init__(self, rtx_run_ids, y_key):
        self.rtx_run_ids = rtx_run_ids
        self.y_key = y_key

    def start(self):
        data, knobs = self.get_data()

        if not data[0]:
            error("Tried to run " + self.name + " on empty data.")
            error("Aborting analysis.")
            return

        result = self.run(data, knobs)
        if result:
            self.save_result(self.name, result)

    def get_data(self):
        first_rtx_run_id = self.rtx_run_ids[0]
        data, knobs, self.exp_count = get_data_for_run(first_rtx_run_id)

        for rtx_run_id in self.rtx_run_ids[1:]:
            new_data, new_knobs, new_exp_count = get_data_for_run(rtx_run_id)
            for i in range(0,self.exp_count):
                data[i] += new_data[i]
                knobs[i] += new_knobs[i]

        return data, knobs

    @abstractmethod
    def run(self, data, knobs):
        """ analysis-specific logic """
        pass

    def save_result(self, analysis_name, result):
        db().save_analysis(self.rtx_run_ids, analysis_name, result)
        info("> ", Fore.CYAN)
        info("> Analysis of type '" + self.name + "' performed on datasets [" +
             ", ".join(str(x) for x in self.rtx_run_ids) + "] of " + str(self.exp_count) + " experiments", Fore.CYAN)
        info("> Result: " + str(result), Fore.CYAN)
