# Abstract interface for a database
#
# A database stores the raw data and the experiment runs of RTX.


class Database:

    def __init__(self):
        pass

    def save_target_system(self, target_system_id, primary_data_provider, change_provider):
        """ saves the parameters of an OEDA target system with the provided id """
        pass

    def use_target_system(self, target_system_id):
        """ marks the OEDA target system as in use and retrieves its configuration """
        pass

    def release_target_system(self, target_system_id):
        """ marks the OEDA target system as not in use """
        pass

    def save_rtx_run(self, strategy):
        """ saves the parameters of an rtx run and returns the auto-generated id """
        pass

    def get_exp_count(self, rtx_run_id):
        """ returns the experiment count parameter of the rtx run specified by its id """
        pass

    def save_data_point(self, exp_run, knobs, payload, data_point_id, rtx_run_id):
        """ called for saving experiment configuration runs and raw data """
        pass

    def get_data_points(self, rtx_run_id, exp_run):
        """ called for getting all the data points corresponding to an analytis run """
        pass

    def save_analysis(self, rtx_run_ids, name, result):
        """ saves the parameters and the result of an analysis """
        pass