from analysis_lib import db
from RTXRun import get_data_for_run
from rtxlib import error, info
from colorama import Fore
from abc import ABCMeta, abstractmethod


class Analysis(object):

    __metaclass__ = ABCMeta

    def __init__(self, rtx_run_ids):
        self.rtx_run_ids = rtx_run_ids

    def start(self):
        data = self.get_data()
        result = self.run(data)
        self.save_result(self.name, result)

    def get_data(self):
        first_rtx_run_id = self.rtx_run_ids[0]
        data, exp_count = get_data_for_run(first_rtx_run_id)

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
        info("> " + self.name + " analysis performed on datasets [" + ", ".join(str(x) for x in self.rtx_run_ids) + "]", Fore.CYAN)
        info("> Result: " + str(result), Fore.CYAN)