# for documentation see file /experiment-specification/definition.py

name = "CrowdNav-Gauss"


def evaluator(resultState):
    return resultState["avg_overhead"]


def initial_state(state):
    state["count"] = 0
    state["avg_overhead"] = 0
    return state


def data_reducer(state, newData):
    cnt = state["count"]
    state["avg_overhead"] = (state["avg_overhead"] * cnt + newData["overhead"]) / (cnt + 1)
    state["count"] = cnt + 1
    return state


def change_event_creator(variables):
    return variables


system = {
    "execution_strategy": "self_optimizer",
    "pre_processor": "none",
    "data_provider": "kafka_consumer",
    "change_provider": "kafka_producer",
    "state_initializer": initial_state,
    "data_reducer": data_reducer,
    "evaluator": evaluator,
    "change_event_creator": change_event_creator
}

configuration = {
    "kafka_producer": {
        "kafka_uri": "kafka:9092",
        "topic": "crowd-nav-commands",
        "serializer": "JSON",
    },
    "kafka_consumer": {
        "kafka_uri": "kafka:9092",
        "topic": "crowd-nav-trips",
        "serializer": "JSON",
    }
}

self_optimizer = {
    # Currently only Gauss Process
    "method": "gauss_process",
    # If new changes are not instantly visible, we want to ignore some results after state changes
    "ignore_first_n_results": 100,
    # How many samples of data to receive for one run
    "sample_size": 100,
    # The variables to modify
    "knobs": {
        # defines a [from-to] interval that will be used by the optimizer
        "exploration_percentage": [0.0, 1.0],
    }
}
