# Shows how to integrate Spark into RTX
name = "CrowdNav-Spark"

execution_strategy = {
    "ignore_first_n_results": 10,
    "sample_size": 10,
    "type": "step_explorer",
    "knobs": {
        "route_random_sigma": ([0.0, 1.0], 0.1)
    }
}

pre_processors = [{
    "type": "spark",
    "submit_mode": "client_jar",
    "job_file": "CrowdNavSpark-assembly-1.0.jar",
    "job_class": "crowdnav.Main"
}]


def primary_data_reducer(state, newData, wf):
    new_overhead = newData["overhead"]  # is already the sum
    new_count = newData["count"]
    state["total_overhead"] = state["total_overhead"] + new_overhead
    state["count"] = state["count"] + new_count
    return state


primary_data_provider = {
    "type": "kafka_consumer",
    "kafka_uri": "kafka:9092",
    "topic": "crowd-nav-summary",
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
    return resultState["total_overhead"] / resultState["count"]


def state_initializer(state, wf):
    state["count"] = 0
    state["total_overhead"] = 0
    return state
