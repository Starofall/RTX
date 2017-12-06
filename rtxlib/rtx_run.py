from types import ModuleType
from rtxlib.workflow import execute_workflow
from rtxlib import info, error
from json import load
from rtxlib.databases import create_instance
from colorama import Fore


class RTXRun(object):

    @staticmethod
    def create(target_system_id, execution_strategy):
        primary_data_provider, change_provider = db().use_target_system(target_system_id)
        if not primary_data_provider or not change_provider:
            error("Cannot create rtx run.")
            return None
        return RTXRun(target_system_id, primary_data_provider, change_provider, execution_strategy)

    def __init__(self, target_system_id, primary_data_provider, change_provider, execution_strategy):
        self.target_system_id = target_system_id
        self.wf = ModuleType('workflow')
        primary_data_provider["data_reducer"] = RTXRun.primary_data_reducer
        self.wf.primary_data_provider = primary_data_provider
        self.wf.change_provider = change_provider
        self.wf.execution_strategy = execution_strategy
        self.wf.state_initializer = self.state_initializer
        self.wf.evaluator = self.evaluator
        self.wf.folder = None

    def run(self):
        self.wf.execution_strategy["exp_count"] = \
            calculate_experiment_count(self.wf.execution_strategy["type"], self.wf.execution_strategy["knobs"])
        self.wf.name = self.wf.rtx_run_id = db().save_rtx_run(self.wf.execution_strategy)
        execute_workflow(self.wf)
        db().release_target_system(self.target_system_id)
        return self.wf.rtx_run_id

    @staticmethod
    def primary_data_reducer(state, newData, wf):
        db().save_data_point(wf.experimentCounter, wf.current_knobs, newData, state["data_points"], wf.rtx_run_id)
        state["data_points"] += 1
        return state

    @staticmethod
    def state_initializer(state, wf):
        state["data_points"] = 0
        return state

    @staticmethod
    def evaluator(resultState, wf):
        return 0


def run_rtx_run(rtx_run):
    info("Running rtx on target system with id: " + str(rtx_run.target_system_id))
    return rtx_run.run()


def calculate_experiment_count(type, knobs):

    if type == "sequential":
        return len(knobs)

    if type == "step_explorer":
        variables = []
        parameters_values = []
        for key in knobs:
            variables += [key]
            lower = knobs[key][0][0]
            upper = knobs[key][0][1]
            step = knobs[key][1]
            value = lower
            parameter_values = []
            while value <= upper:
                parameter_values += [[value]]
                value += step
            parameters_values += [parameter_values]
        list_of_configurations = reduce(lambda list1, list2: [x + y for x in list1 for y in list2], parameters_values)
        return len(list_of_configurations)


def get_data_for_run(rtx_run_id):
    data = dict()
    knobs = dict()
    exp_count = db().get_exp_count(rtx_run_id)
    for i in range(exp_count):
        fetched = db().get_data_points(rtx_run_id, i)
        data[i] = [d[0] for d in fetched]
        knobs[i] = [d[1] for d in fetched]
    return data, knobs, exp_count


class NonLocal: DB = None


def setup_database(index_name=None):

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
    if index_name:
        database_config["index"]["name"] = index_name
    info("> OEDA configuration: Using " + database_config["type"] + " database.", Fore.CYAN)
    NonLocal.DB = create_instance(database_config)


def db():
    if not NonLocal.DB:
        error("You have to setup the database.")
        exit(0)
    return NonLocal.DB