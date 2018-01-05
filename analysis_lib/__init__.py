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

    def start(self, data, knobs):

        if not data[0]:
            error("Tried to run " + self.name + " on empty data.")
            error("Aborting analysis.")
            return

        return self.run(data, knobs)

    @abstractmethod
    def run(self, data, knobs):
        """ analysis-specific logic """
        pass

    '''Currently not used'''
    def get_data(self):
        first_rtx_run_id = self.rtx_run_ids[0]
        data, knobs, exp_count = get_data_for_run(first_rtx_run_id)

        for rtx_run_id in self.rtx_run_ids[1:]:
            new_data, new_knobs, new_exp_count = get_data_for_run(rtx_run_id)
            for i in range(new_exp_count):
                data[exp_count+i] = new_data[i]
                knobs[exp_count+i] = new_knobs[i]
            exp_count += new_exp_count

        self.exp_count = exp_count
        return data, knobs

    '''Currently not used'''
    def combine_data(self):
        first_rtx_run_id = self.rtx_run_ids[0]
        data, knobs, self.exp_count = get_data_for_run(first_rtx_run_id)

        for rtx_run_id in self.rtx_run_ids[1:]:
            new_data, new_knobs, new_exp_count = get_data_for_run(rtx_run_id)
            for i in range(self.exp_count):
                data[i] += new_data[i]
                knobs[i] += new_knobs[i]

        return data, knobs

    '''Currently not used'''
    def save_result(self, analysis_name, result):
        db().save_analysis(self.rtx_run_ids, analysis_name, result)
        info("> ", Fore.CYAN)
        info("> Analysis of type '" + self.name + "' performed on datasets [" +
             ", ".join(str(x) for x in self.rtx_run_ids) + "] of " + str(self.exp_count) + " experiments", Fore.CYAN)
        info("> Result: " + str(result), Fore.CYAN)
