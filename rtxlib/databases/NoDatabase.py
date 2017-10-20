from rtxlib.databases.Database import Database
from rtxlib import error


class NoDatabase(Database):

    def __init__(self):
        pass

    def save_target_system(self, target_system_id, primary_data_provider, change_provider):
        error("Cannot save target system data. Please specify a database configuration in config.json")

    def use_target_system(self, target_system_id):
        error("Cannot use target system. Please specify a database configuration in config.json")

    def release_target_system(self, target_system_id):
        error("Cannot release target system. Please specify a database configuration in config.json")

    def save_rtx_run(self, strategy):
        error("Cannot save rtx run data. Please specify a database configuration in config.json")

    def get_exp_count(self, rtx_run_id):
        error("Cannot get rtx run's experiment count. Please specify a database configuration in config.json")

    def save_data_point(self, exp_run, knobs, payload, data_point_id, rtx_run_id):
        error("Cannot save data point. Please specify a database configuration in config.json")

    def get_data_points(self, rtx_run_id, exp_run):
        error("Cannot get data point. Please specify a database configuration in config.json")

    def save_analysis(self, rtx_run_ids, name, result):
        error("Cannot save analysis. Please specify a database configuration in config.json")
