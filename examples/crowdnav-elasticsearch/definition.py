# Simple sequential run of knob values
name = "CrowdNav-Sequential"
analysis = "t-test"

def evaluator(resultState, wf):
    return wf.experimentCounter

def state_initializer(state, wf):
    state["data_points"] = 0
    return state

def primary_data_reducer(state, newData, wf):
    wf.db.save_data_point(wf.experimentCounter, wf.current_knobs, newData, state["data_points"], wf.analysis_id)
    state["data_points"] += 1
    return state


execution_strategy = {
    "ignore_first_n_results": 10,
    "sample_size": 10,
    "type": "sequential",
    "knobs": [
        {"route_random_sigma": 0.0},
        {"route_random_sigma": 0.2}
    ]
}

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