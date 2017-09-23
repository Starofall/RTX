# Simple sequential run of knob values
name = "CrowdNav-Sequential"
type = "t-test"

def evaluator(resultState, wf):
    return wf.experimentCounter

def state_initializer(state, wf):
    state["data_points"] = 0
    return state

def primary_data_reducer(state, newData, wf):

    if wf.using_database:
        datapoint = dict()
        datapoint["body"] = newData
        datapoint["body"]['timestamp'] = wf.dt.now()
        datapoint["body"]['analysis_id'] = wf.analysis_id
        datapoint["body"]['knobs'] = wf.current_knobs
        datapoint["doc_type"] = 'experiment_' + str(wf.experimentCounter)
        datapoint["id"] = state["data_points"]
        datapoint["index"] = "rtx-datapoint"
        wf.db.save_with_id(datapoint)

    state["data_points"] = state["data_points"] + 1
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