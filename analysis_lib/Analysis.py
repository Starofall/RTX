from analysis_lib import db
from types import ModuleType
from rtxlib.workflow import execute_workflow

class Analysis(object):
    """ abstract interface for an analysis.

    An analysis creates a workflow module and invokes RTX with it
    """

    def __init__(self):
        self.wf = ModuleType('workflow')
        self.wf.primary_data_provider = self.primary_data_provider
        self.wf.change_provider = self.change_provider
        self.wf.execution_strategy = self.execution_strategy
        self.wf.state_initializer = self.state_initializer
        self.wf.evaluator = self.evaluator
        self.wf.workflow_evaluator = self.workflow_evaluator
        self.wf.folder = None

    def run(self):
        self.wf.name = self.wf.analysis_id = db().save_analysis(self.analysis, self.wf.execution_strategy)
        execute_workflow(self.wf)
        data = []
        for i in range(0,self.wf.totalExperiments):
            data.append(db().get_data_points(self.wf.analysis_id, i))
        self.workflow_evaluator(self.wf, data)

    def workflow_evaluator(self, wf, result):
        db().save_analysis_result(wf.analysis_id, result)
        print result

    def primary_data_reducer(state, newData, wf):
        db().save_data_point(wf.experimentCounter, wf.current_knobs, newData, state["data_points"], wf.analysis_id)
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