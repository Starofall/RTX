# for documentation see file /experiment-specification/definition.py

name = "CrowdNav-Gauss-Spark"


def evaluator(resultState):
    return resultState["total_overhead"] / resultState["count"]


def initial_state(state):
    state["count"] = 0
    state["total_overhead"] = 0
    return state


def data_reducer(state, new_data):
    new_overhead = new_data["overhead"]  # is already the sum
    new_count = new_data["count"]
    state["total_overhead"] = state["total_overhead"] + new_overhead
    state["count"] = state["count"] + new_count
    return state


def change_event_creator(variables):
    return variables


system = {
    "execution_strategy": "self_optimizer",
    "pre_processor": "spark",
    "data_provider": "kafka_consumer",
    "change_provider": "kafka_producer",
    "state_initializer": initial_state,
    "data_reducer": data_reducer,
    "evaluator": evaluator,
    "change_event_creator": change_event_creator
}

configuration = {
    "spark": {
        "submit_mode": "client_jar",
        "job_file": "CrowdNavSpark-assembly-1.0.jar",
        "job_class": "crowdnav.Main"
    },
    "kafka_producer": {
        "kafka_uri": "kafka:9092",
        "topic": "crowd-nav-commands",
        "serializer": "JSON",
    },
    "kafka_consumer": {
        "kafka_uri": "kafka:9092",
        "topic": "crowd-nav-summary",
        "serializer": "JSON",
    }
}

self_optimizer = {
    # Currently only Gauss Process
    "method": "gauss_process",
    # If new changes are not instantly visible, we want to ignore some results after state changes
    "ignore_first_n_results": 10,
    # How many samples of data to receive for one run
    "sample_size": 10,
    # The variables to modify
    "knobs": {
        # defines a [from-to] interval that will be used by the optimizer
        "exploration_percentage": [0.0, 1.0],
    }
}
