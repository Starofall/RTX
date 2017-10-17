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
        data = self.get_data()
        result = self.run(data)
        self.save_result(self.name, result)

    def get_data(self):
        first_rtx_run_id = self.rtx_run_ids[0]
        data, exp_count = get_data_for_run(first_rtx_run_id)
        self.exp_count = exp_count

        for rtx_run_id in self.rtx_run_ids[1:]:
            new_data, new_exp_count = get_data_for_run(rtx_run_id)
            for i in range(0,exp_count):
                data[i] += new_data[i]

        if not data:
            error("Tried to run analysis on empty data. Aborting.")
            return

        return data

    @abstractmethod
    def run(self, data):
        """ analysis-specific logic """
        pass

    def save_result(self, analysis_name, result):
        db().save_analysis(self.rtx_run_ids, analysis_name, result)
        info("> ", Fore.CYAN)
        info("> Analysis of type '" + self.name + "' performed on datasets [" + ", ".join(str(x) for x in self.rtx_run_ids) + "]", Fore.CYAN)
        info("> Result: " + str(result), Fore.CYAN)
