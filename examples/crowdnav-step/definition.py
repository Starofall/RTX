# Shows how to use two dimensional steps to generate heatmap of results
name = "CrowdNav-Step"

execution_strategy = {
    "ignore_first_n_results": 10000,
    "sample_size": 10000,
    "type": "step_explorer",
    "knobs": {
        "route_random_sigma": ([0.0, 1.0], 0.1),
        "max_speed_and_length_factor": ([0.0, 2.0], 0.1)
    }
}


def primary_data_reducer(state, newData):
    cnt = state["count"]
    state["avg_overhead"] = (state["avg_overhead"] * cnt + newData["overhead"]) / (cnt + 1)
    state["count"] = cnt + 1
    return state


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


def evaluator(resultState):
    return resultState["avg_overhead"]


def state_initializer(state):
    state["count"] = 0
    state["avg_overhead"] = 0
    return state


def change_event_creator(variables):
    return variables


secondary_data_providers = []

pre_processors = []
