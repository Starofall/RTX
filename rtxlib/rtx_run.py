from types import ModuleType
from rtxlib.workflow import execute_workflow
from rtxlib import info, error
from json import load
from rtxlib.databases import create_instance
from colorama import Fore


class RTXRun(object):

    def __init__(self):
        self.wf = ModuleType('workflow')
        self.wf.primary_data_provider = self.primary_data_provider
        self.wf.change_provider = self.change_provider
        self.wf.execution_strategy = self.execution_strategy
        self.wf.state_initializer = self.state_initializer
        self.wf.evaluator = self.evaluator
        self.wf.folder = None

    def start(self):
        self.wf.name = self.wf.rtx_run_id = db().save_rtx_run(self.wf.execution_strategy)
        execute_workflow(self.wf)
        db().update_rtx_run_with_exp_count(self.wf.rtx_run_id, self.wf.totalExperiments)
        return self.wf.rtx_run_id

    def primary_data_reducer(state, newData, wf):
        db().save_data_point(wf.experimentCounter, wf.current_knobs, newData, state["data_points"], wf.rtx_run_id)
        state["data_points"] += 1
        return state

    def state_initializer(self, state, wf):
        state["data_points"] = 0
        return state

    def evaluator(self, resultState, wf):
        return 0

    primary_data_provider = {
        "type": "kafka_consumer",
        "kafka_uri": "kafka:9092",
        "topic": "crowd-nav-trips",
        "serializer": "JSON",
        "data_reducer": primary_data_reducer
    }

    change_provider = {
        "type": "kafka_producer",
        "kafka_uri": "kafka:9092",
        "topic": "crowd-nav-commands",
        "serializer": "JSON",
    }

    execution_strategy = {
        "ignore_first_n_results": 0,
        "sample_size": 2,
        "type": "sequential",
        "knobs": [
            {"route_random_sigma": 0.0},
            {"route_random_sigma": 0.2}
        ]
    }


def get_data_for_run(rtx_run_id):
    data = dict()
    exp_count = db().get_exp_count(rtx_run_id)
    for i in range(0,exp_count):
        data[i] = db().get_data_points(rtx_run_id, i)
    return data, exp_count


class NonLocal: DB = None


def setup_database():

    with open('oeda_config.json') as json_data_file:
        try:
            config_data = load(json_data_file)
        except ValueError:
            error("> You need to specify a database configuration in oeda_config.json.")
            exit(0)

    if "database" not in config_data:
        error("You need to specify a database configuration in oeda_config.json.")
        exit(0)

    database_config = config_data["database"]
    info("> OEDA configuration: Using " + database_config["type"] + " database.", Fore.CYAN)
    NonLocal.DB = create_instance(database_config)


def db():
    if not NonLocal.DB:
        error("You have to setup the database.")
        exit(0)
    return NonLocal.DB