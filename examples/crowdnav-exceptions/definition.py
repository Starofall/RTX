# This example shows how to stop experiments that hit the systems performance to heavy
# - init_knobs
# - default_knobs
# - full stop or single stop of experiments
#
name = "CrowdNav-Exceptions"

execution_strategy = {
    "type": "step_explorer",
    "ignore_first_n_results": 100,
    "sample_size": 100,
    "knobs": {
        "re_route_every_ticks": ([8, 32], 8)
    },
    "pre_workflow_knobs": {
        "total_car_counter": 100
    },
    "post_workflow_knobs": {
        "total_car_counter": 750,
        "re_route_every_ticks": 60
    }
}


def primary_data_reducer(state, newData, wf):
    cnt = state["count"]
    state["avg_overhead"] = (state["avg_overhead"] * cnt + newData["overhead"]) / (cnt + 1)
    state["count"] = cnt + 1
    return state


def performance_data_reducer(state, newData, wf):
    cnt = state["duration_count"]
    state["duration_avg"] = (state["duration_avg"] * cnt + newData["duration"]) / (cnt + 1)
    state["duration_count"] = cnt + 1
    return state


def routing_data_reducer(state, newData, wf):
    cnt = state["routing_count"]
    state["routing_avg"] = (state["routing_avg"] * cnt + newData["duration"]) / (cnt + 1)
    state["routing_count"] = cnt + 1
    if state["routing_count"] > 10 and state["routing_avg"] > 20:
        # stops this specific experiment
        raise StopIteration("routing got too exponsive")
        # alternative is to stop the whole workflow
        # raise RuntimeError("stop the whole workflow")
    return state


primary_data_provider = {
    "type": "kafka_consumer",
    "kafka_uri": "kafka:9092",
    "topic": "crowd-nav-trips",
    "serializer": "JSON",
    "data_reducer": primary_data_reducer
}

secondary_data_providers = [
    {
        "type": "kafka_consumer",
        "kafka_uri": "kafka:9092",
        "topic": "crowd-nav-performance",
        "serializer": "JSON",
        "data_reducer": performance_data_reducer
    },
    {
        "type": "kafka_consumer",
        "kafka_uri": "kafka:9092",
        "topic": "crowd-nav-routing",
        "serializer": "JSON",
        "data_reducer": routing_data_reducer
    }
]

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
    state["duration_avg"] = 0
    state["duration_count"] = 0
    state["routing_avg"] = 0
    state["routing_count"] = 0
    return state


def change_event_creator(variables, wf):
    return variables
