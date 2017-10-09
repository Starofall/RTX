from rtxlib.databases.Database import Database
from rtxlib import error


class NoDatabase(Database):

    def __init__(self):
        pass

    def save_analysis(self, name, strategy):
        error("Cannot save analysis data. Please specify a database configuration in config.json")

    def save_data_point(self, exp_run, knobs, payload, data_point_id, analysis_id):
        error("Cannot save data point. Please specify a database configuration in config.json")

    def get_data_points(self, analysis_id, exp_run):
        error("Cannot get data point. Please specify a database configuration in config.json")

    def save_analysis_result(self, analysis_id):
        error("Cannot save analysis result. Please specify a database configuration in config.json")
