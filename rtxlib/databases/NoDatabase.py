from rtxlib.databases.Database import Database
from rtxlib import error


class NoDatabase(Database):

    def __init__(self):
        pass

    def save_rtx_run(self, strategy):
        error("Cannot save rtx run data. Please specify a database configuration in config.json")

    def update_rtx_run(self, rtx_run_id, exp_count, list_of_configurations):
        error("Cannot update rtx run data. Please specify a database configuration in config.json")

    def get_exp_count(self, rtx_run_id):
        error("Cannot get rtx run's experiment count. Please specify a database configuration in config.json")

    def get_list_of_configurations(self, rtx_run_id):
        error("Cannot get rtx run's list of configurations. Please specify a database configuration in config.json")

    def get_sample_size(self, rtx_run_id):
        error("Cannot get rtx run's strategy's sample size. Please specify a database configuration in config.json")

    def save_data_point(self, exp_run, knobs, payload, data_point_id, rtx_run_id):
        error("Cannot save data point. Please specify a database configuration in config.json")

    def get_data_points(self, rtx_run_id, exp_run):
        error("Cannot get data point. Please specify a database configuration in config.json")

    def save_analysis(self, rtx_run_ids, name, result):
        error("Cannot save analysis. Please specify a database configuration in config.json")
