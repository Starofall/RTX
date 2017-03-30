# Example of using Gauss to find optimal values for a knob
name = "CrowdNav-Gauss"

execution_strategy = {
    "ignore_first_n_results": 10000,
    "sample_size": 10000,
    "type": "self_optimizer",
    "optimizer_method": "gauss",
    "optimizer_iterations": 50,
    "optimizer_random_starts": 10,
    "knobs": {
        "route_random_sigma": (0.0, 1.0)
    }
}


def primary_data_reducer(state, newData, wf):
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


def evaluator(resultState, wf):
    return resultState["avg_overhead"]


def state_initializer(state, wf):
    state["count"] = 0
    state["avg_overhead"] = 0
    return state
