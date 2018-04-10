# Shows how to use mlr MBO for optimization
name = "CrowdNav-mlrMBO"
host = "localhost"
port = "8004"

execution_strategy = {
    "ignore_first_n_results": 50,
    "sample_size": 50,
    "type": "mlr_mbo",
    "optimizer_iterations": 10,
    "optimizer_iterations_in_design": 8,
    "acquisition_method": "ei",
    "knobs": {
        "route_random_sigma": [0.0, 1.0],
        "max_speed_and_length_factor": [0.0, 2.0]
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
